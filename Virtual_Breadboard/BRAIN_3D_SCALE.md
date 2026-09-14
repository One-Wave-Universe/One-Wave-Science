# 3D electrical brain — scalable build

One cell. Then a slice. Then a stack. Then two stacks. Same law every time.
You do not get a new brain by inventing a seventh gate.

```
X Y     hex slice     6 cells around one G ring = one hexagon
Z       cube stack    slices sharing a vertical mid spine
2       hemispheres   Field stack + Void stack, midline G
```

hex = slice. cube = stack. sphere = rotation of the walk (A→B→C and the other way).

## Level 0 — one brain cell (F0, build this)

Already specified in `ONE_WAVE_CELL.md` + `brain_2state.py` + `nerve_cell.py`.

```
Field / Void     software or two tiny MCUs
3 gates          A B C half-bridges
STAR G           blue, I_0
sensor cell      heat vibe Hall on that star
```

That *is* the electrical brain cell. 2-state + 3 nerves + mid.

## Level 1 — hex slice (6 cells, one ring)

Six copies of Level 0 around a **shared G ring**. Neighbor stars tap the same blue with short jumps. No series C in the ring.

```
    C1
 C6    C2
 C5    C3
    C4
      G ring home → I_0_slice
```

Each cell still has its own A B C and its own sensor cell.
Slice Field lists a lean *for a cell index*. Slice Void can cut that cell or the whole ring.
Walk around the ring is rotating B in the plane (the hex slice).

Power: one ±12 for the slice, per-cell STAY default. Don't drive six leans at once on F0 supplies.

## Level 2 — Z stack (cube)

Two or more hex slices, G rings tied by a **vertical spine** (the mid going home through the stack). That is the cube: slice stacked on slice.

```
slice 2   G2 ───┐
slice 1   G1 ───┤ spine → controller
slice 0   G0 ───┘
```

Z-neighbor coupling is only through G and through leftover B / Hall, not a new bus of chat.
A lean on slice 1 that slams I_0 on the spine is a slice problem — Void sees it at home.

Scale ladder you already named: cell → cube (stacked cells) → Rubik (stacked cubes) → two Rubiks (two hemispheres, one midline).

## Level 3 — two hemispheres

```
Field stack     explorer     may list leans
Void stack      checker      engage / override
midline G       spine they share
```

Not two different electronics religions. Same cell hardware. Different *right* to command. Field never grabs engage. Void never invents torque.

## What scales and what does not

Scales: the cell schematic, STAY default, local reference as the free update, sensor cell triad, I_0 home, pulse-not-PWM-hold.

Does not scale on a breadboard: 36 half-bridges, six Halls, a 2212 farm. Next physical step after one cell works is **two cells on one G**, not a 6×6×2 cathedral.

Wiring rule at every scale: star G locally, short tap to the spine, RC across the station, never a cap in the spine.

## Software scale

```
Brain.tick(...)           one cell
for cell in slice:        same Thought schema
spine.i_0                 Void input for the slice
```

No new noun. `live` becomes `(cell, winding)` when there are many cells.

## Done at each level

| level | pass |
|---|---|
| 0 | one cell receipt (ONE_WAVE_CELL §5) |
| 1 | two cells share G, one STAY while the other +1, I_0 readable |
| 2 | two slices, spine I_0, one slice quiet |
| 3 | Field list on left stack cut by Void on the midline |
