# Decisions and execution status

- D-01, approved by the owner in chat on 2026-09-24: a valid unchanged rerun PASSES with zero inserts/updates. This supersedes the zero-delta rejection in BR-17. An empty source is still rejected.
- D-02, owner instruction: private repository. Never push to main. Connection smoke test uses connection-test; project changes use phase-0 through phase-6 and open pull requests. No automatic merge.
- D-03, implementation convention: the 52-week centered average includes 25 preceding and 26 following calendar weeks. It is descriptive and must not be used to predict or calibrate contracts.
- D-04, implementation convention: four-week changes use the exact date 28 days earlier, not the fourth previous observed row. A missing comparison week is UNCLASSIFIED.
- D-05, implementation convention: the one-week index lag uses the exact preceding calendar week; missing lagged prices yield no eligible carrier week. Both clocks use that same price.
- D-06: valid corrections replace an existing price. Invalid corrections quarantine the incoming row and preserve the last accepted value, with a logged warning. Source deletions require manual review; the loader does not silently delete history.
- D-07: no Snowflake account is connected. Local verification cannot certify Snowflake permissions, task scheduling, costs, Marketplace schema, or refresh behavior.

Status: local synthetic build executed; phase review and real deployment gates are separate. No real-world findings.

- D-08: store the last reviewed source fingerprint set per geographic week. Rejected rows in a partially accepted batch are marked reviewed; an entirely blocked batch is not. Replacing that set allows valid corrections and reversions to be detected. Source-state deletions do not automatically remove accepted price history.
- D-09: configuration seeds must run before profiling/landing even though their filename is 03_seeds.sql. The README provides dependency order explicitly.

- D-10, owner request September 24, 2026: present explanations for a general reader instead of mentor/interview prompts. Current vision and business context distinguish sourced business facts from model assumptions; docs/business_flow_validation.md records the evidence gaps. These reader-facing explanations intentionally supersede the original brief’s copied vision wording. This is a documentation clarification, not a change to model rules, inputs or acceptance thresholds. The original brief and audit remain historical records.

- D-11, September 25, 2026: owner requested necessary GitHub publication steps. The repository was already public when checked. Publish a clearly labeled synthetic preview through PR merges, preserving the original audit and open acceptance gaps. This is not final-release or production sign-off. No direct main push.
