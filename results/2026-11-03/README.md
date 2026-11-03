# Combined Azure Responses API benchmark — updated 3 November 2026

**22 measured deployments** across six models. Added GPT-6 Sol and GPT-6.1 Sol PayGo/PTU measurements using the same configured input/load/output cap as the Luna/Terra runs. GPT-6.1 Sol requires reasoning `low`; the other models use `none`. The full CSV includes all **36** model/deployment combinations and measurement dates.

Workload: 60-second arrival window, 20 scheduled RPM, concurrency cap 4, 3,006 content tokens, 302 output-token cap, reasoning `none` except GPT-6.1 Sol (`low`), cold unique-prefix prompts and one excluded warmup. PTU measurements use **15 PTUs**. GPT-6 Sol Data Zone PTU ran in East US 2; the other measured rows ran in Sweden Central.

Timing units below: **milliseconds**. CSV/JSON values are **seconds**.

| Model | Deployment | Region | Date | Reasoning | PTUs | Success/attempts | TTFT p95 | TTFT avg | TBT avg | TBT p95 | E2E avg | E2E p95 | Read cache % | Write cache % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-6-luna | PayGo Global | swedencentral | 2026-10-27 | none | — | 20/20 | 2569.83 | 1785.82 | 8.70 | 10.17 | 2554.69 | 4066.58 | 0.00 | 99.90 |
| gpt-6-luna | PayGo Data Zone | swedencentral | 2026-10-27 | none | — | 19/20 | 2552.22 | 1563.11 | 9.99 | 29.21 | 2256.76 | 3826.54 | 0.00 | 99.90 |
| gpt-6-luna | PTU Global | swedencentral | 2026-11-03 | none | 15 | 20/20 | 4239.64 | 2220.24 | 6.08 | 9.83 | 2741.99 | 4918.11 | 0.00 | 99.90 |
| gpt-6-luna | PTU Data Zone | swedencentral | 2026-11-03 | none | 15 | 18/20 | 3019.12 | 1520.94 | 5.01 | 10.12 | 1925.82 | 3440.69 | 0.00 | 99.90 |
| gpt-6.1-terra | PayGo Global | swedencentral | 2026-10-27 | none | — | 20/20 | 2707.78 | 1903.55 | 6.94 | 10.15 | 2486.72 | 3367.23 | 0.00 | 99.90 |
| gpt-6.1-terra | PayGo Data Zone | swedencentral | 2026-10-27 | none | — | 19/20 | 2669.23 | 1608.05 | 6.26 | 8.95 | 2175.37 | 3281.95 | 0.00 | 99.90 |
| gpt-5.6-luna | PayGo Global | swedencentral | 2026-10-27 | none | — | 20/20 | 2406.86 | 1891.22 | 5.39 | 6.08 | 3481.42 | 4065.91 | 0.00 | 99.90 |
| gpt-5.6-luna | PayGo Data Zone | swedencentral | 2026-10-27 | none | — | 20/20 | 1899.39 | 1465.37 | 6.10 | 6.57 | 3227.68 | 3614.03 | 0.00 | 99.90 |
| gpt-5.6-luna | PTU Global | swedencentral | 2026-10-27 | none | 15 | 19/20 | 2227.94 | 1993.66 | 4.86 | 5.72 | 3424.56 | 3911.16 | 0.00 | 0.00 |
| gpt-5.6-luna | PTU Data Zone | swedencentral | 2026-10-27 | none | 15 | 20/20 | 1622.41 | 1389.60 | 4.90 | 5.31 | 2826.76 | 3091.62 | 0.00 | 0.00 |
| gpt-5.6-terra | PayGo Global | swedencentral | 2026-10-27 | none | — | 20/20 | 1858.41 | 2033.86 | 8.02 | 8.66 | 4419.66 | 4669.92 | 0.00 | 99.90 |
| gpt-5.6-terra | PayGo Data Zone | swedencentral | 2026-10-27 | none | — | 20/20 | 4725.92 | 2191.59 | 8.29 | 8.96 | 4665.99 | 10341.29 | 0.00 | 99.90 |
| gpt-5.6-terra | PTU Global | swedencentral | 2026-10-27 | none | 15 | 18/20 | 1986.82 | 1697.99 | 7.62 | 8.41 | 3914.59 | 4434.74 | 0.00 | 0.00 |
| gpt-5.6-terra | PTU Data Zone | swedencentral | 2026-10-27 | none | 15 | 18/20 | 1827.30 | 1636.56 | 7.80 | 12.15 | 3982.26 | 5412.41 | 0.00 | 0.00 |
| gpt-6-sol | PayGo Global | swedencentral | 2026-11-03 | none | — | 19/20 | 4363.24 | 2209.70 | 7.95 | 10.06 | 2955.16 | 5180.85 | 0.00 | 99.90 |
| gpt-6-sol | PayGo Data Zone | swedencentral | 2026-11-03 | none | — | 20/20 | 1881.17 | 1680.12 | 9.43 | 10.92 | 2435.60 | 4456.79 | 0.00 | 99.90 |
| gpt-6-sol | PTU Global | swedencentral | 2026-11-03 | none | 15 | 19/20 | 6779.11 | 2682.79 | 5.85 | 9.12 | 3158.66 | 7353.41 | 0.00 | 99.90 |
| gpt-6-sol | PTU Data Zone | eastus2 | 2026-11-03 | none | 15 | 20/20 | 3002.63 | 2079.41 | 6.44 | 8.57 | 2643.66 | 3510.89 | 0.00 | 99.90 |
| gpt-6.1-sol | PayGo Global | swedencentral | 2026-11-03 | low | — | 20/20 | 3165.60 | 2365.56 | 15.19 | 16.73 | 6841.76 | 8550.35 | 0.00 | 99.90 |
| gpt-6.1-sol | PayGo Data Zone | swedencentral | 2026-11-03 | low | — | 20/20 | 3205.52 | 2347.47 | 14.67 | 16.41 | 6675.92 | 7408.41 | 0.00 | 99.90 |
| gpt-6.1-sol | PTU Global | swedencentral | 2026-11-03 | low | 15 | 16/20 | 4483.41 | 2461.52 | 11.91 | 16.05 | 5989.60 | 7533.57 | 0.00 | 99.90 |
| gpt-6.1-sol | PTU Data Zone | swedencentral | 2026-11-03 | low | 15 | 16/20 | 3768.57 | 2143.92 | 11.75 | 12.84 | 5582.17 | 7183.55 | 0.00 | 99.90 |

