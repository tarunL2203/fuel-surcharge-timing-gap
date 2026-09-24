# Dialect and execution notes

Canonical model SELECTs are in sql/selects, using DuckDB syntax. local/render_snowflake.py translates them with sqlglot 27.20.0 to Snowflake and writes sql/04_dynamic_tables.sql. No separate hand-maintained model is used.

- DuckDB CTAS becomes Snowflake CREATE OR REPLACE DYNAMIC TABLE; intermediates DOWNSTREAM, final summary one day; full refresh is explicit for predictable compatibility.
- QUANTILE_CONT becomes PERCENTILE_CONT WITHIN GROUP; DATE/interval expressions and date differences are translated.
- Local CSV reading, temporary staging and Python transaction orchestration replace the shared source adapter and Snowflake Scripting procedure. These are infrastructure differences, not model changes. Landing parity remains unverified until the SQL procedure is executed in Snowflake.
- Model round-trip tests translate the generated Snowflake SELECTs back to DuckDB and compare results.
- Numeric calculations run in SQL. Python generates fictional source inputs, controls runs, checks assertions, renders plots, and formats output.
- Local actual timestamps are audit metadata; fixed AS_OF_DATE drives freshness and periods. CSV analytical results are deterministic; audit timestamp files can differ.

- Missing-week calendar: DuckDB uses generate_series through AS_OF_DATE; Snowflake's separate 04b_quality_views.sql uses GENERATOR capped at 10,000 weeks, sufficient for this data horizon. Whole-period exclusions use equivalent aggregation. Source deletions remain a manual-review event.
- Source-state fingerprints are engine-local audit keys. Hash string formatting is not claimed to be portable between databases; model numeric results are compared, not audit hash bytes.
- Single-thread DuckDB execution fixes aggregate evaluation order for repeatability. Load timestamps remain nondeterministic audit metadata.
