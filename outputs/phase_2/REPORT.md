# Phase 2: Land a validated copy [SYNTHETIC DRY RUN]

Business question: Is this batch safe for analysis?

What was built: see docs/phase_file_map.md and the evidence files below.

How it ran: `python local/run_pipeline.py all`, followed by verify_outputs.py, test_pipeline.py and test_app.py. Full pipeline runs took about 40–43 seconds here, excluding dependency installation.

Sample results:

| load_id | status | inserted | updated | quarantined | normalized | raw_rows | days_old | freshness | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PASSED_WITH_QUARANTINE | 14163 | 0 | 2 | 44 | 14163 | 16 | STALE | INVALID_CORRECTIONS_KEEP_LAST_ACCEPTED |
| 2 | PASSED | 11 | 0 | 0 | 0 | 14174 | 9 | FRESH | nan |
| 3 | PASSED | 0 | 0 | 0 | 0 | 14174 | 9 | FRESH | NO_CHANGE |
| 4 | BLOCKED | 0 | 0 | 11 | 0 | 14174 | 9 | FRESH | BAD_ROW_THRESHOLD |

Validation: Initial 14,163 accepted rows; incremental 14,174; repeat unchanged; corrupt week blocked. 44 normalized dates, 2 initial quarantines and 5 missing clean pairs.

Surprises and fixes: A last-reviewed source-state audit avoids repeatedly treating quarantined history as new. Valid correction/reversion tests passed.

Learnings:

- Technical: Transactions protect accepted state.
- Data: Corruption leaves accepted history unchanged.
- Analytical: Repeatability includes no-op reruns.
- Business: Block a bad batch before pricing analysis.

Explain-back:

1. What does this phase establish? Initial 14,163 accepted rows; incremental 14,174; repeat unchanged; corrupt week blocked. 44 normalized dates, 2 initial quarantines and 5 missing clean pairs.
2. What does it not establish? Actual company margins or untested Snowflake behavior.
3. Why does it matter? Block a bad batch before pricing analysis.

Exit criteria: local synthetic evidence is complete with documented scope gaps in docs/acceptance_status.md. Deployment and real-source criteria remain unverified. Publication is confirmed by GitHub PR links, not simulated pushes.

Evidence files:

- `outputs/phase_2/SYNTHETIC_initial_missing_clean_weeks.csv`
- `outputs/phase_2/SYNTHETIC_load_log.csv`
- `outputs/phase_2/SYNTHETIC_normalizations.csv`
- `outputs/phase_2/SYNTHETIC_quarantine.csv`
