# Testing Rules

## Rule 4 — Preserve working behavior

Anything already passing remains a permanent regression requirement. The first
time a capability passes, it becomes permanent: PASS → receipt saved → test
becomes permanent. Future work must keep it passing.

Concretely in this repo: `test/circuit.test.js` (49 tests), `node
test/qualification.test.js` (80 checks: the 7-item first gate plus the remaining
fundamental-circuit tests), `test/primitives.test.js` (26 checks across the 10
reusable primitives), and `node test/run_regression_builds.js` (39 checks across
the 17 permanent regression builds) must all stay green. None of these get
weakened to make a new change pass — see Type J in `update_rules.md`'s bug-triage
table: if a test's *expected* value is itself wrong, that is a rules/test-layer
fix on its own, done explicitly, not a side effect of some other change.

## Tests mirror the architecture

```
09_TESTS/
├── rules/
├── parts/
├── connections/
├── electrical_core/
├── dynamics/
├── measurement/
├── primitives/
├── magnetics/
├── power/
└── integration/
```

Every layer owns its tests. Examples from the canon:

```
parts/resistor_ohms_law
parts/mosfet_low_side
connections/floating_node
connections/short_detection
electrical_core/series_resistors
electrical_core/parallel_resistors
dynamics/capacitor_charge
dynamics/inductor_ramp
measurement/differential_voltage
primitives/loaded_midpoint
primitives/hysteresis
magnetics/coupled_coils
power/battery_sag
```

See `../09_TESTS/MAP.md` for exactly which existing test (in which of the four
current test files) currently proves each of these — the physical test *files*
in this repo are not yet split one-per-layer-directory the way the canon
diagrams them, but every capability the canon lists is either already covered,
or explicitly marked MISSING there.

## No eyeballing

Every check prints expected/actual/tolerance and PASS/FAIL, and the process
exits non-zero on the first failure (`test/qualification.test.js`,
`test/primitives.test.js`) or after running everything and reporting a nonzero
failure count (`test/run_regression_builds.js`). A waveform is never "close
enough" by inspection — see `measurement_rules.md`, Rule 7.

## First build order maps to what's already proven

Per `architecture.md`'s Stage 1-5 order, this codebase's *capabilities* (not yet
its directory layout) already clear every stage:

- **Stage 1** (DC source, resistor, divider, loaded midpoint, node/differential
  voltage, branch current, power) — `qualification.test.js` items #1-#3, Gate 1/2.
- **Stage 2** (capacitor, RC, inductor, LC/RLC, switching) —
  `qualification.test.js` Gate 4, items #8/#9/#10.
- **Stage 3** (source resistance, battery sag, capacity, energy accounting) —
  `qualification.test.js` Gate 7, `primitives.test.js` Primitive 9.
- **Stage 4** (shared center, differential pair, MOSFET switching stages,
  hysteresis, reinjection) — `qualification.test.js` Gates 1-3/5/6,
  `primitives.test.js` Primitives 1/3/4/6.
- **Stage 5** (one winding, coupled pair, three windings, phase, measurable
  field behavior) — `qualification.test.js` items #19/#20, `primitives.test.js`
  Primitive 8. (Bx/By/Bz field-vector measurement specifically is MISSING — see
  `../07_MAGNETICS/MAP.md`.)
