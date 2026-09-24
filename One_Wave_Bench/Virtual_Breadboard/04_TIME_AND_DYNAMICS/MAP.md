# Layer 04 — Time and Dynamics

## Canon

Anything that changes through time: capacitor charging/discharging, inductive
ramp, switching transitions, oscillation, delay, RC timing, LC/RLC ringdown,
hysteresis state through time, simulation history.

## Status: implemented as backward-Euler companion models inside `Circuit.solve()`

| Capability | Location | Status | Covering tests |
|---|---|---|---|
| Sim clock | `this._t`, initialized `circuit.js:548`, advanced `circuit.js:568` | PASSING | `qualification.test.js` #8/#9 |
| Capacitor charge/discharge (backward-Euler) | `circuit.js:996-1022` (stamp), `circuit.js:1865+` (state commit) | PASSING | `qualification.test.js` Gate 4 |
| Capacitor initial condition (`initialV`) | `capInitialV()` `circuit.js:229` | PASSING | `qualification.test.js` Gate 4 |
| Inductor ramp / continuity (backward-Euler, extra branch-current unknown) | `circuit.js:1342-1359` | PASSING (verified current cannot jump instantaneously) | `qualification.test.js` Gate 4 |
| LC/RLC ringdown | same cap+inductor companion models, no separate code path | PASSING at real analytic frequency | `qualification.test.js` #10, `regression-builds/05_lc_ringdown.js` |
| MOSFET switching transition (gate capacitance RC delay) | `circuit.js:1058` (`gGate` stamp) | PASSING — real RC-limited flip, not instant | `qualification.test.js` Gate 3 |
| Comparator propagation delay | `circuit.js:1590-1620` (`_compDesiredSince`/`propDelay` gating) | PASSING | `qualification.test.js` #16 |
| Schmitt hysteresis (state through time) | schmitt stamp `circuit.js:1186`, state readback `circuit.js:2073` | PASSING (no chatter in the deadband) | `qualification.test.js` Gate 5 |
| RC relaxation oscillation | built from schmitt + resistor + capacitor, no dedicated oscillator code | PASSING | `qualification.test.js` #18, `regression-builds/13_relaxation_oscillator.js` |
| Battery state through time (Coulomb counting, EMF knee) | `circuit.js:143` (`batteryEmfScale`), battery post-solve block | PASSING | `qualification.test.js` Gate 7 |
| Magnetic core remanence through time | `circuit.js:1400`-ish + damped fixed-point relaxation (`circuit.js:1779-1798`) | PASSING | `test/circuit.test.js` T-CORE-LOCK/HOLD |
| Simulation history / trace | not stored internally — callers accumulate their own trace arrays across repeated `solve()` calls | PASSING as the established pattern, MISSING as a built-in "record everything" mode | every trace-based test in the repo (e.g. `qualification.test.js` #10's `capTrace`) |

## The real bug found and fixed this session

`Math.max(dt, 1e-6)` appeared 9 times, in every one of: the capacitor stamp
(`circuit.js:1004`), the capacitor state commit (`circuit.js:1870`, `1879`), the
inductor's `Ldt` (`circuit.js:1344`), the toroid's `dtSafe` (`circuit.js:1371`),
the memory core's `dtSafe` (`circuit.js:1411`), the MOSFET gate-capacitance
`gGate` (`circuit.js:1058`), and thermal relaxation's `k` (`circuit.js:579`).
Intended purely as a divide-by-zero guard for `dt=0`, 1 microsecond turned out
to be a real, physically meaningful floor for anything above ~150kHz — any
requested `dt` smaller than that got silently rounded UP inside these formulas
while the actual sim clock kept advancing at the true (smaller) `dt`, making
every reactive component behave as if far more real time had elapsed per step
than actually had.

**Symptom:** a 100nF/1mH LC tank (real analytic ringdown frequency 15915Hz) rang
at anywhere from 50,000Hz to 5,000,000Hz depending on step size, with the ratio
scaling exactly as `1e-6/dt` — never converging toward the right answer as `dt`
shrank, the opposite of what a converging numerical method should do.

**Fix:** floor lowered from `1e-6` to `1e-12` at all 9 sites — small enough that
no physically meaningful `dt` will ever hit it, while still guarding the
original `dt=0` case.

**Verification:** full `test/circuit.test.js` (49/49), `test/qualification.test.js`
(80/80 including the LC/RLC test now matching its analytic frequency to within
0.2%), `test/primitives.test.js` (26/26), and `test/run_regression_builds.js`
(39/39) all still pass after the fix.

## Known gaps

- No dedicated "delay" primitive independent of a real component's own RC/
  propagation-delay behavior — delay is always a side effect of a real part
  (capacitor, comparator), never an abstracted timer. This matches Rule 6 (no
  unexplained magic primitives) and is intentional, not a gap.
