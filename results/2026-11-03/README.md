# Combined Azure Responses API benchmark — updated 3 November 2026

Added **GPT-6 Luna Global PTU and Data Zone PTU**, measured on 3 November at **15 PTUs** in **Sweden Central**. The previous 12 measured rows retain their 27 October results. The CSV includes all 24 requested model/deployment combinations and the measurement date.

Workload for both dates: 60-second arrival window, 20 scheduled RPM, concurrency cap 4, 3,006 content tokens, 302 output-token cap, reasoning `none`, cold unique-prefix prompts and one excluded warmup. Actual generated token lengths are reported below.

Timing units in this table: **milliseconds**. CSV and JSON use **seconds**.

| Model | Deployment | Date | PTUs | Success/attempts | TTFT p95 | TTFT avg | TBT avg | TBT p95 | E2E avg | E2E p95 | Read cache % | Write cache % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-6-luna | PayGo Global | 2026-10-27 | — | 20/20 | 2569.83 | 1785.82 | 8.70 | 10.17 | 2554.69 | 4066.58 | 0.00 | 99.90 |
| gpt-6-luna | PayGo Data Zone | 2026-10-27 | — | 19/20 | 2552.22 | 1563.11 | 9.99 | 29.21 | 2256.76 | 3826.54 | 0.00 | 99.90 |
| gpt-6-luna | PTU Global | 2026-11-03 | 15 | 20/20 | 4239.64 | 2220.24 | 6.08 | 9.83 | 2741.99 | 4918.11 | 0.00 | 99.90 |
| gpt-6-luna | PTU Data Zone | 2026-11-03 | 15 | 18/20 | 3019.12 | 1520.94 | 5.01 | 10.12 | 1925.82 | 3440.69 | 0.00 | 99.90 |
| gpt-6.1-terra | PayGo Global | 2026-10-27 | — | 20/20 | 2707.78 | 1903.55 | 6.94 | 10.15 | 2486.72 | 3367.23 | 0.00 | 99.90 |
| gpt-6.1-terra | PayGo Data Zone | 2026-10-27 | — | 19/20 | 2669.23 | 1608.05 | 6.26 | 8.95 | 2175.37 | 3281.95 | 0.00 | 99.90 |
| gpt-5.6-luna | PayGo Global | 2026-10-27 | — | 20/20 | 2406.86 | 1891.22 | 5.39 | 6.08 | 3481.42 | 4065.91 | 0.00 | 99.90 |
| gpt-5.6-luna | PayGo Data Zone | 2026-10-27 | — | 20/20 | 1899.39 | 1465.37 | 6.10 | 6.57 | 3227.68 | 3614.03 | 0.00 | 99.90 |
| gpt-5.6-luna | PTU Global | 2026-10-27 | 15 | 19/20 | 2227.94 | 1993.66 | 4.86 | 5.72 | 3424.56 | 3911.16 | 0.00 | 0.00 |
| gpt-5.6-luna | PTU Data Zone | 2026-10-27 | 15 | 20/20 | 1622.41 | 1389.60 | 4.90 | 5.31 | 2826.76 | 3091.62 | 0.00 | 0.00 |
| gpt-5.6-terra | PayGo Global | 2026-10-27 | — | 20/20 | 1858.41 | 2033.86 | 8.02 | 8.66 | 4419.66 | 4669.92 | 0.00 | 99.90 |
| gpt-5.6-terra | PayGo Data Zone | 2026-10-27 | — | 20/20 | 4725.92 | 2191.59 | 8.29 | 8.96 | 4665.99 | 10341.29 | 0.00 | 99.90 |
| gpt-5.6-terra | PTU Global | 2026-10-27 | 15 | 18/20 | 1986.82 | 1697.99 | 7.62 | 8.41 | 3914.59 | 4434.74 | 0.00 | 0.00 |
| gpt-5.6-terra | PTU Data Zone | 2026-10-27 | 15 | 18/20 | 1827.30 | 1636.56 | 7.80 | 12.15 | 3982.26 | 5412.41 | 0.00 | 0.00 |

## Actual token averages

| Model | Deployment | Mean input tokens | Mean output tokens |
|---|---|---:|---:|
| gpt-6-luna | PayGo Global | 3012.00 | 81.45 |
| gpt-6-luna | PayGo Data Zone | 3012.00 | 69.05 |
| gpt-6-luna | PTU Global | 3012.00 | 84.20 |
| gpt-6-luna | PTU Data Zone | 3012.00 | 76.11 |
| gpt-6.1-terra | PayGo Global | 3012.00 | 90.30 |
| gpt-6.1-terra | PayGo Data Zone | 3012.00 | 92.47 |
| gpt-5.6-luna | PayGo Global | 3012.00 | 292.85 |
| gpt-5.6-luna | PayGo Data Zone | 3012.00 | 287.70 |
| gpt-5.6-luna | PTU Global | 3012.00 | 293.32 |
| gpt-5.6-luna | PTU Data Zone | 3012.00 | 292.90 |
| gpt-5.6-terra | PayGo Global | 3012.00 | 296.55 |
| gpt-5.6-terra | PayGo Data Zone | 3012.00 | 296.55 |
| gpt-5.6-terra | PTU Global | 3012.00 | 290.56 |
| gpt-5.6-terra | PTU Data Zone | 3012.00 | 299.50 |

## Unmeasured combinations

| Model | Deployment | Status | Last check |
|---|---|---|---|
| gpt-6-luna | PayGo Regional | not_listed_in_checked_subscriptions | 2026-10-27 |
| gpt-6-luna | PTU Regional | not_listed_in_checked_subscriptions | 2026-10-27 |
| gpt-6.1-terra | PayGo Regional | not_listed_in_checked_subscriptions | 2026-10-27 |
| gpt-6.1-terra | PTU Global | not_listed_in_checked_subscriptions | 2026-11-03 |
| gpt-6.1-terra | PTU Data Zone | not_listed_in_checked_subscriptions | 2026-11-03 |
| gpt-6.1-terra | PTU Regional | not_listed_in_checked_subscriptions | 2026-11-03 |
| gpt-5.6-luna | PayGo Regional | not_listed_in_checked_subscriptions | 2026-10-27 |
| gpt-5.6-luna | PTU Regional | blocked_by_policy | 2026-10-27 |
| gpt-5.6-terra | PayGo Regional | not_listed_in_checked_subscriptions | 2026-10-27 |
| gpt-5.6-terra | PTU Regional | blocked_by_policy | 2026-10-27 |

The 3 November all-region queries list GPT-6 Luna Global and Data Zone managed PTU in both checked subscriptions. GPT-6.1 Terra managed PTU is still absent; Azure AI MaaS lists a separate `Provisioned` SKU with zero available capacity. Other unmeasured rows retain their dated 27 October checks.

TBT p95 is the percentile across request-level mean inter-token estimates from streamed chunks. Cache percentages use service-reported token counters. Latencies include successful responses; failed attempts remain in the success counts. Cold mode changes the initial prompt prefix, so the measured read-cache percentage is zero.

[Full 24-row CSV](summary.csv) · [Summary JSON](summary.json) · [Sanitized request timings](requests.jsonl) · [Settings](settings.json) · [Current GPT-6 capacity review](availability-review.json) · [Metadata](metadata.json)
