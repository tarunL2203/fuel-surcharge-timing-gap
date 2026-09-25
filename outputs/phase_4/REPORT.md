# Phase 4: Measure the spread [SYNTHETIC DRY RUN]

Business question: How does timing change the downside distribution?

What was built: see docs/phase_file_map.md and the evidence files below.

How it ran: `python local/run_pipeline.py all`, followed by verify_outputs.py, test_pipeline.py and test_app.py. Full pipeline runs took about 40–43 seconds here, excluding dependency installation.

Sample results:

| scenario_id | first_date | last_date | weeks | mean_spread | mean_dollars_per_1000_loads | squeeze_share |
| --- | --- | --- | --- | --- | --- | --- |
| S1 | 2002-01-07 | 2026-06-29 | 1278 | 0.000000 | 0.000000 | 0.000000 |
| S2 | 2002-01-07 | 2026-06-29 | 1278 | 0.009969 | 4984.350548 | 0.000000 |
| S3 | 2002-01-07 | 2026-06-29 | 1278 | 0.000027 | 13.432447 | 0.373239 |
| S4 | 2002-01-07 | 2026-06-29 | 1278 | 0.009996 | 4997.782994 | 0.165884 |
| S5 | 2002-01-07 | 2026-06-29 | 1278 | 0.000135 | 67.553469 | 0.442097 |
| S6 | 2002-01-07 | 2026-06-29 | 1278 | 0.010104 | 5051.904017 | 0.206573 |

Validation: INV-01 through INV-05 pass. E1 and E3 pass all regions. E2 passes both regimes. Exact errors and confusion matrix are saved as CSVs.

| Check | Expected | Observed | Status |
|---|---|---|---|
| INV-01 through INV-05 | Zero failing rows | Zero failing rows | PASS |
| E1 maximum error | At most 1 percentage point | 0.29374 percentage points | PASS |
| E2 rising / falling | At least 70% each | 93.59% / 89.74% | PASS |
| E3 maximum error | At most 1 percentage point | 0.05497 percentage points | PASS |
| E4 sign compliance | 100% | 100% | PASS |

Table evidence: existing phase CSVs and outputs/review/INDEPENDENT_CHECKS.json; execution evidence is in outputs/review/RERUN_LOG.txt and outputs/phase_6/SYNTHETIC_verification_log.txt.

Surprises and fixes: DuckDB rejected weeks and error as implicit aliases; explicit aliases fixed them. Final repeatability checks exposed sensitivity state leaking into baseline outputs. Each sensitivity scenario now runs in a transaction that is rolled back, with assertions that both parameters and weekly rows are unchanged. No source values or expected answers were changed.

Learnings:

- Technical: Summaries reconcile to detail.
- Data: Recovery is expected for planted effects.
- Analytical: Positive means can hide adverse weeks.
- Business: Review downside distributions.

Understanding the results:

1. What do these results show? INV-01 through INV-05 pass. E1 and E3 pass all regions. E2 passes both regimes. Exact errors and confusion matrix are saved as CSVs.
2. What remains unverified? Actual company margins or untested Snowflake behavior.
3. Why does it matter? Review downside distributions.

Exit criteria: local synthetic evidence is complete with documented scope gaps in docs/acceptance_status.md. Deployment and real-source criteria remain unverified. Publication is confirmed by GitHub PR links, not simulated pushes.

Evidence files:

- `outputs/phase_4/SYNTHETIC_E1_seasonality_recovery.csv`
- `outputs/phase_4/SYNTHETIC_E2_confusion_matrix.csv`
- `outputs/phase_4/SYNTHETIC_E2_recovery.csv`
- `outputs/phase_4/SYNTHETIC_E3_offset_recovery.csv`
- `outputs/phase_4/SYNTHETIC_clause.png`
- `outputs/phase_4/SYNTHETIC_clause_effect.csv`
- `outputs/phase_4/SYNTHETIC_monthly_seasonal_index.csv`
- `outputs/phase_4/SYNTHETIC_recovery.png`
- `outputs/phase_4/SYNTHETIC_regime_season.csv`
- `outputs/phase_4/SYNTHETIC_regime_season.png`
- `outputs/phase_4/SYNTHETIC_regions.png`
- `outputs/phase_4/SYNTHETIC_regions_common_window.csv`
- `outputs/phase_4/SYNTHETIC_same_window_contracts.csv`
- `outputs/phase_4/SYNTHETIC_sensitivity.csv`
- `outputs/phase_4/SYNTHETIC_spread.png`
- `outputs/phase_4/SYNTHETIC_summary.csv`
- `outputs/phase_4/SYNTHETIC_validation.csv`
- `outputs/phase_4/SYNTHETIC_worst_stretches.csv`
