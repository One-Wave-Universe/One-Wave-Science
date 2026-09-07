# Layer 02 — Connections

## Canon

"What is physically connected to what?" Node creation, wires, breadboard row
connectivity, rails, component pins, junctions, shared references, open
circuits, shorts, floating nodes, branch/loop discovery. No voltage calculation
belongs here.

## Status: implemented, split across two files

Two real connectivity mechanisms exist today, at two different levels:

### Electrical topology (union-find) — `js/circuit.js`

Every node reference in a component spec is passed through a union-find
structure (`uf`) built at the top of `solve()`:

- `wires.forEach((w) => uf.union(w.a, w.b))` (`circuit.js:652`) — explicit wires
  merge two node names into one electrical node.
- A closed switch/pushbutton unions its two terminals (`circuit.js:657`) — a
  closed switch *is* a wire, not a component with its own equation.
- Every component's own pin names are registered into `uf` via `uf.find(...)`
  (`circuit.js:653-673`) so every part participates in the same shared node
  space, without needing to know which other components share its nodes.
- The implicit reference/ground node is chosen at `circuit.js:715-720`: a real
  battery's negative terminal takes priority if one exists, else the first
  wire's `.a`, else the first component's `.a`. This is a real, honest
  "arbitrary but consistent" choice for an unanchored circuit — see
  `../00_RULES/measurement_rules.md`'s floating-reference note for what that
  means for anyone reading raw node voltages.

### Physical breadboard connectivity — `js/board.js`

Row/column hole layout, hole occupancy, and multi-board addressing (which
physical hole a wire or component terminal actually lands on) live here,
separate from the electrical union-find above. This is the layer that enforces
"only one lead per physical hole" and resolves which board a given hole
reference belongs to.

| Capability | Location | Status | Covering tests |
|---|---|---|---|
| Wire union | `circuit.js:652` | PASSING | `test/circuit.test.js` Test 10 (Y-split) |
| Closed-switch union | `circuit.js:657` | PASSING | `test/circuit.test.js` Test 7 |
| Reference/ground node selection | `circuit.js:715-720` | PASSING, with a real documented gotcha | `qualification.test.js` (multiple fixes this session for the floating-reference case) |
| Hole occupancy (one lead per hole) | `js/board.js` | PASSING | `test/circuit.test.js` T-HOLE-COLLIDE |
| Multi-board addressing | `js/board.js` + `simulate.js:75` (`H()`) | PASSING | `test/circuit.test.js` T-BOARD2 |
| Named-node aliasing (name → cellId, no topology change) | `simulate.js:308` (`resolveNodeNames`) | PASSING | `test/circuit.test.js` T-NAMED-NODES |
| Open circuit / floating node | implicit — an unconnected pin simply never gets a `uf.union`, and GMIN (`circuit.js:109`) prevents a singular matrix | PASSING | `qualification.test.js` capacitor/inductor floating-reference checks |
| Short-circuit detection | not a separate check — a real short simply produces a real, large, physically consistent current (per Rule 5) rather than being flagged as invalid | PASSING as "let it happen," see `test/circuit.test.js` Test 4 (short-circuit current limits at the real supply's brownout, doesn't crash) | `test/circuit.test.js` Test 4 |

## Known gaps

- No explicit "branch/loop discovery" report exists as a standalone
  capability — loops are solved implicitly by the MNA formulation
  (`03_ELECTRICAL_CORE`), not enumerated as a connectivity-layer output. If a
  future build genuinely needs an explicit loop list (rather than just solved
  V/I), that is new Layer 02 work, not a Layer 03 change.
