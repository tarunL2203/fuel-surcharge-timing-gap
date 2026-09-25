# Sources and limits

Checked 2026-09-24. No source establishes an individual broker's margins.

- Snowflake CREATE DYNAMIC TABLE: https://docs.snowflake.com/en/sql-reference/sql/create-dynamic-table ; syntax for lag, warehouse and refresh mode.
- Snowflake target lag: https://docs.snowflake.com/en/user-guide/dynamic-tables/target-lag ; DOWNSTREAM requires a scheduled downstream consumer.
- Snowflake resource monitors: https://docs.snowflake.com/en/user-guide/resource-monitors ; warehouse guardrails, not an absolute cap on every account charge.
- EIA survey definitions: https://www.eia.gov/Survey/ ; EIA-888 is weekly on-highway retail diesel; EIA-877 is weekly October-March and monthly April-September. This supports a season label, not a causal diesel-price claim.
- Public formula-style surcharge schedule: TODO(source). Base price and miles-per-gallon assumptions remain ILLUSTRATIVE, not industry-standard values.
- Listing availability, regional coverage, lag and free access: TODO(Phase 1 real-source profiling). No Marketplace listing has been inspected.
- Trial/Cortex availability: TODO(account verification). Optional AI features are excluded from the core build.

The original brief contains stronger assumptions about trial access and Marketplace availability. Treat those as unverified until checked in the actual account.

## Business-process evidence

The [business-flow validation record](business_flow_validation.md) documents a September 24, 2026 public-source check of FMCSA roles, EIA surcharge guidance and C.H. Robinson contract-pricing commentary. It distinguishes sourced facts from scenario assumptions and lists the contract/invoice evidence still required. Public-source review does not validate a particular broker’s contracts.
