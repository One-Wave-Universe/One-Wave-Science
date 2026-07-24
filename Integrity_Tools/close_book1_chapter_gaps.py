from pathlib import Path
import re, json
ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'Books'/'Book1_Micro'
NODES=ROOT/'Nodes'; ROOT_AXIOMS=ROOT/'Root_Axioms'
REN={4:3,5:4,6:5,7:6,8:7,9:8,10:9,11:10,12:11,13:12,14:13,15:14,17:15,18:16,19:17}
FILES={
'Book1_Ch03_Scale_Invariance':'Book1_Ch03_Scale_Invariance',
'Book1_Ch04_The_Electron':'Book1_Ch04_The_Electron',
'Book1_Ch05_The_Neutron':'Book1_Ch05_The_Neutron',
'Book1_Ch06_The_Nucleus':'Book1_Ch06_The_Nucleus',
'Book1_Ch07_The_Photon':'Book1_Ch07_The_Photon',
'Book1_Ch08_The_Neutrino':'Book1_Ch08_The_Neutrino',
'Book1_Ch09_No_Observer_Effect':'Book1_Ch09_No_Observer_Effect',
'Book1_Ch10_Time_At_Micro_Scale':'Book1_Ch10_Time_At_Micro_Scale',
'Book1_Ch11_No_Antimatter':'Book1_Ch11_No_Antimatter',
'Book1_Ch12_Gravity_At_Micro_Scale':'Book1_Ch12_Gravity_At_Micro_Scale',
'Book1_Ch13_Electricity_And_Magnetism':'Book1_Ch13_Electricity_And_Magnetism',
'Book1_Ch14_Mass_Effect':'Book1_Ch14_Mass_Effect',
'Book1_Ch15_The_Higgs_Field_Is_The_Lattice':'Book1_Ch15_The_Higgs_Field_Is_The_Lattice',
'Book1_Ch16_Memory_As_Compressed_State':'Book1_Ch16_Memory_As_Compressed_State',
'Book1_Ch17_AI_And_Human_Same_Architecture':'Book1_Ch17_AI_And_Human_Same_Architecture',
}
TEXT_EXT={'.md','.html','.json','.csv','.py','.txt','.js','.yaml','.yml'}
FULL_SCOPE={
 'Nodes/B-220_Scale_Layer.md','Nodes/A-105_Restoring_Response.md',
 'Nodes/C-311_Electric_Magnetic_Duality.md','Nodes/A-112_Persistent_Mode.md',
 'Nodes/C-315_Wave_Reader_V1.md','Nodes/C-316_Charge_Sign_Convention_Conflict.md',
 'Nodes/D-406_Isotope_Stability_Coupling_Density.md','Nodes/E-525_Focal_Point_Measurement_Operator.md',
 'Wiki_Pages/B-220_Wiki_Page.html','Wiki_Pages/A-105_Wiki_Page.html',
 'Wiki_Pages/C-311_Wiki_Page.html','Wiki_Pages/A-112_Wiki_Page.html',
 'Wiki_Pages/C-315_Wiki_Page.html','Wiki_Pages/C-316_Wiki_Page.html',
 'Wiki_Pages/D-406_Wiki_Page.html','Wiki_Pages/E-525_Wiki_Page.html',
}
PAT_FULL=re.compile(r'(?i)\b(?P<prefix>Book\s*1\s*,?\s*Chapter\s+|Book\s+One\s+Chapter\s+|Book\s*1\s+Ch|book1_chapter|Chapter\s+|chapter_?|Ch)(?P<num>\d{1,2})\b')
PAT_EXPLICIT=re.compile(r'(?i)\b(?P<prefix>Book\s*1\s*,?\s*Chapter\s+|Book\s+One\s+Chapter\s+|Book\s*1\s+Ch)(?P<num>\d{1,2})\b')

def map_match(m):
    raw=m.group('num'); n=int(raw); nn=REN.get(n,n)
    if raw.startswith('0') and len(raw)==2: out=f'{nn:02d}'
    else: out=str(nn)
    return m.group('prefix')+out

