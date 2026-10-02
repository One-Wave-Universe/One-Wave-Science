# CELL_V1 Anti-Drift Lock

**Read this before drawing, simulating, routing, fabricating, or describing CELL_V1.**

## 1. Primary primitive

CELL_V1 is one repeatable hex cell. Internal stateful elements, bidirectional switches, reference circuitry, sensing, motor/actuator interfaces, and reinjection hardware are **inside or attached to that primitive**. They do not replace the hex.

Every serious architecture description must preserve:

```text
ONE CELL_V1 HEX
 -> identical edge-to-edge neighbor
 -> path
 -> closed rotation
 -> seven-cell flower / larger field
 -> 3D volume
 -> resolved next-scale point
```

Current compact scale rule:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

## 2. Red-line geometry

```text
PORTS: FLAT SIDES / EDGES ONLY
CORNERS / VERTICES: NO PORTS

CLOCKWISE:
A+ -> B+ -> C+ -> A- -> B- -> C-

DIRECT OPPOSITES / PHYSICAL MIRRORS:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

If a drawing moves a connection to a corner or changes the clockwise order, it is wrong.

## 3. Three-bidirectional-mirror physical lock

CELL_V1 has **three physical bidirectional mirrors**, not six separate one-way gates and not three Mirror gates followed by three separate Action gates.

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

The same physical mirrors carry both directions:

```text
UP   = View / state / relation toward higher resolution
DOWN = Action / conditioning / Override toward lower/local state
```

Legacy notation such as `M1 -> A1 -> M2 -> A2 -> M3 -> A3` may survive only as logical/receipt notation. It must never be interpreted as six physical CELL_V1 gates.

## 4. Count separation

Keep these counts separate:

```text
PHYSICAL MIRRORS: 3 bidirectional A/B/C axes
DIRECTED HEX EDGES: 6 = A+ B+ C+ A- B- C-
ROUTE ADDRESS SPACE: 6 = 2 binary relations x 3 ternary moves
LOGICAL/RECEIPT POSITIONS: may use six labels but are not six physical gates
OUTER TOROID WINDINGS: 6 per outer toroid = one winding per triangular sector
WINDING TURNS / GAUGE / POLARITY DETAIL: experimental
MOSFET COUNT: implementation dependent
BRAIN / VOLUME LAYER COUNT: experimental
```

## 5. Processing-is-memory lock

The active path itself is intended to be the memory and the process:

```text
current physical state affects current flow
 -> flow changes that same physical state
 -> changed state remains locally available
 -> next traversal encounters the changed state
```

Do not draw a conventional `processor -> separate memory -> processor` as the CELL_V1 primitive.

A memristive, hysteretic magnetic, spintronic/magnetoresistive, phase-retaining, oscillatory, or other stateful device may be tested. No named device is automatically accepted.

**Failure test:** if the claimed memory can be removed from the active A/B/C processing path without changing the operation, it is not the required processing-memory implementation.

## 6. Repeated-path muscle-memory lock

The build must develop and test a physical muscle-memory analogue from **repeated use of the same paths**.

Target rule:

```text
successful path traversal
 -> same stateful path changes
 -> repeated traversal accumulates a bounded bias
 -> later traversal of that path becomes measurably easier / faster / more likely
```

The training must live in the physical path, not only in a software counter, log, lookup table, or external RAM.

A valid repeated-path effect must change at least one measured quantity such as:

- activation threshold;
- drive energy;
- settling/decision latency;
- retained conductance;
- magnetic or phase bias;
- route preference under the same differential;
- number of higher-level interventions needed for a repeated task.

The build must also test bounded correction:

```text
useful repetition -> reinforce path bias
strain / repeated error -> do not blindly reinforce
Override -> can redirect / weaken / reverse trained bias
inactivity -> persistence or decay must be measured
```

Do not call a permanent uncontrolled lock-in `muscle memory` just because repetition changed something.

## 7. Nerve-level energy and command lock

Current nerve-level roles:

```text
DC = power + controlled recovery + reinjection
AC = alternating / recurring path activity
TERNARY = DOWN / HOLD / UP local movement and motor/actuator command
QUADRATIC VIEWS UP = Direction / Phase / Strength / Reference
QUADRATIC ACTIONS DOWN = conditioning / corrective action / Override through the same mirrors
```

`V0` is the electrical reference. It is **not** the recovery reservoir and must not be used as a power dump.

Returned inductive/magnetic energy belongs in the **gated hysteretic lattice beneath the cell/flower**, which is the distributed reinjection/body-memory layer. Recoverable energy is deliberately routed back into the local/body loop for later permitted use rather than intentionally dumped. The lattice path must be gated and instrumented.

"Nothing is wasted" is a design objective, not a thermodynamic claim: unavoidable resistive, magnetic, switching, radiative, and heat losses must be measured and minimized.

## 8. Local automatic nerve recurrence

The current nerve target is local recurrence when conditions are healthy and escalation only when declared limits are crossed:

```text
within limits
 -> settle locally
 -> recover/reinject through DC loop
 -> reuse trained path when appropriate

