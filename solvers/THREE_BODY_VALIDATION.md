# Three-body validation: repaired control, open One-Wave derivation

Date: 2026-10-05. Reference: Science main `15e880e9cc710a0e67bf2e37348f8b7ead3f6e03`.

**Result:** the numerical control passes; the general three-body problem and the One-Wave source-field derivation are not solved. The original Gaussian implementation is retained as a rejected candidate, with an executable negative control. No physical node gate is promoted.

## Model and dimensions

A-115 requires the exterior recovery `Phi_OW -> -G M_eff/r`, `g=-grad(Phi_OW)`. The control implements that supplied Newtonian limit directly:

- `Phi_i = -G sum(j != i) m_j / |r_i-r_j|` (potential per unit test mass).
- `a_i = G sum(j != i) m_j (r_j-r_i)/|r_j-r_i|^3`.
- `E = sum_i m_i |v_i|^2/2 - G sum(i<j) m_i m_j/r_ij`.
- Linear momentum, angular momentum and ballistic center-of-mass motion are checked separately.

All coordinates are native R^3; the figure-eight and Euler fixtures explicitly restrict `z=vz=0`. A nonplanar, unequal-mass fixture tests the spatial implementation. Dimensionless units, G=1, no softening and no damping. Input masses are conventional control parameters, not generated One-Wave Mass Effects. The point-source control does not simulate a nucleus, mirror, lattice, finite wake or bounded internal recurrence; it does not overwrite their architecture.

