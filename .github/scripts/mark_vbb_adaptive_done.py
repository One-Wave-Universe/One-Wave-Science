from pathlib import Path
p=Path('Virtual_Breadboard/SPICE_PARITY.md')
s=p.read_text()
old='17. Adaptive transient timestep with local-error control.'
new="17. **Adaptive transient timestep with local-error control** — IMPLEMENTED in `js/spice-analysis.js` as `adaptiveTransientAnalysis()`. The controller uses backward-Euler step doubling: from the exact same saved circuit state it compares one full step against two half steps, normalizes the resulting voltage/current differences by configurable absolute/relative tolerances, rejects and retries smaller when the error exceeds 1 or either path fails to converge, and retains the two-half-step state only after acceptance. Accepted steps grow conservatively when the local error is small, final time is landed exactly, and rejected trials restore every persisted circuit state including reactive memory, nonlinear decisions, thermal state, noise state, and simulator clock. The original fixed-step transient path remains unchanged. Permanent qualification compares an RC startup against the continuous-time analytic solution including battery resistance, capacitor ESR, and leakage; verifies oversized-step rejection, bounded accepted errors, timestep recovery, tighter-tolerance accuracy, deterministic rollback, and invalid-bound rejection."
if old not in s: raise SystemExit('roadmap anchor missing')
p.write_text(s.replace(old,new,1))
