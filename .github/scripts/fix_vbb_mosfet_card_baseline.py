from pathlib import Path
p=Path('Virtual_Breadboard/js/circuit.js')
s=p.read_text()
old='bodyDiodeVf: 0.7, bodyDiodeRon: 10'
count=s.count(old)
if count != 4:
    raise SystemExit(f'expected 4 body-diode card anchors, found {count}')
s=s.replace(old,'bodyDiodeVf: 0.7, bodyDiodeRon: 5')
p.write_text(s)
