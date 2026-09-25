"""Scan every unique blob in the phase history plus the connection-test branch.
Run from the repository root: python outputs/review/history_checks.py
API tree evidence and historical-only text are saved next to this script.
This is a heuristic secret scan, not a guarantee that arbitrary secrets are absent.
"""
from pathlib import Path
import json,hashlib,re
root=Path(__file__).resolve().parents[2];review=root/'outputs/review';trees=json.loads((review/'HISTORY_TREES.json').read_text());extra=json.loads((review/'HISTORICAL_TEXT.json').read_text());blobs={};versions={}
for t in trees:
 for b in t['blobs']:
  blobs[b['sha']]=b;versions.setdefault(b['path'],set()).add(b['sha'])
content={};mismatches=[]
for b in trees[0]['blobs']:
 data=(root/b['path']).read_bytes();sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if sha!=b['sha']:mismatches.append(b['path'])
 content[b['sha']]=data
for b in extra:
 data=b['content'].encode();sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
 if sha!=b['sha']:mismatches.append(b['path'])
 blobs[b['sha']]={'path':b['path'],'size':len(data),'sha':b['sha']};content[b['sha']]=data
patterns={'github_token':r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}','aws_key':r'AKIA[A-Z0-9]{16}','private_key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----','snowflake_account_url':r'https?://[A-Za-z0-9_.-]+\.snowflakecomputing\.com','assigned_secret':r'(?i)(?:password|api_key|secret_key)\s*[:=]\s*[\x22\x27][^\x22\x27]{8,}[\x22\x27]'}
hits=[]
for sha,data in content.items():
 try:s=data.decode()
 except UnicodeDecodeError:continue
 for name,pattern in patterns.items():
  if re.search(pattern,s):hits.append({'sha':sha,'path':blobs[sha]['path'],'pattern':name})
result={'unique_blobs_scanned':len(content),'missing_blobs':sorted(set(blobs)-set(content)),'hash_mismatches':mismatches,'pattern_hits':hits,'largest_blob_bytes':max(b['size'] for b in blobs.values()),'large_files':[b for b in blobs.values() if b['size']>5_000_000],'changed_paths':{k:sorted(v) for k,v in versions.items() if len(v)>1},'stray_paths':[b['path'] for b in blobs.values() if re.search(r'(\.duckdb|\.db|\.zip|\.DS_Store|\.env)$|__pycache__|ipynb_checkpoints',b['path'])]}
print(json.dumps(result,indent=2))
