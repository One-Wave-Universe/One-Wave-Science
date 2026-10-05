# Native compression bridge: a constrained constitutive candidate

Evidence class: tested dimensionless mathematical hypothesis, not a physical closure.
Reference: Science main `12b385d410564857cbc2b67d2af22cd2f5702cac`.
Owners: A-115 compression, D-409 geometry, D-412 simulation discipline;
C-317/C-318 remain owners of weave and the complete four-interaction mechanism.

## What this step resolves

The previous bulk candidate introduced a first-order complex-field cubic/quintic
force independently of the canonical second-order recurrence. This experiment
instead retains vector displacement u, its velocity, real excitation psi and its
velocity. Compression is chi = -D u, the actual discrete divergence of displacement.
The nonlinear coupling is explicitly assumed; its forces and its static reduction
are then derived from a single energy. This solves an integrability and geometric
compatibility problem, not the physical origin of the coupling.

The code and raw evidence are [native_compression_bridge.py](native_compression_bridge.py)
and [native_compression_results.json](native_compression_results.json).

## Correct the independent-compression shortcut

An unconstrained local trial E(c,rho)=(k+a rho)c²/2-eta rho c gives
c*=eta rho/(k+a rho) and E_eff=-eta²rho²/[2(k+a rho)]. Its small-density expansion
contains a negative rho² term and positive rho³ term. This explains how a chosen
constitutive energy can generate a cubic/quintic *approximation* in psi when
rho=psi². It does not derive that energy from the fixed linear update.

More importantly, c* is not generally an admissible periodic compression field.
Because chi=-D u, sum chi=0. For the published nonnegative Gaussian rho, the
independent local shortcut gives sum c*=12.0515039232. It violates that constraint.
The constrained solve gives sum chi=4.44e-16, with positive compression and negative
release. This failed shortcut stays visible; it is not used by the solver.

## Native operators and energy

Sites are even-parity Cartesian integer triples in an even-period periodic box.
Physical positions are a/sqrt(2) times those triples; each site has twelve FCC
neighbors and volume DeltaV=a³/sqrt(2). Only even sites hold state; the ambient
array's odd sites are unused. There is no enclosing wall or imposed well.

For neighbor unit vectors n and displacement offsets a n, define

    (D u)_i = (1/(4a)) sum_n n dot u_(i+a n)
    (G f)_i = (1/(4a)) sum_n n f_(i+a n)
    L f = (12 f - sum_n f_(i+a n))/(2a²).

Periodic summation gives D^T=-G and, for C=-D, C^T=G. The bond operator L is positive
semidefinite; its small-wavenumber limit is -Laplacian. The factor follows from
sum_n n n^T=4 I, preserving the native three-dimensional shell.

Set rho=psi² and declare the potential

    V = DeltaV [ beta/2 psi^T L psi + shear/2 u^T L u
                 + sum_i ((k+a_c rho_i) chi_i²/2 - eta rho_i chi_i) ].

Here `a_c` is called `a` in the Python parameter interface, separately from grid
spacing. beta,shear,k are positive and a_c is nonnegative. eta is a coupling.
These are dimensionless model inputs. No SI calibration or observed mass enters.
The added rho-dependent stiffness and density/compression interaction are new
constitutive hypotheses. A-115's displacement energy motivates the retained
variables; it does not already supply or validate those added terms.

Per-volume work gradients are

    dV/dpsi = beta L psi + (a_c chi² - 2 eta chi) psi
    dV/du   = shear L u + G[(k+a_c rho) chi - eta rho].

They are reciprocal derivatives of the same V. With unit kinetic coefficients,
ddot psi=-dV/dpsi and ddot u=-dV/du. Velocity Verlet integrates both retained
variables without normalization resets. When eta=0 and u=0, the excitation update
reduces exactly to psi_(n+1)=2psi_n-psi_(n-1)-dt² beta L psi_n. This is the gamma=0
canonical transport form with the graph-averaging coefficient
beta_canonical=6 dt² beta/a_spacing². Coupling-on behavior is an explicit extension,
not a claim that a fixed linear recurrence secretly creates nonlinearity.

