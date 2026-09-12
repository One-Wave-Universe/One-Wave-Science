from pathlib import Path
p=Path('Virtual_Breadboard/js/circuit.js')
s=p.read_text()
old="""            });
           else if (c.type === 'nmos' || c.type === 'pmos') {
"""
new="""            });
          } else if (c.type === 'nmos' || c.type === 'pmos') {
"""
if old not in s: raise SystemExit('stale BJT splice anchor')
p.write_text(s.replace(old,new,1))