strained / unresolved / unsafe
 -> Views UP
 -> higher resolution
 -> Action / Override DOWN through same mirrors
 -> resulting new local state remains
```

Resource/strain must be an explicit measured set of variables such as voltage margin, current, energy-reservoir state, temperature, unresolved phase, route conflict, or repeated failure. Do not hide the decision in an undefined scalar.

## 9. Ternary motor-control lock

Ternary is also the candidate local motor/actuator command grammar:

```text
DOWN = one commanded direction
HOLD = active balanced/rest state
UP   = opposite commanded direction
```

HOLD is not automatically power-off. Exact motor topology remains experimental.

A motor turning does not by itself prove the path memory, ternary architecture, or rotating-field claim; each requires its own measurements.

## 10. Bidirectional nerve-gate lock

Connection hardware must actually support the intended bidirectional path. A single MOSFET body diode must not silently defeat the blocked direction.

Back-to-back MOSFETs or another true bidirectional switch are candidates. SiC MOSFETs may be tested in later nerve/power domains where their speed, thermal, endurance, or power properties help, but direct millivolt/microvolt gate control is not assumed. Gate-drive circuitry must be explicit and measured.

The bidirectional switch is connection hardware unless experiment proves it also carries the retained processing state.

## 11. Six-sector hex, toroid stack, and paired flowers

The planar hex is divided by lines from all six corners to the common center. This creates six triangular sectors whose **bases are the six flat hex edges**. The sector labels remain:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
opposites: A+<->A-, B+<->B-, C+<->C-
```

The geometry and symbolism are locked; the exact physical implementation of the triangular differential sectors remains an open build problem.

Each outer round toroid has **six windings, one winding mapped to each triangular sector**. Do not describe the six windings as unrelated decoration or collapse them into a generic three-winding motor.

The magnetic stack target uses **two round six-winding toroids in opposed/inverted orientation** as a Helmholtz-like candidate field pair. Their combined field is intended to interact with the inner figure-eight nucleus toroid(s). "Helmholtz-like" is a build hypothesis until field uniformity/coupling is measured; do not claim an ideal Helmholtz field without measurement.

Nucleus roles:
- center/control cell: **square figure-eight toroidal nucleus**;
- surrounding sensor cells: **round figure-eight toroidal nuclei**.

Seven-cell flower:
- one center hex + six surrounding hexes;
- flat-edge to flat-edge connections only;
- neighboring shared boundaries mate + to - by the defined geometry;
- no adapter cell;
- every cell preserves the six-sector / six-edge mapping.

The larger nerve/body unit uses **two flower halves opposite one another with the second half inverted in +/- orientation**. This paired-flower inversion is architectural canon; its exact electrical/magnetic implementation and measurable advantage remain experimental.

## 12. Scale recurrence

```text
ONE HEX
 -> PATH THROUGH IDENTICAL HEXES
 -> CLOSED ROTATION
 -> SEVEN-CELL / MULTI-CELL FIELD
 -> 3D VOLUME
 -> RESOLVED NEXT-SCALE POINT
```

Real-hardware improvements may change the **inside** of the hex. They may not silently delete the repeatable edge-connected cell.

## 13. Current physical package target

The preferred bench target contains:

- six canonical flat-edge directed interfaces;
- three physical bidirectional A/B/C mirrors;
- true bidirectional connection/switching where required;
- separately generated/measured electrical reference;
- active stateful processing-memory path;
- repeated-path training capability;
- voltage/current/state sensing;
- gated lower hysteretic lattice for DC recovery/reinjection and distributed body/path memory, with energy accounting;
- two opposed/inverted outer round toroids, each with six windings mapped one-per-triangular-sector;
- inner figure-eight nucleus coupling: square figure-eight in the center/control cell, round figure-eight in sensor cells;
- optional magnetic/memristive/spintronic material implementations chosen by measurement;
- test points adequate to distinguish state, path training, energy recovery, phase, and reference motion.

Electrical reference, retained state, learned path bias, and recoverable energy are different measured quantities even if the architecture couples them.

## 14. Scaling candidates — not yet canon

Keep these as explicit experiments:

```text
NERVE / BODY architecture:
2 opposite flower halves = one orientation + one +/- inverted orientation
(lower-level performance and exact coupling remain experimental)

M4 candidate:
2 + 2 flower/volume layers

HIGHER-BRAIN candidate:
3 / 3 / 3 volumetric expansion
and/or 3 x 3 x 3 proven lower-scale units

HEMISPHERE candidate:
resolved higher volume <-> mirror-flipped counterpart
```

