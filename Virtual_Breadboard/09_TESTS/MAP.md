# Layer 09 — Tests

## Canon

```
09_TESTS/
├── rules/  ├── parts/  ├── connections/  ├── electrical_core/  ├── dynamics/
├── measurement/  ├── primitives/  ├── magnetics/  ├── power/  └── integration/
```

Every layer owns its tests. No eyeballing a waveform and calling it good.

## Status: capability coverage is complete; physical test-file layout is not yet split per-layer

Four test files exist today, none split along the canon's per-layer directory
lines. This table is the actual cross-reference — the thing that lets a worker
find "does `dynamics/capacitor_charge` exist" without knowing it currently
lives inside a much larger file.

| Canon test category | Real coverage today |
|---|---|
| `rules/` | No dedicated rule-conformance tests exist (e.g. "a failing circuit is never silently corrected" isn't asserted as its own test) — this is itself a real, admitted gap. Every OTHER category below is exercised because individual tests happen to prove a rule in passing (e.g. the shoot-through test proves Rule 5), not because a rules-layer test suite asserts the rule directly. |
| `parts/` | `test/circuit.test.js` Tests 1-9, 12, 14-15, 18-21, 36; `test/qualification.test.js` Gate 3, #1-#5; `test/regression-builds/01,02,07,08,11,12.js` |
| `connections/` | `test/circuit.test.js` Test 10 (Y-split), T-HOLE-COLLIDE, T-BOARD2, T-SUPPLY-CONFLICT; floating-reference handling throughout `qualification.test.js` |
| `electrical_core/` | `test/qualification.test.js` #1-#3 (series/parallel/divider); every test transitively |
| `dynamics/` | `test/circuit.test.js` Test 6, 12, 13; `test/qualification.test.js` Gate 4, #8/#9/#10, #18; `test/regression-builds/03,04,05,13.js` |
| `measurement/` | `test/circuit.test.js` Test 32 (T-DIFFSCOPE), Test 47 (T-MEASURE-PRIMITIVES) |
| `primitives/` | `test/primitives.test.js` (all 10), `test/qualification.test.js` Gates 1/2/5/6, #12-#14, #16 |
| `magnetics/` | `test/circuit.test.js` Test 14-15; `test/qualification.test.js` #19/#20; `test/primitives.test.js` Primitive 8; `test/regression-builds/14,15.js` |
| `power/` | `test/circuit.test.js` Test 4, T-POWER-NETWORK, T-BATTERY-CAPACITY, T-LED-LIGHT-OUTPUT; `test/qualification.test.js` Gate 7, #1; `test/primitives.test.js` Primitive 9/10; `test/regression-builds/16.js` |
| `integration/` (the first qualification gate — everything must pass together) | `test/qualification.test.js` Gates 1-7 as a single required block, and `test/run_regression_builds.js` running all 17 permanent builds together |

## Bug-triage cross-reference

`../00_RULES/update_rules.md`'s Type A-K table maps a *symptom* to an owning
layer. This table maps *layers* to the actual test files that would catch a
regression in them — read together, a failing test's file tells you which Type
it probably is before you've even opened the diff.

## Receipts

See `../10_RECEIPTS/`. `test/regression-builds/*.js` already return structured
`{name, expected, actual, tolerance, pass, note}` records per check — the
closest thing in the repo today to the canon's required receipt shape.
`test/qualification.test.js` and `test/primitives.test.js` print the same
shape to the console but did not (until this pass) also export it as
structured data; see `../10_RECEIPTS/generate_receipts.js`.

## Known gaps

- No `rules/` test category exists as its own thing (see above).
- Test files are organized by *when they were written* (`circuit.test.js` grew
  incrementally over many PRs, `qualification.test.js` and `primitives.test.js`
  are this session's additions), not by *which layer they prove*. This table
  is the bridge until someone does the (real, scoped, non-trivial) work of
  physically splitting them.
