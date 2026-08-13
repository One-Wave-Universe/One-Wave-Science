---
node_id: "D-435"
canonical_name: "Twelvefold-Shell Rotation-Group Closure (Order 24, No 6/12-Fold Periodicity)"
namespace: "NODE"
gate: "BRONZE"
lifecycle: "ACTIVE"
classification: "Discrete Symmetry Geometry / Ratio-Domain Numerology Guardrail"
claim_gate_detail: "BRONZE (reproducible group-theoretic result for the idealized D-409 point set) / YELLOW (physical significance for actual lattice dynamics, unestablished)"
metadata_standard: "I-06"
---

# Node D-435: Twelvefold-Shell Rotation-Group Closure

**Origin note:** this node did not start as a hypothesis to prove. It
started as a backlog placeholder titled "6:1 / 1:12 Rotational Closure
Relation" (see `RELATIONAL_MECHANICS_NODE_BACKLOG.md`'s Evidence
Dossier for that retired backlog row) with no content behind the
title. Exhausting the existing evidence against that title found the
counting relationship already fully stated in D-409 and D-411 — that
original backlog meaning is therefore retired, with no node built for
it. This node is the one genuinely new, non-redundant
question that exhaustion surfaced, investigated on its own terms and
promoted only after the derivation actually held up.

**Dependencies**
Upstream: D-409 Twelvefold 3D Close-Packed Coordination (this node's entire geometric source — the point set analyzed below is D-409's own `N_12`, not a new geometry)
Lateral: G-716 One-Wave Conversion Grammar, D-411 Mirrored Axis Pairs and Directed Route Counts (corrective boundary on numeral interpretation — see Non-Claims below)
Non-equivalence only (not a real dependency): C-301 Mirror Gate (see Explicit Non-Equivalence Warning below)
Downstream: none yet — no simulation or physical node currently uses this result

## Core Claim (stated first, not as a footnote)

**D-409's twelve-point neighbor shell has a finite spatial rotation
group of order 24, with element orders 1, 2, 3, and 4 only. No
order-6 or order-12 rotational closure exists for that shell.**

This is a negative result and is filed as first-class content, not a
qualifier: it directly refutes the reading that "twelve neighbors"
implies twelve-fold rotational periodicity, or that "six opposite
pairs" implies six-fold periodicity. Neighbor-count and
rotational-closure order are not the same quantity, and this node is
the guardrail against silently assuming they are.

## Method

D-409 defines its twelve-neighbor shell explicitly:

\[
\mathcal N_{12}
=
\frac{a}{\sqrt2}
\left\{
(\pm1,\pm1,0),
(\pm1,0,\pm1),
(0,\pm1,\pm1)
\right\}
\]

This node analyzes that exact point set — no substitute geometry, no
borrowed result. `Integrity_Tools/verify_d409_rotational_closure.py`
constructs the twelve points directly, then searches numerically for
which rotations map the set onto itself, rather than asserting a
textbook answer. The search is a direct computation, reproducible by
running the script.

## Mathematics

The point set `N_12` is exactly the set of cube edge-midpoints (a cube
with vertices `(±1,±1,±1)` has twelve edges; each midpoint is a point
with one coordinate `0` and the other two `±1`, which is `N_12`).
Its rotational symmetry is therefore the cube's own proper rotation
group, verified directly against the point set rather than assumed
from that identification:

```text
3 four-fold axes  (through opposite square faces): rotations of order 4 and 2
4 three-fold axes (through opposite triangular faces): rotations of order 3
6 two-fold axes   (through opposite edges): rotations of order 2
1 identity
```

Generating the group numerically from one order-4 element (90° about a
face axis) and one order-3 element (120° about a vertex axis) and
closing under composition produces:

```text
full rotation group order:        24
element order distribution:       {1: 1, 2: 9, 3: 8, 4: 6}
max single-element order:         4
order-6 element exists:           False
order-12 element exists:          False
```

Direct exhaustive check over a single 4-fold axis (all integer degrees
1 through 359) confirms only 90°, 180°, and 270° preserve `N_12` — no
finer rotation does, and in particular no 30° (order 12) or 60° (order
6) rotation does.

