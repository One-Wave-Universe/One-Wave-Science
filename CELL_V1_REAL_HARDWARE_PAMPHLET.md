# CELL_V1 - Real-Hardware Bench Pamphlet

## What is real, and what CELL_V1 adds

CELL_V1 does not start from nothing. Its current physical direction combines mechanisms that have already been built separately:

- **Fluxgate sensors:** one magnetic core with separate excitation, sense, and feedback functions.
- **Magnetic amplifiers / saturable reactors:** control and maintaining windings that change a larger power path through magnetic saturation.
- **Transfluxor memory:** remanent magnetic state, separate write/read/sense paths, and non-destructive readout concepts.
- **Three-phase motor bridges:** six MOSFETs arranged as three A/B/C half-bridges.
- **Regenerative inverters:** inductive/motor energy returned to a DC-link capacitor.

The combined CELL_V1 topology remains experimental.

## Locked CELL_V1 geometry

```text
FLAT EDGE PORTS ONLY

clockwise:
A+ -> B+ -> C+ -> A- -> B- -> C-

opposites:
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

The six edge labels are external cell interfaces. They are not six mandatory magnetic windings.

## Preferred first magnetic element

Instead of an ordinary toroid with six arbitrary windings, test one multifunction magnetic element with separately measurable functions:

```text
POWER / DRIVE
CONTROL / WRITE
SENSE
FEEDBACK / MAINTAIN
```

The exact number of physical windings is determined by the actual core geometry and measured behavior.

A toroid may be useful for the first excitation/sense test. A multi-aperture or shaped ferrite may be better for nonvolatile magnetic memory because transfluxors deliberately separated magnetic paths.

## Three-element A/B/C bench fixture

After one element passes write-retain-read-rewrite testing, copy it into three matched elements:

```text
                 [ A ]
                  / \
                 /   \
              [ C ]-[ B ]
                   o
              REFERENCE
```

The physical triangle is a useful symmetric fixture, not a law derived from 120 electrical degrees.

The center `o` is the measured electrical reference. Empty geometric space does not create virtual ground.

## Six-MOSFET power stage

Six MOSFETs are used as three half-bridges:

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

This is standard three-phase bridge architecture. It does not mean six independent bidirectional winding channels exist.

## Reinjection / recovery

Use the engineering pattern already used in regenerative drives:

```text
magnetic / inductive return
          |
      bridge / steering
          |
       DC-LINK CAP
          |
 later permitted event
```

Do not dump flyback energy into the virtual reference. Keep the reference quiet and measured.

## Shared magnetic floor

A shared magnetic substrate remains an experiment.

Do not assume an ordinary ferromagnetic nanoparticle sheet stores useful spatial memory.

Required proof:

```text
write at A
remove drive
measure remanence
probe A/B/C locations
compare response with and without prior write
```

Only repeatable spatial history dependence earns the substrate a role in CELL_V1.

## First build - smallest decisive test

Build one multifunction element first.

1. Measure normal inductive behavior.
2. Apply controlled write pulse.
3. Remove drive completely.
4. Read retained state with minimal disturbance.
5. Reverse write and repeat.
6. Show old state changes the standardized next response.
7. Measure returned energy into the reservoir independently.
8. Only then build matched A/B/C copies.

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
HEX INTERFACE GEOMETRY
        !=
MAGNETIC WINDING COUNT
        !=
POWER SWITCH COUNT
        !=
BRAIN LAYER COUNT
```

Prove each layer with measurements before tying the counts together.
