from __future__ import annotations
import csv, json, re, shutil, hashlib
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parent
NODES = ROOT / 'Nodes'
ROOT_AXIOMS = ROOT / 'Root_Axioms'
GOV = ROOT / 'Governance_I_Series'
HISTORY = ROOT / 'History'

ALLOWED_GATES = ['BROWN','GRAY','GREEN','YELLOW','BRONZE','SILVER','GOLD','RED']
NODE_GATE_ORDER = {'BROWN':0,'GREEN':1,'YELLOW':2,'BRONZE':3,'SILVER':4,'GOLD':5,'RED':6}
ALLOWED_LIFECYCLES = ['ACTIVE','ACTIVE_HYPOTHESIS','PROPOSED_BUILD','HELD','BLOCKED','SUPERSEDED','HISTORY']

ALIASES = {
    # Appendix A short IDs
    'A-01': ('A-101', 'Ground / Zero'),
    'A-02': ('A-102', 'Displacement'),
    'A-03': ('A-103', 'Differential'),
    'A-04': ('A-104', 'Gradient'),
    'A-05': ('A-105', 'Restoring Response'),
    'A-05b': ('A-106', 'Pressure Response'),
    'A-05c': ('B-201', 'Equilibrium Balance; title-based legacy mapping'),
    'A-06': ('A-107', 'Bounded Motion'),
    'A-07': ('A-109', 'Inertial Memory'),
    'A-08': ('A-110', 'Oscillation'),
    'A-09': ('A-111', 'Recursion'),
    'A-10': ('A-112', 'Persistent Mode'),
    'A-11': ('A-113', 'Projection'),
    # Appendix B short IDs
    'B-01': ('B-201', 'Equilibrium Balance'),
    'B-02': ('B-202', 'Pressure'),
    'B-03': ('B-203', 'Expression'),
    'B-04': ('B-204', 'Compression'),
    'B-05': ('B-205', 'Mirror'),
    'B-06': ('B-206', 'Paired Loop'),
    'B-06a': ('B-206a', 'Shared Boundary'),
    'B-06b': ('B-206b', 'Four Views'),
    'B-07': ('B-207', 'Threshold State'),
    'B-08': ('B-208', 'Threshold Windows'),
    'B-09': ('B-209', 'Break Condition'),
    'B-10': ('B-210', 'Return'),
    'B-11': ('B-211', 'Loop Break'),
    'B-12': ('B-212', 'Loop Counter'),
    'B-13': ('B-213', 'Access Line'),
    'B-14': ('B-214', 'Recursive Access Growth'),
    'B-15': ('B-215', 'Hyperloop'),
    'B-16': ('B-216', 'Threshold Mathematics'),
    # Appendix C short IDs
    'C-01': ('C-301', 'Mirror Gate'),
    'C-02': ('C-302', 'Momentum'),
    'C-03': ('C-303', 'Kinetic Energy'),
    'C-04': ('C-304', 'Potential'),
    'C-05': ('C-305', 'Work'),
    'C-06': ('C-306', 'Torque'),
    'C-07': ('C-307', 'Angular Momentum'),
    'C-08': ('C-308', 'Spin-half'),
    # Appendix D short IDs
    'D-01': ('D-401', 'Flux'),
    'D-02': ('D-402', 'Resonant Mode'),
    'D-03': ('D-403', 'Spherical Modes'),
    'D-04': ('D-404', 'Nested Resonance'),
    'D-05': ('D-405', 'Harmonic Shell'),
    # Appendix E short IDs (title-verified, not raw number-offset assumptions)
    'E-01': ('E-501', 'Zero Compression'),
    'E-02': ('E-503', 'Pressure (Gradient Form)'),
    'E-03': ('E-504', 'Surface'),
    'E-04': ('E-505', 'Coupling'),
    'E-05': ('E-506', 'Stability'),
    'E-06': ('E-507', 'Scale-Invariant Loop'),
    # Appendix F short IDs
    'F-01': ('F-601', 'Influence'),
    'F-02': ('F-602', 'Interaction Differential'),
    'F-03': ('F-603', 'Transfer'),
    'F-04': ('F-604', 'Resonance'),
    'F-05': ('F-605', 'Interference'),
    'F-06': ('F-606', 'Reflection'),
    'F-07': ('F-607', 'Transmission'),
    'F-08': ('F-608', 'Attenuation'),
    # Appendix G short IDs
    'G-01': ('G-701', 'Evaluation Differential'),
    'G-02': ('G-702', 'Evaluation'),
    'G-03': ('G-703', 'Modulation'),
    'G-04': ('G-704', 'Kabeuchi'),
    'G-05': ('G-705', 'Correction'),
    'G-06': ('G-706', 'Validation'),
    # Retired physics-I aliases
    'I-08': ('E-528', 'Static Redshift Transport'),
    'I-09': ('A-115', 'Unified Compression Field'),
    'I-10': ('C-311', 'Electric-Magnetic Duality'),
    # H/I/J/K/L packet dispositions
    'H-100': ('A+101;A-101', 'Field and Void split into root field and reference condition'),
    'H-101': ('B-204;B-203', 'Compression / Expression'),
    'H-102': ('B-205;C-301', 'Mirror / Mirror Gate'),
    'H-105': ('E-517', 'Negative Space'),
    'H-108': ('B-222', 'Oscillation Center'),
    'I-110': ('F-603', 'Transfer'),
    'J-101': ('C-309', 'Propagation Limit'),
    'J-103': ('A-105', 'Restoring Response'),
    'J-106': ('C-314', 'Three Frames of Reference'),
    'K-103': ('A-112', 'Persistent Mode'),
    'C-3113': ('C-311', 'Electric-Magnetic Duality'),
    'C-3114': ('C-310', 'Resistance Field'),
    'C-3119': ('F-604', 'Resonance'),
}

