from __future__ import annotations
import csv,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
allowed_gates=set(['BROWN', 'GRAY', 'GREEN', 'YELLOW', 'BRONZE', 'SILVER', 'GOLD', 'RED'])
allowed_lifecycles=set(['ACTIVE', 'ACTIVE_HYPOTHESIS', 'PROPOSED_BUILD', 'HELD', 'BLOCKED', 'SUPERSEDED', 'HISTORY'])
front=re.compile(r'^---\n(.*?)\n---\n',re.S)
idpat=re.compile(r'\b([A-L](?:\+|-)[0-9]+[a-z]?)\b')

def parse(p):
 m=front.match(p.read_text(encoding="utf-8",errors="replace")); d={}
 if not m:return d
 for line in m.group(1).splitlines():
  if ':' not in line:continue
  k,v=line.split(':',1)
  try:d[k]=json.loads(v.strip())
  except:d[k]=v.strip().strip('"')
 return d

files=list((ROOT/'Nodes').glob('*.md'))+list((ROOT/'Root_Axioms').glob('*.md'))
errors=[]; ids={}; names={}
for p in files:
 d=parse(p)
 if not d: errors.append(f'MISSING_FRONT_MATTER:{p.relative_to(ROOT)}'); continue
 for key in ['node_id','canonical_name','namespace','gate','lifecycle','classification','claim_gate_detail','metadata_standard']:
  if key not in d: errors.append(f'MISSING_FIELD:{p.relative_to(ROOT)}:{key}')
 if d.get('gate') not in allowed_gates: errors.append(f'BAD_GATE:{p.relative_to(ROOT)}:{d.get("gate")}')
 if d.get('lifecycle') not in allowed_lifecycles: errors.append(f'BAD_LIFECYCLE:{p.relative_to(ROOT)}:{d.get("lifecycle")}')
 nid=d.get('node_id')
 if nid in ids: errors.append(f'DUPLICATE_ID:{nid}:{ids[nid]}:{p}')
 ids[nid]=str(p.relative_to(ROOT)); names.setdefault(d.get('canonical_name'),[]).append(nid)

alias=json.loads((ROOT/'LEGACY_ID_ALIAS_REGISTRY.json').read_text())['aliases']
resolved={r['legacy_id'] for r in alias}
active=[]
for base in ['Nodes','Root_Axioms','Books','Android_Body','Musical_Universe','Governance_I_Series']:
 active += list((ROOT/base).rglob('*.md'))
ignore_names={'LEGACY_ID_ALIAS_REGISTRY.md'}
unresolved={}
for p in active:
 if p.name in ignore_names:continue
 text=p.read_text(encoding='utf-8',errors='replace')
 for m in idpat.finditer(text):
  x=m.group(1)
  if x not in ids and x not in resolved and not x.startswith('I-0'):
   unresolved.setdefault(x,[]).append(str(p.relative_to(ROOT)))
for x,ps in sorted(unresolved.items()): errors.append(f'UNRESOLVED_ID:{x}:{",".join(sorted(set(ps)))}')

# active governance forks
if len(list((ROOT/'Governance_I_Series').glob('I-01*.md'))) != 1: errors.append('I01_FORK_REMAINS')
if len(list((ROOT/'Governance_I_Series').glob('RECONCILIATION_duplex-gates-packet*.md'))) != 1: errors.append('RECONCILIATION_FORK_REMAINS')

book1=ROOT/'Books/Book1_Micro'
chapter_files=sorted(book1.glob('Book1_Ch??_*.md'))
chapter_numbers=[]
for p in chapter_files:
 m=re.match(r'Book1_Ch(\d\d)_',p.name)
 if m: chapter_numbers.append(int(m.group(1)))
if chapter_numbers != list(range(1,18)): errors.append(f'BOOK1_SEQUENCE:{chapter_numbers}')
chapter_map=(book1/'00_CHAPTER_STATUS_MAP.md').read_text()
for i in range(1,18):
 if f'| {i:02d} | ACTIVE |' not in chapter_map: errors.append(f'CHAPTER_MAP_MISSING:{i:02d}')
if 'MISSING' in chapter_map: errors.append('BOOK1_MAP_CONTAINS_MISSING')

proof_index=(ROOT/'Internal_Proofs/00_PROOF_INDEX.md').read_text()
for p in (ROOT/'Internal_Proofs').glob('*.md'):
 if p.name!='00_PROOF_INDEX.md' and p.name not in proof_index: errors.append(f'PROOF_INDEX_MISSING:{p.name}')

report={'pass':not errors,'node_file_count':len(files),'unique_node_ids':len(ids),'gate_counts':{},'lifecycle_counts':{},'unresolved_ids':unresolved,'errors':errors}
from collections import Counter
report['gate_counts']=dict(Counter(parse(p).get('gate') for p in files))
report['lifecycle_counts']=dict(Counter(parse(p).get('lifecycle') for p in files))
out=ROOT/'Integrity_Tools/UPDATED_32_integrity_receipt.json'
out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(0 if report['pass'] else 1)
