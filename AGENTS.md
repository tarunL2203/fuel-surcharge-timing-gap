# Project working rules

Read docs/BUILD_BRIEF.md, docs/DECISIONS.md and the latest phase report first.
Never commit or push to main. Use phase-N branches and open pull requests. Never merge without an explicit request.
Use connection-test only for the connection smoke test.
Keep this repository private unless the owner asks otherwise.
Fixed seed 42; AS_OF_DATE 2026-09-23. Label all sample-derived results SYNTHETIC.
Metrics must be calculated in SQL. Keep shared model SELECTs under sql/selects and translate only dialect syntax.
No credentials, account identifiers, real listing extracts, or local database binaries in git.
Record failing tests honestly. Stop if an unexplained invariant or conflicting business rule remains.
Snowflake code stays UNVERIFIED until executed against the intended account.
