# Phase 5: Serve and translate [SYNTHETIC DRY RUN]

Business question: What should a pricing team examine in contracts?

What was built: see docs/phase_file_map.md and the evidence files below.

How it ran: `python local/run_pipeline.py all`, followed by verify_outputs.py, test_pipeline.py and test_app.py. Full pipeline runs took about 40–43 seconds here, excluding dependency installation.

Sample results:

| document | claim | source | row_key | column |
| --- | --- | --- | --- | --- |
| business_memo | weekly zero | outputs/phase_4/SYNTHETIC_same_window_contracts.csv | S1 | mean_spread |
| business_memo | quarterly squeeze | outputs/phase_4/SYNTHETIC_same_window_contracts.csv | S5 | squeeze_share |
| business_memo | clause squeeze | outputs/phase_4/SYNTHETIC_same_window_contracts.csv | S6 | squeeze_share |
| business_memo | mean dollar impact | outputs/phase_4/SYNTHETIC_same_window_contracts.csv | S5 | mean_dollars_per_1000_loads |
| simulated_narration | all figures | outputs/phase_4/SYNTHETIC_same_window_contracts.csv | S1 S5 S6 | mean_spread squeeze_share |
| linkedin_method_post | no numeric findings | not applicable | not applicable | not applicable |

Validation: All four app pages and a PADD4 quarterly/clause selection passed AppTest. Prose numbers trace to SQL result rows. Snowflake app NOT RUN.

Surprises and fixes: App tests revealed a Streamlit width deprecation; the argument was updated.

Learnings:

- Technical: Model views serve the app.
- Data: Freshness follows accepted observations.
- Analytical: Narration uses existing numbers.
- Business: A markup requires commercial acceptance.

Understanding the results:

1. What do these results show? All four app pages and a PADD4 quarterly/clause selection passed AppTest. Prose numbers trace to SQL result rows. Snowflake app NOT RUN.
2. What remains unverified? Actual company margins or untested Snowflake behavior.
3. Why does it matter? A markup requires commercial acceptance.

Exit criteria: local synthetic evidence is complete with documented scope gaps in docs/acceptance_status.md. Deployment and real-source criteria remain unverified. Publication is confirmed by GitHub PR links, not simulated pushes.

Evidence files:

- `outputs/phase_5/SYNTHETIC_app_walkthrough.md`
- `outputs/phase_5/SYNTHETIC_assumptions_view.png`
- `outputs/phase_5/SYNTHETIC_claim_lineage.csv`
- `outputs/phase_5/SYNTHETIC_data_quality_view.png`
- `outputs/phase_5/SYNTHETIC_memo_evidence.csv`
- `outputs/phase_5/SYNTHETIC_overview_view.png`
- `outputs/phase_5/SYNTHETIC_scenario_explorer_view.png`
- `outputs/phase_5/SYNTHETIC_simulated_narration.md`