Each extra layer must demonstrate a new measurable function. Numerical symmetry alone is not evidence.

## 15. Current authority order

Read these together, with earlier files interpreted through later corrections:

1. `CELL_V1_ANTI_DRIFT.md`
2. `UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md`
3. `CELL_V1_BUILD_PACKET.md`
4. `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
5. `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
6. `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
7. `UPDATED_34_PROCESSING_IS_MEMORY_AND_CUBE_SCALE_ARCHITECTURE.md`
8. `UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md`
9. `Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md`
10. `Nodes/G-741_Crazy_Town_Balanced_Rail_Nested_Loop_Build_Proposition.md`

If older wording conflicts with the three-bidirectional-mirror, processing-is-memory, or repeated-path muscle-memory locks above, the newer lock wins for CELL_V1 hardware.

## 16. Proven vs proposed

### Locked architecture

- one repeatable hex primitive;
- flat-edge interfaces only;
- clockwise order `A+ B+ C+ A- B- C-`;
- three opposed bidirectional A/B/C mirrors;
- Views UP and Actions DOWN use the same mirrors;
- processing and memory are co-located in the active stateful path;
- repeated-path physical training is required for the muscle-memory target;
- ternary DOWN/HOLD/UP is the local movement and candidate motor-control grammar;
- DC handles controlled nerve-level recovery/reinjection separately from V0;
- Point -> Path -> Rotation -> Field -> Volume -> next-scale Point recurrence.

### Experimental

- exact processing-memory device;
- exact reinforcement/decay law;
- useful retention/training margin;
- exact magnetic material and dimensions;
- exact winding turns/gauge/polarity while the six-windings-per-outer-toroid mapping is locked;
- measured field quality/coupling of the opposed outer toroids to the inner nucleus;
- final MOSFET topology;
- reinjection efficiency;
- stable path propagation;
- stable AC/rotation/RMF behaviour;
- exact motor implementation;
- vertical/depth coupling;
- measured performance/advantage of the locked two-opposite-flower nerve/body arrangement;
- `2+2` M4 depth;
- `3/3/3` or `3 x 3 x 3` higher-brain grain;
- hemisphere mirror implementation.

## 17. Rejection rule

Reject and correct any design that:

- puts ports on hex corners;
- changes the canonical edge order;
- creates six separate physical Mirror/Action gates;
- gives UP Views and DOWN Actions separate physical mirror species;
- removes memory from the active path;
- stores muscle memory only in software bookkeeping;
- reinforces failed/strained paths without a correction mechanism;
- treats V0 as an energy reservoir;
- claims recovery without an energy budget;
- separates the six triangular sectors from their one-to-one six-winding outer-toroid mapping;
- omits the opposed/inverted outer-toroid pair or silently treats it as an ideal Helmholtz pair without measurement;
- omits the lower gated reinjection lattice from the body architecture;
- assumes an ordinary ferrite, memristor, MTJ, MOSFET, or SiC device automatically provides every required function;
- promotes `2 flowers`, `2+2`, `3/3/3`, or `3x3x3` to proven hardware without a measured function.

## 18. Diagram completeness test

A CELL_V1 build diagram is complete only if a reader can identify:

```text
1. six flat-edge directed interfaces;
2. three bidirectional A/B/C mirrors;
3. active stateful processing-memory path;
4. repeated-path training / muscle-memory mechanism under test;
5. Views UP and Actions DOWN through the same mirrors;
6. ternary DOWN/HOLD/UP local command;
7. DC recovery/reinjection separate from V0;
8. strain/escalation path;
9. identical-cell edge connection;
10. scale path into flower / field / volume;
11. six triangular sectors formed corner-to-center, with each base on a flat edge;
12. one outer-toroid winding mapped to each triangular sector;
13. opposed/inverted pair of six-winding round toroids and its coupling to the inner figure-eight nucleus;
14. square figure-eight nucleus in the center/control cell and round figure-eight nuclei in sensor cells;
15. two opposite flower halves with the second +/- inverted;
16. gated hysteretic lattice beneath the cell/flower carrying measured reinjection/body-memory flow.
```

If any of the first seven or any locked geometry/stack item 11-16 disappears, the design has drifted away from the current CELL_V1 build.

## 19. View/action flip and retained history

The current directional rule is:

```text
new Views / state information -> UP
new Actions / conditioning     -> DOWN
prior state/history            -> retained in the active hysteretic path/lattice
flip / recombination           -> occurs through the shared center/reference relation
```

Do not invent separate hardware species for "old" and "new" information. The physical requirement is that the incoming/new event encounters retained prior state, and the resulting state becomes the history seen by the next event.
