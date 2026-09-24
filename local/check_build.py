"""Rebuild twice, verify deterministic analytical outputs, and test local teardown."""
from pathlib import Path
import subprocess,sys,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
log=[]
def run(*args):
 p=subprocess.run([sys.executable,*args],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log.append('$ python '+' '.join(args)+'\n'+p.stdout)
 if p.returncode:
  (ROOT/'outputs/phase_6/SYNTHETIC_verification_log.txt').write_text('\n'.join(log));raise SystemExit(p.returncode)
def digest():
 files=list((ROOT/'data/sample').glob('SYNTHETIC_*'))+list((ROOT/'outputs/phase_4').glob('SYNTHETIC_*.csv'))
 return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
run('local/run_pipeline.py','all');run('local/verify_outputs.py');first=digest()
run('local/run_pipeline.py','all');run('local/verify_outputs.py');second=digest()
if first!=second:
 log.append('FAIL: deterministic output mismatches: '+str([p for p in first if first[p]!=second.get(p)]))
 (ROOT/'outputs/phase_6/SYNTHETIC_verification_log.txt').write_text('\n'.join(log))
 raise AssertionError('Deterministic output check failed')
log.append('PASS: input and analytical CSV hashes identical on two independent rebuilds.')
run('local/test_pipeline.py');run('local/test_app.py');run('local/render_page_views.py')
db=ROOT/'local/SYNTHETIC_fuel.duckdb';backup=ROOT/'local/SYNTHETIC_fuel_backup.duckdb';shutil.copyfile(db,backup)
try:
 run('local/run_pipeline.py','teardown');run('local/run_pipeline.py','teardown');assert not db.exists()
finally:backup.replace(db)
log.append('PASS: local teardown runs twice; verified database restored for app use.')
run('local/write_reports.py')
(ROOT/'outputs/phase_6/SYNTHETIC_verification_log.txt').write_text('SYNTHETIC verification evidence\n\n'+'\n'.join(log))
print('All build checks passed. Evidence: outputs/phase_6/SYNTHETIC_verification_log.txt')
