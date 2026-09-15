# CELL_V1 Anti-Drift Lock

**Read this before drawing, simulating, routing, fabricating, or describing CELL_V1.**

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
- no rotated alternate cell type and no adapter geometry is required.

## Current physical package target

- **top/electronic half:** MOSFET switching, gate drive, sensing, six bidirectional edge interfaces, electrical reference routing;
- **bottom/magnetic half:** hysteretic magnetic material, windings, retained state, maintaining/reinjection path;
- magnetic state is stored in hysteretic material, not in the MOSFET gate;
- electrical reference and magnetic remanence are separate physical quantities.

## Current scale objective

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

The primitive should scale without inventing a new cell geometry at every level.

## Proven vs proposed

**Locked geometry does not mean proven hardware.**

Still experimental:

- exact magnetic material and core geometry;
- winding counts/polarities;
- exact MOSFET topology;
- useful retention margin;
- reinjection efficiency;
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

See:

- `UPDATED_60_CELL_V1_HEX_EDGE_FLOWER_VOLUMETRIC_MEMORY_ARCHITECTURE.md`
- `CELL_V1_BUILD_PACKET.md`
- `ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md`
