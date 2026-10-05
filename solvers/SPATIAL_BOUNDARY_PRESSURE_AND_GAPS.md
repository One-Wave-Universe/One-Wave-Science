# The missing closure: spatial pressure, moving skin and exterior channels

**Immediate missing equation found and supplied for a radial cavity control:**
the spatial field's reciprocal force on its moving boundary, including the
radius-dependent kinetic metric. The previous assumed carrier coefficient is
replaced by the computed native FCC four-role spectrum. The remaining physical
lock gap is the evolving skin/exterior/rotation coupling; deleting exterior bonds
still prescribes reflection instead of deriving Knot Lock.

Reference PR #193 at `e2b33bb0bfc547217a7208275f68193ce33c2467`.
Main comparison `9918dbb92614b914b9609cde91de808757071332`; AGENTS,
General Reference Rules, canonical start and Reality Database specification
are unchanged from `007832743369f83b6f4e60e141e6e5e2f8f57952`.
Execution is in the isolated workspace, not a Jetson simulation run.

## What the prior cores did and did not connect

The native compression/path core evolves psi,u,R but has no closed surface or
exterior. Its tested states spread. The radius control has a freely evolving
surface coordinate, but previously used Omega(R)=1/R and an assumed confined
carrier. The joint response fixture computes a real native cavity spectrum, but
fixes its reflecting graph and surface. Thus all three contain useful pieces;
none previously passed the field's computed pressure back into a moving skin.

The new calculation combines the joint spectrum with a moving radial geometry
and one Hamiltonian. Four response roles remain candidate knot, shell, Mirror
and weave coordinates, not microscopic identifications of four derived fields.
No one silently equates those coordinates with the native psi,u,R state.

## Computed carrier and exact reciprocal moving-metric force

Reproduce the existing 13-site FCC reflecting cavity and declared four-role
operator from [Joint Response](JOINT_RESPONSE_DERIVATION.md). Let L be its graph
Laplacian, C=diag(1,.8,1.2,.6)+.12 P and P the four-role cycle Laplacian. Set

    A=(L/12) tensor C,
    B=I tensor (.04 P),
    W(s)=DeltaV_0 s³ I,
    H(s)=DeltaV_0(s A+s³ B).

Here s is the self-similar radius/spacing scale of the fixed material graph;
DeltaV_0=1/sqrt(2). Surface area is the declared spherical approximation 4 pi s².
The s³ material-coordinate metric is a constitutive choice, not measured Mass
Effect. It must be included consistently in both field evolution and surface
force. A fixed field inertia with the same varying volume would be a different
model, not the one stated here.

The coupled Hamiltonian is

    E=.5 p^T W(s)^-1 p + .5 q^T H(s) q
      + P_s²/(2W_s) + 4 pi sigma_T s².

Its equations use canonical field momentum p; q-dot=W^-1 p. The surface force is

    P_s-dot = .5 v^T W'(s) v - .5 q^T H'(s) q - 8 pi sigma_T s.

This is the missing feedback. The kinetic-metric derivative is essential, not an
optional correction. The executable evolves all 52 field coordinates, momenta
and the radius/momentum through this same instantaneous Hamiltonian.

The computed normal-mode equation is

    [A/s²+B] f = omega(s)² f.

For a spatial graph eigenvalue lambda_L, the role block is only 4 by 4:

    D(s)=lambda_L C/(12s²)+.04 P.

Thus the role spectrum and its radius response are computed rather than assigning
a_omega=1. Hellmann–Feynman differentiation gives

    omega'(s)=-lambda_L f^T C f/(12 omega s³),
    DeltaP_carrier=-J omega'(s)/(4 pi s²).

The averaged radial balance and stability conditions are

    J omega'(s_*)+8 pi sigma_T s_*=0,
    J omega''(s_*)+8 pi sigma_T > 0.

J is used for the prediction and initial field amplitude, not reset in the full
Hamiltonian evolution. Only radius-dependent spectral energy supplies pressure.
For lambda_L=0, uniform relative-phase recurrences have frequencies .2828427,
.2828427 and .4 yet omega'=0 and zero cycle-averaged radius pressure. The common uniform role
is free. A nonzero recurrence frequency is not by itself confinement work or
Mass Effect. Treating all role energy as J/s pressure would miss this distinction.

## Measured replacement of the assumed coefficient

Keep sigma_T=.01, J=8 pi sigma_T and surface kinetic weight W_s=100 from the
previous radius control. Use the lowest nonzero spatial graph eigenvalue and
lowest role branch. At s=1 its computed frequency is **.459660896**, reproducing
the prior joint cavity's first spatial frequency, rather than the assumed 1.
The actual balance is

    s_*=.758813219,
    omega(s_*)=.599233807,
    DeltaP_carrier=DeltaP_skin=.0263569473,
    averaged radial curvature=.746709228 > 0.

The old radius 1 therefore does not remain the predicted balance under the same
J and sigma_T. This is a model correction, not a particle-scale calibration.
Five checks pass: spectral derivative, full moving-metric energy gradient,
positive averaged curvature, all four radius runs, and zero cycle-averaged pressure for uniform
phase controls. The program uses adaptive DOP853 with maximum step .2; checks
energy and radius at accepted integration steps and publishes a trace every 2
units. Tight tolerance repeats the balanced run. The same field equations and
coefficients are used for all cases, with no mode/action resetting or radius clamp.

