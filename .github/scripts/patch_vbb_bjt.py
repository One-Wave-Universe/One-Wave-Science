from pathlib import Path
import re

CIR=Path('Virtual_Breadboard/js/circuit.js')
AC=Path('Virtual_Breadboard/js/ac-analysis.js')


def once(s, old, new, name):
    if old not in s:
        raise SystemExit(f'stale anchor: {name}')
    return s.replace(old, new, 1)

s=CIR.read_text()

# Basic Ebers-Moll defaults: deliberately first-order, continuous, and symmetric enough
# to represent NPN/PNP cutoff, forward active, saturation, and reverse operation without
# pretending to be a full Gummel-Poon/model-card implementation.
s=once(s,
"  const THERMAL_VOLTAGE_25C = 0.025852; // V = kT/q at 25 C\n",
"  const THERMAL_VOLTAGE_25C = 0.025852; // V = kT/q at 25 C\n  const BJT_IS = 1e-15; // A, generic small-signal silicon transistor transport saturation current\n  const BJT_BETA_F = 100; // forward common-emitter current gain\n  const BJT_BETA_R = 1; // reverse gain is intentionally much smaller than forward gain\n  const BJT_NF = 1.0; // forward junction emission coefficient\n  const BJT_NR = 1.0; // reverse junction emission coefficient\n",
'bjt constants')

helper_anchor="""    return { id, gm, gdd, gss, ieq: id - gm * vg - gdd * vd - gss * vs };
  }

  // Real TLV3202 dual comparator"""
helper_new="""    return { id, gm, gdd, gss, ieq: id - gm * vg - gdd * vd - gss * vs };
  }

  function bjtSpec(c) {
    const betaF = Math.max(1e-6, Number(c.betaF != null ? c.betaF : c.bf != null ? c.bf : BJT_BETA_F));
    const betaR = Math.max(1e-6, Number(c.betaR != null ? c.betaR : c.br != null ? c.br : BJT_BETA_R));
    return {
      is: Math.max(1e-30, Number(c.is != null ? c.is : BJT_IS)),
      betaF,
      betaR,
      alphaF: betaF / (betaF + 1),
      alphaR: betaR / (betaR + 1),
      nf: Math.max(0.1, Number(c.nf != null ? c.nf : BJT_NF)),
      nr: Math.max(0.1, Number(c.nr != null ? c.nr : BJT_NR)),
    };
  }

  function bjtCurrents(c, vb, vc, ve, tempC) {
    const spec = bjtSpec(c);
    const p = c.type === 'pnp' ? -1 : 1;
    const vt = THERMAL_VOLTAGE_25C * (((Number.isFinite(tempC) ? tempC : 25) + 273.15) / 298.15);
    const vbe = p * (vb - ve);
    const vbc = p * (vb - vc);
    const ebe = Math.exp(Math.max(-80, Math.min(40, vbe / (spec.nf * vt))));
    const ebc = Math.exp(Math.max(-80, Math.min(40, vbc / (spec.nr * vt))));
    const iF = spec.is * (ebe - 1);
    const iR = spec.is * (ebc - 1);
    const icN = spec.alphaF * iF - iR;
    const ieN = -iF + spec.alphaR * iR;
    const ibN = -(icN + ieN);
    return { collector: p * icN, base: p * ibN, emitter: p * ieN };
  }

  function bjtLinearization(c, vb, vc, ve, tempC) {
    const h = 1e-5;
    const base = bjtCurrents(c, vb, vc, ve, tempC);
    const vars = [vb, vc, ve];
    const names = ['base', 'collector', 'emitter'];
    const jacobian = {};
    const ieq = {};
    names.forEach((terminal) => { jacobian[terminal] = [0, 0, 0]; });
    for (let k = 0; k < 3; k++) {
      const plus = vars.slice(); plus[k] += h;
      const minus = vars.slice(); minus[k] -= h;
      const ip = bjtCurrents(c, plus[0], plus[1], plus[2], tempC);
      const im = bjtCurrents(c, minus[0], minus[1], minus[2], tempC);
      names.forEach((terminal) => { jacobian[terminal][k] = (ip[terminal] - im[terminal]) / (2 * h); });
    }
    names.forEach((terminal) => {
      const g = jacobian[terminal];
      ieq[terminal] = base[terminal] - g[0] * vb - g[1] * vc - g[2] * ve;
    });
    return { currents: base, jacobian, ieq };
  }

  // Real TLV3202 dual comparator"""
s=once(s, helper_anchor, helper_new, 'bjt helpers')

# Topology registration.
s=once(s,
"      if (c.type === 'nmos' || c.type === 'pmos') { uf.find(c.gate); uf.find(c.drain); uf.find(c.source); }\n",
"      if (c.type === 'nmos' || c.type === 'pmos') { uf.find(c.gate); uf.find(c.drain); uf.find(c.source); }\n      if (c.type === 'npn' || c.type === 'pnp') { uf.find(c.base); uf.find(c.collector); uf.find(c.emitter); }\n",
'topology bjt pins')

