# CELL_V1 - Hex-First Real-Hardware Bench Pamphlet

## The main object is the hex cell

CELL_V1 is **one repeatable six-edge hex cell**. The magnetic cores, windings, MOSFETs, reference circuit, sensing, and reinjection hardware are all candidate mechanisms **inside that cell**.

```text
                         [ A+ ]
                    ______________
                   /              \
            [ C- ]/                \[ B+ ]
                 /   A / B / C      \
                 \  MAGNETIC +      /
            [ B- ]\  ELECTRONIC    /[ C+ ]
                   \______________/
                         [ A- ]
```

Ports are centered on the six flat sides. Corners have no port function.

Clockwise order is locked:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
```

Direct opposites:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

## What real hardware contributes inside the hex

The current internal implementation combines mechanisms that have already been built separately:

- **Fluxgate sensors:** one magnetic core with separate excitation, sense, and feedback functions.
- **Magnetic amplifiers / saturable reactors:** control and maintaining windings that change a larger power path through magnetic saturation.
- **Transfluxor memory:** remanent magnetic state, separate write/read/sense paths, and non-destructive readout concepts.
- **Three-phase motor bridges:** six MOSFETs arranged as three A/B/C half-bridges.
- **Regenerative inverters:** inductive/motor energy returned to a DC-link capacitor.

These are the engineering floor for the **inside** of CELL_V1. The combined scalable CELL_V1 remains experimental.

## Internal A/B/C mechanism

The preferred first internal model is three multifunction magnetic axes corresponding to the three opposite external edge pairs:

```text
A+ <-> [ A magnetic/electrical axis ] <-> A-
B+ <-> [ B magnetic/electrical axis ] <-> B-
C+ <-> [ C magnetic/electrical axis ] <-> C-
```

Candidate functions on each magnetic axis:

```text
POWER / DRIVE
CONTROL / WRITE
SENSE
FEEDBACK / MAINTAIN
```

The exact number of physical windings is determined by core geometry and measured behavior. Six external edge ports do **not** require six windings.

## One hex must connect to another identical hex

The first scale test is not merely whether one magnetic core remembers. It is whether a completed CELL_V1 module can pass a controlled state through a canonical flat edge to an identical neighbor.

```text
CELL 1                         CELL 2
A+ B+ C+ A- B- C-   ||   A+ B+ C+ A- B- C-
                     ^
                shared flat edge
```

Shared edges pair matching axes with opposite outward polarity. No corner connectors or adapter cell are introduced.

## Seven-cell flower - first planar field unit

```text
                 [HEX]
             [HEX] [HEX]
          [HEX] [CENTER] [HEX]
             [HEX] [HEX]
```

The exact drawing geometry is flat-edge hex tiling: one center CELL_V1 plus six identical same-orientation CELL_V1 neighbors.

Every one of the seven cells contains the same A/B/C internal implementation.

The flower is the first place to test:

- cell-to-cell path propagation;
- closed circulating phase/state;
- competing routes;
- retained local memory affecting later whole-flower behavior;
- combined field state without erasing each cell's local identity.

## Scaling rule

The core recurrence remains:

```text
ONE HEX CELL
     ->
PATH THROUGH IDENTICAL CELLS
     ->
CLOSED ROTATION
     ->
SEVEN-CELL / MULTI-CELL FIELD
     ->
3D VOLUME
     ->
NEXT-SCALE POINT
```

Compact form:

```text
Point -> Path -> Rotation -> Field -> Volume -> next-scale Point
```

Real-hardware grounding changes how one hex is implemented internally. It does **not** replace this scaling rule.

## 3D / volumetric growth

A current candidate is `3 x 3 x 3` recurrence. The exact lower-scale unit is still open: individual cells, flowers, or resolved submodules may eventually be the right grain.

The rule is that the lower-scale unit must expose a reusable relational interface so the architecture can repeat rather than inventing a new connector at every scale.

A mirror-flipped companion volume remains a later candidate for whole-state history, checking, and reinjection.

## Six-MOSFET power stage inside the cell

Six MOSFETs can form three A/B/C half-bridges:

```text
            +DC BUS
         |     |     |
        A_H   B_H   C_H
         |     |     |
         A     B     C
         |     |     |
        A_L   B_L   C_L
         |     |     |
            -DC BUS
