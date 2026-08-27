---
id: G-738
title: Center Geometry Classification and Receipt
status: yellow
tier: executable-math
claim_boundary: trajectory classifier; does not declare one universal physical center geometry
---

# Node G-738: Center Geometry Classification and Receipt

## Purpose

The shared center must not be silently collapsed into a single point. A measured
trajectory can encounter several distinct structures:

1. **point residence**: both displacement and scaled velocity are near zero;
2. **finite center band**: displacement remains within a declared nonzero band;
3. **crossing section**: displacement changes sign with nonzero velocity;
4. **limit-cycle section**: repeated same-direction crossings recur with bounded
   return time and speed dispersion;
5. **slow-manifold candidate**: motion inside the band is slower than motion
   outside it for a declared time-scale ratio.

These receipts are compatible with G-731: Ground, center residence, center
crossing, movement Hold, and coherent Hold remain different measurements.

## Declared variables

Let (x(t)) be displacement from the chosen center coordinate and (v(t)) its
velocity. Units are declared by the caller. Thresholds inherit those units:

- (epsilon_x): point tolerance for (x);
- (epsilon_v): point/Hold tolerance for (v);
- (b_x>epsilon_x): finite-band half-width;
- (ho_T): maximum coefficient of variation for recurrent return times;
- (ho_v): maximum coefficient of variation for crossing speeds;
- (kappa>1): minimum outside/inside median-speed ratio for a slow-manifold
  candidate.

A crossing at samples (i,i+1) is detected when (x_i x_{i+1}<0). Linear
interpolation gives

[
t_	imes=t_i+rac{-x_i}{x_{i+1}-x_i}(t_{i+1}-t_i).
]

The direction is the sign of the interpolated velocity. Point residence requires
both (|x|leepsilon_x) and (|v|leepsilon_v); a fast center crossing is
therefore never mislabeled Hold.

## Executable decision boundary

The implementation emits independent booleans and raw statistics. They are not
mutually exclusive ontologies. In particular, a stable limit cycle may possess
a crossing section and a finite observational band while having no point
residence.

A limit-cycle section candidate requires at least three same-direction
crossings plus both return-time and crossing-speed dispersion below their
declared tolerances. A slow-manifold candidate requires samples both inside and
outside the band and a median outside/inside speed ratio at least (kappa).

## Result and gate

Deterministic reference trajectories distinguish:

- harmonic center crossings from turning-point Hold;
- equilibrium point residence from a fast crossing;
- recurrent low-dispersion sections from irregular returns;
- finite-band slow motion from ordinary passage.

This closes B2 as executable classification math. It does **not** decide that
all One-Wave systems share one center type. Physical selection remains local to
the simulator, variables, units, boundary, and evidence.

**Brick recommendation:** Yellow.
