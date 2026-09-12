from pathlib import Path


def rep(path, old, new):
    p=Path(path); s=p.read_text()
    if old not in s:
        raise SystemExit(f'stale anchor in {path}: {old[:80]!r}')
    p.write_text(s.replace(old,new,1))

p='Virtual_Breadboard/js/circuit.js'
rep(p,"""      if (c.type === 'nmos' || c.type === 'pmos') { uf.find(c.gate); uf.find(c.drain); uf.find(c.source); }
""","""      if (c.type === 'nmos' || c.type === 'pmos') { uf.find(c.gate); uf.find(c.drain); uf.find(c.source); }
      if (c.type === 'vccs' || c.type === 'vcvs') { uf.find(c.controlP); uf.find(c.controlN); }
""")
rep(p,"""        case 'battery': case 'diffsource':
          add(c.a, c.b);
          break;
""","""        case 'battery': case 'diffsource': case 'vcvs': case 'ccvs':
          add(c.a, c.b);
          break;
        case 'isource': case 'vccs': case 'cccs':
          // ideal current sources do not create a passive DC-conductive path
          break;
""")
rep(p,"""      const schmitts = components.filter((c) => c.type === 'schmitt');
""","""      const schmitts = components.filter((c) => c.type === 'schmitt');
      const controlledVoltageSources = components.filter((c) => c.type === 'vcvs' || c.type === 'ccvs');
""")
rep(p,"""        if (c.type === 'nmos' || c.type === 'pmos') { touch(c.gate); touch(c.drain); touch(c.source); }
""","""        if (c.type === 'nmos' || c.type === 'pmos') { touch(c.gate); touch(c.drain); touch(c.source); }
        if (c.type === 'vccs' || c.type === 'vcvs') { touch(c.controlP); touch(c.controlN); }
""")
rep(p,"""      const nMemCoreRows = memoryCores.reduce((s, mc) => s + mc.windings.length, 0);
      const memCoreRowBase = toroidRowBase + nToroidRows;
""","""      const nMemCoreRows = memoryCores.reduce((s, mc) => s + mc.windings.length, 0);
      const memCoreRowBase = toroidRowBase + nToroidRows;
""")
rep(p,"""      const rowMemCore = (mcK, windingIdx) => memCoreRowOffsets[mcK] + windingIdx;
      const size = memCoreRowBase + nMemCoreRows;

      const gi = (rt) => (rt === groundRoot ? -1 : nodeIndex.get(rt));
""","""      const rowMemCore = (mcK, windingIdx) => memCoreRowOffsets[mcK] + windingIdx;
      const ctrlVRowBase = memCoreRowBase + nMemCoreRows;
      const rowCtrlV = (k) => ctrlVRowBase + k;
      const size = ctrlVRowBase + controlledVoltageSources.length;

      const gi = (rt) => (rt === groundRoot ? -1 : nodeIndex.get(rt));
      const branchRowBySourceId = new Map();
      batteries.forEach((c,k)=>branchRowBySourceId.set(c.id,rowBat(k)));
      acsources.forEach((c,k)=>branchRowBySourceId.set(c.id,rowAc(k)));
      controlledVoltageSources.forEach((c,k)=>branchRowBySourceId.set(c.id,rowCtrlV(k)));
""")
rep(p,"""          } else if (c.type === 'battery' || c.type === 'diffsource') {
""","""          } else if (c.type === 'isource') {
            const ia = gi(uf.find(c.a));
            const ib = gi(uf.find(c.b));
            const I = Number(c.value) || 0;
            stampI(ia, -I);
            stampI(ib, I);
          } else if (c.type === 'vccs') {
            const ia = gi(uf.find(c.a)), ib = gi(uf.find(c.b));
            const cp = gi(uf.find(c.controlP)), cn = gi(uf.find(c.controlN));
            const g = Number(c.gain != null ? c.gain : c.value) || 0;
            if (ia >= 0 && cp >= 0) A[ia][cp] += g;
            if (ia >= 0 && cn >= 0) A[ia][cn] -= g;
            if (ib >= 0 && cp >= 0) A[ib][cp] -= g;
            if (ib >= 0 && cn >= 0) A[ib][cn] += g;
          } else if (c.type === 'cccs') {
            const ctrlRow = branchRowBySourceId.get(c.controlSourceId);
            if (ctrlRow == null) throw new Error(`CCCS ${c.id} controlSourceId '${c.controlSourceId}' is not a voltage-source branch`);
            const ia = gi(uf.find(c.a)), ib = gi(uf.find(c.b));
            const gain = Number(c.gain != null ? c.gain : c.value) || 0;
            if (ia >= 0) A[ia][ctrlRow] += gain;
            if (ib >= 0) A[ib][ctrlRow] -= gain;
          } else if (c.type === 'battery' || c.type === 'diffsource') {
""")
rep(p,"""        // rail-splitter constraint: V(internal) = 0.5*(V(a) + V(b)), an
""","""        controlledVoltageSources.forEach((src, k) => {
          const row = rowCtrlV(k);
          const ia = gi(uf.find(src.a)), ib = gi(uf.find(src.b));
          if (ia >= 0) { A[ia][row] += 1; A[row][ia] += 1; }
          if (ib >= 0) { A[ib][row] -= 1; A[row][ib] -= 1; }
          const gain = Number(src.gain != null ? src.gain : src.value) || 0;
          if (src.type === 'vcvs') {
            const cp = gi(uf.find(src.controlP)), cn = gi(uf.find(src.controlN));
            if (cp >= 0) A[row][cp] -= gain;
            if (cn >= 0) A[row][cn] += gain;
          } else {
            const ctrlRow = branchRowBySourceId.get(src.controlSourceId);
            if (ctrlRow == null || ctrlRow === row) throw new Error(`CCVS ${src.id} controlSourceId '${src.controlSourceId}' is not a distinct voltage-source branch`);
            A[row][ctrlRow] -= gain;
          }
        });

        // rail-splitter constraint: V(internal) = 0.5*(V(a) + V(b)), an
""")
# current reporting: add source family results before thermal block marker
rep(p,"""      // persist capacitor and inductor states for the next real frame
""","""      components.forEach((c) => {
        if (c.type === 'isource') currents.set(c.id, Number(c.value) || 0);
        else if (c.type === 'vccs') {
          const vp = voltages.get(uf.find(c.controlP)) || 0;
          const vn = voltages.get(uf.find(c.controlN)) || 0;
          currents.set(c.id, (Number(c.gain != null ? c.gain : c.value) || 0) * (vp - vn));
        } else if (c.type === 'cccs') {
          const rr = branchRowBySourceId.get(c.controlSourceId);
          currents.set(c.id, (Number(c.gain != null ? c.gain : c.value) || 0) * (rr == null ? 0 : (xSol[rr] || 0)));
        } else if (c.type === 'vcvs' || c.type === 'ccvs') {
          const rr = branchRowBySourceId.get(c.id);
          currents.set(c.id, rr == null ? 0 : (xSol[rr] || 0));
        }
      });

      // persist capacitor and inductor states for the next real frame
""")