The balanced and ±10% radius-perturbed runs complete 200 units and remain within
(.8 s_*,1.2 s_*), with maximum accepted-step scaled energy error below 2e-13.
Exact observed ranges and solver settings are in the raw results. This is a
computed-cavity radial work/lock control; no outgoing continuum or freely formed
skin is present, so it is not physical Knot Lock.

[Executable](spatial_boundary_pressure.py) · [Computed spectrum, pressure and trajectories](spatial_boundary_pressure_results.json).

```sh
OPENBLAS_NUM_THREADS=1 python solvers/spatial_boundary_pressure.py > solvers/spatial_boundary_pressure_results.json
```

NumPy/SciPy and native_compression_bridge.py required. Script exit success
certifies the five scoped checks, not the full four-interaction recurrence.

## Exact remaining missing pieces, in dependency order

| Missing piece | Required state/equation | Why the existing result does not supply it | Acceptance evidence |
|---|---|---|---|
| Native field-to-skin map | Put psi,u,chi=-div(u),R and boundary geometry in one common energy | The 52 four-role cavity coordinates are response fixtures; they are not the nonlinear native fields | Full mixed-force reciprocity, native recovery and pressure-work identity |
| Evolving closed 3D skin | Closed mesh vertices s_a, surface area A(s), strain/twist energy and reciprocal vertex forces | One radial coordinate excludes shape modes, necks, reclosure and center motion | Perturb radius and nonspherical shapes; no artificial wall, clamp or reset; stable energy/geometry |
| Exterior/Mirror channel geometry | Exterior field plus normal reflection, tangential redistribution and passive phase-coupling ports | Current absent exterior bonds impose zero flux; abstract role ports are not angular scattering | Resolve bounce, deflection, roll-off and scatter from states; account for all boundary/exterior work |
| Circulation and phase topology | Computed velocity circulation, three internal Vortex Phase candidates and their phase/twist coupling | Seeded swirl or four named response coordinates do not establish a three-vortex knot | Persistent topology and three-phase recurrence; fixed-law extraction/reclosure test |
| Electrical shell and Mirror feedback | Derived inner/outer differential shell, Mirror phase state and surface-work cross terms | Existing response labels provide neither shell formation nor its constitutive coupling | Coupling ablation must break the appropriate response, with conservative/passive ledgers |
| Constitutive and physical calibration | Derive sigma_T, phase/twist/path terms, amplitudes and units from the declared medium | Illustrative coefficients prove numerical mechanisms only | Independent scale/observable match, without target-fitting labels |

For general moving geometry s_a, the required surface force has the form

    F_a = .5 v^T (partial_a W) v
          - .5 q^T (partial_a H) q
          - sigma_T partial_a A
          - partial_a E_other.

For the actual native nonlinear energy, E_other includes compression, path
reorganization, twist, shell and Mirror terms; derivatives of geometry-dependent
chi/divergence and coupling maps must be included. Putting K_L only in the field
force while omitting its reciprocal geometry/R forces repeats the previous
energy-accounting failure. Normal pressure balance alone does not control
nonspherical or phase/topological instabilities.

The first construction target is the native field/closed-skin interface with
this reciprocal force, followed by exterior channels. Topology and phase lock
then become tested properties of that evolving field/boundary system. Translation,
Mass Effect and time measurements follow its stable complete recurrence; they
cannot be assigned from a uniform phase resonance or a prescribed cavity radius.

## Field/Void receipt

Goal: identify what is missing and replace the immediate assumed pressure law.
Choice: one additive computed spatial-carrier/moving-metric pressure control plus
explicit closure map; preserve the original successful and failed reports.
Allowed: executable, raw results, this derivation and additive C-317/laboratory
receipts. Protected: earlier solvers/data, node metadata/gates, full architecture,
hardware and dirty Jetson work. Field derived the actual pressure feedback;
Void checked frequency derivatives, Hamiltonian gradients, zero-cycle-averaged-pressure phase
controls, radius perturbations and tighter integration tolerance. Same assistant
proposed and checked; no independent corroboration.

The initial run passed the five controls. Checking identified a floating-point
near-zero uniform frequency; the final run clamps eigenvalues below 1e-12 and
checks radius/energy at accepted solver steps rather than only output samples.
All four runs were repeated. No physical coefficient changed.

State: immediate pressure feedback and computed-cavity radial balance RESOLVED;
full native spatial/topological lock PARTIAL. Scale: no node gate, persistent-mode
or physical-mass claim. Next: implement the native field/closed-skin/exterior
interface under the same work law, retaining the complete four-role architecture.


Precision check at `c2caefb1bea18bccf53acdbe26809d0b2cf2a1e6`: the uniform-mode
zero-pressure result is cycle-averaged/adiabatic. The instantaneous moving-metric
force can still oscillate within a carrier cycle. Those oscillatory forces are
retained in the Hamiltonian evolution; zero averaged pressure is not a claim of
zero instantaneous stress. This reporting-only clarification preserves every
solver/result blob and all measured gates.