# DC reachability: the two PN junctions are real semiconductor paths.
edge_pat=re.compile(r"(        case 'nmos': case 'pmos':\n(?:.*\n){0,8}?          add\(c\.drain, c\.source\);\n          break;\n)")
m=edge_pat.search(s)
if not m: raise SystemExit('stale anchor: realDcEdges mosfet block')
s=s[:m.end()] + "        case 'npn': case 'pnp':\n          add(c.base, c.emitter);\n          add(c.base, c.collector);\n          break;\n" + s[m.end():]

s=once(s,
"      const mosfets = components.filter((c) => c.type === 'nmos' || c.type === 'pmos');\n",
"      const mosfets = components.filter((c) => c.type === 'nmos' || c.type === 'pmos');\n      const bjts = components.filter((c) => c.type === 'npn' || c.type === 'pnp');\n",
'bjt list')

# Solve-time node/touch registration. Match the special MOSFET touch clause, not topology.
touch_pat=re.compile(r"(\s*if \(c\.type === 'nmos' \|\| c\.type === 'pmos'\)\s*\{[^\n{}]*touch\(c\.gate\)[^\n{}]*touch\(c\.drain\)[^\n{}]*touch\(c\.source\)[^\n{}]*\}\n)")
m=touch_pat.search(s)
if not m: raise SystemExit('stale anchor: solve touch mosfet pins')
indent=re.match(r"\s*",m.group(1)).group(0)
s=s[:m.end()] + indent + "if (c.type === 'npn' || c.type === 'pnp') { touch(c.base); touch(c.collector); touch(c.emitter); }\n" + s[m.end():]

# Insert BJT Newton stamp immediately before the MOSFET stamp branch that owns the
# continuous-channel Jacobian.
needle='// Newton Jacobian for drain->source channel current Id(Vg,Vd,Vs).'
pos=s.index(needle)
branch="} else if (c.type === 'nmos' || c.type === 'pmos') {"
start=s.rfind(branch,0,pos)
if start < 0: raise SystemExit('stale anchor: mosfet stamp branch')
bjt_stamp="""} else if (c.type === 'npn' || c.type === 'pnp') {
            const b_ = gi(uf.find(c.base));
            const c_ = gi(uf.find(c.collector));
            const e_ = gi(uf.find(c.emitter));
            const vb0 = previousVoltages.get(uf.find(c.base)) || 0;
            const vc0 = previousVoltages.get(uf.find(c.collector)) || 0;
            const ve0 = previousVoltages.get(uf.find(c.emitter)) || 0;
            const lin = bjtLinearization(c, vb0, vc0, ve0, tempOf(c.id));
            const cols = [b_, c_, e_];
            [['base', b_], ['collector', c_], ['emitter', e_]].forEach(([terminal, row]) => {
              const g = lin.jacobian[terminal];
              cols.forEach((col, k) => { if (row >= 0 && col >= 0) stampG(row, col, g[k]); });
              if (row >= 0) stampI(row, -lin.ieq[terminal]);
            });
          """
s=s[:start]+bjt_stamp+s[start+1:]

# BJT is always a precision nonlinear model, so it participates in shared RELTOL/VNTOL/ABSTOL checks.
s=once(s,
"      const precisionConvergenceActive = !!(solverOptions && (solverOptions.diodeModel === 'newton' || solverOptions.mosfetModel === 'continuous'));\n",
"      const precisionConvergenceActive = bjts.length > 0 || !!(solverOptions && (solverOptions.diodeModel === 'newton' || solverOptions.mosfetModel === 'continuous'));\n",
'precision active')

bjt_precision="""            bjts.forEach((q) => {
              const vb = voltages.get(uf.find(q.base)) || 0;
              const vc = voltages.get(uf.find(q.collector)) || 0;
              const ve = voltages.get(uf.find(q.emitter)) || 0;
              const iq = bjtCurrents(q, vb, vc, ve, tempOf(q.id));
              precisionCurrents.set('bjt:' + q.id + ':collector', iq.collector);
              precisionCurrents.set('bjt:' + q.id + ':base', iq.base);
              precisionCurrents.set('bjt:' + q.id + ':emitter', iq.emitter);
            });
"""
s=once(s,
"            precisionCurrents.forEach((now, key) => {\n",
bjt_precision+"            precisionCurrents.forEach((now, key) => {\n",
'bjt precision currents')

bjt_seed="""            bjts.forEach((q) => {
              const vb = voltages.get(uf.find(q.base)) || 0;
              const vc = voltages.get(uf.find(q.collector)) || 0;
              const ve = voltages.get(uf.find(q.emitter)) || 0;
              const iq = bjtCurrents(q, vb, vc, ve, tempOf(q.id));
              seedCurrents.set('bjt:' + q.id + ':collector', iq.collector);
              seedCurrents.set('bjt:' + q.id + ':base', iq.base);
              seedCurrents.set('bjt:' + q.id + ':emitter', iq.emitter);
            });
"""
s=once(s,
"            previousPrecisionCurrents = seedCurrents;\n",
bjt_seed+"            previousPrecisionCurrents = seedCurrents;\n",
'bjt seed currents')

