# Phase 0: Frame the business and guardrails [SYNTHETIC DRY RUN]

Business question: Why is a broker exposed if it buys no fuel?

What was built: see docs/phase_file_map.md and the evidence files below.

How it ran: `python local/run_pipeline.py all`, followed by verify_outputs.py, test_pipeline.py and test_app.py. Full pipeline runs took about 40–43 seconds here, excluding dependency installation.

Sample results:

| week_date | price | carrier_fsc | shipper_fsc | spread |
| --- | --- | --- | --- | --- |
| 2026-01-05 | 2.450000 | 0.200000 | 0.200000 | 0.000000 |
| 2026-01-12 | 2.750000 | 0.250000 | 0.200000 | -0.050000 |
| 2026-01-19 | 3.050000 | 0.300000 | 0.200000 | -0.100000 |
| 2026-01-26 | 2.150000 | 0.150000 | 0.200000 | 0.050000 |
| 2026-02-02 | 1.250000 | 0.000000 | 0.200000 | 0.200000 |
| 2026-02-09 | 1.100000 | 0.000000 | 0.200000 | 0.200000 |

Validation: Named checks map to all BR/FR/NFR IDs in docs/traceability.md. The six-week example is computed in SQL.

| Check | Expected | Observed | Status |
|---|---|---|---|
| Six-week worked example | Six displayed weeks, nonnegative carrier surcharge | Six rows; carrier surcharge floors at zero | PASS |
| Identical initial reset | Zero first-week spread | 0.000000 | PASS |

Table evidence: existing phase CSVs and outputs/review/INDEPENDENT_CHECKS.json; execution evidence is in outputs/review/RERUN_LOG.txt and outputs/phase_6/SYNTHETIC_verification_log.txt.

Surprises and fixes: The owner approved passing unchanged reruns, resolving the BR-17 conflict.

Learnings:

- Technical: Shared formulas isolate timing.
- Data: Region is a dimension, not a lever.
- Analytical: The zero control proves the baseline.
- Business: Exposure is created in contracting.

Understanding the results:

1. What do these results show? Named checks map to all BR/FR/NFR IDs in docs/traceability.md. The six-week example is computed in SQL.
2. What remains unverified? Actual company margins or untested Snowflake behavior.
3. Why does it matter? Exposure is created in contracting.

Exit criteria: local synthetic evidence is complete with documented scope gaps in docs/acceptance_status.md. Deployment and real-source criteria remain unverified. Publication is confirmed by GitHub PR links, not simulated pushes.

Evidence files:

- `outputs/phase_0/SYNTHETIC_six_week_example.csv`
