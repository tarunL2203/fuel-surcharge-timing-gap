# SYNTHETIC audit, Part 3: presentation

Verdict: **PASS WITH FIXES**. This is a static content and chart review, not a measured study with recruiters or business users. Actual timed human walkthroughs are CANNOT VERIFY. The target-time assessments below describe findability, not observed reading times.

## Audience paths

| Audience target | Assessment | Evidence |
|---|---|---|
| Recruiter, 60 seconds | NEEDS WORK | README explains the clocks immediately, but skills and hero image are below setup and architecture. License and author are not explicit. |
| Business reader, 30 seconds | NEEDS WORK | Memo leads with the decision and includes $67.55 per 1,000 assumed loads, but the dollar context and limits are not in its first two sentences. |
| Technical reviewer, 3 minutes | PASS for findability | README run order links to dialect notes; validation and teardown files are clearly named. Snowflake idempotency validation gap remains F-02. |
| Mentor, 5 minutes | PASS for findability | README, acceptance_status and real_source_gate expose traps, zero control, limitations and the next deployment gate. Owner learnings remain F-08. |

## Documentation

Vision matches the supplied framing. Business rules, requirements and traceability retain BR/FR IDs. A-01 to A-11 are present with a global ILLUSTRATIVE status. Memo is short, decision-led, labeled SYNTHETIC and rated Share with caveats. Its one-page visual pagination was not rendered or measured. Method post discusses the method without outcome numbers. Mermaid has balanced node/edge syntax and matches the conceptual flow, though it does not name every physical SQL object. A GitHub renderer preview was not available.

**F-08, MAJOR, OWNER DECISION:** docs/LEARNINGS.md is titled `Actual learnings` and contains agent-authored first-person claims for every phase. Lines 9/11, 19/21, 29/31, 39/41, 49/51, 59/61 and 69/71 respectively say `What I changed` and `Concept I can now explain`. The owner must replace these with their own experiences and explanations before presenting them as personal learning. This review cannot write those experiences or edit that file. Repeated Expected / What happened / What I changed / Concept scaffolding is useful, but generic explain-back questions in phase reports provide weak evidence of personal understanding.

**F-09, MINOR, SAFE:** README has the required mechanism, synthetic disclosure, architecture, results, local instructions, Snowflake order, map, traps and limits. Add explicit author/license information and a short skills paragraph; move the existing spread chart above installation steps. Label the trap table T1-T8 and add E4 to the verification preview. Current `Start with the vision...` could become `Start with the decision memo for the contract question, then use the local quickstart to reproduce the synthetic checks.` Keep the exact disclosure unchanged.

The memo's current first decision sentence is `use aligned weekly resets as the benchmark when reviewing shipper contracts.` Suggested opening: `Use aligned weekly resets as the benchmark for contract review. In this synthetic example, quarterly resets average $67.55 per 1,000 assumed loads while 44.2% of weeks are adverse; these are illustrative contract mechanics, not a pricing recommendation.` This retains existing figures and brings the units and caveat forward.

Acronym polish remains useful: README mentions EIA without expansion, and supporting prose uses PADD/FSC in technical contexts without consistently defining them per document. Expand Energy Information Administration, Petroleum Administration for Defense Districts, fuel surcharge and third-party logistics where first used. Spread sign, scenario IDs and carrier/shipper clock terminology are otherwise consistent. No material synthetic result was presented as a real business finding.

## Chart inspection

All five chart files carry SYNTHETIC titles. Regional and January-recovery PNGs were visually inspected during this audit; spread, heatmap and clause construction was also checked in local/analyze.py:40-49. Charts are legible at their native widths. Bars start at zero; the regional comparison includes a zero line. Heatmap uses a fixed diverging range, and paired bars use common axes. Blue/orange is distinguishable in the paired plots; the three-line full-history chart relies more heavily on color and would benefit from line styles and a shorter illustrative window.

**F-10, MAJOR, SAFE:** Regional exposure and January recovery charts omit y-axis labels/units (local/analyze.py:48-49; SYNTHETIC_regions.png and SYNTHETIC_recovery.png). The numbers can be mistaken for dollars per load, dollars per mile, fractions or percent. Label the regional axis `Mean spread ($/mile)` and recovery `January amplitude (fraction)` or explicitly format as percent. Use the same input hashes and do not change any result. The recovery title should identify the actual valid-window endpoint rather than the broad 2002-2026 source span. These are chart-presentation fixes only.

**F-11, MINOR, SAFE:** The spread chart includes the incomplete current period through September 14 but does not label that fact (local/analyze.py:41-44). It is weekly detail, so retaining it is reasonable; add a partial-period note. Period summary and regional comparison outputs already filter completed periods. Worst-stretch output retains a complete_period field and enforces consecutive four-week dates, so consumers should retain that field when displaying excerpts.

## GitHub page copy, for owner application only

About: A synthetic SQL and Snowflake project showing how carrier and shipper fuel-surcharge reset timing changes a broker's modeled exposure.

Topics: snowflake, sql, duckdb, streamlit, data-quality, logistics, synthetic-data.

Draft release notes for v0.1-synthetic-dry-run:

> Includes deterministic synthetic inputs, documented data-quality traps, validated local landing and two-clock models, SQL result tables, a Streamlit demo and phase reports. Local invariants and planted-effect checks pass. All prices, contract assumptions and effects are synthetic or illustrative. Snowflake deployment, real-source access, live operations and contract suitability are unverified. Known review findings must be closed before release; the next step is owner review followed by controlled real-source profiling and Snowflake validation.

Do not publish these notes as a completed release or claim Snowflake certification while findings remain open.
