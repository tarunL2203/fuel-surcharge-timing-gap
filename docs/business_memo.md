# SYNTHETIC decision memo: align reset clocks first

**Decision:** use aligned weekly resets as the benchmark when reviewing shipper contracts. Evaluate a seasonal clause as a negotiated alternative only after replacing illustrative assumptions with actual contract terms.

**Dry-run evidence:** over the common US window 2002-01-07 to 2026-06-29, the weekly control has zero timing spread. Quarterly resets without the clause have a squeeze-week share of 44.2%; the illustrative seasonal clause reduces it to 20.7%. Quarterly resets without the clause nevertheless have a positive mean of $67.55 per 1,000 assumed loads. A positive average does not rule out many adverse weeks.

**Interpretation:** aligned clocks remove the modeled mismatch by construction. A clause improves collections because it adds a price increment in heating weeks. This does not establish shipper acceptance, a fair price, or real winter losses.

**Limits:** all prices and effects were planted. The smooth formula and equal weekly weights are not actual contracts or shipment volumes. Dollar translations use the configured distance. Regions overlap and must not be summed. Centered seasonal averages include future weeks and are descriptive only.

**Next gate:** profile the real listing, obtain contract terms and shipment weights, rerun the controls, and review the downside distribution with a contracting manager before changing rates.

Evidence: outputs/phase_4/SYNTHETIC_same_window_contracts.csv, rows S1/S5/S6. Rating: **Share with caveats** as a method demonstration, not a commercial pricing recommendation.
