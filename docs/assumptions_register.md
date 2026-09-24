# Assumptions register

All values are **ILLUSTRATIVE** until replaced by a cited schedule or by Phase 1 profiling.

| ID | Parameter | Default | Sensitivity range | Rationale |
|---|---|---|---|---|
| A-01 | BASE_PRICE | 1.25 $/gal | 1.00 to 1.50 | Placeholder; replace with the cited schedule's value |
| A-02 | MPG | 6.0 | 5.5 to 7.0 | Fleet fuel economy assumed inside the schedule |
| A-03 | INDEX_LAG_WEEKS | 0 | 0 to 1 | Price published for week w applies to week w |
| A-04 | RESET_FREQUENCIES | WEEKLY, MONTHLY, QUARTERLY | fixed | Scenario design |
| A-05 | STEP_UP_PER_MILE | 0.02 $/mile | 0.01 to 0.04 | Clause size; tested, not recommended |
| A-06 | HEATING_MONTHS | Oct to Mar | fixed | EIA heating oil survey window |
| A-07 | REGIME_THRESHOLD | 3% over 4 weeks | 2% to 5% | Separates trend from weekly noise |
| A-08 | LOAD_MILES | 500 | 250 to 1,000 | Business translation only |
| A-09 | FRESHNESS_MAX_DAYS | 10 | set from Phase 1 item 5 | Weekly data plus listing lag |
| A-10 | PRICE_RANGE | 1.00 to 8.00 $/gal | set from Phase 1 Step 8 | Catches unit errors |
| A-11 | BATCH_MAX_BAD_PCT | 5% | 1% to 10% | Separates row issues from a broken batch |

All schedule and threshold values remain ILLUSTRATIVE. EIA season convention is a descriptive grouping, not proof of causation. Additional operational parameters: seed=42, as_of_date=2026-09-23, monthly warehouse quota=5 illustrative credits, daily downstream target lag. Review costs and freshness cadence in the real-source gate.
