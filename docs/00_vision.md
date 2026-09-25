# Vision (mentor version)

**The pitch**

Freight brokers sit between shippers and carriers. They pay carriers a fuel surcharge that resets every week with the government's diesel price index, but they bill shippers under contract terms that reset monthly, quarterly, or not at all. When diesel moves, the two clocks drift apart and the difference lands on the broker's margin, even though the broker never buys a gallon of fuel. This project measures that gap on real EIA diesel data inside Snowflake: how large it gets under different contract terms, when it is worst (rising prices, the winter heating season), and whether a contract clause closes it. The deliverable is a Streamlit app where a pricing team can change contract terms and see the margin impact, plus a one-page memo that leads with the decision.

**Why it is credible**

- **Real, free data**: EIA weekly retail diesel prices from the Snowflake Marketplace, with data limits stated upfront.
- **A built-in correctness proof**: when both clocks reset weekly, the model must show zero spread in every week. Any spread in the other scenarios comes from the mechanism, not a bug.
- **Method tested before the real run**: a synthetic dry run plants eight known data errors (the checks must catch all of them) and known effects (the analysis must recover them).
- **Every assumption is labeled, registered, and stress-tested.**

**What it does not claim**

- No real company's margins or surcharge collections (that data is private).
- No forecasting.
- Synthetic results show the method works. Only the real run produces findings.

**Why Snowflake, when the data is small**

The real diesel slice is expected to be under about 20,000 rows, so the case is not volume. The case is that the data arrives live through the Marketplace with no pipeline to maintain, every weekly load is validated before it touches the model, the rebuild is declarative, and the app sits next to the data, so a pricing analyst can test contract terms without exporting anything.

**Questions a mentor will ask**

- *Is the surcharge schedule real?* The formula structure is public and cited. The parameter values are labeled assumptions with sensitivity ranges.
- *What if the listing has no regional data?* The core mechanism runs on the national index. Regional analysis is a scope option decided in Phase 1.
- *How do you know the model is right?* The zero-spread control, known-answer tests on synthetic data, and reconciliation checks on every run.
- *What would an owner-operator version change?* Same data, different exposure: an owner-operator buys the fuel, so the question becomes whether the surcharge received covers the fuel burned. That is the planned second lens.
