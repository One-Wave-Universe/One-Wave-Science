# CELL_V1 Anti-Drift Lock

**Read this before drawing, simulating, routing, fabricating, or describing CELL_V1.**

## Primary primitive - do not lose this

**CELL_V1 is one repeatable hex cell.** The A/B/C magnetic or other stateful path elements, bidirectional switching, reference circuit, sensing, and reinjection hardware are candidate **internals of that hex**. They do not replace the hex as the primitive.

Every serious architecture drawing must show or explicitly preserve:

```text
ONE CELL_V1 HEX
 -> identical edge-to-edge neighbor
 -> seven-cell flower
 -> larger field / volume recurrence
```

A drawing of three internal elements by themselves is an **internal-component drawing**, not a complete CELL_V1 architecture drawing.

Read `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md` for the integration rule.

## Red-line geometry

```text
PORTS: FLAT SIDES / EDGES ONLY
CORNERS / VERTICES: NO PORTS

CLOCKWISE EDGE ORDER:
A+ -> B+ -> C+ -> A- -> B- -> C-

DIRECT OPPOSITES / PHYSICAL MIRRORS:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

If a diagram puts a connection on a corner, it is wrong.

If a diagram changes the clockwise edge order, it is wrong.

## Three-bidirectional-mirror physical lock

CELL_V1 has **three physical bidirectional Mirror axes**, not six one-way physical gates and not three physical Mirror gates followed by three separate physical Action gates.

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-

3 physical bidirectional mirrors
= 6 directed edge interfaces
```

The same physical mirror/path carries both directions:

```text
UP   = View / state / relation propagation through the mirror toward higher resolution
DOWN = Action / conditioning / Override propagation through the same mirror toward the lower/local state
```

`UP` and `DOWN` do **not** create separate hardware gate species.

Any legacy notation such as `M1 -> A1 -> M2 -> A2 -> M3 -> A3` is, at most, a six-position logical/receipt description of activity on the three bidirectional mirrors. It must never be interpreted as six separate physical gates. If legacy wording conflicts with this physical lock, this file wins for CELL_V1 hardware.

## Count separation - mandatory

Do not collapse these counts into one another:

```text
PHYSICAL MIRRORS: 3 bidirectional axes A/B/C
DIRECTED EDGE INTERFACES: 6 = A+ B+ C+ A- B- C-
ROUTE ADDRESS SPACE: 6 = 2 binary relations x 3 ternary moves
LOGICAL/RECEIPT POSITIONS: may use six labels, but they are not six physical gates
MAGNETIC WINDING COUNT: experimental
POWER-MOSFET COUNT: implementation dependent
BRAIN / VOLUME LAYER COUNT: experimental
```

## Processing-is-memory lock

The active stateful path is intended to be both the thing being processed and the thing retaining history.

```text
current state affects current flow
 -> current flow changes the same local state
 -> changed state remains locally available
 -> next pass encounters that changed state
```

Do not draw a conventional `processor -> separate memory block -> processor` as the CELL_V1 primitive.

A memristive, hysteretic magnetic, spintronic, oscillatory, or other physical stateful implementation may be tested. The exact device remains experimental. The architecture fails this rule if the claimed memory can be removed from the active A/B/C processing path without changing the operation.

## Nerve-level power and command lock

For the current nerve-level architecture:

```text
DC = power supply + controlled recovery + reinjection loop
AC = alternating/recurring activity produced through the mirrored paths
TERNARY = UP / HOLD / DOWN local movement command and motor/actuator command
QUADRATIC VIEWS UP = Direction / Phase / Strength / Reference
QUADRATIC ACTIONS DOWN = conditioning / corrective action / Override through the same three mirrors
```

DC recovery/reinjection must use a controlled energy reservoir or DC link with measured accounting. The electrical reference `V0` is not the energy reservoir and must not be used as a power dump.

Ternary `HOLD` is an active balanced state, not a missing command. For motor/actuator use, the same ternary relation is the candidate local command grammar: one direction / balanced Hold / opposite direction. Exact motor topology remains experimental.

Local nerve recurrence is intended to remain local while within declared limits. A candidate higher-level policy is:

```text
local state within limits -> continue / recover / reinject locally
local state or resource condition outside limits -> Views UP -> higher resolution -> Action/Override DOWN
```

The thresholds, resource variables, and proof that this control is useful remain experimental.

## Bidirectional nerve-gate lock

Connection hardware must support the intended bidirectional path rather than silently conducting one polarity through a body diode.

Back-to-back MOSFETs or another true bidirectional switch are candidates. SiC MOSFETs may be tested where their power, thermal, endurance, or switching properties are useful, but a SiC power MOSFET is **not assumed to directly resolve a millivolt or microvolt information signal**. Any required gate-drive interface must be explicit and measured.

The bidirectional switch is a connection/nerve-gate candidate. It is not automatically the processing-memory element.

## Seven-cell flower