# AC analyzer support
p='Virtual_Breadboard/js/ac-analysis.js'
rep(p,"""  const source = components.find((c) => c.id === sourceId);
  if (!source) throw new Error(`AC source '${sourceId}' was not found`);
  if (!['battery', 'diffsource', 'acsource'].includes(source.type)) {
    throw new Error(`AC source '${sourceId}' must be battery, diffsource, or acsource`);
  }

  const supported = new Set(['resistor', 'capacitor', 'inductor', 'battery', 'diffsource', 'acsource', 'diode', 'led', 'nmos', 'pmos', 'switch', 'pushbutton']);
""","""  const source = components.find((c) => c.id === sourceId);
  if (!source) throw new Error(`AC source '${sourceId}' was not found`);
  if (!['battery', 'diffsource', 'acsource', 'isource'].includes(source.type)) {
    throw new Error(`AC source '${sourceId}' must be battery, diffsource, acsource, or isource`);
  }

  const supported = new Set(['resistor', 'capacitor', 'inductor', 'battery', 'diffsource', 'acsource', 'isource', 'vccs', 'vcvs', 'cccs', 'ccvs', 'diode', 'led', 'nmos', 'pmos', 'switch', 'pushbutton']);
""")
rep(p,"""  const voltageSources = components.filter((c) => ['battery', 'diffsource', 'acsource'].includes(c.type));
""","""  const voltageSources = components.filter((c) => ['battery', 'diffsource', 'acsource', 'vcvs', 'ccvs'].includes(c.type));
""")
rep(p,"""    components.forEach((c) => {
      const a = idx(c.a);
      const bb = idx(c.b);
      if (c.type === 'resistor') {
""","""    const sourceRowById = new Map(voltageSources.map((s,k)=>[s.id,rowSource(k)]));
    components.forEach((c) => {
      const a = idx(c.a);
      const bb = idx(c.b);
      if (c.type === 'isource') {
        if (c.id === sourceId) {
          const iz = polar(magnitude, phaseDeg);
          if (a >= 0) b[a] = sub(b[a], iz);
          if (bb >= 0) b[bb] = add(b[bb], iz);
        }
      } else if (c.type === 'vccs') {
        const cp=idx(c.controlP), cn=idx(c.controlN), g=Number(c.gain != null ? c.gain : c.value)||0;
        if (a>=0&&cp>=0) A[a][cp]=add(A[a][cp],C(g,0));
        if (a>=0&&cn>=0) A[a][cn]=sub(A[a][cn],C(g,0));
        if (bb>=0&&cp>=0) A[bb][cp]=sub(A[bb][cp],C(g,0));
        if (bb>=0&&cn>=0) A[bb][cn]=add(A[bb][cn],C(g,0));
      } else if (c.type === 'cccs') {
        const cr=sourceRowById.get(c.controlSourceId), gain=Number(c.gain != null ? c.gain : c.value)||0;
        if (cr == null) throw new Error(`CCCS ${c.id} controlSourceId '${c.controlSourceId}' is not a voltage-source branch`);
        if (a>=0) A[a][cr]=add(A[a][cr],C(gain,0));
        if (bb>=0) A[bb][cr]=sub(A[bb][cr],C(gain,0));
      } else if (c.type === 'resistor') {
""")
rep(p,"""    voltageSources.forEach((s, k) => {
      const internal = idx(sourceInternal.get(s.id));
      const a = idx(s.a);
      const ref = idx(s.b);
      stampY(A, internal, a, C(1 / Math.max(sourceResistance(s), 1e-12), 0));
      const row = rowSource(k);
      if (internal >= 0) { A[internal][row] = add(A[internal][row], C(1, 0)); A[row][internal] = add(A[row][internal], C(1, 0)); }
      if (ref >= 0) { A[ref][row] = sub(A[ref][row], C(1, 0)); A[row][ref] = sub(A[row][ref], C(1, 0)); }
      if (s.id === sourceId) b[row] = add(b[row], polar(magnitude, phaseDeg));
    });
""","""    voltageSources.forEach((s, k) => {
      const row = rowSource(k);
      const a = idx(s.a), ref = idx(s.b);
      if (s.type === 'vcvs' || s.type === 'ccvs') {
        if (a >= 0) { A[a][row]=add(A[a][row],C(1,0)); A[row][a]=add(A[row][a],C(1,0)); }
        if (ref >= 0) { A[ref][row]=sub(A[ref][row],C(1,0)); A[row][ref]=sub(A[row][ref],C(1,0)); }
        const gain=Number(s.gain != null ? s.gain : s.value)||0;
        if (s.type === 'vcvs') {
          const cp=idx(s.controlP), cn=idx(s.controlN);
          if (cp>=0) A[row][cp]=sub(A[row][cp],C(gain,0));
          if (cn>=0) A[row][cn]=add(A[row][cn],C(gain,0));
        } else {
          const cr=sourceRowById.get(s.controlSourceId);
          if (cr == null || cr === row) throw new Error(`CCVS ${s.id} controlSourceId '${s.controlSourceId}' is not a distinct voltage-source branch`);
          A[row][cr]=sub(A[row][cr],C(gain,0));
        }
      } else {
        const internal = idx(sourceInternal.get(s.id));
        stampY(A, internal, a, C(1 / Math.max(sourceResistance(s), 1e-12), 0));
        if (internal >= 0) { A[internal][row] = add(A[internal][row], C(1, 0)); A[row][internal] = add(A[row][internal], C(1, 0)); }
        if (ref >= 0) { A[ref][row] = sub(A[ref][row], C(1, 0)); A[row][ref] = sub(A[row][ref], C(1, 0)); }
        if (s.id === sourceId) b[row] = add(b[row], polar(magnitude, phaseDeg));
      }
    });
""")
# avoid internal nodes for controlled voltage sources
rep(p,"""  voltageSources.forEach((c) => {
    const name = `__acsmall__${c.id}`;
    uf.find(name);
    sourceInternal.set(c.id, name);
  });
""","""  voltageSources.forEach((c) => {
    if (c.type === 'vcvs' || c.type === 'ccvs') return;
    const name = `__acsmall__${c.id}`;
    uf.find(name);
    sourceInternal.set(c.id, name);
  });
""")
rep(p,"""  sourceInternal.forEach((n) => touch(n));
""","""  sourceInternal.forEach((n) => touch(n));
  components.forEach((c) => { if (c.type === 'vccs' || c.type === 'vcvs') { touch(c.controlP); touch(c.controlN); } });
""")
# sourceResistance only called for actual independent voltage sources now, okay.

# docs package/workflow later by direct APIs
