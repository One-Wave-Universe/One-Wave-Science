# Deeper lattice architecture

How OW1F + GRAV-LAB go down one more floor without inventing a new religion.

## Both packs

Run `python sim/lattice.py`. Stacked-hex is the working volume. FCC-12 is the same sites with a stricter neighbor rule. Compare receipts on the *same* `(m,n,p)` slab. If FCC does not change lock@ vs stacked, 12-NN was decoration for that test.

## Architecture already in canon (do not skip)

From One-Wave-Science `ARCHITECTURE_POINT_PATH_FIELD_SCALE_RECURSION.md`:

```
state     = Field | Void          # site.field_void
polarity  = route direction       # neighbor k, or q facing
M4        = path coordinator      # header.m4_pair, not memory
ternary   = mirrored whole        # trit of the 7-cluster, not a third voltage
Delta     = MirrorA - MirrorB     # admin output
Field(n)  = Point(n+1)            # octave / scale compression
```

Deeper is this ladder on the D-408 stencil, not more floats per cell.

## Seven-cell is the path

Center = point.
Six ring = path candidates (three axis pairs).
Resolved ring differential + hold = field of that scale.

Update order (prototype, already listed in that architecture note):

1. Field/Void holds on the site (P and field_void).
2. Polarity is facing / neighbor index — not a second stored bit pretending to be state.
3. Six + M4 geometry (we have verts + m4_pair).
4. Two mirrored wholes (axis pair + flip, HEX face/flip).
5. Signed Delta between mirrors (GCAC two-Rubik vote is the same shape at brain scale).
6. Magnetic / align channel retains Field/Void after the route (align=0 insulator falsifier).
7. That Delta is the *point* handed to the next octave floor.
8. Same law, next `a' = 2a` or next sheet-block. If the law changes, it was not scale.

## What “deeper” is this week

- Wire `cluster7` into `parent_lock`: parent line = M4 pair direction in XY.
- `psi` average only over the six ring + center, not a cubic halo.
- `trit` computed as consensus of the cluster, written back to center only.
- Field sites (`field_void=1`) may lock. Void sites sit. Dream Engine writes Void, not Field.
- One octave test: coarse lattice with `a2=2a`, each coarse point = resolved Delta of its 7-fine-cluster. If coarse lock@ does not track fine lock@, compression failed.

## What deeper is not

- Not cubic voxels.
- Not helium.
- Not merging 6:1, 3:1 axis, 3:1 gate, 12-tone, 12-NN.
- Not simulating the whole lattice flowing by default.
