# Physics Experimental Wing

This directory is the aggressive expansion area for the One-Wave physics atlas. It is intentionally separate from `sims/` and from the stable `physics-atlas/` interface.

## Purpose

The wing is for models that need stronger quantitative controls, parameter sweeps, residuals, and visible failure modes before they deserve promotion into the stable atlas.

## Runnable scenes

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
