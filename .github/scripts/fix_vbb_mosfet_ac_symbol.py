from pathlib import Path
p=Path('Virtual_Breadboard/js/ac-analysis.js')
s=p.read_text()
old='stampY(A, gate, sourceNode, C(0, omega * spec.ciss));'
if s.count(old) != 1:
    raise SystemExit('AC Ciss symbol anchor not found exactly once')
p.write_text(s.replace(old,'stampY(A, gate, sourceNode, C(0, w * spec.ciss));'))
