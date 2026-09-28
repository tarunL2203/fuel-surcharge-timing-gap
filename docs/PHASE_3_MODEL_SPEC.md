# Phase 3 model specification: policy calculations and comparisons

Status: DESIGN READY; revised SQL, local twin and Snowflake execution pending. Approved direction: owner request September 27, 2026. Replaces the old two-clock rules for the forthcoming real-source track only. See [current brief](BUILD_BRIEF.md).

## Scope and grain

Calculate a per-mile surcharge for each policy version, geography and scheduled evaluation date, using already accepted RAW diesel observations. V1 evaluates Monday dates as a modeling convention, not actual shipment events. Compare alternative policies with a weekly baseline on the same eligible dates. No actual invoices, shipment volumes or named-carrier replication.

## Configuration to add (do not overwrite legacy configuration)

| Proposed object | Required fields and constraints |
|---|---|
| CONFIG.POLICY_VERSIONS | policy_id, version_id, effective_from inclusive, effective_to exclusive/nullable, evidence_status, source_url/note, source_review_date, policy_scope, formula_type, base_price, mpg, reset_frequency, index_lag_weeks, availability_lag_days, rounding_scale |
| CONFIG.POLICY_GEOGRAPHIES | policy/version and explicit geo_id mappings; no assumed national code |
| CONFIG.POLICY_COMPARISONS | comparison_id, baseline_policy_id, alternative_policy_id, scenario_label |
| CONFIG.POLICY_RUN_CONFIG | run_id, as_of_date, evaluation_start/end, data_cutoff, policy_set_version, price_provenance, analysis_label, optional assumed_miles/load_count |

Assert unique policy/version keys and nonoverlapping effective ranges per policy. Reject negative lags, mpg <= 0, unsupported frequency/formula, invalid date ranges, missing source notes, and inconsistent units. Documented policies require sufficient source and applicability evidence; a nonempty URL alone is not sufficient. Snowflake metadata constraints alone are not the validation gate.

V1 formula_type = PER_MILE_LINEAR_FLOOR_ZERO, output USD/mile. Use fixed-decimal arithmetic, preserve unrounded values, and round displayed values to six decimal places. Round assumed dollar totals to cents only after aggregation. Policy parameters are versioned, not read from the legacy global CONFIG.PARAMETERS formula.

## Initial policy set (all ILLUSTRATIVE)

| ID | Reset | Additional index lag | Base/MPG | Role |
|---|---|---|---|---|
| P01 | WEEKLY | 0 weeks | $1.25/gallon; 6 miles/gallon | Baseline |
| P02 | WEEKLY | 1 week | Same as P01 | Isolate additional lag |
| P03 | MONTHLY | 0 weeks | Same as P01 | Isolate adjustment frequency |

Availability lag is seven calendar days for all three initial policies. This is an explicit conservative modeling convention because the loaded adapter does not contain historical release timestamps. It is not an EIA publication rule and cannot prove historical point-in-time availability or account for later revisions. P02 has an additional seven-day lag beyond this convention. No policy claims to reproduce FedEx Freight's percentage table.

Policy effective ranges define simulation applicability, not actual commercial contract history. For initial full-history simulations, set the start from the reviewed evaluation window and label it accordingly. Geography coverage is discovered from RAW, not copied from the synthetic set of 11 geographies.

## Deterministic date selection

1. Build the expected Monday evaluation spine per geography between its observed minimum and the earlier of its observed maximum, configured evaluation_end and as_of_date. Retain internal gaps as expected dates. Do not manufacture data beyond the loaded tail or mark pre-coverage dates as missing.
2. Select the unique policy version whose effective range contains the evaluation date. Zero or multiple matches produce an exclusion with a reason, not an arbitrary selection.
3. WEEKLY reset anchor = evaluation date. MONTHLY anchor = first calendar day of that month. On a new version's effective date, reset immediately: anchor is the later of the ordinary anchor and effective_from. Record the anchor separately from the evaluation date.
4. Calculate cutoff = reset_anchor - availability_lag_days - 7 * index_lag_weeks. Expected index week = Monday on or immediately before cutoff (set WEEK_START=1 explicitly).
5. Join on that exact geography/index week. Never use “latest available price” to hide an internal gap; never take a later week because the reset observation is missing. Distinguish MISSING_INDEX_WEEK from INSUFFICIENT_LOOKBACK before regional coverage begins.
6. Compute max(0, (index_price - base_price) / mpg). Hold the monthly reset calculation until the next reset or version change. Do not use centered seasonal statistics in price selection or policy calibration.

