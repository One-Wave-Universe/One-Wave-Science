# Challenge 03 — Three-Body Dynamics

**Target:** L2/L3 mathematical recovery first; L4 only if One-Wave produces a distinct quantitative result.

## Standard problem

The Newtonian three-body problem has exact special solutions and excellent numerical solutions, but the generic problem is nonintegrable and can be chaotic. The One-Wave target is **not** to claim that there are no solutions. The working hypothesis is that the difficulty is partly representational: treating the system as a sum of local pairwise interactions may hide a more natural **nonlocal whole-system state**.

## One-Wave question

Can the three bodies be represented as one nonlocal relational state whose Point -> Path -> Field update is defined for the **whole configuration at once**, rather than as three independently updated bodies plus pairwise corrections?

The key hypothesis is:

```text
local pairwise bookkeeping
        ↓ may obscure
one simultaneous nonlocal relational state
        ↓
whole-system update
        ↓
local body trajectories as outputs
```

The mathematical task is to determine whether this whole-state formulation is merely a coordinate rewrite of ordinary mechanics or whether it exposes a genuinely simpler invariant, closure law, or prediction.

## Minimum mathematical program

1. Start from the already-recovered (1/r^2) radial interaction candidate.
2. Write three relational pair vectors (r_{12},r_{23},r_{31}) with the closure identity
   [
   r_{12}+r_{23}+r_{31}=0.
   ]
3. Derive the full equations of motion from one common **whole-state update rule**, then show how ordinary pairwise forces emerge as a limit or projection if they do.
4. Recover standard total linear momentum, angular momentum, and energy conservation.
5. Transform to center-of-mass/Jacobi or an equivalent relational representation.
6. Reproduce at least:
   - Euler collinear solutions;
   - Lagrange equilateral solutions;
   - restricted-three-body Lagrange points;
   - one known chaotic trajectory under identical initial conditions.
7. Only after recovery, ask whether Point/Path/Field supplies a new invariant, regularization, or bounded-error representation.

## Nonlocality criterion

Calling the formulation "nonlocal" is not enough. It must show mathematically that at least one state variable or update cannot be decomposed into independent pairwise contributions without loss of information.

Candidate tests:
- a global closure constraint that changes the update of all three bodies simultaneously;
- a conserved whole-state quantity not reducible to a sum of pair terms;
- a reduction in dimensionality or singular behavior compared with pairwise coordinates;
- a distinct measurable prediction under matched initial conditions.

If every update can be algebraically reduced to ordinary pairwise Newtonian interactions, then the formulation is relational but not physically new nonlocal dynamics.

## What would count as novelty

A new coordinate grammar is not enough.

A strong result would be one of:
- a genuinely new exact family of solutions;
- a new integral/invariant under clearly stated conditions;
- a rigorous regularization that simplifies a known singular/chaotic regime;
- a quantitative prediction distinguishable from Newtonian/GR dynamics.

## Failure condition

If the Point/Path/Field formulation is only a relabeling of standard three-body equations and yields no new invariant, simplification, or prediction, classify it as **L3 recovery**, not a new solution of the three-body problem.
