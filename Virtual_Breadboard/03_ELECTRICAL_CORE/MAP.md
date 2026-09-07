# Layer 03 — Electrical Core

## Canon

"Given these connected components, what are the electrical conditions?" Node
voltage, branch current, Kirchhoff relationships, nonlinear component solving,
source/load interaction, power calculation, solver convergence, numerical
tolerances. No Field/Void/flashlight/nerve/motor logic belongs here.

## Status: implemented, generic, no build-specific logic found

| Capability | Location | Status | Covering tests |
|---|---|---|---|
| Linear solve (Gauss-Jordan, partial pivoting) | `solveLinear()`, `circuit.js:465` | PASSING | every test in the repo exercises this transitively |
| Modified Nodal Analysis assembly (stamping) | `circuit.js:920-1450` (the `A`/`b` matrix build inside the fixed-point loop) | PASSING | `qualification.test.js` #1-#3 |
| Nonlinear device iteration (MOSFET channel state, comparator decision, core B, etc.) | fixed-point loop `circuit.js:921-1802`, convergence check `if (!changed) break` at `circuit.js:1802` | PASSING — verified this session that a linear-only circuit (no MOSFET/comparator/core) converges in exactly 1 iteration, confirmed by direct instrumentation | `qualification.test.js` Gate 3, Gate 5 |
| GMIN (numerical stability floor) | `circuit.js:109`, stamped at `circuit.js:949` | PASSING | implicit in every floating-node test |
| Power calculation | derived per-part from solved V/I at readback time (e.g. resistor power-rating warning at `circuit.js:1854+`) | PASSING | `qualification.test.js` #2 (resistor-power-warning) |
| Numerical tolerance / pivot floor | `solveLinear()`'s `maxAbs < 1e-15` skip, `circuit.js:477` | PASSING | — |

## A real bug found and fixed here this session (receipt-worthy)

`Math.max(dt, 1e-6)` guards existed in every reactive-element companion-model
formula (capacitor, inductor, toroid, memory core, MOSFET gate capacitance,
thermal relaxation) — meant only to prevent divide-by-zero on `dt=0`, they
silently clamped any simulation stepping faster than 1µs to a 1µs internal step
while the real sim clock kept advancing at the true, smaller `dt`. This made a
resonant LC tank ring 3-300x faster than its own analytic frequency, scaling
exactly with `1e-6/dt`. This is properly a `04_TIME_AND_DYNAMICS` bug (it's in
the transient/backward-Euler companion models, not the DC solve itself) but is
noted here too because it was found via `03_ELECTRICAL_CORE`-adjacent debugging
(instrumenting the fixed-point loop, verifying single-iteration convergence)
before the actual root cause was isolated. Fixed by lowering the floor to
`1e-12`. See `04_TIME_AND_DYNAMICS/MAP.md` for the full writeup.

## Known gaps

- No standalone `nonlinear_solver/`, `convergence/`, `power_balance/`, or
  `numerical_tolerance/` sub-files exist yet — all of the above lives inside
  one `Circuit.solve()` method. Splitting this out is real, valuable future
  work but touches the single most load-bearing function in the codebase;
  per `../00_RULES/architecture.md`'s Change Budget, that split should be its
  own dedicated, carefully-tested change, not bundled with anything else.
