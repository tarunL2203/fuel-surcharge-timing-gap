# Fuel Surcharge Policy and Exposure Analytics

Version 2.0 | Owner: Sai Tarun Reddy | Revised September 27, 2026 (America/New_York)

## Data and execution limits come first

The owner profiled 16,275 weekly diesel-price observations across 10 geographies, with overall coverage March 21, 1994 through June 22, 2026. Geography start dates differ. Historical loading and an unchanged rerun are recorded in [Phase 2 evidence](../outputs/phase_2/REAL_SNOWFLAKE_REPORT.md). The feed is stale; the cause is unresolved. There are no private contracts, shipments, invoices or observed brokerage margins in this dataset.

This project will calculate **historical policy simulations using real prices and illustrative rules**. Existing published charts, local tests and the app remain the original SYNTHETIC demonstration. The revised model is specified, not implemented or executed. No Snowflake model is certified by this documentation change.

## Business question and motivation

How do surcharge rules, index lags and adjustment schedules change calculated fuel charges, and can every result be explained from its source observation and policy version?

The engineering challenge is turning a small external dataset into reliable, repeatable decisions: validating incoming data, handling corrections, interpreting effective dates, avoiding future information in date selection, reporting missing inputs, and reconciling detailed calculations to summaries. Size alone is not the reason to use Snowflake.

The initial proposed audience is pricing and finance teams at mid-market shippers. Brokers with separately identified customer and carrier fuel terms are a secondary audience. This audience selection is a research-informed hypothesis, not validated product demand. The Broker's Two Clocks remains the name of a possible paired-policy scenario, not a universal industry description.

## Evidence-based scope

[The research record](research/fuel_policy_evidence.md) supports index-linked rules, review-frequency decisions and invoice checks as practical concerns. It does not establish that carriers normally reset weekly while shippers reset monthly or quarterly. A monthly bill does not imply a monthly reset.

V1 compares three illustrative per-mile policies: a weekly baseline, a weekly policy with one additional week of index lag, and a monthly policy. All use the same geography and formula parameters to isolate one change at a time. Quarterly resets and seasonal uplifts remain optional stress tests in the old sample; they are excluded from the new default model.

The published FedEx Freight example illustrates effective-date complexity and customer overrides. It is not a truckload brokerage contract, and its percentage schedule must not be substituted into our per-mile formula. No named carrier's actual charges are reproduced in v1.

## Delivery plan

| Phase | Current state | Next deliverable |
|---|---|---|
| 0: framing/setup | Setup exists; business framing revised | This brief and evidence register |
| 1: source profiling | Owner-run profiling complete | Preserve coverage and source limitations |
| 2: historical landing | Initial load owner-confirmed; unchanged rerun and no duplicates exported | Preserve RAW and configuration; failure-path certification remains open |
| 3: policy model | Revised specification ready; implementation pending | Policy versions, date mapping, calculation detail, eligibility log and comparisons |
| 4: validation/analysis | Old synthetic tests exist only | New known-answer tests, boundary checks and reconciled historical scenario results |
| 5: app/story | Old synthetic app exists only | Policy explorer, traceable calculations, coverage warnings and qualified memo |
| 6: operations/release | Pending | Refresh, costs, permissions, recovery and final release evidence |

GitHub phase-N branches are change batches, not Snowflake execution phases. For example, phase-11 records this design revision; the owner is still preparing for Snowflake Phase 3.

## Implementation contract

[PHASE_3_MODEL_SPEC.md](PHASE_3_MODEL_SPEC.md) is authoritative for the new model and acceptance tests. [SNOWFLAKE_NEXT_STEPS.md](SNOWFLAKE_NEXT_STEPS.md) is the current execution guide. Do not run the old 04/04b/05 chain for the revised model.

Keep accepted RAW prices and Phase 2 source settings. Add new policy configuration alongside existing tables; do not repurpose legacy S1-S6 identifiers or overwrite their historical reports. Use shared SQL SELECTs for local and Snowflake versions. All metrics come from SQL. Mark deployment SQL UNVERIFIED until executed in the intended account.

Use seed 42 and AS_OF_DATE 2026-09-23 for the preserved synthetic demonstration. For the real-source checkpoint, retain the recorded AS_OF_DATE 2026-09-27 and record any later change explicitly. Do not move the clock backward to hide stale data. Keep the task suspended while freshness and scheduling readiness are unresolved.

## Acceptance and claims

New model acceptance requires zero unexplained policy overlaps, correct date and lag boundaries, identical-policy zero differences, correct handling of missing prices, and reconciliation of detail, exclusions and summaries. A partial month must not become complete merely because today's date is later than the source tail. Regional comparisons use common eligible weeks, and overlapping geographies are never added as independent markets.

Use “modeled surcharge difference,” not realized savings, margin leakage or total profit. Assumed miles and load counts must be explicit. Even a real-price simulation is not evidence of an actual invoice outcome. Real contracts, shipment dates and billed amounts are needed for a business pilot.

## Working rules and historical record

Follow AGENTS.md: work on phase-N branches, open a pull request, never push directly to main, and merge only on explicit request. Do not commit credentials, account identifiers, real listing extracts or database binaries. Record failed tests honestly; stop on unexplained invariants or conflicting rules.

The [original brief](archive/BUILD_BRIEF_v1.md), old shared models, app, reports and tests remain historical synthetic artifacts. Their numerical outputs have not been reinterpreted as validation of this revised design. This brief supersedes their instructions for the forthcoming real-source modeling track.
