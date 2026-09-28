# Sources and limits

Public-source references checked 2026-09-24; dataset status updated from the owner's September 27, 2026 Snowflake profiling results. No source establishes an individual broker's margins.

Read [dataset availability and evidence](dataset_availability.md) first: the inspected output ends June 22, 2026, and the published analytical outputs remain SYNTHETIC. Real prices do not provide actual contract or shipment economics.

- Snowflake CREATE DYNAMIC TABLE: https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table ; syntax for lag, warehouse and refresh mode.
- Snowflake target lag: https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag ; DOWNSTREAM requires a scheduled downstream consumer.
- Snowflake resource monitors: https://docs.snowflake.com/en/user-guide/resource-monitors ; warehouse guardrails, not an absolute cap on every account charge.
- EIA survey definitions: https://www.eia.gov/Survey/ ; EIA-888 is weekly on-highway retail diesel; EIA-877 is weekly October-March and monthly April-September. This supports a season label, not a causal diesel-price claim.
- Public formula-style surcharge schedule: TODO(source). Base price and miles-per-gallon assumptions remain ILLUSTRATIVE, not industry-standard values.
- Listing availability and coverage: owner completed real-source profiling in Snowflake on September 27, 2026. Reviewed summaries show 16,275 observations, 10 geographies and data through June 22, 2026. Provider lag, refresh behavior, source terms and ongoing access/cost conditions remain unresolved. This does not establish that EIA's upstream publications end on that date.
- Trial/Cortex availability: TODO(account verification). Optional AI features are excluded from the core build.

The original brief contains stronger assumptions about trial access and Marketplace availability. Treat those as unverified until checked in the actual account.

## Business-process evidence

The [business-flow validation record](business_flow_validation.md) documents a September 24, 2026 public-source check of FMCSA roles, EIA surcharge guidance and C.H. Robinson contract-pricing commentary. It distinguishes sourced facts from scenario assumptions and lists the contract/invoice evidence still required. Public-source review does not validate a particular broker’s contracts.
