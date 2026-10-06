# A-115 compact-source exterior diagnostic

## Result

The static, spherical, constant-coefficient A-115 branch with V_b=0,
regular origin and K_L=I produces **zero exterior acceleration** for the
smooth compact radial vector source tested here. Five focused tests pass.
This identifies an actual source-closure gap; it does not rule out nonlinear,
dynamic, nonlocal or other explicitly specified One-Wave source models.

## Derivation from the existing equation

[A-115](../Nodes/A-115_Unified_Compression_Field.md) declares chi=-div(u) and

rho_u u_tt + mu_u u_t - K_chi grad(div(u)) - S_u laplacian(u) + dV_b/du = J.

Set time derivatives and V_b to zero, with constant positive K_chi and S_u.
Taking divergence gives

(K_chi+S_u) laplacian(chi) = div(J).

In spherical symmetry integration yields

r^2 [(K_chi+S_u) chi'(r) - J_r(r)] = C.

Regularity at the origin sets C=0. Thus

chi'=J_r/(K_chi+S_u),  g_r=-alpha_g J_r/(K_chi+S_u).

A compact radial J_r therefore has no exterior gradient in this branch.
Setting a nonzero exterior integration constant would introduce an origin
singularity or unmatched boundary/source flux; it is not supplied by this
regular source. This is not an imposed Newtonian well.

For J_r=r(1-r^2)^2 at r<1 and zero elsewhere, chi(R)=0 at R=4 gives

chi(r)=-(1-r^2)^3/[6(K_chi+S_u)] inside; chi=0 outside.

The negative chi here is expression/release under A-115's sign convention,
despite inward g for positive alpha_g. This chosen mathematical control is
not asserted to represent a physical mass source.

Regular displacement is reconstructed independently through

u_r(r)=-r^-2 integral_0^r chi(s)s^2 ds.

In a spherical curl-free field laplacian(u)=grad(div(u)); this reconstruction
and the source-gradient balance satisfy the original restricted vector equation.
Nonzero exterior displacement can remain as 1/r^2 while exterior chi and g vanish.

## Numerical evidence

The solver independently solves the radial finite-volume tridiagonal Poisson
system, rather than assigning chi from the analytic expression. Analytic chi
is used only for comparison. Source flux is evaluated at cell faces; the origin
has zero flux and the outer Dirichlet boundary uses its half-cell distance.

| Cells | Maximum absolute chi error | Maximum exterior acceleration |
|---|---:|---:|
| 64 | 8.05060845e-5 | 0 |
| 128 | 2.02904157e-5 | 0 |
| 256 | 5.08284819e-6 | 0 |
| 512 | 1.27135233e-6 | 0 |

Errors decrease approximately fourfold with doubled resolution. Source flux
balance and acceleration-gradient errors are zero for these exactly aligned
fixtures; displacement identity error is below 2.82e-16.
All quantities are dimensionless. No observed galaxy speeds, G, particle masses
or fitted coefficients enter this diagnostic. Full results and source hashes:
[a115_static_source_receipt.json](a115_static_source_receipt.json).

Reproduce from the repository root with Python, NumPy and SciPy:

```sh
python3 -m unittest discover -s solvers -p test_a115_static_source.py -v
python3 solvers/a115_static_source.py --output /tmp/a115-source.json
python3 -m unittest discover -s solvers -p test_galaxy_validation.py -v
```

## Consequence for the next source derivation

A-115 does not yet specify the physical J_source or V_b. To recover an exterior
1/r potential, the source law must explain the required exterior compression
gradient and its amplitude, without inserting observed rotation speeds.
Possible nonlinear boundary-potential terms, time-dependent memory/wakes,
or extended sources require their own declared equations and controls.
This result does not choose among them or authorize inventing a law.

[C-320](../Nodes/C-320_Magnetic_Compression_Path_Coupling.md) cannot repair
a zero gradient simply by multiplying it by a finite K_L. Its zero-gradient
control remains mandatory. No node gate, galaxy contract or existing solver
is changed.

## Branch-step and retained consequence

- MAIN GOAL: advance the reliable Field/Void coding engine with a reproducible
  source-derived scientific diagnostic.
- WHY/current goal: test the missing exterior-source closure before tuning
  galaxy candidates that already failed their fixed published-data comparison.
- HARD START: Science main 87ad3af06c86498bd6d4f868b73540346e1934d2;
  remote Jetson localhost.localdomain, aarch64, Scales; default branch main.
- Root: /home/Scales/One-Wave-Science; isolated task worktree
  .one-wave-metadata/task-worktrees/a115-source-20261006; branch
  science/a115-compact-source-20261006 at that base.
- References: GENERAL_REFERENCE_RULES, AGENTS, AI_CANONICAL_START_HERE,
  AI_BRIDGE_START_HERE, BRANCH_STEP_PROJECT_TEMPLATE, Reality Database Builder
  specification, Engine/ALGORITHMS, A-115, C-320 and GALAXY_EXTERNAL_VALIDATION.
  JETSON_OPENCLAW_RUNTIME is absent from the current tracked tree.
- Allowed: this report, a115_static_source.py, test_a115_static_source.py,
  a115_static_source_receipt.json. Protected: dirty primary checkout,
  existing solvers, frozen galaxy data/contracts, physical calibration and gates.
- Choice/Field: one additive static-source diagnostic with analytic control,
  refinement, source-flux conservation and displacement reconstruction.
- Void pre-check: ALLOW this restricted calculation; no generic physical
  no-go or unified-physics proof follows. Proposal/check are same-model roles;
  no independent AI corroboration, Claude connection or M4 dispatch claimed.
- Move: finite-volume source solve, five tests and hash-qualified receipt.
- Attempt: 1/3. No outcome-driven coefficient changes.
- View/Action: five new tests pass; existing eight galaxy regressions pass.
  Four refinement grids preserve zero exterior response and second-order chi
  convergence. Diff restricted to the four allowed additive files.
- Void post-check: ALLOW scoped mathematical/numerical evidence.
- State/Scale: RESOLVED diagnostic; PARTIAL physical source closure;
  DO NOT SCALE into a claim about all One-Wave source models.
- Reflection: the source-to-compression route is now executable without an
  imposed well. The restricted branch cannot supply the exterior gravity
  required by A-115. The prior failed galaxy comparison is preserved.
- Hard stop: tested diagnostic and retained evidence; next step must reference
  an explicit constitutive source/boundary law before another solver change.
