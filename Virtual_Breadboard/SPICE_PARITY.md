# Virtual Breadboard — SPICE-parity upgrade ladder

The target is not to replace the breadboard UI with a generic SPICE front end. The target is to keep the physical breadboard editor and progressively make the solver/analysis layer behave like a serious circuit simulator.

## Baseline already present

- Modified Nodal Analysis (MNA)
- partial-pivot linear solve
- GMIN stabilization
- backward-Euler capacitor/inductor transient companions
- nonlinear fixed-point device iteration
- batteries, differential sources, AC time-domain sources
- diodes/LEDs, MOSFET channel + body diode
- real source/internal resistance and current limits
- toroid/mutual-inductance and magnetic-memory models
- netlist/fault diagnostics
- regression and physical-reference test suites

## Upgrade order

### P1 — analysis modes and numerical truth

1. **DC source sweep (`.dc`-class)** — IMPLEMENTED on this branch in `js/spice-analysis.js`.
2. **Convergence report** — every solve must report iteration count, converged/not-converged, and a numerical residual/tolerance result. Hitting the iteration ceiling must be a named solver failure, never a silent answer.
3. **True DC operating point (`.op`-class)** — capacitors open at DC, inductors use their DC path, independent transient history must not be required to obtain the operating point.
4. **Source stepping / GMIN stepping** — hard nonlinear circuits should be approached gradually instead of only retrying the same fixed point.

### P2 — nonlinear device quality

5. **Continuous diode equation + Newton linearization** — replace the constant-drop on/off diode model for precision work while retaining the simple model as an optional fast mode.
6. **Continuous MOSFET I-V model** — cutoff / triode / saturation rather than threshold + fixed RDS(on) only; preserve explicit body diode and parasitics.
7. **Convergence tolerances** — RELTOL / VNTOL / ABSTOL-style voltage-current criteria rather than state flips alone.

### P3 — frequency-domain analysis

8. **Small-signal AC analysis (`.ac`-class)** — linearize around the DC operating point and solve complex admittance versus frequency.
9. **Bode output** — magnitude/phase probes and transfer-function plotting.
10. **Pole/zero sanity checks** for simple RC/RL/RLC networks against analytic answers.

### P4 — sources, controlled elements, and model coverage

11. Current sources and controlled sources (VCCS/VCVS/CCCS/CCVS).
12. BJT support.
13. Better MOSFET parameter sets / model cards.
14. Piecewise-linear and pulse sources for repeatable transient tests.
15. Initial conditions and startup/uic-like behavior.

### P5 — solver robustness/performance

16. Sparse matrix representation and factorization for large breadboards.
17. Adaptive transient timestep with local-error control.
18. Trapezoidal/Gear integration choices with ringing/stiffness tests.
19. Deterministic convergence diagnostics: worst node/branch residual and reason for failure.
20. Cross-check suite against ngspice for ordinary reference circuits, with tolerances declared per analysis/device model.

## Acceptance rule

No feature is considered SPICE-grade because the waveform looks right. Every analysis mode gets at least one independent analytic reference circuit and, where appropriate, an ngspice comparison. Existing One-Wave-specific hardware primitives stay above the generic electrical solver; they do not get hard-coded into the MNA mathematics.
