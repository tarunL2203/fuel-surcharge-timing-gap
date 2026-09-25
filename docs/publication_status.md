# Public preview status

Prepared September 25, 2026. Scope: a reproducible SYNTHETIC demonstration for readers and technical reviewers. This is not the final v0.1 release or a live small-business tool.

## What visitors can use

Start with the README, vision, business-flow validation, sample results and local quickstart. The app can run locally; GitHub does not host a running Streamlit app. No live dashboard URL is available. The model is intended for exploration of configured scenarios.

## Follow-up to the original audit

| Finding | Current disposition |
|---|---|
| F-01 validation tables | Added expected/observed/status tables to seven phase reports and their formatter, using existing evidence |
| F-02 Snowflake INV-03 | OPEN: local idempotency passes, but the Snowflake validation file omits its equivalent. Requires a separately scoped SQL/test change before deployment |
| F-03 report evidence link | Added the phase-6 verification-log link |
| F-04 timestamp difference | Expected run metadata; analytical data is unaffected |
| F-05 GitHub closure | Publishing through sequential PR merges; final tag deferred. Connection test is to be closed without merging; its branch may remain as historical evidence |
| F-06 numeric SQL order | Follow README dependency order, not filename sorting |
| F-07 ignore patterns | Added desktop and notebook checkpoint patterns |
| F-08 owner learnings | OPEN: docs/LEARNINGS.md is preserved historical agent-generated text, not verified owner testimony. README discloses this; owner rewrite required before presenting it as personal experience |
| F-09 reader orientation | Motivation, business scope, author, license and source-validation links are present |
| F-10 chart units | Added regional and January-amplitude units and clarified January date coverage |
| F-11 partial periods | Weekly spread chart explicitly identifies inclusion of partial current periods |

The original audit remains intact as evidence of its earlier snapshot. Passing local checks does not resolve business-validation or Snowflake gaps. Later business-source review also qualified claims in the original vision; see business_flow_validation.md.

Track these items in [GitHub issue #11](https://github.com/tarunL2203/fuel-surcharge-timing-gap/issues/11).

## Still required for a completed release or real use

- Resolve Snowflake idempotency validation and execute the deployment, permissions, refresh, scheduling and teardown checks.
- Replace historical agent-written learnings with the owner's own words.
- Validate actual paired contracts and shipment invoices with an operator; no financial benefit is proven.
- Confirm source access, terms, live freshness, operating costs and responsibility for exceptions.

Public sharing is for feedback on a work-in-progress sample. No production certification, savings claim or final release tag is implied.
