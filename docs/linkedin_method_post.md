# Method post draft

I’m building a freight-broker pricing analysis around two clocks: the fuel surcharge paid to carriers and the surcharge collected from shippers.

The first test is simple. When both contracts use the same index, formula and weekly reset, the timing spread must be zero. Slower shipper resets isolate the effect of contract timing.

Before using real data, I tested a clearly labeled synthetic dataset with planted quality issues and known effects. The calculations stay in SQL, rejected rows are separated from rejected batches, and summaries reconcile to weekly detail.

The next stage is real-source profiling and contract validation. Synthetic outputs validate the method; they are not findings about a company’s margins.
