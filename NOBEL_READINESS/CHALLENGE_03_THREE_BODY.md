# Challenge 03 — Three-Body Dynamics

**Target:** L2/L3 mathematical recovery first; L4 only if One-Wave produces a distinct quantitative result.

## Standard problem

The Newtonian three-body problem is deterministic but generally nonintegrable. It has important exact/special solutions, perturbative regimes, KAM-stable regions, chaotic regions, and high-quality numerical solutions. The prize-level target is **not** to claim that nobody can calculate three bodies.

## One-Wave question

Can the Point -> Path -> Field recursion produce the coupled three-body equations or an equivalent reduced law **without adding body-specific fitted terms**, and does the resulting formulation expose a conserved/reduced structure not obvious in the ordinary coordinates?

## Minimum mathematical program

1. Start from the already-recovered (1/r^2) radial interaction candidate.
2. Write three relational pair vectors (r_{12},r_{23},r_{31}) with the closure identity
   [
   r_{12}+r_{23}+r_{31}=0.
   ]
3. Derive the full equations of motion from one common interaction rule.
4. Recover standard total linear momentum, angular momentum, and energy conservation.
5. Transform to center-of-mass/Jacobi or an equivalent relational representation.
6. Reproduce at least:
   - Euler collinear solutions;
   - Lagrange equilateral solutions;
   - restricted-three-body Lagrange points;
   - one known chaotic trajectory under identical initial conditions.
7. Only after recovery, ask whether Point/Path/Field supplies a new invariant, regularization, or bounded-error representation.

## What would count as novelty

A new coordinate grammar is not enough.

A strong result would be one of:
- a genuinely new exact family of solutions;
- a new integral/invariant under clearly stated conditions;
- a rigorous regularization that simplifies a known singular/chaotic regime;
- a quantitative prediction distinguishable from Newtonian/GR dynamics.

## Failure condition

If the Point/Path/Field formulation is only a relabeling of standard three-body equations and yields no new invariant, simplification, or prediction, classify it as **L3 recovery**, not a new solution of the three-body problem.
