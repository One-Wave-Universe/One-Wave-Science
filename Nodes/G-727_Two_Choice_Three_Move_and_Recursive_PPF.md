# G-727 — Two Choice, Three Move, and Recursive Point–Path–Field

**Status:** YELLOW finite logic / proposed dynamics  
**Dependencies:** B-208, B-216, B-222, B-223, B-224, D-408, D-409, D-410

## Canonical primitive

The decision primitive is one-hot binary: YES `(1,0)` or NO `(0,1)`.
Ground `(0,0)` is no committed choice, and `(1,1)` is conflict. Movement is
DOWN, HOLD, or UP. The combined address space is therefore `2 x 3 = 6`.

The five downstream commitment amplitudes are not another choice axis. Their
map from route, phase, differential, history, and threshold remains to be
derived.

## Recursive geometry

At every scale, keep three kinematic roles distinct:

- Point rotation: local/intrinsic orientation;
- Path rotation: curvature or circulation of the transported center;
- Field rotation: circulation of the enclosing carrier/boundary.

Any Point, Path, or Field may contain lower-scale Point–Path–Field states. The
solver must therefore carry frame transforms and receipts across nesting
boundaries instead of replacing all rotations with one angular velocity.

## Dimensional recurrence

The candidate Mirror-Gate sequence remains:

```text
3 > 1(0)1 < 6    2D
6 > 1(0)1 < 12   3D
12 > 1(0)1 < 24  4D recurrence state
```

Matching counts are evidence of a pattern, not a derivation. Adjacency,
spectra, isotropy, transform invariants, and projection error must establish
what survives between dimensions.

## Orbital guardrail

One Wave may add mechanism state, but orbital calculations retain Newtonian
and appropriate relativistic controls. Candidate corrections are reported as
`a=a_Gray+delta_a_OW`, must vanish to the Gray limit, and must improve held-out
tests without degrading conserved quantities or established orbital results.

## Executable reference

- `One_Wave_Bench/logic_core/six_route_logic.py`
- `One_Wave_Bench/logic_core/test_six_route_logic.py`
- `UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md`
- `MATH_ATTACK_MAP_UPDATED_43.md`

