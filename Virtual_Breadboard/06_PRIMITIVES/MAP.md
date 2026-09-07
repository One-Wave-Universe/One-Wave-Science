# Layer 06 — Reusable Primitives

## Canon

A reusable circuit arrangement made from lower layers — never a magical new
component. Must be expandable so a user can inspect the real parts underneath.

## Status: implemented as callable recipe functions, proven in `test/primitives.test.js`

Every primitive below is a real circuit-element list (resistors, comparators,
MOSFETs, capacitors — never a shortcut component), built and checked in
`test/primitives.test.js`. None of them are separate `js/circuit.js` component
types.

| Canon primitive | Implementation | Status | Test |
|---|---|---|---|
| Voltage divider / loaded midpoint | plain two-resistor divider, any test file | PASSING | `qualification.test.js` #3, `regression-builds/01_resistor_divider.js` |
| Shared center | buffered vgnd + two resistor arms | PASSING (generalizes across rail voltages) | `primitives.test.js` Primitive 1 |
| Differential pair | shared-center's +/CENTER/- reading, `V+ - V-` | PASSING | `qualification.test.js` Gate 2 |
| Balanced load | center-tapped supply, two symmetric resistor branches | PASSING | `primitives.test.js` Primitive 6 |
| Low-side switch | NMOS, source at ground | PASSING | `qualification.test.js` Gate 3 |
| High-side switch | PMOS, source at VCC (fixed reference — an NMOS high-side design was tried, found to self-reference its own Vgs, and replaced) | PASSING | `qualification.test.js` #12 |
| Half-bridge | discrete PMOS+NMOS sharing one output node, driven independently (can genuinely shoot-through, unlike the abstracted `hbridge` component) | PASSING | `qualification.test.js` #13, `regression-builds/09_halfbridge_deadtime.js` |
| Full bridge | `hbridge` component + differential load | PASSING | `qualification.test.js` #14 |
| RC delay / threshold | resistor+capacitor into a comparator or Schmitt | PASSING | `qualification.test.js` #16, `primitives.test.js` Primitive 2 |
| Hysteresis | Schmitt trigger, real distinct thresholds | PASSING | `qualification.test.js` Gate 5 |
| Energy storage (cap-only / inductor-only / LC exchange, configurable losses) | direct RLC builds with a variable loss resistor | PASSING | `primitives.test.js` Primitive 5 |
| Reinjection | storage cap + Schmitt pair + PMOS high-side reconnect | PASSING (parametric — bleed-resistor change measurably changes period) | `qualification.test.js` Gate 6, `primitives.test.js` Primitive 4 |
| Resolved three-state (-/0/HOLD/+) | window-comparator pair (real 124k/1k thresholds) + PMOS/NMOS + hold cap — the real Stage-1 hardware topology, rebuilt as raw nodes | PASSING | `primitives.test.js` Primitive 3 |
| Field/Void validation | two threshold comparators + `Sim.resolvedOutputFrom` on real simulated voltages | PASSING | `primitives.test.js` Primitive 2 |
| Phase-handoff | two cascaded RC stages off one AC source | PASSING | `primitives.test.js` Primitive 7 |

## What this replaced

An earlier "Ternary Cell" macro component hard-coded a Hold/Pos/Neg decision
inside `js/circuit.js` itself — a real violation of Rule 6 (no unexplained
magic primitives), since the solver was handing back a decision instead of
requiring it be built from real parts. It was found and removed in PR #15; see
`../00_RULES/physics_rules.md`. The `resolved_three_state` and `reinjection`
primitives above are the real, inspectable replacements.

## Known gaps

- No standalone `06_PRIMITIVES/<name>/` files exist yet holding just the
  recipe function + its own doc — today they live as functions inside
  `test/primitives.test.js`, coupled to their own test assertions. Splitting
  the reusable recipe out from its test is real future Layer-06 work; the
  physics and the proof both already exist, just not yet in separable files.
