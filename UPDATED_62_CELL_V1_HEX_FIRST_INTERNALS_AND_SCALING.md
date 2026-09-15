# UPDATED 62 - CELL_V1 Hex-First Internals and Scaling

**Status:** Current integration correction. Updated 60 geometry remains locked. Updated 61 real-hardware grounding remains valid, but its A/B/C magnetic elements are **internal mechanisms of one CELL_V1 hex**. They do not replace the hex cell as the primitive that connects and scales.

## 1. Primary rule

The physical primitive is still **one CELL_V1 hex**.

```text
ONE CELL_V1 HEX
  external flat-edge interfaces:
  A+ -> B+ -> C+ -> A- -> B- -> C-

  internal implementation candidate:
  A/B/C multifunction magnetic elements
  + switching / sensing electronics
  + electrical reference
  + controlled recovery / reinjection reservoir
```

The real-hardware mechanisms from fluxgates, magnetic amplifiers, transfluxors, three-phase bridges, and regenerative DC links are used to implement the **inside** of the cell.

They do not replace the cell-to-cell geometry.

## 2. Locked external geometry

Ports remain centered on flat sides only.

```text
CLOCKWISE:
A+ -> B+ -> C+ -> A- -> B- -> C-

DIRECT OPPOSITES:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Corners / vertices have no port function.

The cell must remain usable as an identical repeatable module regardless of how its internal magnetic hardware evolves.

## 3. Internal A/B/C hardware belongs inside one hex

The grounded A/B/C magnetic-element model from Updated 61 is interpreted as the current **internal three-axis mechanism** for one CELL_V1.

Conceptually:

```text
                   A+ EDGE
                     |
                 [ A AXIS ]
                     |
C- EDGE -- [ C AXIS / CELL CORE ] -- B+ EDGE
                     |
B- EDGE -- [ B AXIS / CELL CORE ] -- C+ EDGE
                     |
                   A- EDGE
```

The drawing is functional, not a literal final PCB placement.

The important relationship is:

```text
A+ / A- external pair -> internal A-axis magnetic/electrical mechanism
B+ / B- external pair -> internal B-axis magnetic/electrical mechanism
C+ / C- external pair -> internal C-axis magnetic/electrical mechanism
```

Each internal axis may use drive/write/sense/feedback functions derived from measured need. The exact number of windings remains open.

## 4. Electronics and energy are also internal to the cell package

The current implementation candidate for one cell includes:

- switching / gate-drive electronics for A/B/C routing;
- voltage/current sensing;
- one separately established electrical reference;
- one or more hysteretic magnetic paths;
- write/read/sense/feedback functions;
- controlled energy-recovery path;
- local DC-link / reinjection reservoir where appropriate;
- protection and test points during development.

A standard six-MOSFET three-half-bridge stage is a grounded candidate for A/B/C power routing. It is not itself the CELL_V1 architecture.

## 5. The scale path must stay visible in every diagram

Every CELL_V1 hardware diagram should preserve the full scaling ladder:

```text
ONE HEX CELL
     |
     v
EDGE-TO-EDGE PATH
     |
     v
SEVEN-CELL FLOWER
     |
     v
COUPLED FLOWER / FIELD NETWORK
     |
     v
3D VOLUME
     |
     v
RESOLVED VOLUME AS NEXT-SCALE POINT
```

The purpose of the internal hardware is to make that external recurrence physically possible.

A diagram that shows only three magnetic elements and omits the enclosing hex interface is incomplete as a CELL_V1 architecture diagram.

## 6. Seven-cell flower remains the first planar scale unit

The first scaling assembly remains:

```text
one center CELL_V1
+
six surrounding identical CELL_V1 cells
```

Rules:

- all seven cells use the same physical orientation;
- all connections are flat-edge to flat-edge;
- shared edges mate matching axes with opposite polarity;
- no adapter cell is introduced;
- each cell retains its own internal A/B/C magnetic/electrical mechanism;
- the center cell is not replaced by a separate M4-only object.

The flower is where local cell state first becomes a larger path / rotation / field problem.

## 7. Scaling objective

The current physical scaling target remains:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

Working interpretation:

- **Point:** one CELL_V1 local state or one resolved lower-scale state;
- **Path:** transfer through flat-edge connections;
- **Rotation:** traveling/circulating state or phase through a closed route;
- **Field:** multiple coupled paths/rotations acting together;
- **Volume:** X/Y/Z coupling among field units;
- **next-scale Point:** a resolved lower-scale volume exposed as one higher-scale relational unit.

Real-hardware grounding changes how one cell may be built. It does **not** change this recurrence.

## 8. 3D scaling remains experimental but must preserve the same primitive

A current candidate is `3 x 3 x 3` recurrence. The exact grain remains open:

- 27 individual cells;
- 27 flower-scale points;
- 27 resolved submodules;
- another experimentally justified unit.

Whatever grain is chosen, the lower-scale unit must expose the same relational interface it consumes. Do not solve 3D scale by inventing a completely different connector primitive.

## 9. Mirrored memory / reinjection scale

The candidate whole-volume mirror remains:

```text
PRIMARY VOLUME
      <->
MIRROR-FLIPPED VOLUME
```

That is a **higher-scale recurrence of the same cell/field architecture**, not a replacement for it.

The mirror may eventually provide retained whole-state history, checking/comparison, and controlled return/reinjection. This remains unproven until smaller levels demonstrate the function.

## 10. What is locked vs open

### Locked

- one CELL_V1 hex is the repeatable physical primitive;
- six flat-edge ports only;
- clockwise order `A+ B+ C+ A- B- C-`;
- direct opposite A/B/C pairs;
- seven identical same-orientation cells form the first flower;
- scale is built by connecting the same primitive, not replacing it;
- real-hardware A/B/C magnetic components belong inside the cell implementation;
- electrical reference, magnetic state, and energy reservoir remain separate physical functions.

### Open

- exact internal core geometry;
- exact winding count;
- exact MOSFET topology inside the final cell;
- whether all three magnetic axes fit one shared magnetic body or use three separate elements;
- shared magnetic substrate;
- final vertical connector implementation;
- `3 x 3 x 3` grain;
- mirrored-volume implementation;
- M4 / brain physical depth.

## 11. Diagram acceptance rule

A complete CELL_V1 architecture drawing must answer all four questions:

```text
1. WHERE ARE THE SIX FLAT-EDGE PORTS?
2. WHAT INTERNAL A/B/C HARDWARE IMPLEMENTS THE CELL?
3. HOW DOES ONE CELL CONNECT TO AN IDENTICAL NEIGHBOR?
4. HOW DOES THAT CONNECTION REPEAT INTO FLOWER / FIELD / VOLUME SCALE?
```

If a drawing answers only #2, it is an internal-component drawing, not a CELL_V1 architecture drawing.

## 12. Build sequence with scale preserved

The shortest grounded path is:

```text
prove one multifunction magnetic element
 -> reproduce A/B/C internal axes
 -> package / emulate them as ONE CELL_V1 HEX
 -> prove one edge-to-edge transfer between two identical hexes
 -> prove a three-cell path
 -> prove closed circulating behavior
 -> build the seven-cell flower
 -> test stacked / volumetric coupling
 -> only then test mirrored higher volumes
```

The cell is not finished when one core remembers. CELL_V1 is only established when the **hex module itself** can retain state, communicate through its locked edges, and scale through identical copies.
