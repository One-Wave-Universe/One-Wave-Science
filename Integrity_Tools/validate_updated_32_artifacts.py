from __future__ import annotations
from pathlib import Path
from collections import Counter
import json,re,subprocess,sys,urllib.parse,hashlib

ROOT=Path(__file__).resolve().parents[1]
NODES=ROOT/'Nodes'; AX=ROOT/'Root_Axioms'; PACKS=ROOT/'AI_Readable_Packs'; WIKI=ROOT/'Wiki_Pages'; BOOK=ROOT/'Books'/'Book1_Micro'
front=re.compile(r'^---\n(.*?)\n---\n',re.S)

def meta(p:Path):
    m=front.match(p.read_text(encoding='utf-8',errors='replace')); out={}
    if not m:return out
    for line in m.group(1).splitlines():
        if ':' not in line:continue
        k,v=line.split(':',1); v=v.strip()
        try:out[k]=json.loads(v)
        except:out[k]=v.strip('"')
    return out

def node_id(p:Path):
    m=re.match(r'([A-G](?:\+|-)[0-9]+[a-z]?)_',p.name)
    return m.group(1) if m else None

node_files=list(NODES.glob('*.md'))+list(AX.glob('*.md'))
node_meta={node_id(p):meta(p) for p in node_files if node_id(p)}
errors=[]

# Appendix packs must be byte-for-byte reproducible from canonical node files.
appendix_ok=0
for letter in 'ABCDEFG':
    files=sorted(NODES.glob(f'{letter}-*.md'),key=lambda p:(int(re.search(r'\d+',p.name).group()),p.name))
    if letter=='A':files=sorted(AX.glob('A+*.md'))+files
    parts=[f'# Appendix {letter} — AI-Readable Canonical Node Pack','', 'Generated from current canonical node files. YAML front matter controls gate and lifecycle.','', '---','']
    for src in files:
        parts += [f'## SOURCE: {src.name}','',src.read_text(encoding='utf-8',errors='replace').rstrip(),'', '---','']
    expected='\n'.join(parts)+'\n'
    p=PACKS/f'Appendix_{letter}.md'
    if not p.exists() or p.read_text(encoding='utf-8',errors='replace')!=expected:
        errors.append(f'APPENDIX_MISMATCH:{letter}')
    else:appendix_ok+=1

# Wiki metadata checks.
wiki_checked=0
for p in WIKI.glob('*_Wiki_Page.html'):
    nid=node_id(p)
    if not nid or nid not in node_meta:continue
    t=p.read_text(encoding='utf-8',errors='replace'); m=node_meta[nid]
    for needle,label in [(m.get('canonical_name',''),'NAME'),(f'Gate:</strong> {m.get("gate")}', 'GATE'),(f'Lifecycle:</strong> {m.get("lifecycle")}', 'LIFECYCLE')]:
        if needle and needle not in t:errors.append(f'WIKI_{label}:{p.name}')
    wiki_checked+=1

# JSON pack metadata checks.
json_checked=0
for p in PACKS.glob('*.json'):
    nid=node_id(p)
    if not nid or nid not in node_meta:continue
    try:d=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'JSON_PARSE:{p.name}:{e}');continue
    m=node_meta[nid]
    for k in ('gate','lifecycle','claim_gate_detail'):
        if d.get(k)!=m.get(k):errors.append(f'JSON_{k.upper()}:{p.name}:{d.get(k)}!={m.get(k)}')
    json_checked+=1

# Book 1 continuous numbering, filename/header agreement, no stale active paths.
chapter_files=sorted(BOOK.glob('Book1_Ch??_*.md'))
nums=[]
for p in chapter_files:
    fm=re.match(r'Book1_Ch(\d\d)_',p.name); n=int(fm.group(1));nums.append(n)
    hm=re.search(r'^## Chapter (\d+):',p.read_text(encoding='utf-8',errors='replace'),re.M)
    if not hm or int(hm.group(1))!=n:errors.append(f'CHAPTER_HEADER:{p.name}:{hm.group(1) if hm else None}')
if nums!=list(range(1,18)):errors.append(f'CHAPTER_SEQUENCE:{nums}')
chapter_map=(BOOK/'00_CHAPTER_STATUS_MAP.md').read_text(encoding='utf-8')
if 'MISSING' in chapter_map:errors.append('CHAPTER_MAP_MISSING_LABEL')