## Actual token averages

| Model | Deployment | Mean input tokens | Mean total output tokens | Mean reasoning tokens | Mean visible output tokens |
|---|---|---:|---:|---:|---:|
| gpt-6-luna | PayGo Global | 3012.00 | 81.45 | 0.00 | 81.45 |
| gpt-6-luna | PayGo Data Zone | 3012.00 | 69.05 | 0.00 | 69.05 |
| gpt-6-luna | PTU Global | 3012.00 | 84.20 | 0.00 | 84.20 |
| gpt-6-luna | PTU Data Zone | 3012.00 | 76.11 | 0.00 | 76.11 |
| gpt-6.1-terra | PayGo Global | 3012.00 | 90.30 | 0.00 | 90.30 |
| gpt-6.1-terra | PayGo Data Zone | 3012.00 | 92.47 | 0.00 | 92.47 |
| gpt-5.6-luna | PayGo Global | 3012.00 | 292.85 | 0.00 | 292.85 |
| gpt-5.6-luna | PayGo Data Zone | 3012.00 | 287.70 | 0.00 | 287.70 |
| gpt-5.6-luna | PTU Global | 3012.00 | 293.32 | 0.00 | 293.32 |
| gpt-5.6-luna | PTU Data Zone | 3012.00 | 292.90 | 0.00 | 292.90 |
| gpt-5.6-terra | PayGo Global | 3012.00 | 296.55 | 0.00 | 296.55 |
| gpt-5.6-terra | PayGo Data Zone | 3012.00 | 296.55 | 0.00 | 296.55 |
| gpt-5.6-terra | PTU Global | 3012.00 | 290.56 | 0.00 | 290.56 |
| gpt-5.6-terra | PTU Data Zone | 3012.00 | 299.50 | 0.00 | 299.50 |
| gpt-6-sol | PayGo Global | 3012.00 | 95.16 | 0.00 | 95.16 |
| gpt-6-sol | PayGo Data Zone | 3012.00 | 79.00 | 0.00 | 79.00 |
| gpt-6-sol | PTU Global | 3012.00 | 79.95 | 0.00 | 79.95 |
| gpt-6-sol | PTU Data Zone | 3012.00 | 87.40 | 0.00 | 87.40 |
| gpt-6.1-sol | PayGo Global | 3012.00 | 302.00 | 9.50 | 292.50 |
| gpt-6.1-sol | PayGo Data Zone | 3012.00 | 302.00 | 7.35 | 294.65 |
| gpt-6.1-sol | PTU Global | 3012.00 | 302.00 | 6.12 | 295.88 |
| gpt-6.1-sol | PTU Data Zone | 3012.00 | 302.00 | 10.00 | 292.00 |

## Unmeasured combinations

| Model | Deployment | Status | Region/check scope | Last check |
|---|---|---|---|---|
| gpt-6-luna | PayGo Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-10-27 |
| gpt-6-luna | PTU Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-10-27 |
| gpt-6.1-terra | PayGo Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-10-27 |
| gpt-6.1-terra | PTU Global | not_listed_in_checked_subscriptions | all_regions_checked | 2026-11-03 |
| gpt-6.1-terra | PTU Data Zone | not_listed_in_checked_subscriptions | all_regions_checked | 2026-11-03 |
| gpt-6.1-terra | PTU Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-11-03 |
| gpt-5.6-luna | PayGo Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-10-27 |
| gpt-5.6-luna | PTU Regional | blocked_by_policy | eastus2 | 2026-10-27 |
| gpt-5.6-terra | PayGo Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-10-27 |
| gpt-5.6-terra | PTU Regional | blocked_by_policy | westus | 2026-10-27 |
| gpt-6-sol | PayGo Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-11-03 |
| gpt-6-sol | PTU Regional | blocked_by_policy | uaenorth | 2026-11-03 |
| gpt-6.1-sol | PayGo Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-11-03 |
| gpt-6.1-sol | PTU Regional | not_listed_in_checked_subscriptions | all_regions_checked | 2026-11-03 |

GPT-6 Sol Regional PTU at 50 PTUs in UAE North was attempted and rejected by the MCAPS Azure policy. GPT-6.1 Sol Regional PTU and both Sol Regional PayGo types were absent from the all-region capacity query responses. No Regional PTU timing has been substituted from a Global or Data Zone deployment.

GPT-6.1 Terra managed PTU remains absent from the checked subscriptions. Other historical unmeasured rows retain the check dates shown above.

TBT p95 is a percentile across per-request mean inter-token estimates derived from streamed chunks. Cache percentages use reported token counters. Timing summaries cover successful requests; unsuccessful attempts remain counted. Actual generated output lengths differ by model.

[Full CSV](summary.csv) · [JSON](summary.json) · [Sanitized request timings](requests.jsonl) · [Default settings](settings.json) · [GPT-6.1 Sol settings](settings-sol61-low.json) · [Metadata](metadata.json) · [GPT-6 capacity review](availability-review.json)
