from pathlib import Path
p=Path('Virtual_Breadboard/js/circuit.js')
s=p.read_text()
old="""      let previousSolution = null;
      let previousPrecisionCurrents = new Map();
"""
new="""      let previousSolution = null;
      let previousPrecisionCurrents = new Map();
      // Per-solve PN-junction limiting for BJT Newton continuation. A hard-driven
      // saturated transistor can otherwise jump from an off-state linearization
      // straight into decades of exponential junction current. Limiting only the
      // linearization point (not the final device equation) walks Vbe/Vbc toward
      // the solved node voltages in bounded increments, the same numerical idea
      // used by classic SPICE pnjlim-style junction limiting.
      const bjtLimitedJunctions = new Map();
      bjts.forEach((q) => bjtLimitedJunctions.set(q.id, { vbe: 0, vbc: 0 }));
"""
if old not in s: raise SystemExit('stale BJT limiter state anchor')
s=s.replace(old,new,1)
old="""            const vb0 = previousVoltages.get(uf.find(c.base)) || 0;
            const vc0 = previousVoltages.get(uf.find(c.collector)) || 0;
            const ve0 = previousVoltages.get(uf.find(c.emitter)) || 0;
            const lin = bjtLinearization(c, vb0, vc0, ve0, tempOf(c.id));
"""
new="""            const vb0 = previousVoltages.get(uf.find(c.base)) || 0;
            const vc0 = previousVoltages.get(uf.find(c.collector)) || 0;
            const ve0 = previousVoltages.get(uf.find(c.emitter)) || 0;
            const polarity = c.type === 'pnp' ? -1 : 1;
            const targetVbe = polarity * (vb0 - ve0);
            const targetVbc = polarity * (vb0 - vc0);
            const limited = bjtLimitedJunctions.get(c.id) || { vbe: 0, vbc: 0 };
            const maxJunctionStep = 0.05; // V per nonlinear iteration
            const approach = (target, last) => Math.max(last - maxJunctionStep, Math.min(last + maxJunctionStep, target));
            const vbeLin = approach(targetVbe, limited.vbe);
            const vbcLin = approach(targetVbc, limited.vbc);
            bjtLimitedJunctions.set(c.id, { vbe: vbeLin, vbc: vbcLin });
            // Reconstruct an equivalent terminal point carrying the limited
            // junction voltages; the stamped tangent is still a full 3-terminal
            // Ebers-Moll Jacobian and converges to the actual node voltages once
            // the limiter catches up.
            const veLin = ve0;
            const vbLin = veLin + polarity * vbeLin;
            const vcLin = vbLin - polarity * vbcLin;
            const lin = bjtLinearization(c, vbLin, vcLin, veLin, tempOf(c.id));
"""
if old not in s: raise SystemExit('stale BJT Newton stamp anchor')
p.write_text(s.replace(old,new,1))