For equal masses at x=-1,0,1, the outer acceleration is inward with magnitude 1+1/4. Thus omega=sqrt(5/4) gives an analytic rotating collinear reference. Its verification interval is t=0..1 because the orbit is unstable. The figure-eight runs one approximate period T=6.32591398 with the rounded initial conditions published by [Richard Montgomery, credited to Carles Simo](https://people.ucsc.edu/~rmont/Nbdy.html). The period and initial conditions are supplied reference data, not newly predicted results. Their finite precision limits the recurrence comparison.

## Failure preserved

`ThreeBodyPressureField` in `three_body_solver.py` retains the old Gaussian force calculation:

1. Positive Gaussian peaks and `-grad(P)` repel. At the corrected collinear fixture the left outer body's radial acceleration is +0.8090213 (outward).
2. Dividing the gradient by the test body's mass gives the wrong unequal-mass acceleration/momentum structure for gravitational attraction.
3. No lattice evolution is present; the damping argument is stored but unused.
4. The old default Euler setup coincided two bodies. Compatibility helpers now return distinct equal-mass positions; unsupported mass ratios fail explicitly.
5. Pressure at the center was mislabeled conserved energy. The new control computes kinetic plus pair-potential energy.
6. The old Lyapunov helper fits separation in position/velocity coordinates, not pressure space. Too little fit data now returns NaN/inconclusive rather than zero/integrable. It remains a legacy diagnostic, not an asymptotic Lyapunov calculation.
7. Unconditional success prose is removed. The command exits nonzero if an acceptance check fails.

The existing command now runs the separately labeled control; importing the legacy class still exposes the original rejected force for reproduction. This intentional command behavior change prevents presenting the old demonstration as a solution.

## Reproduce

From repository root, with NumPy and SciPy:

```sh
python -m unittest discover -s solvers -p 'test_three_body_control.py' -v
python solvers/three_body_solver.py --output /tmp/three_body_validation.json
```

The tracked `three_body_validation.json` contains thresholds, metrics, inputs, environment and SHA-256 hashes of solver/test sources. Eight tests passed in the isolated execution environment (Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0). This is not a Jetson, hardware, OpenClaw or Nexus execution receipt.

| Measurement | Observed |
|---|---:|
| Figure-eight complete position/velocity return norm | 7.52342e-8 |
| Maximum relative mechanical energy drift | 4.66140e-11 |
| Maximum linear momentum drift norm | 2.61315e-15 |
| Maximum angular momentum drift norm | 8.75490e-11 |
| Center-of-mass trajectory error | 2.53909e-15 |
| Tighter-tolerance trajectory difference | 2.42567e-10 |
| Euler analytic full-state error over t<=1 | 2.10088e-11 |
| Verlet final-state errors at 2000/4000/8000 steps | 5.00403e-5 / 1.25118e-5 / 3.12806e-6 |
| Minimum error reduction on halving Verlet step | 3.99946 |
| Unequal-mass 3D relative energy drift over t<=0.2 | 2.86756e-11 |

DOP853 and velocity Verlet are different integrators of the same supplied force law; their agreement is numerical corroboration, not independent confirmation of One-Wave physics. Full-state norms combine dimensionless position and velocity coordinates with unit weights; they are control diagnostics, not physical error bars. Thresholds are software acceptance tolerances, not observational uncertainties. Near coincidences <=1e-10 raise an error at evaluated states; there is no collision regularization or guarantee of detecting every close approach between solver evaluations. Long chaotic integrations, collisions and relativistic regimes are outside this verification.

## Next derivation, without replacing the architecture

Read `Nodes/A-115_Unified_Compression_Field.md` and its source/displacement equation. The scalar relation `chi=-div(u)` and `Phi=alpha_g chi` alone does not determine the field of a bounded source. The source term, constitutive coefficients, boundary conditions and mapping from the complete recurrence to source strength remain required.

A conditional route is explicit: **if** the quasistatic source equation can be derived as `laplacian(Phi)=4*pi*G*rho_eff`, with Phi tending to zero at infinity, its Green function supplies `Phi=-G integral rho_eff(x')/|x-x'| d^3x'`. That would recover this control outside spherical localized sources. This Poisson closure is a target condition here, not a derivation from A-115. Finite propagation, wake memory and their energy/momentum exchange require separate dynamic field accounting. Renaming the Newtonian potential pressure does not complete that step.

Next permitted bounded work: derive or falsify this source closure from A-115 with a declared native 3D source and boundary conditions; require the same coefficients to recover a two-source limit before three-source predictions. Retain the four-interaction source architecture. Do not tune a separate coupling for each orbit or infer disappearance of chaos from determinism.

## Branch-step / Field-Void record

- MAIN GOAL: improve the Field/Void construction engine through reproducible, checked solver work.
- WHY: the existing solver printed success despite a repulsive force and invalid energy diagnostic.
- CURRENT STEP: repair three-body validation and expose the precise remaining scientific gap.
- HARD START: verified GitHub main and current source blobs; read General Reference Rules, AGENTS, Reality Database Builder specification, branch-step template, Jetson runtime scope, canonical start and A-115.
- ROUTE: GitHub connector; ephemeral execution staging at `/workspace/scratch/33a9efee9aef/three_body_work`. No local repository checkout, branch or dirty worktree exists there. No laptop or Jetson changes.
- BRANCH: `fix/three-body-validation-20261005`, based on the reference above.
- ALLOWED FILES: three_body_solver.py, three_body_control.py, test_three_body_control.py, three_body_validation.json, this record (all under solvers), and the three-body entries in STANDARD_MODEL_MYSTERIES_CASCADE.md.
- PROTECTED: other solvers, physical nodes, canon, databases, runtime routes and all device working trees.
- FIELD PROPOSAL: preserve rejected Gaussian force; add an explicit Newtonian recovery control, corrected fixtures and falsifiable validation.
- VOID PRE-CHECK: ALLOW this bounded implementation with no claim of a source-derived One-Wave law. Same-model role review, not independent AI corroboration.
- EXACT ACTION: implement the control and numerical acceptance gates, retain failed mechanism, link status to actual receipts.
- SUCCESS CRITERIA: analytic Euler agreement, figure-eight recurrence, force/potential consistency, conservation including unequal masses, R^3 symmetries, independent integrator refinement, negative-control rejection and failure exit.
- ATTEMPT: numerical implementation 1/3 passed. An initial shell test-file write used the wrong relative staging path and ran zero tests (exit 5); the corrected invocation ran all eight, exit 0. The zero-test invocation is not counted as validation.
- FIELD FINDING: attraction, true mechanical energy and correct fixtures pass; Gaussian repulsion is structural, not a tolerance issue.
- VOID POST-CHECK: ALLOW numerical-control scope only. Eight tests and ten receipt checks pass. The open One-Wave source derivation remains PARTIAL; do not scale to an N-body or astrophysical validation claim.
- REFLECTION: a model can be deterministic and still fail the intended dynamics. Existing legacy force reproduction is protected; no unrelated solver was modified or tested.
- HARD STOP: verified task branch and reviewable PR, no automatic merge. No scientific gate promotion.
- HANDOFF: preserve these control receipts and rejection evidence; next work must derive the A-115 source closure against this baseline.
