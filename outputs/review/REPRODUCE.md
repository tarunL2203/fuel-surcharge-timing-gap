# SYNTHETIC audit reproduction

Audit date: 2026-09-24. Baseline: `69a7c9b69451ded75aa4bf442b208370eaf83f29`.

Use two isolated checkouts, one left unchanged and one for the README rerun. Do not execute reruns over the evidence checkout: the supplied runner regenerates sample data, SQL and reports.

```bash
# In the rerun checkout, follow README:
python -m venv .venv
source .venv/bin/activate
python -m pip install -r local/requirements.txt
python local/run_pipeline.py all
python local/verify_outputs.py
python local/test_pipeline.py
python local/test_app.py
python local/write_reports.py
# Set these paths to the two checkouts:
python /path/to/original/outputs/review/audit_checks.py /path/to/original /path/to/rerun
# In the unchanged evidence checkout:
python outputs/review/history_checks.py
```

The reviewer could not authenticate a command-line clone. Instead, all 108 original files were checked using Git blob hashes against the GitHub recursive tree, then copied into a fresh directory without a database or environment. A new venv installed every pinned dependency successfully. The entire baseline and all historical-only blobs were subsequently hash-checked again by history_checks.py. No test, parameter, SQL or original result was edited.

The README's noninteractive commands all exited zero. Pipeline runtime was 8.92 seconds; targeted tests took 2.296 seconds. Total elapsed installation and walkthrough time was not instrumented, so it is CANNOT VERIFY. AppTest exercised all four pages and alternate selection; a separate interactive Streamlit browser session was not timed. This is a verified-snapshot rerun, not a literal fresh git clone.

`INDEPENDENT_CHECKS.json` is recomputed from CSVs and the rerun database using separate checks. Floating-point comparison tolerance of 1e-12 applies only to comparing exported CSVs, not to project invariants or acceptance thresholds. Exact hashes matched all sample files, all charts and all generated SQL. Two output hashes differed: load-log run timestamps, and an added evidence-file link in the generated phase-6 report. Both differences are findings in Part 1.

`HISTORY_TREES.json` records all eight commits reachable from phase-6. `HISTORICAL_TEXT.json` preserves the two older README blobs and connection-test content for scanning. GitHub evidence records the PRs, private setting and branches. This covers accessible reachable history, not deleted/unreachable GitHub objects or account secrets. Pattern-based scanning cannot prove the absence of arbitrary credentials.
