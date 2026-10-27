# Azure Responses API benchmark

Timing units: seconds. Cache units: percent of input tokens. TBT percentiles are across request-level mean inter-token estimates.

| model | deployment_type | region | ptus | status | requests | successes | failures | ttft_95th | ttft_avg | tbt_avg | tbt_95th | e2e_avg | e2e_95th | read_cache_pct | write_cache_pct | mean_input_tokens | mean_output_tokens |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-6-luna | PayGo Global | swedencentral | — | measured | 20 | 20 | 0 | 2.5698 | 1.7858 | 0.0087 | 0.0102 | 2.5547 | 4.0666 | 0.0000 | 99.9004 | 3012 | 81.4500 |
| gpt-6-luna | PayGo Data Zone | swedencentral | — | measured | 20 | 19 | 1 | 2.5522 | 1.5631 | 0.0100 | 0.0292 | 2.2568 | 3.8265 | 0.0000 | 99.9004 | 3012 | 69.0526 |
| gpt-6-luna | PayGo Regional | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-6-luna | PTU Global | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-6-luna | PTU Data Zone | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-6-luna | PTU Regional | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-6.1-terra | PayGo Global | swedencentral | — | measured | 20 | 20 | 0 | 2.7078 | 1.9036 | 0.0069 | 0.0101 | 2.4867 | 3.3672 | 0.0000 | 99.9004 | 3012 | 90.3000 |
| gpt-6.1-terra | PayGo Data Zone | swedencentral | — | measured | 20 | 19 | 1 | 2.6692 | 1.6080 | 0.0063 | 0.0090 | 2.1754 | 3.2819 | 0.0000 | 99.9004 | 3012 | 92.4737 |
| gpt-6.1-terra | PayGo Regional | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-6.1-terra | PTU Global | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-6.1-terra | PTU Data Zone | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-6.1-terra | PTU Regional | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-5.6-luna | PayGo Global | swedencentral | — | measured | 20 | 20 | 0 | 2.4069 | 1.8912 | 0.0054 | 0.0061 | 3.4814 | 4.0659 | 0.0000 | 99.9004 | 3012 | 292.8500 |
| gpt-5.6-luna | PayGo Data Zone | swedencentral | — | measured | 20 | 20 | 0 | 1.8994 | 1.4654 | 0.0061 | 0.0066 | 3.2277 | 3.6140 | 0.0000 | 99.9004 | 3012 | 287.7000 |
| gpt-5.6-luna | PayGo Regional | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-5.6-luna | PTU Global | swedencentral | 15 | measured | 20 | 19 | 1 | 2.2279 | 1.9937 | 0.0049 | 0.0057 | 3.4246 | 3.9112 | 0.0000 | 0.0000 | 3012 | 293.3158 |
| gpt-5.6-luna | PTU Data Zone | swedencentral | 15 | measured | 20 | 20 | 0 | 1.6224 | 1.3896 | 0.0049 | 0.0053 | 2.8268 | 3.0916 | 0.0000 | 0.0000 | 3012 | 292.9000 |
| gpt-5.6-luna | PTU Regional | eastus2 | 50 | blocked_by_policy | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-5.6-terra | PayGo Global | swedencentral | — | measured | 20 | 20 | 0 | 1.8584 | 2.0339 | 0.0080 | 0.0087 | 4.4197 | 4.6699 | 0.0000 | 99.9004 | 3012 | 296.5500 |
| gpt-5.6-terra | PayGo Data Zone | swedencentral | — | measured | 20 | 20 | 0 | 4.7259 | 2.1916 | 0.0083 | 0.0090 | 4.6660 | 10.3413 | 0.0000 | 99.9004 | 3012 | 296.5500 |
| gpt-5.6-terra | PayGo Regional | all_regions_checked | — | not_listed_in_checked_subscriptions | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
| gpt-5.6-terra | PTU Global | swedencentral | 15 | measured | 20 | 18 | 2 | 1.9868 | 1.6980 | 0.0076 | 0.0084 | 3.9146 | 4.4347 | 0.0000 | 0.0000 | 3012 | 290.5556 |
| gpt-5.6-terra | PTU Data Zone | swedencentral | 15 | measured | 20 | 18 | 2 | 1.8273 | 1.6366 | 0.0078 | 0.0121 | 3.9823 | 5.4124 | 0.0000 | 0.0000 | 3012 | 299.5000 |
| gpt-5.6-terra | PTU Regional | westus | 50 | blocked_by_policy | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — | — |
