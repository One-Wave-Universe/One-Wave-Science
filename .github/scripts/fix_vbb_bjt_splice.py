from pathlib import Path
p=Path('Virtual_Breadboard/js/circuit.js')
s=p.read_text()
old="""          currents.set(c.id + ':emitter', iq.emitter);
         else if (c.type === 'nmos' || c.type === 'pmos') {
"""
new="""          currents.set(c.id + ':emitter', iq.emitter);
        } else if (c.type === 'nmos' || c.type === 'pmos') {
"""
if old not in s: raise SystemExit('stale BJT current-report splice anchor')
p.write_text(s.replace(old,new,1))
