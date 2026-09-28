# Snowflake: next steps after the Phase 3 design revision

Current checkpoint: real historical prices are loaded; revised policy-model implementation is pending. No reload is needed. This document replaces the old instruction to run sql/04_dynamic_tables.sql next.

## Do now: read-only preflight

1. Create a fresh SQL worksheet named `Phase 3 - Policy Analytics`.
2. Open [sql/03a_policy_preflight.sql](../sql/03a_policy_preflight.sql). Run the USE statements first, then each SELECT separately so every result is visible.
3. Export the overall coverage summary, per-geography coverage, latest loader summary and duplicate-check result. Keep identifiers and source extracts private; only reviewed summaries belong in GitHub.
4. Inspect the task state with the final SHOW statement. The loader task should remain suspended. SHOW output is separate from SELECT results; zero returned rows means the expected task was not found or visible, not proof of success.

Expected from the recorded Phase 2 checkpoint: 16,275 RAW rows, 10 geographies, latest week June 22, 2026, and no duplicate groups. Configuration retained from that run: AS_OF_DATE 2026-09-27, MIN_PRICE 0.50, MAX_PRICE 8, freshness threshold 10 days. A changed result should be investigated rather than forced to match.

Do not rerun setup, overwrite source configuration, reseed legacy defaults, reload RAW, resume tasks, or deploy the old 04/04b/05 scripts as part of this preflight. The old six-scenario tables remain the synthetic reference.

## What we will build next

| Step | GitHub deliverable | Snowflake action after code review |
|---|---|---|
| 3A | Versioned illustrative policy seeds | Add policy tables alongside existing configuration |
| 3B | Shared date-selection and formula SQL with known-answer fixtures | Calculate policy detail and named exclusions |
| 3C | Comparison SQL and validation queries | Compare weekly baseline, extra lag and monthly reset on common dates |
| 3D | Evidence template and revised app integration | Export validation summaries; connect app only after model passes |

Those implementation files do not exist yet. [The specification](PHASE_3_MODEL_SPEC.md) defines their exact rules and tests. The current PR completes the requested brief/specification revision; it does not claim that the revised model is deployable.

## Evidence to record at model completion

Save run and policy version, query IDs, coverage, eligible/excluded counts, test results and reviewed calculation summaries. Record actual Snowflake execution separately from local tests. Do not publish real listing extracts, credentials or account identifiers. Continue to label all outputs as historical simulations until real contract and invoice evidence exists.
