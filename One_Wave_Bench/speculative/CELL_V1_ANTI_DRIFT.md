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
WINDING COUNT: experimental
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

Returned inductive/magnetic energy belongs in a measured DC-link/reinjection reservoir and is deliberately reused in a later permitted event.

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

## 11. Seven-cell flower

- one center hex + six surrounding identical hexes;
- all seven use the same orientation;
- flat-edge to flat-edge connections only;
- shared edges mate the intended matching axis/opposed polarity;
- no adapter cell;
- every cell retains the same CELL_V1 internal architecture.

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
- DC recovery/reinjection reservoir with energy accounting;
- optional magnetic/memristive/spintronic structures chosen only by measurement;
- test points adequate to distinguish state, path training, energy recovery, phase, and reference motion.

Electrical reference, retained state, learned path bias, and recoverable energy are different measured quantities even if the architecture couples them.

## 14. Scaling candidates — not yet canon

Keep these as explicit experiments:

```text
NERVE candidate:
2 flowers = normal + mirrored/inverted

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

1. `One_Wave_Bench/speculative/CELL_V1_ANTI_DRIFT.md`
2. `UPDATED_63_CELL_V1_STATEFUL_MUSCLE_MEMORY_BUILD.md`
3. `One_Wave_Bench/speculative/CELL_V1_BUILD_PACKET.md`
4. `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
5. `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
6. `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
7. `UPDATED_34_PROCESSING_IS_MEMORY_AND_CUBE_SCALE_ARCHITECTURE.md`
8. `UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md`
9. `One_Wave_Bench/speculative/Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md`
10. `One_Wave_Bench/speculative/Nodes/G-741_Crazy_Town_Balanced_Rail_Nested_Loop_Build_Proposition.md`

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
- magnetic material/core geometry;
- winding count/ratios/polarity;
- final MOSFET topology;
- reinjection efficiency;
- stable path propagation;
- stable AC/rotation/RMF behaviour;
- exact motor implementation;
- vertical/depth coupling;
- two-flower nerve role;
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
- treats six edge interfaces as six windings;
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
10. scale path into flower / field / volume.
```

If any of the first seven disappear, the design has drifted away from the current CELL_V1 build.
