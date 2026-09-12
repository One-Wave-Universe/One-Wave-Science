from pathlib import Path
p=Path('Virtual_Breadboard/js/circuit.js')
s=p.read_text()
old="""        const stampI = (i, val) => {
          if (i >= 0) b[i] += val;
        };
"""
new="""        const stampI = (i, val) => {
          if (i >= 0) b[i] += val;
        };
        // A limited BJT junction is deliberately NOT yet at the true Newton
        // expansion point. Do not let stable node voltages alone masquerade
        // as convergence while the limiter is still walking toward Vbe/Vbc.
        let bjtJunctionLimitsSettled = true;
"""
if old not in s: raise SystemExit('stale stampI anchor')
s=s.replace(old,new,1)
old="""            const maxJunctionStep = 0.05; // V per nonlinear iteration
            const approach = (target, last) => Math.max(last - maxJunctionStep, Math.min(last + maxJunctionStep, target));
            const vbeLin = approach(targetVbe, limited.vbe);
            const vbcLin = approach(targetVbc, limited.vbc);
            bjtLimitedJunctions.set(c.id, { vbe: vbeLin, vbc: vbcLin });
"""
new="""            const maxJunctionStep = 0.05; // V per nonlinear iteration
            // Only a jump deeper into forward bias needs exponential limiting.
            // Reverse-bias moves are safe to take directly; forcing a -5 V
            // reverse-biased collector junction to crawl in 50 mV steps would
            // waste ~100 iterations without improving numerical safety.
            const approach = (target, last) => target > last + maxJunctionStep ? last + maxJunctionStep : target;
            const vbeLin = approach(targetVbe, limited.vbe);
            const vbcLin = approach(targetVbc, limited.vbc);
            bjtLimitedJunctions.set(c.id, { vbe: vbeLin, vbc: vbcLin });
            const vbeLimitTol = vntol + reltol * Math.max(Math.abs(targetVbe), Math.abs(vbeLin));
            const vbcLimitTol = vntol + reltol * Math.max(Math.abs(targetVbc), Math.abs(vbcLin));
            if (Math.abs(targetVbe - vbeLin) > vbeLimitTol || Math.abs(targetVbc - vbcLin) > vbcLimitTol) {
              bjtJunctionLimitsSettled = false;
            }
"""
if old not in s: raise SystemExit('stale limiter approach anchor')
s=s.replace(old,new,1)
old="""        let changed = false;
"""
new="""        let changed = !bjtJunctionLimitsSettled;
"""
if old not in s: raise SystemExit('stale changed anchor')
s=s.replace(old,new,1)
p.write_text(s)
