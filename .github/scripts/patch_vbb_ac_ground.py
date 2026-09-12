from pathlib import Path
p=Path('Virtual_Breadboard/js/ac-analysis.js')
s=p.read_text()
old="""  let groundRoot = null;
  const dcSources = components.filter((c) => c.type === 'battery' || c.type === 'diffsource');
  if (dcSources.length) groundRoot = uf.find(dcSources[0].b);
  else if (wires.length) groundRoot = uf.find(wires[0].a);
  else if (components.length) groundRoot = uf.find(components[0].b != null ? components[0].b : components[0].a);
  if (groundRoot == null) throw new Error('AC analysis needs a circuit reference node');
"""
new="""  let groundRoot = null;
  const dcSources = components.filter((c) => c.type === 'battery' || c.type === 'diffsource');
  const namedNodes = [];
  const collectNode = (n) => { if (typeof n === 'string') namedNodes.push(n); };
  wires.forEach((w) => { collectNode(w.a); collectNode(w.b); });
  components.forEach((c) => {
    collectNode(c.a); collectNode(c.b); collectNode(c.controlP); collectNode(c.controlN);
    if (c.type === 'nmos' || c.type === 'pmos') { collectNode(c.gate); collectNode(c.drain); collectNode(c.source); }
  });
  const explicitGround = namedNodes.find((n) => /^(gnd|ground|0)$/i.test(n));
  if (explicitGround != null) groundRoot = uf.find(explicitGround);
  else if (dcSources.length) groundRoot = uf.find(dcSources[0].b);
  else if (wires.length) groundRoot = uf.find(wires[0].a);
  else if (components.length) groundRoot = uf.find(components[0].b != null ? components[0].b : components[0].a);
  if (groundRoot == null) throw new Error('AC analysis needs a circuit reference node');
"""
if old not in s: raise SystemExit('stale AC ground anchor')
p.write_text(s.replace(old,new,1))