Example dates only: for a Monday evaluation on June 8, 2026, P01 selects June 1; P02 selects May 25. P03 uses its June 1 anchor and selects May 25 throughout June, absent a version change. Confirm these mappings with executable tests rather than treating this illustration as execution evidence.

## Detail, exclusions and comparisons

Proposed MODEL.POLICY_CALCULATION_DETAIL contains run_id, policy/version, geo_id, evaluation_date, reset_anchor, index_cutoff_date, expected_index_week, selected_index_week, index_price, source load_id, effective range, all formula parameters, evidence_status, price_provenance, unrounded/display surcharge and eligibility_reason.

Exactly one record per expected evaluation/policy pair must be accounted for. Missing inputs retain a record with a null calculated amount and a named exclusion. Keep the reason rows in MODEL.POLICY_EXCLUSIONS; do not drop them before reconciliation. Reject conflicting source keys before joining.

MODEL.POLICY_COMPARISON_DETAIL joins baseline and alternative on run, geography and evaluation date. Difference = alternative surcharge - baseline surcharge. Positive means the alternative calculates a higher charge; negative means lower. Neither sign is inherently favorable without identifying the payer and the rest of the commercial terms. Compare only eligible pairs, and report the excluded denominator.

MODEL.POLICY_COMPARISON_SUMMARY reports comparable/excluded week counts, mean difference, lower-charge-week share and distribution statistics with units. Optional assumed dollars = sum of per-mile differences * stated assumed miles * stated assumed loads per evaluation week. Label assumptions and exposure horizon; do not multiply an equally weighted average by an unstated shipment count. Do not sum overlapping geographies as separate business volumes.

## Period completeness and coverage

For month-level comparisons, require every expected evaluation Monday in the month to be covered and eligible for both policies, the month to have ended by as_of_date, and the final expected Monday to fall within the geography's accepted coverage. Missing lookback, missing evaluation weeks and mid-month source starts/tails make the period incomplete. With a June 22 tail, June 2026 is incomplete because June 29 is absent even if as_of_date is in September. Show partial periods only as explicitly labeled detail, excluding them from complete-month rankings.

Regional comparisons use the intersection of eligible evaluation dates for selected geographies and disclose that common window. Freshness is independent of historical eligibility. Preserve the latest observed date and data age in every results package.

## Required tests before Snowflake modeling acceptance

| Test | Expected behavior |
|---|---|
| P3-01 identical-policy control | Zero difference on every eligible row (add a test-only copy of P01) |
| P3-02 known-answer formula | SQL fixture prices below, at and above base produce independently specified expected values |
| P3-03 date boundaries | Exact week selection for weekly/additional lag/monthly, year boundary, leap February and mid-period version change |
| P3-04 unavailable index | Missing exact index week yields exclusion; no substitution or future price |
| P3-05 invalid/overlapping policies | Validation fails before calculations; adjacent half-open versions select one policy |
| P3-06 coverage | Regional starts, internal gaps and June 22 tail produce explicit exclusions/incomplete June |
| P3-07 reconciliation | Expected pairs = eligible + excluded; comparison totals match detail on the same dates |
| P3-08 repeatability | Same price snapshot and policy/run version produce identical calculations |
| P3-09 type/rounding | Unit mismatch blocked; decimal boundary values and aggregation rounding checked |
| P3-10 provenance | Every result resolves to source load, price date and policy version; labels persist into exports |

Local fixtures and Snowflake execution are separate evidence gates. Do not reuse the old 97,650-row expectation: new policy count, lookback, expected-date exclusions and comparison eligibility determine counts. Compute expectations independently in SQL and report them with actuals.

## Implementation sequence and compatibility

1. Run the read-only Phase 3 preflight and preserve its summary exports.
2. Implement additive policy seeds and shared SELECTs under sql/selects/policy/. Add a separate renderer/deployment entry point; do not overwrite the legacy generated file.
3. Execute deterministic synthetic fixtures locally, including the ten tests above. Record dialect differences and any failures.
4. Create the new model objects manually in Snowflake, validate detail and exclusions, and record query IDs plus summary evidence. Start with manually materialized outputs; automatic refresh design follows validation.
5. Add the app integration only after model acceptance. The current app cannot read these proposed objects without changes.

Steps 2-5 are pending implementation, not instructions to run nonexistent files. Revised DDL must include role grants, additive object lifecycle and teardown coverage. Policy run metadata alone is not an immutable price snapshot: before reproducibility claims, retain the actual input snapshot within Snowflake (never commit the listing extract), or explicitly record that historical corrections can change results. RAW currently retains accepted latest values, not complete provider vintages.
