# Live Azure Responses API results — 27 October 2026

Live measurements from temporary deployments in **Sweden Central**, using the repository runner. Timings below are **milliseconds**. CSV/JSON timing values are **seconds**.

60-second arrival window per deployment; 20 scheduled requests/minute; concurrency cap 4; 3,006 synthetic content tokens; 302 output-token cap; reasoning `none`; cold unique-prefix prompts; one excluded warmup. The actual generated token averages are in the workload table below.

| Model | Deployment | PTUs | Success/attempts | TTFT p95 | TTFT avg | TBT avg | TBT p95 | E2E avg | E2E p95 | Read cache % | Write cache % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-6-luna | PayGo Global | — | 20/20 | 2569.83 | 1785.82 | 8.70 | 10.17 | 2554.69 | 4066.58 | 0.00 | 99.90 |
| gpt-6-luna | PayGo Data Zone | — | 19/20 | 2552.22 | 1563.11 | 9.99 | 29.21 | 2256.76 | 3826.54 | 0.00 | 99.90 |
| gpt-6.1-terra | PayGo Global | — | 20/20 | 2707.78 | 1903.55 | 6.94 | 10.15 | 2486.72 | 3367.23 | 0.00 | 99.90 |
| gpt-6.1-terra | PayGo Data Zone | — | 19/20 | 2669.23 | 1608.05 | 6.26 | 8.95 | 2175.37 | 3281.95 | 0.00 | 99.90 |
| gpt-5.6-luna | PayGo Global | — | 20/20 | 2406.86 | 1891.22 | 5.39 | 6.08 | 3481.42 | 4065.91 | 0.00 | 99.90 |
| gpt-5.6-luna | PayGo Data Zone | — | 20/20 | 1899.39 | 1465.37 | 6.10 | 6.57 | 3227.68 | 3614.03 | 0.00 | 99.90 |
| gpt-5.6-luna | PTU Global | 15 | 19/20 | 2227.94 | 1993.66 | 4.86 | 5.72 | 3424.56 | 3911.16 | 0.00 | 0.00 |
| gpt-5.6-luna | PTU Data Zone | 15 | 20/20 | 1622.41 | 1389.60 | 4.90 | 5.31 | 2826.76 | 3091.62 | 0.00 | 0.00 |
| gpt-5.6-terra | PayGo Global | — | 20/20 | 1858.41 | 2033.86 | 8.02 | 8.66 | 4419.66 | 4669.92 | 0.00 | 99.90 |
| gpt-5.6-terra | PayGo Data Zone | — | 20/20 | 4725.92 | 2191.59 | 8.29 | 8.96 | 4665.99 | 10341.29 | 0.00 | 99.90 |
| gpt-5.6-terra | PTU Global | 15 | 18/20 | 1986.82 | 1697.99 | 7.62 | 8.41 | 3914.59 | 4434.74 | 0.00 | 0.00 |
| gpt-5.6-terra | PTU Data Zone | 15 | 18/20 | 1827.30 | 1636.56 | 7.80 | 12.15 | 3982.26 | 5412.41 | 0.00 | 0.00 |

## Actual workload

| Model | Deployment | Mean input tokens | Mean output tokens |
|---|---|---:|---:|
| gpt-6-luna | PayGo Global | 3012.00 | 81.45 |
| gpt-6-luna | PayGo Data Zone | 3012.00 | 69.05 |
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

## Other requested combinations

| Model | Deployment | Region checked | Result |
|---|---|---|---|
| gpt-6-luna | PayGo Regional | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-6-luna | PTU Global | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-6-luna | PTU Data Zone | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-6-luna | PTU Regional | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-6.1-terra | PayGo Regional | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-6.1-terra | PTU Global | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-6.1-terra | PTU Data Zone | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-6.1-terra | PTU Regional | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-5.6-luna | PayGo Regional | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-5.6-luna | PTU Regional | eastus2 | blocked_by_policy |
| gpt-5.6-terra | PayGo Regional | All regions in the two checked subscriptions | not_listed_in_checked_subscriptions |
| gpt-5.6-terra | PTU Regional | westus | blocked_by_policy |

TBT p95 is the p95 across per-request mean inter-token estimates derived from streamed chunks. Read/write cache percentages use reported cache tokens divided by reported input tokens; **—** means the API did not report that field. Latencies cover successful responses; success counts retain failed attempts.

Exact model versions: `gpt-6-luna` → `2026-09-22`, `gpt-6.1-terra` → `2026-10-26`, `gpt-5.6-luna` → `2026-07-09`, `gpt-5.6-terra` → `2026-07-09`.

[Full 24-row CSV](summary.csv) · [JSON](summary.json) · [Run settings](settings.json) · [Metadata](metadata.json)

## Cross-region review

The all-region model-capacity API was queried for every unmeasured model/SKU combination in both the MCAPS benchmark subscription and the Azure AI MaaS subscription. There were no pagination links left unread. `not_listed_in_checked_subscriptions` means the combination had no matching SKU entry in those responses; it is scoped to the subscriptions queried.

GPT-5.6 Luna Regional PTU was listed in East US 2 and UK South. The additional UK South attempt at 50 PTUs was rejected by the MCAPS Azure policy, matching the earlier East US 2 rejection. GPT-5.6 Terra Regional PTU was listed in West US, where the MCAPS attempt was also policy-rejected.

Azure AI MaaS is the `azureaimaas` tenant, containing the accessible subscription displayed as **Azure subscription 1**. Its model-specific Regional PTU quotas are zero for GPT-5.6 Luna in East US 2 and UK South and GPT-5.6 Terra in West US. The general 300-PTU allowance in East US 2 and UK South is a separate quota counter and does not provide the required model-specific quota.

[Sanitized capacity-query results and quota counters](availability-review.json).
