# PR #34 Expansion Summary

This branch now contains three layers of experimental controls beyond the original 12-scene physics wing.

## Layer 1 — Core experimental wing

12 modules covering numerical integrator drift, waves, modes, RLC resonance, diffusion, lensing, three-body sensitivity, blackbody spectra, galaxy curves, redshift references, finite-wake candidate families, and residual/falsification testing.

## Layer 2 — Orientation & quaternion controls

8 runnable scenes covering:

- axis-angle quaternion rotation;
- noncommutative rotation composition;
- SLERP;
- Euler gimbal lock;
- angular-velocity quaternion integration;
- torque-free asymmetric rigid-body dynamics;
- local/world frame composition;
- three-phase rotation embedded in a quaternion-controlled 3D frame.

The rigid-body control has an offline 100-time-unit invariant check in `orientation-quaternion/VALIDATION.md`.

## Layer 3 — Field topology and global cross-checks

6 local vector-field topology scenes:

- uniform field;
- radial source;
- vortex;
- saddle;
- dipole pair;
- source + vortex superposition.

4 global integral-theorem scenes:

- divergence theorem on a linear expansion field;
- circulation/curl identity on solid rotation;
- zero-integral saddle control;
- simultaneous divergence/curl mixed field.

These compare finite-difference local derivatives with boundary/area integral identities so visually plausible fields can still fail numerically.

## Integrity lock

All hypothesis tracks remain non-causal with respect to control solvers. Exports record `solver_affects_hypothesis=false`. The new quaternion and field modules are control mathematics, not evidence for a One-Wave physical claim.