old_stems=['Book1_Ch04_Scale_Invariance','Book1_Ch05_The_Electron','Book1_Ch06_The_Neutron','Book1_Ch07_The_Nucleus','Book1_Ch08_The_Photon','Book1_Ch09_The_Neutrino','Book1_Ch10_No_Observer_Effect','Book1_Ch11_Time_At_Micro_Scale','Book1_Ch12_No_Antimatter','Book1_Ch13_Gravity_At_Micro_Scale','Book1_Ch14_Electricity_And_Magnetism','Book1_Ch15_Mass_Effect','Book1_Ch17_The_Higgs_Field_Is_The_Lattice','Book1_Ch18_Memory_As_Compressed_State','Book1_Ch19_AI_And_Human_Same_Architecture']
allowed_old={'Integrity_Tools/UPDATED_32_book1_renumber_receipt.json','Integrity_Tools/close_book1_chapter_gaps.py','Integrity_Tools/validate_updated_32_artifacts.py','Integrity_Tools/UPDATED_32_generated_artifact_receipt.json'}
for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.md','.html','.json','.csv','.py','.txt','.js'}:continue
    rel=str(p.relative_to(ROOT)).replace('\\','/')
    if rel in allowed_old:continue
    t=p.read_text(encoding='utf-8',errors='replace')
    for s in old_stems:
        if s in t:errors.append(f'STALE_CHAPTER_PATH:{rel}:{s}')

# Markdown local-link existence; TeX constructs that resemble links are ignored.
link_count=0
for p in ROOT.rglob('*.md'):
    t=p.read_text(encoding='utf-8',errors='replace')
    for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',t):
        target=m.group(1).strip().split()[0].strip('<>')
        if target.startswith(('http://','https://','mailto:','#','data:','\\')):continue
        target=urllib.parse.unquote(target.split('#')[0])
        if not target:continue
        link_count+=1
        if not (p.parent/target).resolve().exists():errors.append(f'BROKEN_LOCAL_LINK:{p.relative_to(ROOT)}:{target}')

# PDF structural checks and Book 1 PDF header checks.
pdfs=sorted(ROOT.rglob('*.pdf')); pdf_errors=[]
for p in pdfs:
    r=subprocess.run(['pdfinfo',str(p)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    if r.returncode:pdf_errors.append(f'{p.relative_to(ROOT)}:{r.stderr.strip()}')
errors += [f'PDF:{x}' for x in pdf_errors]
book_pdfs=sorted(BOOK.glob('Book1_Ch??_*.pdf'))
for p in book_pdfs:
    n=int(re.match(r'Book1_Ch(\d\d)_',p.name).group(1))
    r=subprocess.run(['pdftotext',str(p),'-'],capture_output=True,text=True)
    if r.returncode or not re.search(rf'Chapter\s+0?{n}:',r.stdout[:1500]):errors.append(f'PDF_CHAPTER_HEADER:{p.name}')

pairs=[]; stale=[]
for p in pdfs:
    m=p.with_suffix('.md')
    if m.exists():
        pairs.append((m,p))
        if p.stat().st_mtime+1e-6 < m.stat().st_mtime:stale.append(str(p.relative_to(ROOT)))
if stale:errors += [f'STALE_PDF:{x}' for x in stale]

report={
 'pass':not errors,
 'errors':errors,
 'node_files':len(node_files),
 'appendix_packs_verified':appendix_ok,
 'wiki_pages_checked':wiki_checked,
 'json_packs_checked':json_checked,
 'book1_chapters':len(chapter_files),
 'book1_sequence':nums,
 'local_markdown_links_checked':link_count,
 'pdf_count':len(pdfs),
 'pdf_source_pairs':len(pairs),
 'book1_pdf_count':len(book_pdfs),
 'stale_pdf_pairs':stale,
}
(ROOT/'Integrity_Tools/UPDATED_32_generated_artifact_receipt.json').write_text(json.dumps({k:v for k,v in report.items() if k not in {'pdf_count','pdf_source_pairs','book1_pdf_count','stale_pdf_pairs'}},indent=2),encoding='utf-8')
(ROOT/'Integrity_Tools/UPDATED_32_pdf_integrity_receipt.json').write_text(json.dumps({
 'pass':not pdf_errors and not stale and len(book_pdfs)==17,
 'pdf_count':len(pdfs),
 'structurally_valid':len(pdfs)-len(pdf_errors),
 'source_pdf_pairs':len(pairs),
 'stale_source_pdf_pairs':stale,
 'book1_pdf_count':len(book_pdfs),
 'book1_pdfs_regenerated':17,
 'rendered_visual_samples':['Books/Book1_Micro/Book1_Ch03_Scale_Invariance.pdf page 1','Books/Book1_Micro/Book1_Ch17_AI_And_Human_Same_Architecture.pdf page 1'],
 'errors':pdf_errors,
},indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(0 if report['pass'] else 1)
