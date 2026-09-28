# Dataset availability and engineering scope

Status reviewed September 27, 2026. This project has two evidence tracks: an executed synthetic end-to-end demonstration and owner-run real-source profiling in Snowflake. Published model outputs, charts and the decision memo still belong to the synthetic track.

## What was available in the inspected real source

| Observation | Reviewed result |
|---|---|
| Total rows | 16,275 |
| Geographies | 10 |
| Canonical variables | 1 |
| Units | USD per gallon |
| Overall coverage | March 21, 1994 through June 22, 2026 |
| Regional coverage | Starting dates differ; regional comparisons need a common window |
| Null prices | 0 |
| Observed price range | $0.916–$7.567 per gallon |

These describe the adapter output inspected in this account. They do not establish the latest upstream EIA publication date, a guaranteed update cadence, continued free access, or why this source ends on June 22. At the September 27 review the latest observation was 97 days old. Historical analysis remains possible; current operational use and automatic scheduling require further investigation.

## What the data cannot establish

Prices alone do not supply paired customer/carrier contracts, effective contract dates, shipment miles, volumes or invoice records. Weekly, monthly and quarterly reset schedules remain scenarios; the model's surcharge difference is not verified company profit. Geographic series overlap and must not be summed into a national total.

The real slice has 10 geographies; the synthetic fixture has 11. Synthetic expected counts and planted effects must not be used as real-data acceptance targets. Valid historical prices below $1 also show why sample defaults require review before the real load.

## Why the pipeline is the central contribution

The engineering question is how to make repeated scenario analysis trustworthy as inputs change. The work connects source adaptation, validation, change detection, quarantine, explicit schedule rules and traceable summaries.

| Capability | Current evidence |
|---|---|
| Standardize the real source into the model's expected columns | Owner-run Snowflake adapter profiling completed |
| Detect duplicates, missing dates, invalid values and stale data | Synthetic checks exercised; real profiling summaries reviewed |
| Load changes without duplicating history; preserve accepted values on invalid corrections | Local tests completed; Snowflake landing and unchanged-rerun test pending |
| Calculate different reset schedules with explicit missing-week rules | Shared SQL exercised locally; Snowflake model execution pending |
| Reconcile results and explain assumptions in an app | Synthetic outputs and local app tests available; real analysis and Snowflake app pending |
| Refresh and operate reliably over time | Permissions, scheduling, observed weekly runs and operating-cost evidence still required |

Snowflake is used to explore managed pipeline operation and application deployment. This small dataset does not establish a need for distributed scale, and no performance-at-scale claim is made.

## Evidence provenance

The owner executed the Snowflake checks and supplied exports on September 27. The documentation review inspected these summary files outside the repository:

- DataValP1_2026-09-27-2136.csv: total rows, geographies, variables, overall dates, null prices and price range.
- DataValP1_2026-09-27-2131.csv: dates and counts by geography.
- DataValP1_2026-09-27-2129.csv: counts by geography.
- DataValP1_2026-09-27-2134.csv: price ranges by geography.

The owner separately reported zero duplicate-key, non-seven-day-gap and reconciliation exceptions, and confirmed the canonical variable and units. Those are reported checks, not independent live re-execution by this documentation review.

Only aggregate profiling findings are recorded here. Repository rules exclude real listing extracts and account identifiers. Exact adapter SQL and reproducible check definitions still need a reviewed addition; this note does not claim to replace that evidence.

## Next checkpoint

Prepare the real-source configuration and justified price bounds, deploy the landing procedure with its task suspended, inspect the first manual load, and prove that an unchanged rerun inserts and updates zero rows. Preserve stale-data warnings and keep synthetic and real analytical outputs separate. See [the source gate](real_source_gate.md) and [acceptance status](acceptance_status.md).
