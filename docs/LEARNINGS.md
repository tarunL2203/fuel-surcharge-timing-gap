# Actual learnings

## Phase 0: Frame the business and guardrails

Expected: Why is a broker exposed if it buys no fuel?

What happened: Named checks map to all BR/FR/NFR IDs in docs/traceability.md. The six-week example is computed in SQL.

What I changed: The owner approved passing unchanged reruns, resolving the BR-17 conflict.

Concept I can now explain: The zero control proves the baseline.

## Phase 1: Profile the listing

Expected: Can the source support two clocks?

What happened: All eight traps matched expected values. Six synthetic profiling answers are recorded in docs/SYNTHETIC_profile_checklist.md. The real-source gate is NOT RUN.

What I changed: DuckDB rejected rows as an implicit alias; it was renamed row_count. Expected counts stayed unchanged.

Concept I can now explain: Decoys test source selection.

## Phase 2: Land a validated copy

Expected: Is this batch safe for analysis?

What happened: Initial 14,163 accepted rows; incremental 14,174; repeat unchanged; corrupt week blocked. 44 normalized dates, 2 initial quarantines and 5 missing clean pairs.

What I changed: A last-reviewed source-state audit avoids repeatedly treating quarantined history as new. Valid correction/reversion tests passed.

Concept I can now explain: Repeatability includes no-op reruns.

## Phase 3: Build the two clocks

Expected: What is paid and collected each week?

What happened: 85,044 scenario rows. The planted PADD4 March 2011 monthly reset moves to March 28; other reset periods have no substitutions.

What I changed: Date joins enforce exact calendar lags and four-week comparisons; missing observations are not filled.

Concept I can now explain: Shared lags preserve the control.

## Phase 4: Measure the spread

Expected: How does timing change the downside distribution?

What happened: INV-01 through INV-05 pass. E1 and E3 pass all regions. E2 passes both regimes. Exact errors and confusion matrix are saved as CSVs.

What I changed: DuckDB rejected weeks and error as implicit aliases; explicit aliases fixed them. Final repeatability checks exposed sensitivity state leaking into baseline outputs. Each sensitivity scenario now runs in a transaction that is rolled back, with assertions that both parameters and weekly rows are unchanged. No source values or expected answers were changed.

Concept I can now explain: Positive means can hide adverse weeks.

## Phase 5: Serve and translate

Expected: What should a pricing team examine in contracts?

What happened: All four app pages and a PADD4 quarterly/clause selection passed AppTest. Prose numbers trace to SQL result rows. Snowflake app NOT RUN.

What I changed: App tests revealed a Streamlit width deprecation; the argument was updated.

Concept I can now explain: Narration uses existing numbers.

## Phase 6: Package and publish

Expected: Can another person reproduce and review the build?

What happened: Local checks and two local teardown calls pass. Snowflake execution/teardown and live weekly operation are NOT RUN. Deployment remains gated.

What I changed: A report-generation command initially used the wrong working directory and wrote no files; rerunning from the project parent fixed it. GitHub sign-in was required to create the repository.

Concept I can now explain: Local success is not deployment proof.