\[
\boxed{
|G| = 24,\qquad
\text{element orders} \in \{1,2,3,4\},\qquad
6 \notin \text{orders},\quad 12 \notin \text{orders}
}
\]

`G` is isomorphic to `S_4` (the symmetric group on four elements), the
same group as the cube/octahedron rotation group, acting faithfully on
the twelve edge-midpoints as it acts on the twelve edges themselves.

## Invariants

The full twelve-point set is invariant as a set (not pointwise) under
all 24 elements. Under a single four-fold axis, the twelve points
split into three orbits of four. Under a three-fold axis, into orbits
of three. Under a two-fold edge axis, two of the twelve points lie on
the axis itself (fixed, orbit size 1 each) and the remaining ten split
into five orbits of two.

## Non-Claims (the boundaries this node does not cross)

1. **This is a property of the idealized point set, not a proven
   property of any physical lattice.** It says nothing about whether
   actual One-Wave lattice dynamics respects, uses, or is constrained
   by this symmetry. A physically-motivated departure from the perfect
   cuboctahedral shell (anisotropic coupling, a perturbed lattice)
   could reduce the symmetry group and change these numbers.
2. **There is no single privileged rotation operator here**, unlike
   C-301's one distinguished `M`. The order-24 group contains elements
   of three different orders (2, 3, 4) depending on which axis family
   is chosen; there is no canonical "the" rotation for this shell.
3. **G-716's and D-411's own numerals are explicitly not the same
   quantity as this node's group order**, even where they share
   digits. G-716's `24` is a Field/Void recurrence-shell layer label
   (governed by D-410); D-411's `12:1`/`6:1` are neighbor-count and
   axis-pair-count views of the same shell this node analyzes, but
   counting neighbors is a different operation from finding a rotation
   group's order — the coincidence that this node's group order is
   also `24` is noted and explicitly **not** claimed as a connection to
   G-716's or D-410's `24`. Same digit, different quantity, not merged.

## Explicit Non-Equivalence Warning — C-301 Mirror Gate

C-301 and C-308 already establish a real, derived rotational closure:
`M^4 = I`, "4π closure," giving spin-half's defining property. This
node's rotation group also contains elements of order 4 (the four-fold
face-axis rotations). **This shared order-4 appearance is currently
only a coincidence across two unrelated mechanisms, not evidence of a
connection:**

- C-301's closure operates on an internal two-component `(psi_C,
  psi_E)` Mirror state under symplectic rotation; this node's closure
  operates on twelve explicit spatial points under ordinary 3D
  rotation. Different state spaces, different operators.
- No mapping has been proposed between the two, let alone checked.
- C-301 itself has an open question about whether its own mechanism is
  forced by geometry or defined as a boundary rule (CCD-03, still
  open) — asserting a link to this node's result would compound one
  open question with another rather than resolving either.

Per I-04, this is filed as no more than a noted coincidence pending an
actual proposed mapping. It must not be cited as if C-301 and D-435
were the same phenomenon at different scales.

## Reproducibility

```text
python3 Integrity_Tools/verify_d409_rotational_closure.py
```

The script asserts the group order is exactly 24, that no order-6 or
order-12 element exists, and that the surviving single-axis rotation
angles are exactly `{90, 180, 270}` degrees. It fails loudly (raises
an assertion error) if any of these does not hold, rather than
printing an unchecked result.

## Failure / Revision Conditions

This node fails or must be revised if:

- a different, physically-motivated neighbor-shell geometry (not
  D-409's idealized `N_12`) is later adopted as canonical and its
  rotation group is not recomputed against the new geometry;
- this result is cited as evidence for, or against, any claim about
  C-301, G-716, D-410, or D-411's own numerals without the explicit
  non-equivalence/non-identity boundaries above being restated;
- the negative result (no 6-fold or 12-fold closure) is quietly
  dropped from any future summary in favor of only the positive
  finding (order 24) — the negative result is the point of this node.
