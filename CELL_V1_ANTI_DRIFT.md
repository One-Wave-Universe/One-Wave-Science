# CELL_V1 Anti-Drift Lock

**Read this before drawing, simulating, routing, fabricating, or describing CELL_V1.**

## Primary primitive - do not lose this

**CELL_V1 is one repeatable hex cell.** The A/B/C magnetic elements, MOSFET bridge, reference circuit, sensing, and reinjection hardware are candidate **internals of that hex**. They do not replace the hex as the primitive.

Every serious architecture drawing must show or explicitly preserve:

```text
ONE CELL_V1 HEX
 -> identical edge-to-edge neighbor
 -> seven-cell flower
 -> larger field / volume recurrence
```

A drawing of three magnetic elements by themselves is an **internal-component drawing**, not a complete CELL_V1 architecture drawing.

Read `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md` for the integration rule.

## Red-line geometry

```text
PORTS: FLAT SIDES / EDGES ONLY
CORNERS / VERTICES: NO PORTS

CLOCKWISE EDGE ORDER:
A+ -> B+ -> C+ -> A- -> B- -> C-

DIRECT OPPOSITES:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

If a diagram puts a connection on a corner, it is wrong.

If a diagram changes the clockwise edge order, it is wrong.

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

## Hardware-layer separation - mandatory

Do not collapse different counts into one another:

```text
6 HEX EDGE PORTS
!=
MAGNETIC WINDING COUNT
!=
POWER-MOSFET COUNT
!=
BRAIN / VOLUME LAYER COUNT
```

`A+ B+ C+ A- B- C-` are external CELL_V1 edge interfaces. They are **not automatically six separate windings**.

Six MOSFETs are well grounded when used as **three A/B/C half-bridges**. Six MOSFETs do not automatically provide six independently controlled bidirectional winding channels.

## Current physical package target

The preferred bench target is now grounded in demonstrated magnetic hardware **inside one CELL_V1 hex**:

- **external cell shell/interface:** six canonical flat-edge ports in the locked order;
- **electronics/power layer:** three-half-bridge A/B/C power stage where appropriate, gate drive, dead time/protection, current/voltage sensing;
- **reference layer:** separately generated and measured electrical center/reference; it is not the energy reservoir;
- **magnetic layer:** three multifunction A/B/C magnetic elements, or another measured three-axis magnetic implementation, derived from fluxgate, magnetic-amplifier, and transfluxor precedents;
- **candidate functions per magnetic element:** drive/power, control/write, sense, feedback/maintain - exact winding count remains experimental;
- **energy layer:** DC-link / reinjection capacitor with measured steering and energy accounting;
- **optional shared magnetic substrate:** later experiment only, after single-element retained state is demonstrated.

Magnetic state is stored in measured hysteretic material, not in the MOSFET gate.

Electrical reference and magnetic remanence are separate physical quantities.

Returned inductive/magnetic energy goes to the controlled recovery reservoir / DC link, **not into virtual ground**.

## Real-hardware grounding authority

Read these together:

1. `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
2. `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
3. `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`

The real precedents now used as the engineering floor are:

- fluxgate cores: separate excitation / sense / feedback functions;
- magnetic amplifiers / saturable reactors: control and maintaining windings governing power behavior;
- transfluxors: remanent state with separated write/read/sense magnetic paths;
- three-phase bridges: six switches as three half-bridges;
- regenerative inverters: returned energy collected on a DC-link capacitor.

The combined CELL_V1 remains experimental.

## Proven vs proposed

**Locked geometry does not mean proven hardware.**

Still experimental:

- exact magnetic material and core geometry;
- winding count / turn ratios / polarities;
- exact MOSFET topology for the final cell;
- useful retention margin;
- reinjection efficiency;
- shared magnetic substrate behavior;
- stable path propagation;
- stable field rotation;
- vertical/depth coupling;
- `3 x 3 x 3` unit grain;
- M4 physical depth;
- higher-brain layer/block count;
- hemisphere mirror implementation.

## Brain/M4 count warning

Do not silently promote any of these current ideas to canon:

```text
normal + inverted
2+2
3+3
3+ / 3- / 3+
3 x 3 x 3
```

They are test candidates until measurements show what each added layer or volume contributes.

## Rejection rule

Any generated image, CAD sketch, schematic, simulator topology, or prose description that violates the flat-edge port rule or canonical edge order should be discarded and corrected immediately rather than preserved as an alternative CELL_V1 geometry.

Also reject any design that silently assumes:

- the internal A/B/C magnetic assembly replaces the enclosing CELL_V1 hex;
- a standalone three-core fixture is the final scalable primitive;
- six edge ports = six windings;
- virtual ground = magnetic core or geometric center;
- reinjection capacitor dumps energy into the reference node;
- ordinary ferrite or nanoparticle sheet automatically provides nonvolatile memory;
- three physical toroids at 120 degrees are required merely because a three-phase electrical system uses 120-degree phase spacing.

## Diagram completeness test

A CELL_V1 architecture diagram is complete only if a reader can identify:

```text
1. the six flat-edge ports;
2. the internal A/B/C implementation;
3. the flat-edge connection to an identical neighboring cell;
4. the repeated scale path into flower / field / volume.
```

If #3 and #4 disappear, the design has drifted away from CELL_V1 even if the internal magnetic hardware is plausible.

See:

- `UPDATED_62_CELL_V1_HEX_FIRST_INTERNALS_AND_SCALING.md`
- `UPDATED_61_CELL_V1_REAL_HARDWARE_GROUNDING.md`
- `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
- `CELL_V1_BUILD_PACKET.md`
- `ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md`
