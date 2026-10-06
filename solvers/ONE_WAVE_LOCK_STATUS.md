# One-Wave balance and lock: verified state and next construction

Reference: PR #193 at a8ae110dfa772b5001f252171611cb23c8f0ea8b; main
9918dbb92614b914b9609cde91de808757071332. Repository authority files are unchanged.
This page indexes the measured results; the linked derivations and raw data
remain the evidence owners. No node gate is promoted.

## Verified findings

| Calculation | What passed | What remains open | Evidence |
|---|---|---|---|
| Native retained compression | Reciprocal energy gradients, constrained chi=-div(u), ten controls | Exact-law static nonzero-displacement equilibria are saddles; dynamic holding is unproved | [Native bridge](NATIVE_COMPRESSION_BRIDGE.md) |
| Seed searches | Reproducible phase/velocity and timestep controls | No qualifying localized recurrence | [Phase/velocity search](PHASE_VELOCITY_SEARCH.md) |
| Direct periodic solve | Three small-box near-recurrences and ten-cycle energy-controlled evolution | No Persistent Mode meets the localization screen | [Periodic solve](PERIODIC_ORBIT_SOLVE.md) |
| Harmonic/domain check | Equation defects below 9e-12 | Central activity drops 64.55% to 31.07% on 32 to 108 sites; upper-band tails remain | [Domain and closure audit](RECURRENCE_DOMAIN_CHECK.md) |
| Reciprocal path/circulation core | Six gradient, work, recovery and conditional R-balance checks; small converged compression-to-curl response | All six spatial lock screens fail; no freely evolving skin | [Reciprocal balance](RECIPROCAL_BALANCE_AND_LOCK.md) |
| Reduced pressure/tension radius | Stable radial balance over 200 units and ±10% radius perturbations; both ablations lose lock | Single carrier and inverse-radius frequency were assumed | [Reduced radius lock](RECIPROCAL_BALANCE_AND_LOCK.md) |
| Computed spatial cavity pressure | Five checks; radius .758813219 and matched pressure .0263569473; four bounded 200-unit runs | Reflecting graph and self-similar skin still imposed | [Spatial pressure and gap equations](SPATIAL_BOUNDARY_PRESSURE_AND_GAPS.md) |

Uniform relative-phase recurrences may have nonzero frequency but zero
cycle-averaged radius pressure in the computed cavity model. Their instantaneous
stress can oscillate. Recurrence energy alone cannot be assigned as confinement
work or measured Mass Effect.

## Exact next construction

Build one native field/closed-skin work law. Evolve excitation psi, displacement
u, velocity, chi=-div(u), path reorganization R, circulation, recurrence phase
and a closed 3D skin. Include geometry derivatives of the field metric, spatial
operators, compression map and interaction terms. The skin force must contain

    F_a = .5 v^T(partial_a W)v - .5 q^T(partial_a H)q
          - sigma_T partial_a A - partial_a E_other.

The current four-role response coordinates q are fixtures, not a substitute for
deriving the native nonlinear knot/shell/Mirror/weave fields. Their map into the
native state must be explicit and share a reciprocal energy ledger.

Required next evidence:

1. Force/energy gradient and mixed-derivative reciprocity, including skin forces.
2. Isotropic and coupling-off recovery of the existing native equations.
3. Free radial and nonspherical perturbations without clamping or norm resets.
4. Exterior reflection, deflection, tangential redistribution and Mirror phase
   coupling with a complete work ledger; no forced boundary penetration.
5. Localization and complete-state recurrence on larger domains, followed by
   circulation/three-phase topology, shell formation and coupling ablations.

The remaining dependencies are native field-to-skin mapping, deformable closed
geometry, exterior/Mirror channel geometry, three-phase circulation topology,
electrical-shell feedback and constitutive/physical calibration. C-317 owns
weave/surface/twist; C-319/C-320 own reorganization/path handoff; D-412 owns the
state and measurement standard. Preserve the full architecture while deriving
these interfaces. Translation, Mass Effect and time measurements follow a stable
complete recurrence.

## Repository cycle receipt

Goal: make the complete finding set and exact next implementation target easy
to locate. Choice: one additive status index and laboratory chapter pointer.
Protected: equations, executable code, raw measurements, node gates, hardware
and dirty Jetson checkout. Field assembles the evidence map; Void verifies every
linked file and result gate. Same assistant performs both; no independent
corroboration. No new simulation is claimed in this documentation cycle.
State: evidence index complete; physical spatial/topological lock remains PARTIAL.
Scale: no merge, gate promotion or physical prediction follows from this index.
