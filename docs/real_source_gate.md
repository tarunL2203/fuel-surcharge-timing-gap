# Real-source gate: profiling complete; scheduling gate open

Updated September 27, 2026 from owner-run Snowflake checks and reviewed summary exports. Phase 1 source inspection and adapter validation are complete. This is not full operational-source sign-off. See [dataset availability and evidence](dataset_availability.md).

| Gate | Evidence needed | Current status |
|---|---|---|
| 1 | Listing accessible, source objects and schema known | Owner accessed and profiled a standardized adapter in Snowflake; exact reproducible adapter SQL still needs a reviewed repository addition |
| 2 | Retail on-highway diesel variable identified | PASS: one canonical diesel variable reported |
| 3 | Dollars per gallon confirmed; range investigated | Units confirmed; observed range $0.916–$7.567. Review the configured $1 minimum before loading valid historical prices |
| 4 | Actual geographies checked, including variables; choose US-only or regions | 10 geographies observed; analytical scope and common comparison window must be explicit |
| 5 | Latest date, provider lag and task schedule justified | OPEN: latest observed date June 22, 2026. Provider lag/cause and schedule readiness unresolved |
| 6 | Weekly cadence, duplicates, gaps and shifted dates reviewed | Owner reports zero duplicate-key, non-seven-day-gap and reconciliation exceptions; retain exact queries/results for reproducibility |

The summary exports show 16,275 rows, one canonical variable and zero null prices. Check results reported in chat are distinguished from directly reviewed summaries in the evidence note.

STOP if there is no retail diesel series or it is not weekly. Unexpected units or a broken schema block landing. Geography limits scope; it does not by itself stop the national model. Do not enable the load task until the six answers, adapter schema and first manual load are reviewed.

Historical loading can be evaluated with the stale status explicitly retained, after documenting the source review and price-bound decision. This documentation does not set the configuration approval flag or approve automatic scheduling.

Original referenced profiling “Steps 0 to 9” were not attached. The numbered checks in sql/01_profiling.sql implement the six stated gates; they do not claim to reproduce an unseen earlier worksheet.
