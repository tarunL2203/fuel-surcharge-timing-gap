# Phase 1: Profile the listing [SYNTHETIC DRY RUN]

Business question: Can the source support two clocks?

What was built: see docs/phase_file_map.md and the evidence files below.

How it ran: `python local/run_pipeline.py all`, followed by verify_outputs.py, test_pipeline.py and test_app.py. Full pipeline runs took about 40–43 seconds here, excluding dependency installation.

Sample results:

| trap | expected | actual | passed |
| --- | --- | --- | --- |
| T1 | 3 | 3 | True |
| T2 | 2 | 2 | True |
| T3 | 1 | 1 | True |
| T4 | 1 | 1 | True |
| T5 | 44 | 44 | True |
| T6 | 3 | 3 | True |
| T7 | 10 | 10 | True |
| T8 | 16 | 16 | True |

Validation: All eight traps matched expected values. Six synthetic profiling answers are recorded in docs/SYNTHETIC_profile_checklist.md. The real-source gate is NOT RUN.

| Check | Expected | Observed | Status |
|---|---|---|---|
| Source records | 14,947 | 14,947 | PASS |
| Planted traps | T1 through T8 detected | 8 of 8 | PASS |

Table evidence: existing phase CSVs and outputs/review/INDEPENDENT_CHECKS.json; execution evidence is in outputs/review/RERUN_LOG.txt and outputs/phase_6/SYNTHETIC_verification_log.txt.

Surprises and fixes: DuckDB rejected rows as an implicit alias; it was renamed row_count. Expected counts stayed unchanged.

Learnings:

- Technical: Raw values complement metadata.
- Data: Ten regions were absent from the index.
- Analytical: Decoys test source selection.
- Business: National-only data can still support the mechanism.

Understanding the results:

1. What do these results show? All eight traps matched expected values. Six synthetic profiling answers are recorded in docs/SYNTHETIC_profile_checklist.md. The real-source gate is NOT RUN.
2. What remains unverified? Actual company margins or untested Snowflake behavior.
3. Why does it matter? National-only data can still support the mechanism.

Exit criteria: local synthetic evidence is complete with documented scope gaps in docs/acceptance_status.md. Deployment and real-source criteria remain unverified. Publication is confirmed by GitHub PR links, not simulated pushes.

Evidence files:

- `outputs/phase_1/SYNTHETIC_duplicates.csv`
- `outputs/phase_1/SYNTHETIC_gaps.csv`
- `outputs/phase_1/SYNTHETIC_generator_plateaus.csv`
- `outputs/phase_1/SYNTHETIC_generator_regimes.csv`
- `outputs/phase_1/SYNTHETIC_missing_source_weeks.csv`
- `outputs/phase_1/SYNTHETIC_trap_detection.csv`
- `outputs/phase_1/SYNTHETIC_unindexed_regions.csv`
- `outputs/phase_1/SYNTHETIC_variables.csv`
- `outputs/phase_1/SYNTHETIC_weekdays.csv`
