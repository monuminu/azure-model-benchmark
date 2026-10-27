"""CLI with explicit opt-in Azure lifecycle management."""

import argparse
import csv
import json
import subprocess
import sys
import time
import tomllib
import uuid
from pathlib import Path

from .core import run_target, validate_config

SKUS = {
    "GlobalStandard": "PayGo Global",
    "DataZoneStandard": "PayGo Data Zone",
    "Standard": "PayGo Regional",
    "GlobalProvisionedManaged": "PTU Global",
    "DataZoneProvisionedManaged": "PTU Data Zone",
    "ProvisionedManaged": "PTU Regional",
}
COLUMNS = [
    "model",
    "deployment_type",
    "region",
    "ptus",
    "status",
    "requests",
    "successes",
    "failures",
    "ttft_95th",
    "ttft_avg",
    "tbt_avg",
    "tbt_95th",
    "e2e_avg",
    "e2e_95th",
    "read_cache_pct",
    "write_cache_pct",
    "mean_input_tokens",
    "mean_output_tokens",
]


def az(args):
    r = subprocess.run(
        ["az"] + args + ["-o", "json", "--only-show-errors"],
        capture_output=True,
        text=True,
        timeout=180,
    )
    if r.returncode:
        raise RuntimeError("Azure command failed: " + r.stderr[:500])
    return json.loads(r.stdout) if r.stdout.strip() else None


