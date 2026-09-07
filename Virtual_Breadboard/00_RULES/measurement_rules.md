# Measurement Rules

## Rule 7 — Measurements determine PASS

Visual appearance does not determine success. Numerical measurements and declared
tolerances determine PASS or FAIL. Every test in this repo follows the pattern
`expected`, `actual`, `tolerance`, `PASS`/`FAIL` — printed, never eyeballed off a
plotted waveform.

## Measurement is separate from simulation behavior

Meters observe. Meters do not change the answer, unless the modeled meter
intentionally has real loading (e.g. a real finite scope-probe input impedance,
currently MISSING — see `../05_MEASUREMENT/MAP.md`). A measurement bug is a
Type F problem (`update_rules.md`): if the circuit's own solved state is already
wrong, the fix belongs to `03_ELECTRICAL_CORE` or `04_TIME_AND_DYNAMICS`, not to
the measurement code reading it.

## Required measurement capabilities

- node voltage
- differential voltage
- branch current
- source current
- instantaneous power
- average power
- integrated energy
- RMS voltage
- RMS current
- frequency
- phase difference
- duty cycle
- transient trace
- battery state
- temperature, where available

Every one of these is implemented today in `simulate.js` (`averageValue`,
`rmsValue`, `integrateEnergy`, `powerFromVI`, `findCrossings`, `findPeriod`,
`findFrequency`, `phaseDifferenceDeg`, `dutyCycle`) and cross-checked against
known synthetic signals in `test/circuit.test.js` Test 47 (T-MEASURE-PRIMITIVES).
See `../05_MEASUREMENT/MAP.md` for the exact function-to-capability mapping.

## Machine-readable export

Required by the canon; see `../05_MEASUREMENT/MAP.md` for what `simulate.js`'s
`snapshot()` already exports (voltages, currents, warnings, mosfet/core/
comparator/battery states) versus what's not yet wired to an export path.

## The floating-reference trap

A measurement-layer lesson worth keeping visible: a circuit with no real ground
anchor (no battery/wire forcing a reference) lets the solver's implicit zero
land on an arbitrary node. The fix is never to read one terminal's absolute
value in that situation — always read the real voltage *difference* across the
two terminals that actually matter. This bit three separate tests in this
session (a capacitor persistence check, an inductor flyback check, and several
AC-source-driven filter/rectifier/transformer builds) before the pattern was
written down here. It is not a solver bug — the solver is doing exactly what an
under-constrained linear system is supposed to do — it is a measurement-layer
discipline: know which node is your real reference before you trust an absolute
reading.
