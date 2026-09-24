# What must change before an industry deployment

This repository demonstrates a diagnostic mechanism, not a production pricing system.

1. Pass the real-source gate and verify redistribution rights. Keep real extracts out of GitHub.
2. Obtain actual carrier and shipper contracts: index publication cutoffs, time zones, rounding, floors, tiers, caps, effective dates and dispute rules. The smooth illustrative formula is not a substitute for those contracts.
3. Map accepted load dates, lanes and miles to contracts. Weight by actual volume; never add overlapping national and regional observations.
4. Backtest on an evaluation window held out from parameter calibration. Include collection rates, invoice adjustments, accessorials and negotiated all-in rates when available.
5. Verify Snowflake deployment in a dedicated account environment. Test transactions, failure rollback, manual-call concurrency, permission grants, refresh scheduling and two consecutive teardown runs. Local translation tests do not establish these.
6. Review invalid corrections and provider deletions with an owner. The sample keeps last accepted values on invalid corrections and never silently deletes historical prices. Material deletions should block publication until reconciled.
7. Replace the fixed replay as-of date with an explicit live-run date, measured freshness limits and an approved schedule. Observe four successful weekly task runs before calling the real build complete.
8. Add access controls, run alerts, retention rules and incident ownership; enforce branch protections where the GitHub plan permits. Review operational cost limits separately from model accuracy.
9. Validate recommendations with a contracting manager. A seasonal markup transfers revenue and may not be commercially acceptable; it does not establish the cause of seasonal price variation.

Conclusion for scaling: reuse the validation and two-clock structure, replace the assumptions with contract and shipment evidence, and preserve a separate synthetic regression suite.
