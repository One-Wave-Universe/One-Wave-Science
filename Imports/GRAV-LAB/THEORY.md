# GRAV LAB

Bench. One field. Scale views, not two forces glued together.

Medium: superfluid crystal lattice. Named in HEX-SPLIT `LATTICE.md`. This repo does not own the floor plan. It owns **lock** on that fluid.

## Field

- **alignment** — local phase inside the cells
- **lock** — that phase at rest on a spinning body
- **point rotation** — a site writes its phase onto neighbors
- **parent proximity** — a bigger rotator writes its phase onto a child

A point is a site with phase and spin sense. Not a pellet of stuff.

    ψ_i^{n+1} = ψ_i^n + (1-γ)(ψ_i^n - ψ_i^{n-1}) + β(⟨ψ_j^n⟩ - ψ_i) + τ_parent

- γ inertial memory
- β neighbor restore
- τ_parent from proximity and alignment mismatch
- hold (ternary 0 / dead zone) is legal

Lock = child facing stops walking relative to the parent line.

Time, if you must say it here: how hard that write is (κ on the lattice). Not a cesium envelope. Heat keeps the lock from freezing into a dead crystal — stiffness without flow is just ice.

## Three stacked locks

1. **geometry** — a hex / sphere has a facing. Opposite face is the midline.
2. **rotation** — child's spin period matches the trip around the parent.
3. **alignment** — parent's phase at the child is strong enough that hold-against-parent costs more than facing-the-parent.

Near: alignment can win.
Far: geometry + rotation can still sit the face.
Body-lock (rock face) and field-lock (fluid co-rotation) are different receipts. Do not smash them.

## Octave cascade

Same 3:1 gate at every scale.
Millivolt = override.
Microvolt feeling = inverted, no vote.
Heat = outside-the-cell bath so the lock does not freeze into a dead crystal.

## Falsifiers

- Child with no alignment channel locks on the same clock as an aligned twin → alignment was a passenger for that pair.
- Face sits because you clamped spin and parent phase by hand → not a lock.
- `parent_lock.py` never enters the hold belt → burn the file.
- Hex print and square control show the same lobes → crystal was packaging (HEX-SPLIT).