## Constrained elimination and the effective force

For fixed rho, solve on the zero-mean displacement gauge

    A(rho) u = eta G rho,
    A(rho) = shear L + G diag(k+a_c rho) C.

Positive bond shear makes this operator coercive away from the constant
translation mode. Central divergence has additional high-frequency blind modes;
the bond term regularizes their displacement response without pretending that
the compression readout detects them.

The minimum compression energy is

    V_c,eff = -DeltaV/2 (eta G rho)^T A(rho)^(-1) (eta G rho).

The inverse is on the gauge-fixed displacement subspace. This is nonlocal;
compression at one site cannot be eliminated independently of its neighbors.
The envelope theorem gives the exact reduced density force

    dV_c,eff/d rho_i / DeltaV = a_c chi_i²/2 - eta chi_i.

The test perturbs rho, independently resolves displacement twice, and compares
the measured reduced-energy derivative with that force. Uniform rho produces
G rho=0 and no displacement response. Removing eta also produces no response.
Static elimination is a zero-frequency approximation; dynamic runs retain u.

## Executed controls

Run `python solvers/native_compression_bridge.py` from the repo root with NumPy
and SciPy installed. It prints JSON and exits nonzero if any of nine checks fails.
The published run used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, seed 107,
256 active sites, spacing 1, and beta=shear=k=a_c=1, eta=2.

| Control | Measured result |
|---|---:|
| Discrete compression/gradient adjoint error | 5.33e-15 |
| Constrained stationarity relative residual | 4.47e-12 |
| Total compression | 4.44e-16 |
| Reduced force finite-difference error | 3.73e-11 |
| Full reciprocal gradient error | 1.92e-9 |
| Coupling-off / uniform-density displacement | Zero |
| Canonical linear-limit difference | Below 1e-14 |
| Dynamic energy error, dt=.04 / .02 / .01, time=4 | 1.086e-4 / 2.715e-5 / 6.787e-6 |

Energy errors decrease by approximately four when dt halves, as expected for
the declared second-order integrator. The metric is maximum absolute drift
divided by max(1,abs(initial energy)); it is not always a relative error.
Compression ranges from -0.02958 to +0.45628. The eliminated compression-sector
energy is -1.15458 relative to unrelaxed zero displacement at that fixed density.
This is work from the assumed coupling, not energy creation or a mass prediction.

## What remains open

The small-input dynamic run spreads; it does not establish localization.
psi² is not conserved by these real second-order equations. The full potential
is not shown globally bounded below when psi is unconstrained; no stable-ground,
global saturation or long-time stability claim follows from static elimination.
The local rational shortcut's saturation cannot be transferred to the nonlocal
model without a separate proof. Four-interaction necessity, circulation,
surface/weave geometry, translation, pinning, physical detector response,
domain/spacing refinement, HCP controls, 2D/3D comparison and absolute calibration
remain open. The assumptions eta and a_c must be derived from actual geometry or
independently calibrated before this can bridge the complete canonical theory.

## Branch-step receipt and next test

Authorized goal: move toward a native nonlinear localization derivation.
Bounded action: add the constrained FCC compression candidate, reproducible
report and laboratory derivation pointer. Protect all existing solver laws,
node gates, particle classifications, hardware and dirty Jetson recovery work.
Field proposal: retain displacement and derive both forces from one energy.
Void counter-check: reject independent local compression because it violates
the divergence constraint; require adjoint, gradient, ablation and timestep tests.
Executed evidence: nine controls pass on the declared finite grid and time window.
Attempt 1 initially failed JSON serialization of NumPy booleans; attempt 2
converted check values to Python booleans and returned exit 0. No physics
parameters were retuned to repair a control or match measurements.
State: PARTIAL for the physical goal, accepted scoped mathematical experiment.
Scale: do not promote or extend to mass claims from this result.
Next bounded test: determine whether this reciprocal law has a self-held
localized branch with compression/release balance, then compare its dynamic
stability and pinning with the uncoupled linear control. A failure must remain
visible and drive a new geometrically supported constitutive proposal.
