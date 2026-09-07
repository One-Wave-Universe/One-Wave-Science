# Physics Experimental Wing

This directory is the aggressive expansion area for the One-Wave physics atlas. It is intentionally separate from `sims/` and from the stable `physics-atlas/` interface.

## Purpose

The wing is for models that need stronger quantitative controls, parameter sweeps, residuals, and visible failure modes before they deserve promotion into the stable atlas.

## Core runnable scenes

1. Orbit Integrator Duel — Euler versus velocity-Verlet energy drift.
2. Dispersive Wave Packet — explicit spectral toy model.
3. Coupled Mode Spectrum — classical normal-mode control.
4. RLC Resonance — normalized linear AC circuit control.
5. Thermal Diffusion — finite-difference transport control.
6. Point-Mass Lensing — weak-deflection / thin-lens geometry control.
7. Three-Body Ensemble — perturbed figure-eight sensitivity family.
8. Blackbody Spectrum — normalized Planck-law control.
9. Galaxy Curve Lab — Kepler, soft-core toy, and flat-target comparison.
10. Redshift Comparator — SR Doppler and exterior gravitational reference formulas.
11. Candidate Wake Families — exponential, logistic, and compact-support hypothesis cutoffs over a 1/r² reference.
12. Residual / Falsification Bench — relative RMSE against synthetic control data.

## Orientation & Quaternion Lab

Runnable at `orientation-quaternion/index.html`.

1. Quaternion axis-angle rotation.
2. Noncommutative composition order.
3. SLERP interpolation.
4. Euler gimbal-lock comparison.
5. Angular-velocity quaternion integration with raw-vs-renormalized tracks.
6. Torque-free asymmetric rigid-body dynamics.
7. Parent/child frame composition.
8. Three-phase resultant embedded in a quaternion-controlled 3D frame.

The rigid-body control has a separate `orientation-quaternion/VALIDATION.md` with its offline invariant check.

## Vector Field Topology Lab

Runnable at `vector-field-topology/index.html`.

1. Uniform field.
2. Radial source.
3. Vortex.
4. Saddle field.
5. Dipole source/sink pair.
6. Source + vortex superposition.

This lab measures finite-difference divergence and scalar curl over the rendered analytic field, exposing topology numerically instead of relying on arrows alone.

## Integral Field Theorem Lab

Runnable at `integral-field-theorems/index.html`.

1. Linear expansion field.
2. Solid rotation field.
3. Saddle field.
4. Mixed linear field with simultaneous nonzero divergence and curl.

This lab cross-checks local differential measurements against global integrals:

- boundary flux versus area integral of divergence;
- boundary circulation versus area integral of curl.

The purpose is to catch fields that look plausible locally but fail their global conservation/topology identity.

## Scientific separation

- `control` means a declared standard equation or numerical-control problem.
- `toy` means an explicit simplified model whose limitations are part of the UI.
- `hypothesis` means a candidate family that is allowed to be swept and rejected, but not silently promoted into a physical law.
- Every export records `solver_affects_hypothesis=false`.

## Promotion rule

A candidate model should not move into the stable atlas until it has:

1. declared equations and units;
2. a named control;
3. parameter bounds;
4. timestep / resolution convergence where applicable;
5. residuals against data or a higher-quality solver;
6. failure-region exposure;
7. ablations or alternate candidate families;
8. a falsification condition that can return a real negative result.

## Expansion direction

The next quantitative layer should connect these controls rather than inventing a new physical law prematurely:

- quaternion orientation + rotating vector fields;
- rigid-body response + external torque fields;
- vector-field divergence/curl + flux/circulation integral checks;
- three-phase field rotation + spatial orientation;
- three-body ensembles + candidate finite-reach residual sweeps;
- real versioned datasets for galaxy curves, redshift, lensing, and stellar spectra.
