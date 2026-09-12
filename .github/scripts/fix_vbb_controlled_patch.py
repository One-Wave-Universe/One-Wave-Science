from pathlib import Path
p=Path('.github/scripts/patch_vbb_controlled_sources.py')
s=p.read_text()
start=s.index('# current reporting:')
end=s.index('# AC analyzer support')
replacement=r'''# current reporting: source-family current conventions
rep(p,"""        let I = 0;
        if (c.type === 'resistor') {
""","""        let I = 0;
        if (c.type === 'isource') {
          I = Number(c.value) || 0;
        } else if (c.type === 'vccs') {
          const vp = voltages.get(uf.find(c.controlP)) || 0;
          const vn = voltages.get(uf.find(c.controlN)) || 0;
          I = (Number(c.gain != null ? c.gain : c.value) || 0) * (vp - vn);
        } else if (c.type === 'cccs') {
          const rr = branchRowBySourceId.get(c.controlSourceId);
          I = (Number(c.gain != null ? c.gain : c.value) || 0) * (rr == null ? 0 : (xSol[rr] || 0));
        } else if (c.type === 'vcvs' || c.type === 'ccvs') {
          const rr = branchRowBySourceId.get(c.id);
          I = rr == null ? 0 : (xSol[rr] || 0);
        } else if (c.type === 'resistor') {
""")

'''
p.write_text(s[:start]+replacement+s[end:])
