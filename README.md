# Azure Model Benchmark

Benchmark Azure OpenAI models through the **Responses API**, on PayGo and provisioned (PTU) deployments. Configure the workload in TOML and export the same result schema for every model and SKU.

## Install

Requires Python 3.11 or newer. Azure CLI is needed for Entra authentication, deployment verification and automatic matrix deployment.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
az login
cp examples/benchmark.toml benchmark.local.toml
```

Edit `benchmark.local.toml` with your endpoint and deployment. Use `auth = "azure_cli"`, or set `auth = "api_key"` and export the key in the named environment variable:

```bash
export AZURE_OPENAI_API_KEY='your-key'
azbench validate --config benchmark.local.toml
azbench run --config benchmark.local.toml --output runs/first-run
```

The endpoint can be an Azure resource base URL or its `/openai/v1` URL. The runner calls `/openai/v1/responses`, streams output and sets `store=false`. Existing deployments are never changed by `run`.

## Workload configuration

| Parameter | Meaning |
|---|---|
| `duration_s` | Arrival window in seconds, excluding warmup and final response draining |
| `load_mode` | `rpm` for scheduled arrivals or `concurrency` for continuously occupied workers |
| `rpm` | Target arrivals per minute in scheduled mode |
| `concurrency` | Maximum simultaneous requests; scheduled arrivals exceeding this cap are recorded as not sent |
| `input_tokens` | Exact synthetic content token target under the selected tokenizer; service framing may add tokens |
| `output_tokens` | Maximum generated output tokens; actual output and reasoning tokens are recorded |
| `max_requests` | Additional cap on measured attempts per target |
| `warmup_requests` | Calls excluded from timing summaries; included in raw records |
| `cache_mode` | `cold` uses a unique leading prefix; `warm` uses a repeated prompt across calls |
| `reasoning_effort` | Responses API reasoning effort; omit it if the model does not accept reasoning options |
| `timeout_s` | Socket connect/read timeout per request |
| `drain_timeout_s` | Future result wait after arrivals stop; must cover `timeout_s` |
| `tokenizer` | tiktoken encoding; default `o200k_base` |
| `prompt_file` | Optional UTF-8 prompt file, overriding synthetic input generation |

Add multiple `[[targets]]` blocks to compare existing endpoints. Each target supports its own endpoint, deployment, API-key environment variable, subscription, model, version, SKU, region and expected PTU count. If subscription, resource group and account are provided, the runner verifies model/version/SKU and PTUs against Azure. Otherwise the summary records `declared_not_verified`.

**PTUs are deployed capacity, not a local simulator setting.** An expected `ptus` value must match the deployment. Set `sku` to `GlobalProvisionedManaged`, `DataZoneProvisionedManaged` or `ProvisionedManaged` for PTU targets. Use `GlobalStandard`, `DataZoneStandard` or `Standard` for PayGo.

## Run a model and deployment matrix

```bash
cp examples/matrix.toml matrix.local.toml
# Set your subscription, existing resource group/account and matching region.
azbench matrix --config matrix.local.toml --output runs/model-matrix --allow-create
```

`--allow-create` explicitly enables **billable temporary deployments**. The matrix reads the live Azure catalog, model version, SKU minimum/increment, quota and allocatable capacity before each creation. Targets execute sequentially, and the runner deletes each uniquely named deployment in `finally` before moving on. It does not purchase reservations, change RBAC, modify resource networking or resize existing deployments. No credentials are written to results.

Configure `ptus` for Global/Data Zone, `ptu_regional` for Regional, and `paygo_capacity` in 1,000-TPM capacity units. All values are checked against the live model SKU. Unsupported combinations remain rows in the result table rather than being replaced by another model or scope. Run the matrix against another account/region to cover Regional offerings available there.

The example selects `gpt-6-luna`, `gpt-6.1-terra`, `gpt-5.6-luna` and `gpt-5.6-terra`. Exact model names are preserved. `GPT-6.1 Terra` is not silently relabelled as `GPT-6 Terra`.

## Metrics

All timings are **seconds**. Percentiles use nearest rank. Timing summaries include successful generated responses; attempted, successful, failed and not-sent requests are counted separately.

| Column | Definition |
|---|---|
| `ttft_avg`, `ttft_95th` | Mean and p95 request submission to first nonempty `response.output_text.delta` |
| `tbt_avg`, `tbt_95th` | Mean and p95 across **request-level mean inter-token estimates**: `(last text chunk − first text chunk) / (visible output tokens − 1)` |
| `e2e_avg`, `e2e_95th` | Mean and p95 request submission through stream consumption |
| `read_cache_pct` | Total reported cached input tokens / total input tokens × 100 |
| `write_cache_pct` | Total reported cache-write input tokens / total input tokens × 100 |

TBT is estimated from streamed chunks because the API does not timestamp every token. `tbt_95th` is a percentile of request-level averages, not a claim about individual token tail intervals. Reasoning tokens are excluded from the visible-token TBT denominator. Raw chunk arrival times remain available for other analyses.

Cache percentages are token weighted, not averages of per-request percentages. A cache field missing from any successful response is `null`/blank, not a fabricated zero. A `response.incomplete` caused by `max_output_tokens` is recorded as generated output with its termination reason. A truncated stream, provider failure or incomplete response for another reason is a failure. No automatic retries hide errors.

## Output

- `summary.csv`, `summary.json`, `summary.md`: requested model/deployment metric table.
- `requests.jsonl`: per-request timings, API, usage, actual returned model and stream status; no prompt or response text.
- `settings.json`: workload settings and API used.
- `catalog.json`, `lifecycle.jsonl`: Azure discovery and temporary deployment lifecycle for matrix runs.
- `cleanup-required.jsonl`: generated if cleanup fails; resolve those exact temporary deployments immediately.

Use a new empty output directory for each run. Exit code 2 means at least one test failed or some measured requests failed. Unsupported combinations are status rows, not errors. If the process is forcibly killed, inspect `lifecycle.jsonl` and delete any remaining generated `bench-*` deployments in the specified account.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests run without Azure credentials or billable endpoints. GitHub Actions runs them on Python 3.11, 3.12 and 3.13.

## References

- [Azure Responses API](https://learn.microsoft.com/azure/foundry/openai/how-to/responses)
- [PTU parameters and sizing](https://learn.microsoft.com/azure/foundry/openai/how-to/provisioned-throughput-sizing)
- [Provisioned throughput and deployment scopes](https://learn.microsoft.com/azure/foundry/openai/concepts/provisioned-throughput)
