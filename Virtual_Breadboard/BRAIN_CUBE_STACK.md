# Cube stacking method

A cube is not six new faces of electronics. It is **hex slices stacked on one spine**.

```
        slice 2   (hex ring, local G2)
           |
        slice 1   (hex ring, local G1)
           |
        slice 0   (hex ring, local G0)
           |
         SPINE    = mid home = I_0_stack
```

Each slice is Level 1: cells around a **local** G ring, referenced at every station (the free update). The stack only adds a short tap from each ring to the vertical spine. That tap is the Z axis — DC clothes copied upward, AC stays in the slice, RC is still the window inside each cell.

## Electrical rules

1. Local G first. A cell references its ring, not a far slice.
2. Spine is solid. No series C in Z. No daisy-chain of 0 around the rim then up a spaghetti lead.
3. One I_0 meter at the bottom of the spine for the whole cube. Per-slice shunts optional if Void needs to see *which* floor yelled.
4. Default STAY on every cell. Stacking does not mean more things ON.
5. A lean on slice 1 must not require slice 0 to invert. If it does, you built a puppet, not a stack.
6. Leftover B stays in the cell / slice that earned it. Reinjection is local. The spine carries imbalance, not memory.

## Mechanical picture

One floor = one hexagon of cells (or, F0, two cells on a ring — a cube face).
Floors spaced so the spine is short. Power ±12 can be common; 5 V puck power starred per floor.

Two cubes side by side + one midline spine = the two-hemisphere brain (Field cube, Void cube). Same hardware. Different right to list vs cut.

Rubik scale = cubes stacked until you have three axes of floors. Still the same tap rule.

## What you actually stack on the bench

Not 27 cells. **Two rings, three wires:**

- ring 0 G → spine
- ring 1 G → spine
- spine → I_0 → supply 0

Prove: ring 0 +1, ring 1 STAY, I_0 moves, ring 1 Hall quiet. Then swap. That is a cube of height 2.

## Falsify

- Chat bus between slices instead of G
- Cap in the spine
- PWM hold on the bottom floor to “stabilize” the top
- One Field script driving every floor's engage
