# Layer 05 — Measurement

## Canon

Observation only, never mutation (unless a modeled meter intentionally has real
loading). Voltage, differential voltage, current, power, energy, RMS, frequency,
phase, duty cycle, oscilloscope, temperature, machine-readable export.

## Status: implemented in `simulate.js`, fully covered by synthetic-signal tests

| Capability | Function | Location | Status |
|---|---|---|---|
| Node voltage | direct `result.voltages.get(uf.find(name))` | consumer-side, `simulate.js:326` (`namedVoltagesFrom`) | PASSING |
| Differential voltage | subtraction of two named voltages | `simulate.js:339` (`measurementsFrom`) | PASSING |
| Branch/source current | direct `result.currents.get(id)` | consumer-side | PASSING |
| Instantaneous power | `powerFromVI()` | `simulate.js:599` | PASSING |
| Average power/value | `averageValue()` | `simulate.js:556` | PASSING |
| Integrated energy | `integrateEnergy()` | `simulate.js:584` | PASSING |
| RMS voltage/current | `rmsValue()` | `simulate.js:569` | PASSING |
| Threshold crossings | `findCrossings()` | `simulate.js:616` | PASSING |
| Period / frequency | `findPeriod()` / `findFrequency()` | `simulate.js:638` / `649` | PASSING |
| Phase difference | `phaseDifferenceDeg()` | `simulate.js:658` | PASSING — convention is **positive = output delayed relative to input** (a real lag reads positive), established in `test/circuit.test.js` T-MEASURE-PRIMITIVES and reused correctly by every filter test |
| Duty cycle | `dutyCycle()` | `simulate.js:687` | PASSING |
| Transient trace | caller-accumulated arrays of `{t, value}` | pattern used throughout | PASSING as pattern, MISSING as a built-in feature (see `04_TIME_AND_DYNAMICS/MAP.md`) |
| Battery state (SOC, energy consumed) | `res.batteryStates` (`circuit.js`), surfaced via `snapshot()` | `simulate.js:349`, `circuit.js` battery post-solve block | PASSING |
| Temperature | `res.coreFlux`/self-heating via `THERMAL_SPEC`/`tempOf()` | `circuit.js:157`, `circuit.js:573-581` | PASSING for resistor/MOSFET/H-bridge self-heating; a general per-part temperature *readout* API beyond what's already exposed is a placeholder (matches the qualification spec's own "component temperature placeholder" language) |
| Field/Void resolved-state reading | `resolvedOutputFrom()` | `simulate.js:722` | PASSING — proven against a real driven circuit (not just mock data) in `primitives.test.js` Primitive 2 |
| Machine-readable export | `snapshot()` | `simulate.js:349` | PASSING — exports voltages, currents, warnings, mosfet/core/comparator/battery states as plain objects |

## Known gaps

- **Finite scope-probe input impedance / stray capacitance** — pre-existing
  backlog item (still pending in the task tracker as "Finite scope-probe input
  impedance + stray capacitance (stretch)"). A modeled probe today has no
  loading effect on the circuit it measures; a real probe always does, even if
  small. MISSING, not silently assumed to be zero-impact — this note is the
  honest record of that assumption.
- **Bx/By/Bz field-vector measurement** — the canon's Layer 07 wants this;
  see `07_MAGNETICS/MAP.md`. Not yet exposed as a measurement.