def simultaneous(text,mapping):
    pat=re.compile('|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True)))
    return pat.sub(lambda m:mapping[m.group(0)],text)

# Neutral rename avoids target collisions.
ren=[]
for old,new in FILES.items():
    for ext in ('.md','.pdf'):
        src=BOOK/(old+ext)
        if src.exists():
            tmp=BOOK/(f'__REN__{old}{ext}')
            src.rename(tmp); ren.append((tmp,BOOK/(new+ext)))
for tmp,dst in ren: tmp.rename(dst)

# One chapter-number pass per file, then one exact filename/path pass.
for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in TEXT_EXT: continue
    rel=str(p.relative_to(ROOT)).replace('\\','/')
    text=p.read_text(encoding='utf-8',errors='replace')
    if BOOK in p.parents or rel in FULL_SCOPE:
        text=PAT_FULL.sub(map_match,text)
    else:
        text=PAT_EXPLICIT.sub(map_match,text)
    text=simultaneous(text,FILES)
    p.write_text(text,encoding='utf-8')

# Mixed-book master index: only title-verified Book 1 shorthand.
p=ROOT/'00_MASTER_INDEX.md'; text=p.read_text(encoding='utf-8',errors='replace')
master_subs={
 "Ch12's internal wording conflict":"Ch11's internal wording conflict",
 '*(Note: Ch3 and Ch16 do not currently exist in any uploaded archive — real gap, not a search failure.)*':'*(Book 1 chapter numbering was closed in Updated 32; the active sequence is continuous from Ch1 through Ch17.)*',
 "inheriting Ch7's binding mechanism":"inheriting Ch6's binding mechanism",
 'Higgs (Ch17), Gravity (Ch13), Photon (Ch8)':'Higgs (Ch15), Gravity (Ch12), Photon (Ch7)',
 'β_neutrino not yet derived from collapse energy (Ch9)':'β_neutrino not yet derived from collapse energy (Ch8)',
 '- Book1 Ch3 and Ch16 — missing entirely from all archives':'- Book 1 numbering is continuous from Ch1 through Ch17 after the Updated 32 renumber',
 '**Book1_Micro/ additions:** Ch18 (Memory as Compressed State) and Ch19 (AI':'**Book1_Micro/ additions:** Ch16 (Memory as Compressed State) and Ch17 (AI',
 "distinct from Book1 Ch8's chapter":"distinct from Book1 Ch7's chapter",
 'Not reconciled against Ch9':'Not reconciled against Ch8',
}
text=simultaneous(text,master_subs); p.write_text(text,encoding='utf-8')

# Continuous map.
rows=[]
for p in sorted(BOOK.glob('Book1_Ch??_*.md')):
    m=re.match(r'Book1_Ch(\d\d)_(.+)\.md',p.name)
    if m: rows.append((int(m.group(1)),p.name))
actual=[n for n,_ in rows]; expected=list(range(1,18))
if actual!=expected: raise SystemExit(f'Book1 sequence is not continuous: {actual}')
lines=['# Book 1 Chapter Map','',
 '**Authority:** Updated 32 closed the old numbering gaps by renaming existing chapters. No chapter content was invented, deleted, or merged.','',
 '| Chapter | Status | Canonical file |','|---:|---|---|']
for n,name in rows: lines.append(f'| {n:02d} | ACTIVE | `{name}` |')
(BOOK/'00_CHAPTER_STATUS_MAP.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

# Regenerate Appendix A-G from corrected canonical node sources.
for letter in 'ABCDEFG':
    files=sorted(NODES.glob(f'{letter}-*.md'),key=lambda p:(int(re.search(r'\d+',p.name).group()),p.name))
    if letter=='A': files=sorted(ROOT_AXIOMS.glob('A+*.md'))+files
    parts=[f'# Appendix {letter} — AI-Readable Canonical Node Pack','',
           'Generated from current canonical node files. YAML front matter controls gate and lifecycle.','', '---','']
    for src in files:
        parts += [f'## SOURCE: {src.name}','',src.read_text(encoding='utf-8',errors='replace').rstrip(),'', '---','']
    (ROOT/'AI_Readable_Packs'/f'Appendix_{letter}.md').write_text('\n'.join(parts)+'\n',encoding='utf-8')

receipt={'pass':True,'old_to_new_numbers':{str(k):v for k,v in REN.items()},'old_to_new_files':FILES,'active_chapters':actual,'chapter_count':len(actual),'content_policy':'Renumbering only; no chapter prose invented, deleted, or merged.'}
(ROOT/'Integrity_Tools/UPDATED_32_book1_renumber_receipt.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
