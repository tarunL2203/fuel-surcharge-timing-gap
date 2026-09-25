"""Format SQL-produced results; no metric calculations here."""
import json,platform
import pandas as pd
from run_pipeline import ROOT

def read(p):return pd.read_csv(ROOT/p)
def write(p,s):(ROOT/p).write_text(s)
def table(df):
 def fmt(v):return f'{v:.6f}' if isinstance(v,float) else str(v)
 return '| '+' | '.join(df.columns)+' |\n| '+' | '.join(['---']*len(df.columns))+' |\n'+'\n'.join('| '+' | '.join(fmt(v) for v in row)+' |' for row in df.itertuples(index=False,name=None))+'\n'
def main():
 summary=read('outputs/phase_4/SYNTHETIC_same_window_contracts.csv');s5=summary[summary.scenario_id=='S5'].iloc[0];s6=summary[summary.scenario_id=='S6'].iloc[0]
 write('docs/business_memo.md',f'''# SYNTHETIC decision memo: align reset clocks first

**Decision:** use aligned weekly resets as the benchmark when reviewing shipper contracts. Evaluate a seasonal clause as a negotiated alternative only after replacing illustrative assumptions with actual contract terms.

**Dry-run evidence:** over the common US window {s5.first_date} to {s5.last_date}, the weekly control has zero timing spread. Quarterly resets without the clause have a squeeze-week share of {s5.squeeze_share:.1%}; the illustrative seasonal clause reduces it to {s6.squeeze_share:.1%}. Quarterly resets without the clause nevertheless have a positive mean of ${s5.mean_dollars_per_1000_loads:,.2f} per 1,000 assumed loads. A positive average does not rule out many adverse weeks.

**Interpretation:** aligned clocks remove the modeled mismatch by construction. A clause improves collections because it adds a price increment in heating weeks. This does not establish shipper acceptance, a fair price, or real winter losses.

**Limits:** all prices and effects were planted. The smooth formula and equal weekly weights are not actual contracts or shipment volumes. Dollar translations use the configured distance. Regions overlap and must not be summed. Centered seasonal averages include future weeks and are descriptive only.

**Next gate:** profile the real listing, obtain contract terms and shipment weights, rerun the controls, and review the downside distribution with a contracting manager before changing rates.

Evidence: outputs/phase_4/SYNTHETIC_same_window_contracts.csv, rows S1/S5/S6. Rating: **Share with caveats** as a method demonstration, not a commercial pricing recommendation.
''')
 write('docs/linkedin_method_post.md','''# Method post draft

I’m building a freight-broker pricing analysis around two clocks: the fuel surcharge paid to carriers and the surcharge collected from shippers.

The first test is simple. When both contracts use the same index, formula and weekly reset, the timing spread must be zero. Slower shipper resets isolate the effect of contract timing.

Before using real data, I tested a clearly labeled synthetic dataset with planted quality issues and known effects. The calculations stay in SQL, rejected rows are separated from rejected batches, and summaries reconcile to weekly detail.

The next stage is real-source profiling and contract validation. Synthetic outputs validate the method; they are not findings about a company’s margins.
''')
 write('outputs/phase_5/SYNTHETIC_simulated_narration.md',f'# SYNTHETIC • SIMULATED NARRATION\n\nOn the common US window, quarterly squeeze-week share is {s5.squeeze_share:.1%} without the clause and {s6.squeeze_share:.1%} with it. The weekly control is zero by construction. These generated-data results are not company financial estimates.\n\nSource: outputs/phase_4/SYNTHETIC_same_window_contracts.csv, S1/S5/S6. No AI_COMPLETE call was made.\n')
 write('outputs/phase_5/SYNTHETIC_claim_lineage.csv','document,claim,source,row_key,column\nbusiness_memo,weekly zero,outputs/phase_4/SYNTHETIC_same_window_contracts.csv,S1,mean_spread\nbusiness_memo,quarterly squeeze,outputs/phase_4/SYNTHETIC_same_window_contracts.csv,S5,squeeze_share\nbusiness_memo,clause squeeze,outputs/phase_4/SYNTHETIC_same_window_contracts.csv,S6,squeeze_share\nbusiness_memo,mean dollar impact,outputs/phase_4/SYNTHETIC_same_window_contracts.csv,S5,mean_dollars_per_1000_loads\nsimulated_narration,all figures,outputs/phase_4/SYNTHETIC_same_window_contracts.csv,S1 S5 S6,mean_spread squeeze_share\nlinkedin_method_post,no numeric findings,not applicable,not applicable,not applicable\n')
 titles=['Frame the business and guardrails','Profile the listing','Land a validated copy','Build the two clocks','Measure the spread','Serve and translate','Package and publish']
 questions=['Why is a broker exposed if it buys no fuel?','Can the source support two clocks?','Is this batch safe for analysis?','What is paid and collected each week?','How does timing change the downside distribution?','What should a pricing team examine in contracts?','Can another person reproduce and review the build?']
 results=[table(read('outputs/phase_0/SYNTHETIC_six_week_example.csv')),table(read('outputs/phase_1/SYNTHETIC_trap_detection.csv')),table(read('outputs/phase_2/SYNTHETIC_load_log.csv').drop(columns=['loaded_at'])),table(read('outputs/phase_3/SYNTHETIC_clock_excerpt.csv').head(18)),table(summary),table(read('outputs/phase_5/SYNTHETIC_claim_lineage.csv')),'See manifest.json and SYNTHETIC_verification_log.txt. Stacked phase pull requests preserve review order.']
 validations=['Named checks map to all BR/FR/NFR IDs in docs/traceability.md. The six-week example is computed in SQL.','All eight traps matched expected values. Six synthetic profiling answers are recorded in docs/SYNTHETIC_profile_checklist.md. The real-source gate is NOT RUN.','Initial 14,163 accepted rows; incremental 14,174; repeat unchanged; corrupt week blocked. 44 normalized dates, 2 initial quarantines and 5 missing clean pairs.','85,044 scenario rows. The planted PADD4 March 2011 monthly reset moves to March 28; other reset periods have no substitutions.','INV-01 through INV-05 pass. E1 and E3 pass all regions. E2 passes both regimes. Exact errors and confusion matrix are saved as CSVs.','All four app pages and a PADD4 quarterly/clause selection passed AppTest. Prose numbers trace to SQL result rows. Snowflake app NOT RUN.','Local checks and two local teardown calls pass. Snowflake execution/teardown and live weekly operation are NOT RUN. Deployment remains gated.']
 fixes=['The owner approved passing unchanged reruns, resolving the BR-17 conflict.','DuckDB rejected rows as an implicit alias; it was renamed row_count. Expected counts stayed unchanged.','A last-reviewed source-state audit avoids repeatedly treating quarantined history as new. Valid correction/reversion tests passed.','Date joins enforce exact calendar lags and four-week comparisons; missing observations are not filled.','DuckDB rejected weeks and error as implicit aliases; explicit aliases fixed them. Final repeatability checks exposed sensitivity state leaking into baseline outputs. Each sensitivity scenario now runs in a transaction that is rolled back, with assertions that both parameters and weekly rows are unchanged. No source values or expected answers were changed.','App tests revealed a Streamlit width deprecation; the argument was updated.','A report-generation command initially used the wrong working directory and wrote no files; rerunning from the project parent fixed it. GitHub sign-in was required to create the repository.']
 lessons=[('Shared formulas isolate timing.','Region is a dimension, not a lever.','The zero control proves the baseline.','Exposure is created in contracting.'),('Raw values complement metadata.','Ten regions were absent from the index.','Decoys test source selection.','National-only data can still support the mechanism.'),('Transactions protect accepted state.','Corruption leaves accepted history unchanged.','Repeatability includes no-op reruns.','Block a bad batch before pricing analysis.'),('FIRST_VALUE holds reset prices.','A missing reset moves to the next available week.','Shared lags preserve the control.','Different schedules create exposure.'),('Summaries reconcile to detail.','Recovery is expected for planted effects.','Positive means can hide adverse weeks.','Review downside distributions.'),('Model views serve the app.','Freshness follows accepted observations.','Narration uses existing numbers.','A markup requires commercial acceptance.'),('Phase branches preserve review history.','Real and synthetic data remain separate.','Local success is not deployment proof.','Scaling requires contract and volume evidence.')]
 for i in range(7):
  evidence=[str(p.relative_to(ROOT)) for p in sorted((ROOT/f'outputs/phase_{i}').glob('*')) if p.name!='REPORT.md']
  technical,data,analytical,business=lessons[i]
  write(f'outputs/phase_{i}/REPORT.md',f'''# Phase {i}: {titles[i]} [SYNTHETIC DRY RUN]

Business question: {questions[i]}

What was built: see docs/phase_file_map.md and the evidence files below.

How it ran: `python local/run_pipeline.py all`, followed by verify_outputs.py, test_pipeline.py and test_app.py. Full pipeline runs took about 40–43 seconds here, excluding dependency installation.

Sample results:

{results[i]}
Validation: {validations[i]}

Surprises and fixes: {fixes[i]}

Learnings:

- Technical: {technical}
- Data: {data}
- Analytical: {analytical}
- Business: {business}

Explain-back:

1. What does this phase establish? {validations[i]}
2. What does it not establish? Actual company margins or untested Snowflake behavior.
3. Why does it matter? {business}

Exit criteria: local synthetic evidence is complete with documented scope gaps in docs/acceptance_status.md. Deployment and real-source criteria remain unverified. Publication is confirmed by GitHub PR links, not simulated pushes.

Evidence files:

'''+ '\n'.join('- `'+p+'`' for p in evidence)+'\n')
 write('docs/LEARNINGS.md','# Actual learnings\n\n'+'\n\n'.join(f'## Phase {i}: {titles[i]}\n\nExpected: {questions[i]}\n\nWhat happened: {validations[i]}\n\nWhat I changed: {fixes[i]}\n\nConcept I can now explain: {lessons[i][2]}' for i in range(7))+'\n')
 write('outputs/phase_5/SYNTHETIC_app_walkthrough.md','''# SYNTHETIC app walkthrough

Run `python -m streamlit run app/streamlit_app.py` after building the database.

1. Overview: select US/monthly/clause off. Inspect spread, regime/season and worst contiguous four-week windows. Metrics exclude the unfinished reset period; the detail retains it with a complete_period flag.
2. Scenario explorer: compare reset/clause settings. The full-history comparison table states its date scope. Use the common-window CSV for comparisons across schedules.
3. Data quality: inspect the four attempts and quarantine. The blocked week does not replace the accepted September 14 observations.
4. Assumptions: inspect illustrative values and limitations. The fixed replay date is not a live freshness claim.

Static supporting charts are in outputs/phase_4. They are analysis plots, not claimed browser screenshots. AppTest checks behavior; a visual production review in Snowflake is still required.
''')
 write('outputs/phase_6/manifest.json',json.dumps({'label':'SYNTHETIC','python':platform.python_version(),'seed':42,'as_of_date':'2026-09-23','snowflake_execution':'NOT RUN','optional_ai':'SKIPPED','real_source_gate':'NOT RUN'},indent=2)+'\n')
if __name__=='__main__':main()
