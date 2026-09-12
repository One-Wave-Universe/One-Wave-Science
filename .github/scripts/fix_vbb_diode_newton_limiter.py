from pathlib import Path
p=Path('Virtual_Breadboard/js/circuit.js')
s=p.read_text()

def rep(a,b):
    global s
    if a not in s:
        raise SystemExit('missing anchor: '+a[:180])
    s=s.replace(a,b,1)

rep("""      const bjtLimitedJunctions = new Map();
      bjts.forEach((q) => bjtLimitedJunctions.set(q.id, { vbe: 0, vbc: 0 }));
      const reltol = solverOptions && Number.isFinite(solverOptions.reltol) ? Math.max(0, solverOptions.reltol) : 1e-3;
""","""      const bjtLimitedJunctions = new Map();
      bjts.forEach((q) => bjtLimitedJunctions.set(q.id, { vbe: 0, vbc: 0 }));
      // Plain-diode Newton limiting follows the same SPICE-style principle as
      // the BJT junction limiter above: limit only the expansion point, never
      // the final diode equation. This replaces the old permanent 0.8 V
      // exponential clamp, which incorrectly turned the high-forward-bias
      // Shockley curve into a tangent-line extrapolation.
      const diodeLimitedJunctions = new Map();
      diodes.forEach((d) => {
        if (d.type === 'diode' && solverOptions && solverOptions.diodeModel === 'newton') diodeLimitedJunctions.set(d.id, 0);
      });
      const reltol = solverOptions && Number.isFinite(solverOptions.reltol) ? Math.max(0, solverOptions.reltol) : 1e-3;
""")

rep("""        let bjtJunctionLimitsSettled = true;
        // real output/protection clamp diode: same on/off ideal-diode
""","""        let bjtJunctionLimitsSettled = true;
        let diodeJunctionLimitsSettled = true;
        // real output/protection clamp diode: same on/off ideal-diode
""")

old="""            if (diodeModel === 'newton') {
              const i = gi(uf.find(c.a));
              const j = gi(uf.find(c.b));
              const va0 = previousVoltages.get(uf.find(c.a)) || 0;
              const vb0 = previousVoltages.get(uf.find(c.b)) || 0;
              const vdRaw = va0 - vb0;
              const vt = THERMAL_VOLTAGE_25C * ((tempOf(c.id) + 273.15) / 298.15);
              const nvt = DIODE_N * vt;
              const vd = Math.max(-5, Math.min(0.8, vdRaw));
              const ev = Math.exp(vd / nvt);
              const id0 = DIODE_IS * (ev - 1);
              const gd = Math.max(DIODE_IS / nvt, DIODE_IS * ev / nvt);
              const ieq = id0 - gd * vd;
              stampG(i, i, gd); stampG(j, j, gd); stampG(i, j, -gd); stampG(j, i, -gd);
              stampI(i, -ieq); stampI(j, ieq);
"""
new="""            if (diodeModel === 'newton') {
              const i = gi(uf.find(c.a));
              const j = gi(uf.find(c.b));
              const va0 = previousVoltages.get(uf.find(c.a)) || 0;
              const vb0 = previousVoltages.get(uf.find(c.b)) || 0;
              const targetVd = va0 - vb0;
              const lastVd = diodeLimitedJunctions.get(c.id) || 0;
              const maxJunctionStep = 0.05;
              const vd = targetVd > lastVd + maxJunctionStep ? lastVd + maxJunctionStep : targetVd;
              diodeLimitedJunctions.set(c.id, vd);
              const limitTol = vntol + reltol * Math.max(Math.abs(targetVd), Math.abs(vd));
              if (Math.abs(targetVd - vd) > limitTol) diodeJunctionLimitsSettled = false;
              const vt = THERMAL_VOLTAGE_25C * ((tempOf(c.id) + 273.15) / 298.15);
              const nvt = DIODE_N * vt;
              const exponent = Math.max(-100, Math.min(40, vd / nvt));
              const ev = Math.exp(exponent);
              const id0 = DIODE_IS * (ev - 1);
              const gd = Math.max(DIODE_IS / nvt, DIODE_IS * ev / nvt);
              const ieq = id0 - gd * vd;
              stampG(i, i, gd); stampG(j, j, gd); stampG(i, j, -gd); stampG(j, i, -gd);
              stampI(i, -ieq); stampI(j, ieq);
"""
rep(old,new)

rep("""        let changed = !bjtJunctionLimitsSettled;
""","""        let changed = !bjtJunctionLimitsSettled || !diodeJunctionLimitsSettled;
""")

oldcurr="""                const nvt = DIODE_N * vt;
                const vj = Math.max(-5, Math.min(0.8, va - vb));
                precisionCurrents.set('diode:' + d.id, DIODE_IS * (Math.exp(vj / nvt) - 1));
"""
newcurr="""                const nvt = DIODE_N * vt;
                const vj = va - vb;
                const exponent = Math.max(-100, Math.min(40, vj / nvt));
                precisionCurrents.set('diode:' + d.id, DIODE_IS * (Math.exp(exponent) - 1));
"""
if s.count(oldcurr) != 1:
    raise SystemExit('expected one precision-current clamp block, found '+str(s.count(oldcurr)))
s=s.replace(oldcurr,newcurr,1)

rep("""            const nvt = DIODE_N * vt;
            const vd = Math.max(-5, Math.min(0.8, va - vb));
            I = DIODE_IS * (Math.exp(vd / nvt) - 1);
""","""            const nvt = DIODE_N * vt;
            const vd = va - vb;
            const exponent = Math.max(-100, Math.min(40, vd / nvt));
            I = DIODE_IS * (Math.exp(exponent) - 1);
""")

p.write_text(s)