# Historical proposals deliberately have no active canonical target.
DISPOSITIONS = {
    'H-01': 'SUPERSEDED_HYPOTHESIS_NAMESPACE',
    'H-02': 'SUPERSEDED_HYPOTHESIS_NAMESPACE',
    'H-106': 'UNBUILT_GENERAL_BOUNDARY_CONDITIONS',
    'C-3118': 'UNBUILT_PHASE_LOCKING_PROPOSAL',
    'F-609': 'RETIRED_FORWARD_REFERENCE_NO_NODE',
    'F-610': 'RETIRED_FORWARD_REFERENCE_NO_NODE',
    'K-104': 'ROUTED_TO_BOOKS',
    'L-100': 'ROUTED_TO_BOOKS',
}

NAME_OVERRIDES = {
    'B-201': 'Equilibrium Balance',
    'G-709': 'Regulated-Response Balance',
}
GATE_OVERRIDES = {
    'A+101': 'GREEN',
    'G-723a': 'GREEN',
}
LIFECYCLE_OVERRIDES = {
    'G-722': 'PROPOSED_BUILD',
    'G-723a': 'HELD',
}
SERIES_CLASS = {
    'A': 'Foundation Primitive / Extension',
    'B': 'Cycle and Relationship Structure',
    'C': 'Applied Mechanics and Boundary Structure',
    'D': 'Geometry, Resonance, and Simulation',
    'E': 'Applied Dynamics and Stability',
    'F': 'Interaction Operators',
    'G': 'Evaluation, Control, and Route Grammar',
}


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='replace')

def write(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s.rstrip() + '\n', encoding='utf-8')