- one center hex + six surrounding hexes;
- all seven cells use the **same orientation**;
- cells connect flat-edge to flat-edge;
- shared edges mate matching letters with opposite polarity;
- no rotated alternate cell type and no adapter geometry is required;
- every one of the seven cells retains the same CELL_V1 internal architecture.

## Scale recurrence - mandatory

The external scaling rule is not optional decoration. It is part of the architecture:

```text
ONE HEX
 -> PATH THROUGH IDENTICAL HEXES
 -> CLOSED ROTATION
 -> SEVEN-CELL / MULTI-CELL FIELD
 -> 3D VOLUME
 -> RESOLVED NEXT-SCALE POINT
```

Current compact form:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

Real-hardware grounding may change the **inside** of the hex as measurements improve. It must not silently delete the repeatable edge-connected cell or replace it with a one-off three-core assembly.

## Current physical package target

The preferred bench target remains an experimental implementation **inside one CELL_V1 hex**:

- **external cell shell/interface:** six canonical flat-edge interfaces in the locked order;
- **three physical mirror axes:** A, B, C, each bidirectional;
- **connection/power layer:** bidirectional switching appropriate to A/B/C routing, gate drive, dead time/protection where required, current/voltage sensing;
- **reference layer:** separately generated and measured electrical center/reference;
- **processing-memory layer:** stateful A/B/C path whose retained physical state changes subsequent behavior;
- **energy layer:** DC recovery/reinjection reservoir with measured steering and energy accounting;
- **optional magnetic structures:** hysteretic or other magnetic/spintronic implementations tested only by measurement.

Electrical reference, retained physical state, and recoverable energy are different measured quantities even when the architecture couples them.

## Real-hardware grounding authority

Read these together:

1. `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
2. `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
3. `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
4. `UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md`
5. `Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md`
6. `Nodes/G-741_Crazy_Town_Balanced_Rail_Nested_Loop_Build_Proposition.md`

Useful engineering precedents include fluxgate cores, magnetic amplifiers/saturable reactors, transfluxors, true bidirectional MOSFET switches, three-phase bridges, regenerative inverters, memristive devices, and spintronic/magnetoresistive state elements. None of those precedents by itself proves the combined CELL_V1.

## Proven vs proposed

**Locked architecture does not mean proven hardware.**

Locked for CELL_V1:

- one repeatable hex primitive;
- flat-edge ports only;
- clockwise order `A+ B+ C+ A- B- C-`;
- three opposed bidirectional A/B/C mirrors;
- Views UP and Actions DOWN use those same mirrors;
- processing and memory must be co-located in the active stateful path;
- Point -> Path -> Rotation -> Field -> Volume -> next-scale Point recurrence;
- DC nerve-level recovery/reinjection is distinct from the electrical reference.

Still experimental:

- exact processing-memory device;
- exact magnetic material and core geometry;
- winding count / turn ratios / polarities;
- exact MOSFET topology;
- useful retention margin;
- reinjection efficiency;
- stable path propagation;
- stable field rotation;
- motor implementation;
- vertical/depth coupling;
- `3 x 3 x 3` unit grain;
- M4 physical depth;
- higher-brain layer/block count;
- hemisphere mirror implementation.

## Brain/M4 count warning

Do not silently promote any of these current ideas to canon:

```text
normal + inverted
2 flowers
2+2
3+3
3 / 3 / 3
3+ / 3- / 3+
3 x 3 x 3
```

They remain scale/build candidates until measurements show what each added layer or volume contributes.

## Rejection rule

Reject and correct any design that:

- places CELL_V1 connections on corners;
- changes the canonical clockwise edge order;
- draws six separate physical Mirror/Action gates instead of three bidirectional A/B/C mirrors;
- gives Views and Actions separate physical paths when the claimed design says they are opposite directions on the same mirror;
- separates memory from the active processing path and still calls it CELL_V1 processing-is-memory;
- treats six edge interfaces as six windings;
- treats virtual ground/reference as the energy reservoir;
- sends recovered energy into the reference node;
- treats a standalone three-core fixture as the final scalable primitive;
- silently promotes `2+2`, `3/3/3`, or other brain-layer counts into proven hardware;
- assumes an ordinary ferrite, memristor, MTJ, SiC MOSFET, or other named component automatically supplies every required function without measurement.

## Diagram completeness test

A CELL_V1 architecture diagram is complete only if a reader can identify:

```text
1. the six flat-edge directed interfaces;
2. the three bidirectional A/B/C mirror axes;
3. the stateful processing-memory path;
4. Views UP and Actions DOWN on those same mirrors;
5. DC recovery/reinjection separate from V0 reference;
6. the flat-edge connection to an identical neighboring cell;
7. the repeated scale path into flower / field / volume.
```

If the three-bidirectional-mirror rule disappears, the design has drifted even if the rest of the electronics is plausible.

See:

- `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
- `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
- `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
- `CELL_V1_BUILD_PACKET.md`
- `ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md`
