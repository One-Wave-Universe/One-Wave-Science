# G-732 — Vortex Trial-Profile Diagnostic Repair

**Status:** YELLOW diagnostics / stationary bound mode open  
**Dependencies:** A-107, B-226, G-727, G-728

## Closed diagnostic corrections

- The complex line-vortex dilation integrals are analytic:
  `I1=(5/2)pi^(3/2)sigma`, `I3=(35/4)pi^(3/2)/sigma`.
- At `sigma=2`, `lambda*=sqrt(7/8)`.
- Closed-loop winding uses wrapped complex phase increments.
- Line and toroidal charge require differently linked loops.
- Periodic fourth-order evolution is measured with the same discrete operator
  used by the update.
- The exact leapfrog quadratic invariant is tracked at half steps.
- Toroidal core search is restricted to a declared annulus because the outer
  localized envelope also approaches zero.

## What remains open

The dilation minimum is necessary only along one variational direction. It is
not proof of a stationary solution or stability against splitting, radiation,
shape deformation, translation, or ring-radius contraction. The linear
constant-coefficient equation has no nonzero localized square-integrable
harmonic eigenmode on unbounded space. A nonlinear or self-consistent coupling
must be declared, derived, and tested before the B-226 recursion floor passes.

## Executable authority

- `One_Wave_Bench/micro/vortex_diagnostics.py`
- `One_Wave_Bench/micro/test_vortex_diagnostics.py`