```

This is a grounded power-stage mechanism. It is **not** the cell's external six-port geometry.

## Reference and reinjection

The electrical reference remains a separately generated, measured node. Empty space or a core center does not create virtual ground.

Returned energy uses the regenerative-drive pattern:

```text
magnetic / inductive return
          |
      bridge / steering
          |
       DC-LINK CAP
          |
 later permitted event
```

Do not dump flyback energy into the virtual reference.

## Shared magnetic floor

A shared magnetic substrate remains an experiment, not a required first build.

Required proof:

```text
write at known location
remove drive
measure remanence locally
probe neighboring locations
compare later response with and without prior write
```

Only repeatable spatial history dependence earns the substrate a role in the scalable cell.

## Build order - keep the scale path intact

1. Prove one multifunction magnetic element.
2. Reproduce measured A/B/C internal axes.
3. Package or emulate them as **one complete CELL_V1 hex**.
4. Prove one flat-edge transfer between two identical hexes.
5. Prove a three-cell path.
6. Prove a closed circulating state/phase.
7. Build the seven-cell flower.
8. Test stacked / volumetric coupling.
9. Only then test mirror-flipped higher volumes and brain-scale organization.

The cell is not established merely because one core remembers. CELL_V1 is established only when the **hex module** can retain/process state, communicate through its locked edges, and scale through identical copies.

## Real-world references

- Fluxgate excitation / feedback / induction windings: <https://www.mdpi.com/1424-8220/25/8/2360/html>
- Saturable reactor with bias, maintaining/control, and power windings: <https://patents.google.com/patent/US2958816A/en>
- Magnetic-amplifier motor control: <https://patents.google.com/patent/US2844779A/en>
- Transfluxor write/read/sense magnetic memory: <https://patents.google.com/patent/US3328785A/en>
- Planar transfluxor / flux-logic magnetic sheet memory: <https://patents.google.com/patent/US3206733A/en>
- TI six-NMOS three-phase gate driver: <https://www.ti.com/product/DRV8363-Q1>
- Infineon regenerative DC-link behavior: <https://www.infineon.com/dgdl/Infineon-UG2020_28_REF-22K-GPD-INV-Easy3b-UserManual-v01_00-EN.pdf?fileId=5546d46277fc7439017802de2ffb672a>

## Hard separation rule

```text
HEX CELL + EDGE SCALING
        !=
MAGNETIC WINDING COUNT
        !=
POWER SWITCH COUNT
        !=
BRAIN LAYER COUNT
```

The first line is the architecture. The others are implementation choices that must earn their final form through measurement.


---

## Engineering reference boundary

The component precedents in this pamphlet are grounded as follows:

- TLE2426 virtual midpoint/reference: https://www.ti.com/product/TLE2426
- conventional three-phase BLDC bridge/commutation: https://onlinedocs.microchip.com/oxy/GUID-3AFF556D-77AD-488F-9A04-CD7AAB8F7DBC-en-US-1/GUID-A1DD3CA4-D59F-45CF-AA9F-EBBCB9EF37BA.html
- fluxgate excitation/core/sense structures: https://www.mdpi.com/1424-8220/21/4/1500
- memristive processing-memory research: https://www.nature.com/articles/s41467-024-45670-9
- STT-MRAM magnetic nonvolatile memory: https://www.nature.com/articles/s44287-024-00111-z
- historical transfluxor NDRO ferrite memory: https://www.bitsavers.org/pdf/afips/1959-03_%2315.pdf

These references validate the **existence and behavior of the referenced mechanisms separately**.

They do **not** validate the combined CELL_V1 hex, its proposed three-axis processing-memory behavior, reinjection loop, flower scaling, or brain interpretation. Those remain experimental until their own physical receipts pass G-778.