def write_reports(out, rows):
    out.mkdir(parents=True, exist_ok=True)
    (out / "summary.json").write_text(json.dumps(rows, indent=2))
    with (out / "summary.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    def fmt(x):
        return (
            "—"
            if x is None
            else (f"{x:.4f}" if isinstance(x, float) else str(x).replace("|", "/"))
        )

    lines = [
        "# Azure Responses API benchmark",
        "",
        "Timing units: seconds. Cache units: percent of input tokens. TBT percentiles are across request-level mean inter-token estimates.",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join(["---"] * len(COLUMNS)) + "|",
    ]
    lines += ["| " + " | ".join(fmt(r.get(k)) for k in COLUMNS) + " |" for r in rows]
    (out / "summary.md").write_text("\n".join(lines) + "\n")


def combine_reports(paths):
    """Keep first measured result for each exact model/type; enrich skipped rows."""
    priority = {
        "measured": 10,
        "warmup_failed": 5,
        "execution_failed": 4,
        "insufficient_capacity": 2,
        "insufficient_quota": 2,
        "unsupported_in_region": 0,
    }
    selected = {}
    for path in paths:
        for row in json.loads(Path(path).read_text()):
            key = row["model"], row["deployment_type"]
            previous = selected.get(key)
            if previous is None or priority.get(row["status"], 1) > priority.get(
                previous["status"], 1
            ):
                selected[key] = row
    return list(selected.values())


def measured(target, b, out):
    label = target.get("label", target["deployment"])
    with (out / "requests.jsonl").open("a") as f:

        def save(r):
            f.write(json.dumps({"target": label} | r) + "\n")
            f.flush()

        summary = run_target(target, b, save)
    return dict(
        model=target.get("model", target["deployment"]),
        deployment_type=SKUS.get(target.get("sku"), target.get("sku", "unverified")),
        region=target.get("region", "unverified"),
        ptus=target.get("ptus"),
        verification=target.get("verification", "declared"),
        **summary,
    )


def verify(target):
    fields = ["subscription", "resource_group", "account"]
    if not all(target.get(k) for k in fields):
        return target | {"verification": "declared_not_verified"}
    args = [
        "cognitiveservices",
        "account",
        "deployment",
        "show",
        "--subscription",
        target["subscription"],
        "-g",
        target["resource_group"],
        "-n",
        target["account"],
        "--deployment-name",
        target["deployment"],
    ]
    dep = az(args)
    props = dep.get("properties", dep)
    sku = dep["sku"]
    model = props["model"]
    for k, v in [("sku", sku["name"]), ("model", model["name"])]:
        if target.get(k) and target[k] != v:
            raise ValueError(f"Deployment {k} does not match configuration")
    if target.get("version") and target["version"] != model["version"]:
        raise ValueError("Deployment version mismatch")
    if target.get("ptus") is not None and target["ptus"] != sku["capacity"]:
        raise ValueError("Deployed PTUs do not match configuration")
    return target | dict(
        model=model["name"],
        version=model["version"],
        sku=sku["name"],
        ptus=sku["capacity"] if "Provisioned" in sku["name"] else None,
        verification="azure_management_plane",
    )


def matrix(config, b, out):
    m = config["matrix"]
    sub = m["subscription"]
    group = m["resource_group"]
    account = m["account"]
    region = m["region"]
    ac = az(
        [
            "cognitiveservices",
            "account",
            "show",
            "--subscription",
            sub,
            "-g",
            group,
            "-n",
            account,
        ]
    )
    if ac["location"] != region:
        raise ValueError("Account region differs from configured region")
    catalog = az(
        [
            "cognitiveservices",
            "model",
            "list",
            "--subscription",
            sub,
            "--location",
            region,
        ]
    )
    (out / "catalog.json").write_text(json.dumps(catalog, indent=2))
    usage = az(
        [
            "cognitiveservices",
            "usage",
            "list",
            "--subscription",
            sub,
            "--location",
            region,
        ]
    )
    rows = []
    prefix = "bench-" + uuid.uuid4().hex[:8]
    for name in m["models"]:
        entries = [x["model"] for x in catalog if x["model"]["name"] == name]
        version = m.get("versions", {}).get(name)
        if version:
            entries = [x for x in entries if x["version"] == version]
        model = max(entries, key=lambda x: x["version"]) if entries else None
        for sku in m.get("skus", list(SKUS)):
            row = dict(
                model=name,
                deployment_type=SKUS[sku],
                region=region,
                ptus=None,
                status="unsupported_in_region",
                requests=0,
                successes=0,
                failures=0,
            )
            opts = [x for x in (model or {}).get("skus", []) if x["name"] == sku]
            if not opts:
                rows.append(row)
                write_reports(out, rows)
                continue
            opt = opts[0]
            capinfo = opt.get("capacity") or {}
            provisioned = "Provisioned" in sku
            capacity = (
                m.get("ptu_regional" if sku == "ProvisionedManaged" else "ptus", 15)
                if provisioned
                else m.get("paygo_capacity", 100)
            )
            row["ptus"] = capacity if provisioned else None
            minimum = capinfo.get("minimum") or 1
            step = capinfo.get("step") or 1
            if capacity < minimum or (capacity - minimum) % step:
                rows.append(row | {"status": "invalid_capacity_for_sku"})
                write_reports(out, rows)
                continue
            key = opt.get("usageName")
            u = next((x for x in usage if x["name"]["value"] == key), None)
            if not u or u["limit"] - u["currentValue"] < capacity:
                rows.append(row | {"status": "insufficient_quota"})
                write_reports(out, rows)
                continue
            caps = az(
                [
                    "rest",
                    "--method",
                    "GET",
                    "--url",
                    f"https://management.azure.com/subscriptions/{sub}/providers/Microsoft.CognitiveServices/locations/{region}/modelCapacities?api-version=2024-10-01&modelFormat=OpenAI&modelName={name}&modelVersion={model['version']}",
                ]
            )
            available = max(
                [
                    x["properties"].get("availableCapacity", 0) or 0
                    for x in caps.get("value", [])
                    if x["properties"]["skuName"] == sku
                ]
                or [0]
            )
            if available < capacity:
                rows.append(row | {"status": "insufficient_capacity"})
                write_reports(out, rows)
                continue
            dep = f"{prefix}-{len(rows)}"
            created = False
            common = [
                "--subscription",
                sub,
                "-g",
                group,
                "-n",
                account,
                "--deployment-name",
                dep,
            ]
            print(f"{name} {sku}: creating temporary deployment", flush=True)
            try:
                # This generated name is unique; never update an existing customer deployment.
                created = True
                (out / "lifecycle.jsonl").open("a").write(
                    json.dumps(
                        {
                            "operation": "create_attempt",
                            "deployment": dep,
                            "model": name,
                            "sku": sku,
                        }
                    )
                    + "\n"
                )
                az(
                    ["cognitiveservices", "account", "deployment", "create"]
                    + common
                    + [
                        "--model-format",
                        "OpenAI",
                        "--model-name",
                        name,
                        "--model-version",
                        model["version"],
                        "--sku-name",
                        sku,
                        "--sku-capacity",
                        str(capacity),
                    ]
                )
                deadline = time.monotonic() + 180
                while True:
                    state = (
                        az(
                            ["cognitiveservices", "account", "deployment", "show"]
                            + common
                        )
                        .get("properties", {})
                        .get("provisioningState")
                    )
                    if state == "Succeeded":
                        break
                    if state in ["Failed", "Canceled"] or time.monotonic() > deadline:
                        raise RuntimeError("Deployment did not become ready")
                    time.sleep(2)
                target = dict(
                    endpoint=ac["properties"]["endpoint"],
                    deployment=dep,
                    subscription=sub,
                    resource_group=group,
                    account=account,
                    region=region,
                    model=name,
                    version=model["version"],
                    sku=sku,
                    ptus=capacity if provisioned else None,
                )
                target = verify(target)
                print(f"{name} {sku}: benchmarking via Responses API", flush=True)
                result = measured(target, b, out)
                rows.append(result)
            except Exception as e:
                rows.append(
                    row
                    | {
                        "status": "execution_failed",
                        "error_type": type(e).__name__,
                        "error_detail": str(e),
                    }
                )
                print(f"{name} {sku}: {e}", flush=True)
            finally:
                if created:
                    try:
                        az(
                            ["cognitiveservices", "account", "deployment", "delete"]
                            + common
                        )
                    except Exception as cleanup_error:
                        if "NotFound" not in str(cleanup_error):
                            (out / "cleanup-required.jsonl").open("a").write(
                                json.dumps(
                                    {
                                        "subscription": sub,
                                        "resource_group": group,
                                        "account": account,
                                        "deployment": dep,
                                    }
                                )
                                + "\n"
                            )
                            raise RuntimeError(
                                "Temporary deployment cleanup failed; see cleanup-required.jsonl"
                            ) from cleanup_error
                write_reports(out, rows)
            print(f"{name} {sku}: {rows[-1]['status']}", flush=True)
    return rows


def main():
    p = argparse.ArgumentParser(
        description="Azure PayGo and PTU benchmarks using the Responses API"
    )
    p.add_argument("command", choices=["run", "matrix", "validate", "report"])
    p.add_argument("--config")
    p.add_argument("--inputs", nargs="+", help="Summary JSON files to combine")
    p.add_argument("--output", default="runs/latest")
    p.add_argument(
        "--allow-create",
        action="store_true",
        help="Explicitly authorize temporary billable Azure deployments; always cleaned up",
    )
    args = p.parse_args()
    if args.command == "report":
        if not args.inputs:
            p.error("report requires --inputs")
        out = Path(args.output)
        if out.exists() and any(out.iterdir()):
            p.error("Report output directory must be empty")
        write_reports(out, combine_reports(args.inputs))
        print(out / "summary.md")
        return
    if not args.config:
        p.error("--config is required")
    config = tomllib.loads(Path(args.config).read_text())
    b = validate_config(config)
    if args.command == "validate":
        print("Configuration valid")
        return
    out = Path(args.output)
    if out.exists() and any(out.iterdir()):
        p.error("Output directory must be empty to avoid mixing runs")
    out.mkdir(parents=True, exist_ok=True)
    (out / "settings.json").write_text(
        json.dumps({"benchmark": b, "api": "responses"}, indent=2)
    )
    if args.command == "matrix":
        if not args.allow_create:
            p.error("matrix requires --allow-create; use run for existing endpoints")
        rows = matrix(config, b, out)
    else:
        if not config.get("targets"):
            p.error("At least one target is required")
        rows = []
        for target in config["targets"]:
            rows.append(measured(verify(target), b, out))
            write_reports(out, rows)
    print(out / "summary.md")
    if any(
        x["status"] in ["execution_failed", "warmup_failed"] or x.get("failures", 0)
        for x in rows
    ):
        sys.exit(2)


if __name__ == "__main__":
    main()
