"""Request execution, bounded load generation and reproducible metrics."""

import concurrent.futures
import json
import math
import os
import statistics
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

DEFAULTS = dict(
    duration_s=60,
    concurrency=2,
    rpm=20,
    load_mode="rpm",
    input_tokens=3006,
    output_tokens=302,
    timeout_s=90,
    warmup_requests=1,
    max_requests=1000,
    reasoning_effort="none",
    cache_mode="cold",
    tokenizer="o200k_base",
    drain_timeout_s=100,
)


def percentile(values, q):
    values = sorted(values)
    return values[max(0, math.ceil(len(values) * q) - 1)] if values else None


def validate_config(config):
    b = DEFAULTS | config.get("benchmark", {})
    for k in [
        "duration_s",
        "concurrency",
        "input_tokens",
        "output_tokens",
        "timeout_s",
        "max_requests",
        "drain_timeout_s",
    ]:
        if not isinstance(b[k], (int, float)) or not math.isfinite(b[k]) or b[k] <= 0:
            raise ValueError(f"{k} must be positive and finite")
    for k in [
        "concurrency",
        "input_tokens",
        "output_tokens",
        "warmup_requests",
        "max_requests",
    ]:
        if not isinstance(b[k], int) or isinstance(b[k], bool):
            raise ValueError(f"{k} must be an integer")
    if b["warmup_requests"] < 0:
        raise ValueError("warmup_requests cannot be negative")
    if b["load_mode"] not in ["rpm", "concurrency"]:
        raise ValueError("Invalid load_mode")
    if (
        not isinstance(b["rpm"], (int, float))
        or not math.isfinite(b["rpm"])
        or b["rpm"] <= 0
    ):
        raise ValueError("rpm must be positive")
    if b["cache_mode"] not in ["cold", "warm"]:
        raise ValueError("cache_mode must be cold or warm")
    if b["drain_timeout_s"] < b["timeout_s"]:
        raise ValueError("drain_timeout_s must cover timeout_s")
    for t in config.get("targets", []):
        if "api_key" in t or "token" in t:
            raise ValueError("Use environment variable names for secrets")
        url = urllib.parse.urlparse(t.get("endpoint", "https://example.invalid"))
        if url.username or url.password or url.query:
            raise ValueError(
                "Endpoint must not contain credentials or query parameters"
            )
        if url.scheme != "https" and url.hostname not in ["localhost", "127.0.0.1"]:
            raise ValueError("Use HTTPS endpoints")
    return b


def make_prompt(b, nonce):
    import tiktoken

    enc = tiktoken.get_encoding(b["tokenizer"])
    if b.get("prompt_file"):
        from pathlib import Path

        return Path(b["prompt_file"]).read_text()
    prefix = (
        f"Test {nonce}.\n"
        if b["cache_mode"] == "cold"
        else "Synthetic support workload.\n"
    )
    suffix = "\nContinue a long numbered list of concise diagnostic observations based only on the synthetic records. Do not invent a resolution."
    unit = " Synthetic ticket: intermittent login failure after a configuration update. Support checked credentials and connectivity; investigation is ongoing."
    target = b["input_tokens"]
    if len(enc.encode(prefix + suffix)) > target:
        raise ValueError("input_tokens too small for instructions")
    # Keep whole records, then use a stable one-token filler to avoid BPE
    # boundary oscillation when appending the generation instruction.
    body = prefix
    while len(enc.encode(body + unit + suffix)) <= target - 8:
        body += unit
    padding = max(0, target - len(enc.encode(body + suffix)))
    for _ in range(20):
        result = body + (" a" * padding) + suffix
        diff = target - len(enc.encode(result))
        if diff == 0:
            return result
        padding += diff
        if padding < 0:
            break
    raise ValueError("Could not construct exact content token target")


def consume_stream(stream, start):
    first = last = None
    chunks = []
    terminal = None
    for line in stream:
        line = line.decode("utf-8").strip()
        if not line.startswith("data:"):
            continue
        raw = line[5:].strip()
        if raw == "[DONE]":
            break
        obj = json.loads(raw)
        typ = obj.get("type")
        if typ in ["error", "response.failed"] or obj.get("error"):
            raise ValueError("Responses API stream reported failure")
        if typ == "response.output_text.delta" and obj.get("delta"):
            now = time.perf_counter()
            first = now if first is None else first
            last = now
            chunks.append(now - start)
        if typ in ["response.completed", "response.incomplete"]:
            terminal = obj.get("response", {})
            if (
                typ == "response.incomplete"
                and terminal.get("incomplete_details", {}).get("reason")
                != "max_output_tokens"
            ):
                raise ValueError("Incomplete response")
    if terminal is None or first is None:
        raise ValueError("Stream ended without terminal response and generated text")
    u = terminal.get("usage") or {}
    if not u.get("output_tokens"):
        raise ValueError("No output usage in terminal response")
    visible = u["output_tokens"] - (u.get("output_tokens_details") or {}).get(
        "reasoning_tokens", 0
    )
    usage = {
        "prompt_tokens": u.get("input_tokens", 0),
        "completion_tokens": u["output_tokens"],
        "prompt_tokens_details": u.get("input_tokens_details") or {},
        "output_tokens_details": u.get("output_tokens_details") or {},
    }
    return dict(
        ok=True,
        ttft_s=first - start,
        e2e_s=time.perf_counter() - start,
        tbt_s=(last - first) / (visible - 1) if visible > 1 and last > first else None,
        usage=usage,
        actual_model=terminal.get("model"),
        response_status=terminal.get("status"),
        finish_reason=(terminal.get("incomplete_details") or {}).get(
            "reason", "completed"
        ),
        chunk_arrivals_s=chunks,
        api="responses",
    )