# Report all three terminal currents; plain id aliases collector current.
report_marker='// total conventional current from drain to source: the channel'
pos=s.index(report_marker)
start=s.rfind(branch,0,pos)
if start < 0: raise SystemExit('stale anchor: mosfet current report branch')
bjt_report="""} else if (c.type === 'npn' || c.type === 'pnp') {
          const vb = voltages.get(uf.find(c.base)) || 0;
          const vc = voltages.get(uf.find(c.collector)) || 0;
          const ve = voltages.get(uf.find(c.emitter)) || 0;
          const iq = bjtCurrents(c, vb, vc, ve, tempOf(c.id));
          I = iq.collector;
          currents.set(c.id + ':collector', iq.collector);
          currents.set(c.id + ':base', iq.base);
          currents.set(c.id + ':emitter', iq.emitter);
        """
s=s[:start]+bjt_report+s[start+1:]

# Export the model so AC analysis and independent tests use the exact same equations.
s=once(s,
"    Circuit, UnionFind, solveLinear, LED_VF, LED_RON, LED_WALLPLUG_EFFICIENCY, ledLightOutputW, DIODE_VF, DIODE_RON, DIODE_IS, DIODE_N, THERMAL_VOLTAGE_25C, BATTERY_RINT, VGND_RINT,\n",
"    Circuit, UnionFind, solveLinear, LED_VF, LED_RON, LED_WALLPLUG_EFFICIENCY, ledLightOutputW, DIODE_VF, DIODE_RON, DIODE_IS, DIODE_N, THERMAL_VOLTAGE_25C, BJT_IS, BJT_BETA_F, BJT_BETA_R, BJT_NF, BJT_NR, bjtSpec, bjtCurrents, bjtLinearization, BATTERY_RINT, VGND_RINT,\n",
'bjt exports')

CIR.write_text(s)

# AC support: same operating-point model, same Jacobian.
a=AC.read_text()
a=once(a,
"  mosfetChannelCurrent, MOSFET_OFF_LEAKAGE_G,\n",
"  mosfetChannelCurrent, MOSFET_OFF_LEAKAGE_G, bjtLinearization,\n",
'ac bjt import')
a=once(a,
"  const supported = new Set(['resistor', 'capacitor', 'inductor', 'battery', 'diffsource', 'acsource', 'isource', 'vccs', 'vcvs', 'cccs', 'ccvs', 'diode', 'led', 'nmos', 'pmos', 'switch', 'pushbutton']);\n",
"  const supported = new Set(['resistor', 'capacitor', 'inductor', 'battery', 'diffsource', 'acsource', 'isource', 'vccs', 'vcvs', 'cccs', 'ccvs', 'diode', 'led', 'nmos', 'pmos', 'npn', 'pnp', 'switch', 'pushbutton']);\n",
'ac supported bjts')
a=once(a,
"    if (c.type === 'nmos' || c.type === 'pmos') { collectNode(c.gate); collectNode(c.drain); collectNode(c.source); }\n",
"    if (c.type === 'nmos' || c.type === 'pmos') { collectNode(c.gate); collectNode(c.drain); collectNode(c.source); }\n    if (c.type === 'npn' || c.type === 'pnp') { collectNode(c.base); collectNode(c.collector); collectNode(c.emitter); }\n",
'ac named bjt nodes')
a=once(a,
"    if (c.type === 'nmos' || c.type === 'pmos') { touch(c.gate); touch(c.drain); touch(c.source); }\n",
"    if (c.type === 'nmos' || c.type === 'pmos') { touch(c.gate); touch(c.drain); touch(c.source); }\n    if (c.type === 'npn' || c.type === 'pnp') { touch(c.base); touch(c.collector); touch(c.emitter); }\n",
'ac touch bjt nodes')

# Add BJT small-signal terminal Jacobian before MOSFET AC branch.
ac_branch="} else if (c.type === 'nmos' || c.type === 'pmos') {"
pos=a.index(ac_branch)
bjt_ac="""} else if (c.type === 'npn' || c.type === 'pnp') {
        const bq = idx(c.base), cq = idx(c.collector), eq = idx(c.emitter);
        const lin = bjtLinearization(c, opV(c.base), opV(c.collector), opV(c.emitter), ambientC);
        const cols = [bq, cq, eq];
        [['base', bq], ['collector', cq], ['emitter', eq]].forEach(([terminal, row]) => {
          if (row < 0) return;
          lin.jacobian[terminal].forEach((g, k) => { if (cols[k] >= 0) A[row][cols[k]] = add(A[row][cols[k]], C(g, 0)); });
        });
      """
a=a[:pos]+bjt_ac+a[pos+1:]
AC.write_text(a)
