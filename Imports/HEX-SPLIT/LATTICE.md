# Superfluid crystal lattice

Stay on target. This is the medium. Clocks, fifths, and gravity outfits are readings of it.

Gate: **YELLOW**. Geometry in this repo is exact. The fluid claim is not.

## What the lattice is

A **crystal** so a site has neighbors you can count:

- D-408 — 2D six-neighbor (the hex floor)
- D-409 — 3D twelve-neighbor close pack (the standing-up 12)

A **superfluid** so a site has a phase that can lock, slip, or sit in a dead belt — not a bag of pellets.

```
site = { facing, polarity, sheet, κ }
```

- facing — which pyramid wall (1..6)
- polarity — Express / Compress (face / flip)
- sheet — `lap` 0|1 (2π vs 4π wind)
- κ — stiffness. How hard a write is on that site.

No second substance called time. Time is the cost of moving through this.

## Shapes (jobs, not three worlds)

```
hex     = the slice     — neighbors in a plane
cube    = the stack     — slices piled; a cell you can count
sphere  = the rotation  — the stack allowed to turn
```

Full law: `SHAPES.md`.
Hex without stack is a floor plan. Stack without rotation is a brick. Sphere without hex is a ball with no neighbors.

## Time, on target

    τ = ∫ κ |ds|

- ds is a walk on the 12-slot clock, not a cesium tick.
- Default live generator is **+7** (fifths weave).
- **+6** is flip on the same pyramid.
- **+1** is the diagnostic walk. If +1 and +7 cost the same, κ is constant and this file is a caption.
- polarity 0 / hold ⇒ no ds. Wall-clock may run. Lattice time does not.

NTP/PTP measure oscillator mismatch on an envelope. They do not set phase. They do not measure κ.

## Crystal part (kickable now)

HEX-SPLIT already prints the floor:

- 6 triangles from the centroid
- 6 pyramids up
- 3 opposite-pair hallways (M4 picks one)

If a hex print and a square control of equal mass and perimeter make the same lobes, the crystal is packaging. That falsifier is already in THEORY.md. Keep it.

## Superfluid part (not proven here)

Lock, slip, vortex, critical write:

- below the dead belt — hold. No tick.
- opposed rings at full drive — quit. Defect instead of a hallway.
- sheet / lap — winding. If flipping lap never changes cost, drop the bit.

GRAV-LAB owns alignment / parent proximity / heat-so-it-does-not-freeze-dead. This file does not steal that servo. It names the medium those locks sit in.

Do **not**:

- promote fifths to a force
- glue B-lobes to +7 until a print beats a square
- call κ settled
- let GPU dream packets commit phase
- let a sphere steal the slice's job

## Falsify

1. +1 chromatic and +7 fifths produce the same hit/hold pattern on BUCKET or GCAC at the same wall-clock rate.
2. Phase advances on hold.
3. Hex print ≡ square print (crystal was the magnet shape).
4. Child with no alignment channel locks on the same clock as an aligned twin (GRAV-LAB already holds this).
5. Hex print acts like a sphere lock with no stack in between — slice stole rotation.

Until one of those is run, this stays YELLOW.

## Homes

- HEX-SPLIT — floor plan + 12 slots + this file + SHAPES.md
- GRAV-LAB — lock servo + SCALE_LADDER floors
- POINT-SPIN — rotation object (4π)
- GCAC — millivolt write / dead belt
- BUCKET-R2 — one gray sticker per earned move
- SYNC.md — who may commit a step
- Library card: SUPERFLUID-LATTICE