def get_token(target):
    if target.get("auth", "azure_cli") == "api_key":
        return os.environ[target.get("api_key_env", "AZURE_OPENAI_API_KEY")]
    cmd = [
        "az",
        "account",
        "get-access-token",
        "--resource",
        "https://cognitiveservices.azure.com/",
        "--query",
        "accessToken",
        "-o",
        "tsv",
    ]
    if target.get("subscription"):
        cmd += ["--subscription", target["subscription"]]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if r.returncode:
        raise ValueError(
            "Azure CLI authentication failed; run az login for the target tenant"
        )
    return r.stdout.strip()


def request(target, b, token, index):
    start = time.perf_counter()
    base = dict(
        index=index,
        started_utc=__import__("datetime")
        .datetime.now(__import__("datetime").timezone.utc)
        .isoformat(),
    )
    try:
        prompt = make_prompt(b, str(uuid.uuid4()))
        payload = dict(
            model=target["deployment"],
            input=prompt,
            max_output_tokens=b["output_tokens"],
            stream=True,
            store=False,
        )
        if b.get("reasoning_effort"):
            payload["reasoning"] = {"effort": b["reasoning_effort"]}
        headers = {"Content-Type": "application/json"}
        headers["api-key" if target.get("auth") == "api_key" else "Authorization"] = (
            token if target.get("auth") == "api_key" else "Bearer " + token
        )
        endpoint = target["endpoint"].rstrip("/")
        if not endpoint.endswith("/openai/v1"):
            endpoint += "/openai/v1"
        req = urllib.request.Request(
            endpoint + "/responses", data=json.dumps(payload).encode(), headers=headers
        )
        start = time.perf_counter()
        with urllib.request.urlopen(req, timeout=b["timeout_s"]) as stream:
            return base | consume_stream(stream, start)
    except urllib.error.HTTPError as e:
        return base | dict(
            ok=False,
            status=e.code,
            error=f"HTTP {e.code}",
            e2e_s=time.perf_counter() - start,
        )
    except Exception as e:
        return base | dict(
            ok=False, error=type(e).__name__, e2e_s=time.perf_counter() - start
        )


def summarize(rows):
    ok = [r for r in rows if r.get("ok")]
    out = dict(requests=len(rows), successes=len(ok), failures=len(rows) - len(ok))
    for raw, label in [("ttft_s", "ttft"), ("tbt_s", "tbt"), ("e2e_s", "e2e")]:
        vals = [r[raw] for r in ok if r.get(raw) is not None]
        out[label + "_avg"] = statistics.mean(vals) if vals else None
        out[label + "_95th"] = percentile(vals, 0.95)
    total = sum(r.get("usage", {}).get("prompt_tokens", 0) for r in ok)
    for field, label in [
        ("cached_tokens", "read_cache_pct"),
        ("cache_write_tokens", "write_cache_pct"),
    ]:
        details = [r.get("usage", {}).get("prompt_tokens_details", {}) for r in ok]
        out[label] = (
            100 * sum(x[field] for x in details) / total
            if total and all(field in x for x in details)
            else None
        )
    for field, label in [
        ("prompt_tokens", "mean_input_tokens"),
        ("completion_tokens", "mean_output_tokens"),
    ]:
        vals = [
            r.get("usage", {}).get(field)
            for r in ok
            if r.get("usage", {}).get(field) is not None
        ]
        out[label] = statistics.mean(vals) if vals else None
    return out


def run_target(target, b, on_record):
    token = get_token(target)
    warm = []
    # Preload tokenizer before starting the timed window.
    make_prompt(b, "warmup")
    for i in range(b["warmup_requests"]):
        r = request(target, b, token, f"warmup-{i}")
        warm.append(r)
        on_record(r | {"warmup": True})
        if not r["ok"]:
            return {"status": "warmup_failed"} | summarize([])
    rows = []
    lock = threading.Lock()
    slots = threading.BoundedSemaphore(b["concurrency"])
    stop = time.perf_counter() + b["duration_s"]
    start = time.perf_counter()
    futures = []

    def job(i):
        try:
            r = request(target, b, token, i)
            with lock:
                rows.append(r)
                on_record(r)
        finally:
            slots.release()

    with concurrent.futures.ThreadPoolExecutor(max_workers=b["concurrency"]) as pool:
        i = 0
        while time.perf_counter() < stop and i < b["max_requests"]:
            if b["load_mode"] == "rpm":
                due = start + i * 60 / b["rpm"]
                delay = min(due, stop) - time.perf_counter()
                if delay > 0:
                    time.sleep(delay)
                if time.perf_counter() >= stop:
                    break
                acquired = slots.acquire(blocking=False)
            else:
                acquired = slots.acquire(
                    timeout=min(0.1, max(0, stop - time.perf_counter()))
                )
            if not acquired:
                if b["load_mode"] == "rpm":
                    r = dict(
                        index=i,
                        ok=False,
                        error="concurrency_cap_reached",
                        not_sent=True,
                    )
                    with lock:
                        rows.append(r)
                        on_record(r)
                    i += 1
                continue
            if time.perf_counter() >= stop:
                slots.release()
                break
            futures.append(pool.submit(job, i))
            i += 1
        for f in futures:
            f.result(timeout=b["drain_timeout_s"])
    return {
        "status": "measured",
        "api": "responses",
        "arrival_window_s": min(time.perf_counter() - start, b["duration_s"]),
        "wall_s": time.perf_counter() - start,
    } | summarize(rows)
