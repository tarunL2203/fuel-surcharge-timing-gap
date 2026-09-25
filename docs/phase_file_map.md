# Phase file ownership

| Branch | Files |
|---|---|
| connection-test | docs/connection_test.md only |
| phase-0 | AGENTS.md, .gitignore, initial README, framing/rules/requirements/assumptions/sources/architecture/decisions/traceability, sql/00_setup.sql, outputs/phase_0 |
| phase-1 | local/generate_sample_data.py, data/sample, sql/01_profiling.sql, real-source gate, outputs/phase_1 |
| phase-2 | local/run_pipeline.py, sql/02_landing.sql, outputs/phase_2 |
| phase-3 | sql/03_seeds.sql, sql/selects, sql/04_dynamic_tables.sql, local/render_snowflake.py, local/dialect_notes.md, outputs/phase_3 |
| phase-4 | local/analyze.py, local/test_pipeline.py, local/verify_outputs.py, sql/05_validation.sql, outputs/phase_4 |
| phase-5 | app/streamlit_app.py, local/test_app.py, local/write_reports.py, memo/method post, outputs/phase_5 |
| phase-6 | Final README, LICENSE, pinned dependencies, build/check scripts, acceptance and industry-readiness docs, learnings, teardown, outputs/phase_6 |

These PRs are a stacked review sequence. Later phases depend on earlier phases. The final runnable snapshot is phase-6; intermediate branches are review checkpoints, not promised standalone releases. Phase reports were finalized from the executed full dry run. No merge or release tag is automatic.
