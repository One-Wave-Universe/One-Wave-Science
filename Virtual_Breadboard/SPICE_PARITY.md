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

1. **DC source sweep (`.dc`-class)** — IMPLEMENTED in `js/spice-analysis.js`.
2. **Convergence report** — IMPLEMENTED. Every nonlinear solve reports iteration count, state stability, numerical residual/tolerance, and converged/not-converged; iteration-ceiling failure is named `SOLVER FAILED`.
3. **True DC operating point (`.op`-class)** — IMPLEMENTED in `js/spice-analysis.js`. Capacitors are open at DC, inductors retain their declared winding DCR with no reactive term, and every `.op` solve uses fresh solver state so transient history is not required.
4. **Source stepping / GMIN stepping** — IMPLEMENTED. `steppedOperatingPoint()` ramps independent DC sources from zero to full value while carrying nonlinear device state forward, then reduces configurable solver GMIN back to the normal target. The final answer is accepted only at full source values and target GMIN.

### P2 — nonlinear device quality

5. **Continuous diode equation + Newton linearization** — IMPLEMENTED as opt-in `solverOptions.diodeModel = 'newton'`. Plain diodes use a temperature-scaled Shockley I-V law, each nonlinear iteration stamps the local tangent conductance/current-source companion, voltage limiting prevents exponential overflow, and convergence requires the diode terminal voltage to settle. The original constant-drop threshold model remains the default fast/simple mode so existing breadboard builds keep their prior behavior.
6. **Continuous MOSFET I-V model** — IMPLEMENTED as opt-in `solverOptions.mosfetModel = 'continuous'`. The channel uses a square-law large-signal model with cutoff, triode, and saturation regions plus modest channel-length modulation; each nonlinear iteration stamps a Newton Jacobian around the previous terminal voltages. The channel is bidirectional when enhanced, temperature dependence remains tied to the existing RDS(on) behavior, and the explicit body diode, gate capacitance, leakage, ratings, and thermal accounting remain separate. The original threshold + fixed-RDS(on) model remains the default fast/simple mode.
7. **Convergence tolerances** — IMPLEMENTED for precision nonlinear modes. Newton diode and continuous-MOSFET solves use SPICE-style `RELTOL`/`VNTOL`/`ABSTOL` stopping criteria on successive node-voltage and nonlinear-device-current iterates, with defaults `1e-3`, `1e-6 V`, and `1e-12 A`. Linear/simple-mode circuits keep their existing one-pass/state-stability behavior instead of being forced through artificial extra iterations. Solver metadata reports the active tolerances, worst deltas, and whether voltage/current delta criteria passed.

### P3 — frequency-domain analysis

8. **Small-signal AC analysis (`.ac`-class)** — IMPLEMENTED in `js/ac-analysis.js`. The analyzer first solves a precision DC operating point, zeros independent AC excitation for that bias solve, then builds a complex MNA system at each requested frequency. Resistors, capacitor ESR/leakage, inductor DCR, source impedance, GMIN, diode local conductance, and continuous-MOSFET small-signal derivatives are stamped from the same physical models used elsewhere. Analytic RC, RL, and series-RLC phasors plus a nonlinear diode-bias slope are permanent CI references. Unsupported component classes are rejected explicitly rather than silently ignored.
9. **Bode output** — IMPLEMENTED in `js/bode-analysis.js`. Named single-ended or differential input/output voltage probes produce `H(jw)=Vout/Vin` from the complex AC phasors, with linear magnitude, dB magnitude, wrapped phase, and continuous unwrapped phase for plotting/export. Permanent CI checks the complex RC transfer against the physical ESR/leakage model, differential-probe gain, sweep ordering/trends, and phase unwrapping. This item provides plot-ready Bode data; a graphical UI renderer is intentionally separate from the solver/analysis truth.
10. **Pole/zero sanity checks** — IMPLEMENTED as a permanent analytic qualification in `test/pole-zero-sanity.test.js`. RC low-pass verifies its analytic pole, -3 dB neighborhood, phase, and post-pole rolloff; RC high-pass verifies the zero at the origin through its +20 dB/decade low-frequency slope plus its pole/flat passband; RL verifies the pole including the simulator's declared inductor DCR; series RLC verifies the measured resonance peak and phase crossing against `1/(2*pi*sqrt(L*C))`. These tests run in the normal CI chain and use the Bode/AC solver without adding a separate electrical model.

### P4 — sources, controlled elements, and model coverage

11. **Current sources and controlled sources (VCCS/VCVS/CCCS/CCVS)** — IMPLEMENTED in the generic MNA core and small-signal AC analyzer. `isource` is an ideal independent current source with positive current defined from `a` to `b`; VCCS/VCVS use differential `controlP`/`controlN` voltage; CCCS/CCVS use classic SPICE-style `controlSourceId` to reference the MNA branch current of a named voltage-source element. VCVS/CCVS get their own MNA branch-current unknowns, invalid current-control references fail loudly, and the same definitions work through transient/DC solves and `.op`. AC analysis supports all five source families, including an independent current source as the selected phasor excitation, and explicitly prefers a named `gnd`/`ground`/`0` node for the AC reference. Permanent qualification checks independent-current Ohm's law, VCCS/VCVS gain, CCCS/CCVS sign and gain, AC excitation/gain, and invalid-reference rejection.
12. **BJT support** — IMPLEMENTED as a continuous first-order Ebers–Moll-class `npn`/`pnp` model in the generic electrical core. The model includes exponential base-emitter and base-collector junction transport, temperature-scaled thermal voltage, configurable `IS`, forward/reverse gain (`betaF`/`betaR`, aliases `bf`/`br`), and forward/reverse emission coefficients (`nf`/`nr`). Every nonlinear iteration stamps a full three-terminal Newton Jacobian, BJT terminal currents participate in the shared `RELTOL`/`VNTOL`/`ABSTOL` convergence tests, and forward-bias junction-step limiting prevents hard saturation from producing runaway Newton steps or false convergence. Small-signal AC stamps the same three-terminal Jacobian at the solved operating point. Permanent qualification covers NPN forward-active gain/KCL, cutoff, hard saturation with beta collapse, mirrored PNP behavior, parameter override, and inverting common-emitter AC gain. This is deliberately not a full Gummel–Poon/model-card implementation yet: Early effect/output resistance, depletion/diffusion capacitances, transit time, high-current beta rolloff, noise, thermal self-heating, and richer transistor model cards remain future fidelity work.
13. **Better MOSFET parameter sets / model cards** — IMPLEMENTED as named reusable MOSFET cards shared by the simple switch, continuous channel, transient, thermal, ratings, body-diode, leakage, and small-signal AC paths. Built-in AO3400A-class, 2N7000-class, AO3401A-class, and BS250-class cards preserve the prior numeric `value` selector for existing builds while also allowing explicit `model`/string `modelCard` selection, inline model-card objects, and per-device parameter overrides. Cards carry threshold voltage, RDS(on), VGS/VDS ratings, Ciss, continuous-model beta calibration and channel-length modulation, off-state leakage, RDS(on) temperature coefficient, and body-diode Vf/Ron; unknown cards and N/P polarity mismatches fail loudly. AC analysis now stamps the same card's Ciss as gate-source `jωC`, so frequency-domain input loading agrees with transient gate capacitance instead of silently discarding it. Permanent qualification proves legacy equivalence, card/override resolution, electrical effects of RDS(on), lambda and leakage, and Ciss-dependent AC loading. This is a structured Virtual Breadboard model-card layer, not a BSIM implementation or textual SPICE `.MODEL` parser.
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