def move(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists(): dst.unlink()
    shutil.move(str(src), str(dst))

def file_id(p: Path) -> str:
    m = re.match(r'([A-G](?:\+|-)[0-9]+[a-z]?)_', p.name)
    if not m: raise ValueError(f'No node id in {p}')
    return m.group(1)

def title_from_text(node_id: str, text: str, p: Path) -> str:
    if node_id in NAME_OVERRIDES: return NAME_OVERRIDES[node_id]
    for line in text.splitlines()[:30]:
        m = re.match(r'^\s*#{0,3}\s*(?:NODE|Node|Root Axiom)\s+(?:[A-Z][+-][0-9]+[a-z]?|[0-9]+)\s*:\s*(.+?)\s*$', line)
        if m:
            return re.sub(r'\s*\([^)]*status[^)]*\)\s*$', '', m.group(1), flags=re.I).strip()
    stem = p.stem.split('_',1)[1] if '_' in p.stem else p.stem
    return stem.replace('_',' ')

def extract_field(text: str, key: str) -> str | None:
    pat = re.compile(rf'^\s*(?:\*\*)?{re.escape(key)}(?:\*\*)?\s*:\s*(.*?)\s*$', re.I)
    for line in text.splitlines()[:40]:
        m = pat.match(line)
        if m: return m.group(1).strip().rstrip('  ')
    return None

def determine_gate(node_id: str, raw: str | None, is_root: bool) -> str:
    if node_id in GATE_OVERRIDES: return GATE_OVERRIDES[node_id]
    u = (raw or '').upper().replace('🟡','YELLOW')
    gates = [g for g in NODE_GATE_ORDER if re.search(rf'\b{g}\b', u)]
    if gates: return min(gates, key=lambda g: NODE_GATE_ORDER[g])
    if 'GRAY' in u: return 'GREEN'  # Gray is a comparison layer for chapters, not a node gate.
    if 'ROOT AXIOM' in u or is_root: return 'GREEN'
    return 'BROWN'

def determine_lifecycle(node_id: str, raw: str | None) -> str:
    if node_id in LIFECYCLE_OVERRIDES: return LIFECYCLE_OVERRIDES[node_id]
    u = (raw or '').upper()
    if 'BLOCKED' in u: return 'BLOCKED'
    if any(x in u for x in ['HELD','DEFERRED','PARKED']): return 'HELD'
    if any(x in u for x in ['HYPOTHESIS','PROPOSED']): return 'ACTIVE_HYPOTHESIS'
    return 'ACTIVE'

def strip_initial_metadata(text: str) -> str:
    lines = text.splitlines()
    out=[]
    skipped_heading=False
    for idx,line in enumerate(lines):
        if idx < 45:
            if re.match(r'^\s*#{0,3}\s*(?:NODE|Node|Root Axiom)\s+(?:[A-Z][+-][0-9]+[a-z]?|[0-9]+)\s*:', line):
                skipped_heading=True; continue
            if re.match(r'^\s*(?:\*\*)?(?:STATUS|Status)(?:\*\*)?\s*:', line): continue
            if re.match(r'^\s*(?:\*\*)?(?:CLASSIFICATION|Classification)(?:\*\*)?\s*:', line): continue
        out.append(line)
    while out and not out[0].strip(): out.pop(0)
    return '\n'.join(out)

def yaml_q(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)

def normalize_node(p: Path):
    text=read(p)
    node_id=file_id(p)
    is_root=p.parent.name=='Root_Axioms'
    name=title_from_text(node_id,text,p)
    raw=extract_field(text,'Status')
    cls=extract_field(text,'Classification') or ('Foundation Root' if is_root else SERIES_CLASS.get(node_id[0],'Canonical Node'))
    gate=determine_gate(node_id,raw,is_root)
    lifecycle=determine_lifecycle(node_id,raw)
    detail=(raw or 'No prior status field found').strip()
    if detail.upper().replace('🟡','').strip() == gate:
        detail='None'
    namespace='ROOT_AXIOM' if is_root else 'NODE'
    body=strip_initial_metadata(text)
    # Remove any stale YAML front matter from repeated runs.
    if body.startswith('---\n'):
        end=body.find('\n---\n',4)
        if end!=-1: body=body[end+5:]
    header=(
        '---\n'
        f'node_id: {yaml_q(node_id)}\n'
        f'canonical_name: {yaml_q(name)}\n'
        f'namespace: {yaml_q(namespace)}\n'
        f'gate: {yaml_q(gate)}\n'
        f'lifecycle: {yaml_q(lifecycle)}\n'
        f'classification: {yaml_q(cls)}\n'
        f'claim_gate_detail: {yaml_q(detail)}\n'
        f'metadata_standard: "I-06"\n'
        '---\n\n'
        f'# {"Root Axiom" if is_root else "Node"} {node_id}: {name}\n\n'
    )
    write(p,header+body)


def insert_after_header(text: str, block: str) -> str:
    # after YAML and H1
    m=re.search(r'\n# .*?\n',text)
    if not m: return block+'\n'+text
    pos=m.end()
    return text[:pos]+'\n'+block.rstrip()+'\n\n'+text[pos:].lstrip('\n')

# 1. Governance fork resolution
histgov=HISTORY/'Superseded_Governance'
histgov.mkdir(parents=True, exist_ok=True)
addendum=GOV/'I-01_Addendum_HIJKL_Resolution.md'
alt=GOV/'I-01_Special_Rules_ALT_NEEDS_RECONCILING.md'
if addendum.exists(): move(addendum,histgov/'I-01_HIJKL_Resolution_Source.md')
if alt.exists(): move(alt,histgov/'I-01_Lifecycle_ALT_Superseded_by_I-02.md')

v1=GOV/'RECONCILIATION_duplex-gates-packet.md'
v2=GOV/'RECONCILIATION_duplex-gates-packet_v2.md'
v3=GOV/'RECONCILIATION_duplex-gates-packet_v3.md'
if v1.exists(): move(v1,histgov/'RECONCILIATION_duplex-gates-packet_v1.md')
if v2.exists(): move(v2,histgov/'RECONCILIATION_duplex-gates-packet_v2.md')
if v3.exists():
    t=read(v3)
    t=re.sub(r'^# RECONCILIATION — Duplex Six-Gate Packet v3', '# RECONCILIATION — Duplex Six-Gate Packet (Canonical)', t)
    t=t.replace('History: v1 and v2 remain preserved.', 'Canonical authority: this file controls the current disposition. Historical v1 and v2 are preserved under `History/Superseded_Governance/`.')
    write(v1,t)
    v3.unlink()

# Bind the HIJKL resolution into I-01
p_i01=GOV/'I-01_Special_Rules.md'
i01=read(p_i01)
if 'RULE 19 — Active Namespace Authority' not in i01:
    i01 += '''\n\n---\n\nRULE 19 — Active Namespace Authority and H/I/J/K/L Resolution\n\nThe active canonical namespaces are:\n\n```text\nA+1xx   Root axioms\nA-1xx   Foundation primitives and extensions\nB-2xx   Cycle and relationship structure\nC-3xx   Applied mechanics and boundary structure\nD-4xx   Geometry, resonance, and simulation\nE-5xx   Applied dynamics and stability\nF-6xx   Interaction operators\nG-7xx   Evaluation, control, and route grammar\nI-0x    Repository governance only\n```\n\nH, J, K, and L are not active node namespaces. Their historical proposals were routed into A-G nodes or Books, or left explicitly unbuilt. The binding legacy dispositions are recorded in `LEGACY_ID_ALIAS_REGISTRY.md`. Hypothesis is a lifecycle state, not an appendix letter.\n\nThere is one active I-01 file: `I-01_Special_Rules.md`. I-02 controls proof/trust lifecycle. I-06 controls canonical metadata and alias resolution. Alternate I-01 drafts and earlier duplex reconciliation versions are historical sources only.\n'''
write(p_i01,i01)

# 2. New metadata governance
write(GOV/'I-06_Canonical_Node_Metadata_and_Alias_Resolution.md', '''# Node I-06: Canonical Node Metadata and Alias Resolution\n\n**Gate:** GREEN\n**Lifecycle:** ACTIVE\n**Classification:** Repository Governance\n\n## Purpose\n\nEvery active node and root axiom must expose one machine-readable metadata block. Gate color, lifecycle state, and audit commentary are separate fields. A status sentence may not carry all three jobs.\n\n## Canonical Metadata\n\nEvery file directly under `Nodes/` or `Root_Axioms/` begins with YAML front matter containing:\n\n```yaml\nnode_id: "B-201"\ncanonical_name: "Equilibrium Balance"\nnamespace: "NODE"\ngate: "GREEN"\nlifecycle: "ACTIVE"\nclassification: "Cycle and Relationship Structure"\nclaim_gate_detail: "Previous mixed-status detail, or None"\nmetadata_standard: "I-06"\n```\n\n## Gate Rule\n\nAllowed gate values are:\n\n```text\nBROWN, GRAY, GREEN, YELLOW, BRONZE, SILVER, GOLD, RED\n```\n\nFor active A-G nodes, the ordinary ladder is Brown -> Green -> Yellow -> Bronze -> Silver -> Gold. Gray remains the Standard-Model comparison track for chapters. A node containing external Gray reference material still receives a node gate, with the comparison role stated separately. Red remains governed by I-02.\n\nA composite node receives the most conservative gate among its load-bearing claims. More advanced subclaims remain in `claim_gate_detail`; they do not silently promote the whole node.\n\n## Lifecycle Rule\n\nAllowed lifecycle values are:\n\n```text\nACTIVE, ACTIVE_HYPOTHESIS, PROPOSED_BUILD, HELD, BLOCKED, SUPERSEDED, HISTORY\n```\n\nLifecycle does not change gate. `HELD` is not a color. `BLOCKED` is not a color. `CANDIDATE` is commentary or a promotion target, not a gate.\n\n## Alias Rule\n\nLegacy short IDs do not become duplicate nodes. They resolve through `LEGACY_ID_ALIAS_REGISTRY.json`. Each alias must identify a canonical target or an explicit historical disposition. Title verification outranks assumed numeric offset.\n\n## Duplicate-Name Rule\n\nDuplicate display terms are permitted only when every affected node carries an explicit `distinct, do not merge` note and `DUPLICATE_NAME_DISAMBIGUATION.md` records the distinction.\n\n## Failure Conditions\n\nThe metadata layer fails if an active node lacks front matter, uses an unapproved gate/lifecycle, duplicates an active ID, or cites an ID that resolves to neither a canonical target nor a declared historical disposition.\n''')

# 3. Move loose alternate neutrino node out of active Nodes
neut=NODES/'Neutrino_Node_ALT_FORMAT.md'
if neut.exists():
    target=HISTORY/'Unintegrated_Nodes'/'Neutrino_Node_ALT_FORMAT.md'
    t=read(neut)
    notice='# Historical Unintegrated Node Draft\n\nThis file was removed from the active `Nodes/` namespace in Updated 32 because it has no canonical node ID, uses an alternate template, and contains stale dependency assumptions. Its subject remains covered by Book 1 Chapter 8. No new node ID was invented during the integrity repair.\n\n---\n\n'
    write(target,notice+t)
    neut.unlink()

# 4. Normalize active node metadata
for p in sorted(list(NODES.glob('*.md'))+list(ROOT_AXIOMS.glob('*.md'))):
    normalize_node(p)

# 5. Duplicate-name disambiguation
b201=NODES/'B-201_Balance.md'
g709=NODES/'G-709_Balance.md'
for p, block in [
    (b201, '''## Name Disambiguation\n\nB-201 **Equilibrium Balance** is the scalar equilibrium/imbalance measure. It is distinct from G-709 **Regulated-Response Balance**, which is a feedback-scaled response rule. The two nodes share a historical word but not a mechanism. **Do not merge them.**'''),
    (g709, '''## Name Disambiguation\n\nG-709 **Regulated-Response Balance** is a feedback-scaled response rule. It is distinct from B-201 **Equilibrium Balance**, which measures scalar equilibrium/imbalance. The two nodes share a historical word but not a mechanism. **Do not merge them.**''')]:
    t=read(p)
    if '## Name Disambiguation' not in t:
        write(p,insert_after_header(t,block))

write(ROOT/'DUPLICATE_NAME_DISAMBIGUATION.md', '''# Duplicate-Name Disambiguation Registry\n\n| Shared term | Node | Canonical display name | Distinction | Merge rule |\n|---|---|---|---|---|\n| Balance | B-201 | Equilibrium Balance | Scalar equilibrium/imbalance measure | Do not merge with G-709 |\n| Balance | G-709 | Regulated-Response Balance | Feedback-scaled response rule | Do not merge with B-201 |\n| Pressure | B-202 | Pressure | State generated from scalar imbalance | Do not merge with E-503 |\n| Pressure | E-503 | Pressure (Gradient Form) | Spatial-gradient energy/pressure specialization | Do not merge with B-202 |\n| Mirror | B-205 | Mirror | Flip operation | Do not merge with C-301 |\n| Mirror Gate | C-301 | Mirror Gate | Boundary/location where the flip operates | Do not merge with B-205 |\n''')

# update explicit names in active text files
active_text_roots=[NODES,ROOT_AXIOMS,ROOT/'Books',ROOT/'Android_Body',ROOT/'Musical_Universe',GOV]
for base in active_text_roots:
    if not base.exists(): continue
    for p in base.rglob('*.md'):
        t=read(p)
        t=t.replace('B-201 Balance','B-201 Equilibrium Balance')
        t=t.replace('G-709 Balance','G-709 Regulated-Response Balance')
        write(p,t)

# 6. Node-specific dependency repairs
p=NODES/'D-402_Resonant_Mode.md'; t=read(p)
t=t.replace('deferred to Appendix E (Node D-02b address)','deferred to E-508 Real Persistence Under Loss')
t=t.replace('Node D-02b (parked):\nReal persistence under loss, compensation mechanisms, and feedback stabilization.\nAddress: Appendix E stability mechanisms.\nDoes not block D-402 at current scope.', 'Canonical downstream address: E-508 Real Persistence Under Loss. The legacy D-02b address is retired and resolves through the alias registry.')
write(p,t)

p=NODES/'E-501_Zero_Compression.md'; t=read(p)
t=t.replace('Interaction with Balance Condition (A-05c) to be derived.', 'Interaction with B-201 Equilibrium Balance to be derived. The legacy A-05c label is retired.')
marker='---\n\n## Node : Real Persistence Under Loss'
if marker in t:
    t=t.split(marker)[0].rstrip()+'''\n\n---\n\n## Canonical Persistence Dependency\n\nReal Persistence Under Loss is defined only in E-508. The anonymous embedded duplicate formerly appended to this file was removed.\n'''
# remove empty receive line
t=t.replace('Also receives:\n (Real persistence under loss) — parked address from Appendix D', 'Also receives:\n- E-508 Real Persistence Under Loss')
write(p,t)

p=NODES/'E-508_Real_Persistence_Under_Loss.md'; t=read(p).replace('E-504 coupling draws energy','E-505 coupling draws energy'); write(p,t)

# Remove nonexistent F-609/F-610 forward dependencies and F-10 typo.
for fn in ['F-601_Influence.md','F-603_Transfer.md','F-604_Resonance.md','F-606_Reflection.md','F-607_Transmission.md','F-608_Attenuation.md']:
    p=NODES/fn; t=read(p)
    t=t.replace('F-602 through F-10','F-602 through F-608')
    t=re.sub(r',?\s*F-609 Amplification', '', t)
    t=re.sub(r',?\s*F-610 Persistence', '', t)
    t=t.replace('[All Interaction Outcomes F-602 through F-608]', '[Canonical Interaction Outcomes F-602 through F-608]')
    if 'Updated 32 forward-reference repair' not in t:
        t += '\n\n## Updated 32 forward-reference repair\n\nLegacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.\n'
    write(p,t)

# 7. Alias registry
rows=[]
for old,(target,note) in sorted(ALIASES.items()): rows.append({'legacy_id':old,'resolution':'ALIAS','canonical_target':target,'note':note})
for old,disp in sorted(DISPOSITIONS.items()): rows.append({'legacy_id':old,'resolution':'DISPOSITION','canonical_target':'','note':disp})
with open(ROOT/'LEGACY_ID_ALIAS_REGISTRY.csv','w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['legacy_id','resolution','canonical_target','note']); w.writeheader(); w.writerows(rows)
write(ROOT/'LEGACY_ID_ALIAS_REGISTRY.json',json.dumps({'metadata_standard':'I-06','aliases':rows},indent=2,ensure_ascii=False))
md=['# Legacy ID Alias Registry','', 'Legacy IDs are resolvers, not active duplicate nodes. Title-verified mappings override assumed numerical offsets.','', '| Legacy ID | Resolution | Canonical target | Note |','|---|---|---|---|']
for r in rows: md.append(f"| {r['legacy_id']} | {r['resolution']} | {r['canonical_target'] or '—'} | {r['note']} |")
write(ROOT/'LEGACY_ID_ALIAS_REGISTRY.md','\n'.join(md))

# 8. Rebuild Internal_Proofs
proofdir=ROOT/'Internal_Proofs'; rawdir=HISTORY/'Raw_AI_Proof_Discussions'; rawdir.mkdir(parents=True,exist_ok=True)
old_files=['02_internal_proofs.md','03_ Chapter._intetnal_proofs.md','04_proofs_internal.md','05_onternal_proofs.md','06_mathproofs.md','07_proofs.md','proofs.md']
raw={}
for fn in old_files:
    p=proofdir/fn
    if p.exists():
        raw[fn]=read(p)
        move(p,rawdir/fn)

def cleaned_doc(title,status,body):
    return f'# {title}\n\n**Document status:** {status}  \n**Authority:** Internal derivation draft only. Current canonical node files override this document wherever they differ.\n\n---\n\n'+body.strip()+'\n'

if '02_internal_proofs.md' in raw:
    body=re.sub(r'^Fair\..*?Horrible little clipboard behavior\.\s*', '', raw['02_internal_proofs.md'], flags=re.S)
    write(proofdir/'02_Proof_Upgrade_Attempt.md',cleaned_doc('Internal Proof Draft 02: Proof Upgrade Attempt','DRAFT / LEGACY EXTRACTION',body))
if '03_ Chapter._intetnal_proofs.md' in raw:
    write(proofdir/'03_Motion_and_Topology_Draft_Index.md',cleaned_doc('Internal Proof Draft 03: Motion and Topology','DRAFT INDEX', '''The original file mixed conversational closure language, old node numbers, and proof fragments. It is preserved verbatim under `History/Raw_AI_Proof_Discussions/03_ Chapter._intetnal_proofs.md`.\n\nCurrent canonical homes for this material are:\n\n- C-302 Momentum\n- C-303 Kinetic Energy\n- C-306 Torque\n- C-307 Angular Momentum\n- C-308 Spin-half\n\nNo statement in the raw draft promotes those nodes beyond their current I-06 gate metadata.'''))
if '04_proofs_internal.md' in raw:
    body=raw['04_proofs_internal.md'].replace('Chapter 4: CLOSED.','# Legacy closure statement removed; current nodes control closure.',1)
    write(proofdir/'04_Resonance_and_Mode_Structure_Audit.md',cleaned_doc('Internal Proof Draft 04: Resonance and Mode Structure','DRAFT / LEGACY EXTRACTION',body))
if '05_onternal_proofs.md' in raw:
    body=re.sub(r'^Chapter 5: Stability Definitions and Definition-Level Math Proofs\s*','',raw['05_onternal_proofs.md'])
    write(proofdir/'05_Stability_Definition_Proofs.md',cleaned_doc('Internal Proof Draft 05: Stability Definition Proofs','DRAFT / INTERNAL',body))
if '06_mathproofs.md' in raw:
    body=re.sub(r'^Here’s the cleaned upload-ready Chapter 6 proof file\..*?Barely\.\s*','',raw['06_mathproofs.md'],flags=re.S)
    body=re.sub(r'^Chapter 6: Choice Interaction Terms — Internal Math Proof Stack\s*','',body)
    write(proofdir/'06_Choice_Interaction_Terms.md',cleaned_doc('Internal Proof Draft 06: Choice Interaction Terms','DRAFT / INTERNAL',body))
if '07_proofs.md' in raw:
    body=re.sub(r'^Yep\..*?Just Chapter 7 as it stands\.\s*','',raw['07_proofs.md'],flags=re.S)
    body=re.sub(r'^Chapter 7: Evaluation, Modulation, Validation, and Balance\s*','',body)
    write(proofdir/'07_Evaluation_Modulation_Validation_and_Balance.md',cleaned_doc('Internal Proof Draft 07: Evaluation, Modulation, Validation, and Balance','DRAFT / INTERNAL',body))

write(proofdir/'01_Foundation_Proof_Index.md', '''# Internal Proof Index 01: Foundation\n\n**Document status:** INDEX ONLY\n\nNo standalone Chapter 01 proof file was found in Updated 31. This index prevents the missing number from being mistaken for lost canonical proof. The current foundation authority is the active A-series and Root Axiom files:\n\n- A+101 through A+103\n- A-101 through A-117\n\nTheir I-06 gate metadata controls proof status. No proof claim is invented here.\n''')

active_proofs=sorted(p.name for p in proofdir.glob('*.md') if p.name!='00_PROOF_INDEX.md')
lines=['# Internal Proofs: Canonical Directory Index','', '**Rule:** These documents are internal derivation drafts or audits. They do not override current node gates. Raw conversational sources are preserved under `History/Raw_AI_Proof_Discussions/`.','', '| File | Role |','|---|---|']
for fn in active_proofs:
    role='Formal audit' if fn=='Mass_Effect_Mirror_Gate_Four_Interaction_Audit.md' else ('Foundation index' if fn.startswith('01_') else 'Internal draft')
    lines.append(f'| `{fn}` | {role} |')
write(proofdir/'00_PROOF_INDEX.md','\n'.join(lines))

# 9. Chapter status map
book1=ROOT/'Books'/'Book1_Micro'
chapter_titles={}
for p in book1.glob('Book1_Ch??_*.md'):
    m=re.match(r'Book1_Ch(\d\d)_(.+)\.md',p.name)
    if m: chapter_titles[int(m.group(1))]=m.group(2).replace('_',' ')
numbers=sorted(chapter_titles)
if numbers != list(range(1,18)):
    raise RuntimeError(f'Book 1 chapter numbering is not continuous: {numbers}')
lines=['# Book 1 Chapter Map','', '**Authority:** Updated 32 closed the old numbering gaps by renaming existing chapters. No chapter content was invented, deleted, or merged.','', '| Chapter | Status | Canonical file |','|---:|---|---|']
for i in numbers:
    lines.append(f'| {i:02d} | ACTIVE | `Book1_Ch{i:02d}_{chapter_titles[i].replace(" ","_")}.md` |')
write(book1/'00_CHAPTER_STATUS_MAP.md','\n'.join(lines))

# 10. Regenerate AI appendix packs from canonical node files
for letter in 'ABCDEFG':
    files=sorted(NODES.glob(f'{letter}-*.md'),key=lambda p:(int(re.search(r'\d+',p.name).group()),p.name))
    if letter=='A': files=sorted(ROOT_AXIOMS.glob('A+*.md'))+files
    parts=[f'# Appendix {letter} — AI-Readable Canonical Node Pack','', 'Generated from current canonical node files. YAML front matter controls gate and lifecycle.','', '---','']
    for p in files:
        parts += [f'## SOURCE: {p.name}','',read(p).rstrip(),'', '---','']
    write(ROOT/'AI_Readable_Packs'/f'Appendix_{letter}.md','\n'.join(parts))

# JSON pack normalization
front_re=re.compile(r'^---\n(.*?)\n---\n',re.S)
def parse_front(p: Path):
    m=front_re.match(read(p)); d={}
    if not m:return d
    for line in m.group(1).splitlines():
        if ':' not in line:continue
        k,v=line.split(':',1)
        try:d[k]=json.loads(v.strip())
        except:d[k]=v.strip().strip('"')
    return d
node_meta={file_id(p):parse_front(p) for p in list(NODES.glob('*.md'))+list(ROOT_AXIOMS.glob('*.md'))}
for p in (ROOT/'AI_Readable_Packs').glob('*.json'):
    try:d=json.loads(read(p))
    except:continue
    mid=re.match(r'([A-G](?:\+|-)[0-9]+[a-z]?)_',p.name)
    if not mid or mid.group(1) not in node_meta: continue
    meta=node_meta[mid.group(1)]
    old=d.pop('status',None)
    d['gate']=meta['gate']; d['lifecycle']=meta['lifecycle']; d['claim_gate_detail']=meta['claim_gate_detail']
    if old is not None and meta['claim_gate_detail']=='None': d['claim_gate_detail']=old
    write(p,json.dumps(d,indent=2,ensure_ascii=False))

# 11. Patch wiki metadata and canonical duplicate names
for p in (ROOT/'Wiki_Pages').glob('*_Wiki_Page.html'):
    mid=re.match(r'([A-G](?:\+|-)[0-9]+[a-z]?)_',p.name)
    if not mid or mid.group(1) not in node_meta: continue
    nid=mid.group(1); meta=node_meta[nid]; name=meta['canonical_name']; gate=meta['gate']; lifecycle=meta['lifecycle']
    t=read(p)
    t=re.sub(r'<title>.*?</title>',f'<title>{nid}: {name}</title>',t,count=1,flags=re.S)
    t=re.sub(r'<h1>.*?</h1>',f'<h1>{nid}: {name}</h1>',t,count=1,flags=re.S)
    t=re.sub(r'<div class="status-banner">.*?</div>',f'<div class="status-banner"><strong>Gate: {gate} | Lifecycle: {lifecycle}</strong></div>',t,count=1,flags=re.S)
    t=re.sub(r'<tr><td class="label">Status</td><td>.*?</td></tr>',f'<tr><td class="label">Gate</td><td>{gate}</td></tr>\n<tr><td class="label">Lifecycle</td><td>{lifecycle}</td></tr>',t,count=1,flags=re.S)
    t=t.replace('B-201 Balance','B-201 Equilibrium Balance').replace('G-709 Balance','G-709 Regulated-Response Balance')
    write(p,t)

# 12. Master index normalization and repository navigation
master=ROOT/'00_MASTER_INDEX.md'; t=read(master)
t=re.sub(r'Compiled from .*?updated .*?\.', 'Compiled from the current consolidated node repository; updated July 23, 2026.', t, count=1)
if 'Updated 32 repository-integrity handoff' not in t:
    insertion='Updated 32 repository-integrity handoff: `UPDATED_32_REPOSITORY_INTEGRITY_REPAIR.md`.\nMetadata authority: `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md`.\nLegacy ID resolution: `LEGACY_ID_ALIAS_REGISTRY.md`.\n'
    t=t.replace('Updated 28 alphabet/Fibonacci-word handoff: `UPDATED_28_ALPHABET_FIBONACCI_WORD_VALIDATION.md`.\n', 'Updated 28 alphabet/Fibonacci-word handoff: `UPDATED_28_ALPHABET_FIBONACCI_WORD_VALIDATION.md`.\n'+insertion)
t=t.replace('| B-201 | Balance |','| B-201 | Equilibrium Balance |').replace('| G-709 | Balance |','| G-709 | Regulated-Response Balance |')
# replace table status with canonical gate
for nid,meta in node_meta.items():
    t=re.sub(rf'^(\|\s*{re.escape(nid)}\s*\|.*\|)\s*[^|]+\|\s*$',lambda m:m.group(1)+' '+meta['gate']+' |',t,flags=re.M)
# loose neutrino record becomes historical
if '**Nodes/Neutrino_Node_ALT_FORMAT.md (NEW, flagged):**' in t:
    t=t.replace('**Nodes/Neutrino_Node_ALT_FORMAT.md (NEW, flagged):**','**History/Unintegrated_Nodes/Neutrino_Node_ALT_FORMAT.md (historical unintegrated draft):**')
write(master,t)

start=ROOT/'AI_CANONICAL_START_HERE.md'; t=read(start)
nav='''\n## Updated 32 Integrity Authorities\n\n- `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md`\n- `LEGACY_ID_ALIAS_REGISTRY.md`\n- `DUPLICATE_NAME_DISAMBIGUATION.md`\n- `Books/Book1_Micro/00_CHAPTER_STATUS_MAP.md`\n- `Internal_Proofs/00_PROOF_INDEX.md`\n\nRead gate and lifecycle from node YAML front matter. Do not reconstruct status from prose.\n'''
if '## Updated 32 Integrity Authorities' not in t:t+=nav
write(start,t)

# 13. Integrity validator and receipts
TOOLS=ROOT/'Integrity_Tools'; TOOLS.mkdir(exist_ok=True)
validator='''from __future__ import annotations\nimport csv,json,re,sys\nfrom pathlib import Path\nROOT=Path(__file__).resolve().parents[1]\nallowed_gates=set(%r)\nallowed_lifecycles=set(%r)\nfront=re.compile(r'^---\\n(.*?)\\n---\\n',re.S)\nidpat=re.compile(r'\\b([A-L](?:\\+|-)[0-9]+[a-z]?)\\b')\n\ndef parse(p):\n m=front.match(p.read_text(encoding="utf-8",errors="replace")); d={}\n if not m:return d\n for line in m.group(1).splitlines():\n  if ':' not in line:continue\n  k,v=line.split(':',1)\n  try:d[k]=json.loads(v.strip())\n  except:d[k]=v.strip().strip('"')\n return d\n\nfiles=list((ROOT/'Nodes').glob('*.md'))+list((ROOT/'Root_Axioms').glob('*.md'))\nerrors=[]; ids={}; names={}\nfor p in files:\n d=parse(p)\n if not d: errors.append(f'MISSING_FRONT_MATTER:{p.relative_to(ROOT)}'); continue\n for key in ['node_id','canonical_name','namespace','gate','lifecycle','classification','claim_gate_detail','metadata_standard']:\n  if key not in d: errors.append(f'MISSING_FIELD:{p.relative_to(ROOT)}:{key}')\n if d.get('gate') not in allowed_gates: errors.append(f'BAD_GATE:{p.relative_to(ROOT)}:{d.get("gate")}')\n if d.get('lifecycle') not in allowed_lifecycles: errors.append(f'BAD_LIFECYCLE:{p.relative_to(ROOT)}:{d.get("lifecycle")}')\n nid=d.get('node_id')\n if nid in ids: errors.append(f'DUPLICATE_ID:{nid}:{ids[nid]}:{p}')\n ids[nid]=str(p.relative_to(ROOT)); names.setdefault(d.get('canonical_name'),[]).append(nid)\n\nalias=json.loads((ROOT/'LEGACY_ID_ALIAS_REGISTRY.json').read_text())['aliases']\nresolved={r['legacy_id'] for r in alias}\nactive=[]\nfor base in ['Nodes','Root_Axioms','Books','Android_Body','Musical_Universe','Governance_I_Series']:\n active += list((ROOT/base).rglob('*.md'))\nignore_names={'LEGACY_ID_ALIAS_REGISTRY.md'}\nunresolved={}\nfor p in active:\n if p.name in ignore_names:continue\n text=p.read_text(encoding='utf-8',errors='replace')\n for m in idpat.finditer(text):\n  x=m.group(1)\n  if x not in ids and x not in resolved and not x.startswith('I-0'):\n   unresolved.setdefault(x,[]).append(str(p.relative_to(ROOT)))\nfor x,ps in sorted(unresolved.items()): errors.append(f'UNRESOLVED_ID:{x}:{",".join(sorted(set(ps)))}')\n\n# active governance forks\nif len(list((ROOT/'Governance_I_Series').glob('I-01*.md'))) != 1: errors.append('I01_FORK_REMAINS')\nif len(list((ROOT/'Governance_I_Series').glob('RECONCILIATION_duplex-gates-packet*.md'))) != 1: errors.append('RECONCILIATION_FORK_REMAINS')\n\nbook1=ROOT/'Books/Book1_Micro'\nchapter_files=sorted(book1.glob('Book1_Ch??_*.md'))\nchapter_numbers=[]\nfor p in chapter_files:\n m=re.match(r'Book1_Ch(\\d\\d)_',p.name)\n if m: chapter_numbers.append(int(m.group(1)))\nif chapter_numbers != list(range(1,18)): errors.append(f'BOOK1_SEQUENCE:{chapter_numbers}')\nchapter_map=(book1/'00_CHAPTER_STATUS_MAP.md').read_text()\nfor i in range(1,18):\n if f'| {i:02d} | ACTIVE |' not in chapter_map: errors.append(f'CHAPTER_MAP_MISSING:{i:02d}')\nif 'MISSING' in chapter_map: errors.append('BOOK1_MAP_CONTAINS_MISSING')\n\nproof_index=(ROOT/'Internal_Proofs/00_PROOF_INDEX.md').read_text()\nfor p in (ROOT/'Internal_Proofs').glob('*.md'):\n if p.name!='00_PROOF_INDEX.md' and p.name not in proof_index: errors.append(f'PROOF_INDEX_MISSING:{p.name}')\n\nreport={'pass':not errors,'node_file_count':len(files),'unique_node_ids':len(ids),'gate_counts':{},'lifecycle_counts':{},'unresolved_ids':unresolved,'errors':errors}\nfrom collections import Counter\nreport['gate_counts']=dict(Counter(parse(p).get('gate') for p in files))\nreport['lifecycle_counts']=dict(Counter(parse(p).get('lifecycle') for p in files))\nout=ROOT/'Integrity_Tools/UPDATED_32_integrity_receipt.json'\nout.write_text(json.dumps(report,indent=2),encoding='utf-8')\nprint(json.dumps(report,indent=2))\nsys.exit(0 if report['pass'] else 1)\n'''%(ALLOWED_GATES,ALLOWED_LIFECYCLES)
write(TOOLS/'validate_repository_integrity.py',validator)

# 14. Changelog / handoff placeholders; final metrics added after validator
ch=ROOT/'CHANGELOG.md'; c=read(ch)
entry='''\n## Updated 32 — Repository Integrity Repair\n\n- Established I-06 canonical YAML metadata for every active node and root axiom.\n- Split gate, lifecycle, classification, and claim-detail fields.\n- Conservatively normalized mixed statuses to one node gate without deleting subclaim detail.\n- Disambiguated B-201 Equilibrium Balance and G-709 Regulated-Response Balance.\n- Resolved the I-01 and duplex reconciliation governance forks; historical variants moved under History.\n- Added a title-verified legacy ID alias registry and removed nonexistent F-609/F-610 forward dependencies.\n- Repaired D-02b to E-508 and removed the anonymous E-501 embedded persistence duplicate.\n- Rebuilt Internal_Proofs with a canonical index and moved raw conversational sources to History.\n- Closed the Book 1 numbering gaps by renaming the existing chapters into one continuous Ch1-Ch17 sequence; no chapter prose was invented, deleted, or merged.\n- Moved the unnumbered Neutrino ALT draft out of active Nodes.\n- Regenerated Appendix A-G AI packs and normalized wiki gate/lifecycle banners.\n'''
if '## Updated 32 — Repository Integrity Repair' not in c:c=entry+'\n'+c
write(ch,c)

print('APPLIED')
