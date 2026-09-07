# Layer 02 — Connections

## Canon

"What is physically connected to what?" Node creation, wires, breadboard row
connectivity, rails, component pins, junctions, shared references, open
circuits, shorts, floating nodes, branch/loop discovery. No voltage calculation
belongs here.

## Status: implemented, split across two files, now independently inspectable

Two real connectivity mechanisms exist, at two different levels — and, since
this was flagged as needing hard validation rather than trust-me behavior,
both are now exposed as real, queryable netlists instead of only being an
internal detail of `solve()`.

### Electrical topology (union-find) — `js/circuit.js`

- `buildTopologyUnionFind(components, wires)` (`circuit.js:104`) does exactly
  what `solve()` itself needs for its own matrix assembly — wires and closed
  switches/pushbuttons are the only things that ever merge two node names into
  one node; every other component type just registers its own pins. `solve()`
  calls this same function (`circuit.js:657`) rather than duplicating it, so
  there is exactly one place this logic lives.
- `netlist(elements)` (`circuit.js:151`) is the queryable form: every real node
  name grouped by the electrical node it belongs to, with internal bookkeeping
  nodes (a battery's own hidden reference node, etc.) reported separately so
  nothing is silently invisible but nothing internal is mistaken for a real,
  placeable node either.
- The implicit reference/ground node is chosen at `circuit.js:938-940`: a real
  battery's negative terminal takes priority if one exists, else the first
  wire's `.a`, else the first component's `.a` — a real, honest "arbitrary but
  consistent" choice for an unanchored circuit (see
  `../00_RULES/measurement_rules.md`'s floating-reference note). `diagnose()`
  (`circuit.js:262`) now names this explicitly as `noReference: true` whenever
  no battery/diffsource exists to justify that choice, instead of leaving it
  an implicit gotcha only visible to someone who already knows to look for it.

### Physical breadboard connectivity — `js/board.js`

- Row/column hole layout, hole occupancy, and multi-board addressing live
  here, separate from the electrical union-find above.
- `Board.netlist(board)` groups every hole by the `cellId` `cellIdFor()`
  already assigns it — the pure, component-free ground truth for "do 5 holes
  on one strip really become one node," "does the center trench connect top
  and bottom," and "do split rails stay split." Needs no circuit or solve.

| Capability | Location | Status | Covering tests |
|---|---|---|---|
| Wire union | `circuit.js:106` | PASSING | `test/circuit.test.js` Test 10, `test/netlist.test.js` |
| Closed-switch union | `circuit.js:111` | PASSING | `test/circuit.test.js` Test 7, `test/netlist.test.js` |
| Electrical netlist export | `circuit.js:151` (`netlist()`) | PASSING | `test/netlist.test.js` (jumper merges exactly the intended nodes, a two-terminal part never merges its own terminals) |
| Physical (board) netlist export | `js/board.js` (`netlist()`) | PASSING | `test/netlist.test.js` (every strip has exactly 5 holes, trench never connects banks, rails never cross boards) |
| Reference/ground node selection | `circuit.js:938-940` | PASSING, with a real documented gotcha | `qualification.test.js` floating-reference fixes |
| Hole occupancy (one lead per hole) | `js/board.js` | PASSING | `test/circuit.test.js` T-HOLE-COLLIDE |
| Multi-board addressing | `js/board.js` + `simulate.js:75` (`H()`) | PASSING | `test/circuit.test.js` T-BOARD2, `test/netlist.test.js` |
| Named-node aliasing (name → cellId, no topology change) | `simulate.js:308` (`resolveNodeNames`) | PASSING | `test/circuit.test.js` T-NAMED-NODES |
| **Open circuit / floating node — explicitly named** | `circuit.js:262` (`diagnose()`, real DC-reachability search via `realDcEdges()`) | PASSING | `test/fault-states.test.js` |
| **Short-circuit — explicitly named** | `circuit.js:262` (`diagnose()`, classified from the battery's own real current-limit warning) | PASSING | `test/fault-states.test.js` |
| **NO REFERENCE — explicitly named** | `circuit.js:262` (`diagnose()`) | PASSING | `test/fault-states.test.js` |

## Known gaps

- No explicit "branch/loop discovery" report exists as a standalone
  capability — loops are solved implicitly by the MNA formulation
  (`03_ELECTRICAL_CORE`), not enumerated as a connectivity-layer output.
- `diagnose()`'s FLOATING check uses a hand-specified real-DC-conductance edge
  list (`realDcEdges()`) rather than reading the solver's own matrix directly
  — a reasonable, physics-grounded approximation (real op-amp/logic inputs
  correctly get no edge and so correctly show as floating if genuinely
  dangling), but a node whose only real path runs through a component type
  not yet listed in `realDcEdges()` would be a false FLOATING positive. New
  component types must add their own real DC-path edges there.
