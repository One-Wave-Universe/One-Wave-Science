# Chapter 3 — From Candidate to Canonical Derivation

**Status:** explicit derivation and acceptance program; no new physical result claimed.  
Canonical owners: A-109, A-112, A-115, C-317, C-318, C-322, D-409 and D-412.  
[Previous](Ch02_Localized_Excitations_and_Measurements.md) · [Contents](README.md)

## The remaining problem is a missing equation

The working laboratories now demonstrate two useful numerical facts. A coupled linear operator can satisfy response and energy checks. A declared nonlinear bulk hypothesis can maintain a localized excitation for a finite observation window. The physical derivation still needs to explain how the canonical lattice update generates the nonlinear, geometric and coupled relations used by a material excitation.

This chapter makes that question an executable research program. A successful program must preserve the passed controls and confront the failed ones. It cannot close the gap by renaming the nonlinear law as the canonical update.

## Start with the actual memory recurrence

The canonical scalar transport recurrence has the form

\[
\psi_i^{n+1}=\psi_i^n+(1-\gamma)(\psi_i^n-\psi_i^{n-1})
+\beta\left(\langle\psi_j^n\rangle-\psi_i^n\right).
\]

For a regular native neighbor graph, define P as its averaging operator. With γ=0,

\[
\psi^{n+1}-2\psi^n+\psi^{n-1}=-\beta(I-P)\psi^n.
\]

This is a linear second-order equation at fixed β. It supplies transport and recurrence, but the density-dependent quartic/sextic response in the bulk candidate is an additional constitutive assumption. The missing bridge must produce that response, replace it with a derived one, or show why it is incompatible with the canonical structure.

For an eigenmode of I−P with eigenvalue ℓ, trial amplitude λⁿ gives

\[
\lambda^2-(2-\gamma-\beta\ell)\lambda+(1-\gamma)=0.
\]

This is a concrete starting check. Oscillatory frequency comes from the argument of a complex recurrence root, and decay from its modulus. A real root is not automatically an oscillation frequency. With γ=0, the regular positive-energy oscillatory interval requires 0<βℓ<4. Endpoints and zero modes need their own treatment.

The matrix four-coordinate operator extends this calculation only after its blocks and cross terms are derived. Scalar transport parameters cannot be silently renamed as the four-interaction work metric.

## Derive the nonlinear response from retained variables

A-115 supplies displacement and compression candidates. C-317 supplies surface, relative-phase and twist energy candidates. Their coefficients are open. To connect them to the recurrence, specify the native state variables and write how one update changes displacement, compression, rotation, shell response and weave strain.

Then compute work from those same changes. A constitutive force must be the declared response of those variables, with matching dimensions and cross derivatives. If variables are eliminated to obtain an effective nonlinearity, record the constraints, approximation and conserved quantities used in that elimination.

For example, the bulk candidate's effective force is density dependent. A valid derivation would show which compression or boundary relation generates that dependence and why saturation occurs. It must also identify whether norm conservation survives the reduction or was introduced by the complex first-order model. The present calculation does not answer these questions.

This directs a bounded next implementation: construct one native 3D update with explicit compression and weave variables, compare its measured work gradient to the proposed effective force, and publish the residual over a declared state range. A failed comparison should revise the force law, not retune it toward a particle mass.

## Make the four-interaction requirement testable

The nonlinear candidate localizes with coupling removed. A more complete model must distinguish concentration from the full coupled architecture. Removing a knot, shell, Mirror or weave mechanism may leave a concentration somewhere, but it must change the claimed complete response in a measurable way.

Freeze one parameter set. Define an observable contract before ablation: recurrence, native circulation, shell response, boundary phase coupling, translation and acceleration response. For each interaction removed, measure what changes and whether the complete contract survives. Preserve total injected work and initial conditions where the ablation permits a meaningful comparison.

Do not declare success because four arrays have nonzero values. Participation is weaker than necessity. Do not require every ablation to destroy every possible excitation either; the actual question is whether it destroys or changes the specific coupled behavior being claimed.

## Translation before mass assignment

A site-centered stationary branch is not yet a carried recurrence. The shifted-seed result shows that lattice pinning may matter. Translation experiments must resolve it rather than measuring a profile while keeping its center artificially fixed.

Start with a native excitation and a declared small intervention. Track its center, deformation, energy and wake. Repeat in several directions, velocities and accelerations with fixed coefficients. Separate the response associated with velocity drag from the response associated with acceleration.

C-318's target is

\[
\overline E_4(v)=\overline E_4(0)+\tfrac12v_i\mathcal M_{ij}v_j+\cdots,
\qquad F_i\simeq\mathcal M_{ij}a_j
\]

after dissipative contributions are separated. Measure the energy curvature and the force response independently under the same law. The first-order bulk candidate has not established that bridge. Its frequency, conserved norm or binding energy cannot be relabeled as mass to avoid the experiment.

## Boundary and detector closure

Mirror coupling must preserve the no-forced-penetration rule. Introduce spatial incident and outgoing channels and measure reflection, deflection, tangential redistribution and scattering from the actual excitation geometry. Keep the input/output/storage/loss ledger from the joint response control.

A detector model adds another explicit coupled system. Specify its sensitive coordinates, aperture, bandwidth, phase response and energy exchange. Use it to predict the signal before assigning an external particle classification. Passive windows are a good sampling control, but their success does not establish detector backreaction or event statistics.

CERN, LIGO and other external datasets can provide comparison measurements only after a forward mapping is fixed. Metadata availability proves acquisition, not agreement with the field model. Absolute energy and time scales need independent calibration, and each comparator must match the model's observable and units.

## Acceptance matrix for the next worker

| Question | Required evidence | Failure that must remain visible |
|---|---|---|
| Canonical constitutive bridge | Work/force residual from the native update over a declared state range | Nonlinear law introduced independently or coefficients retuned per state |
| Responsive Ground | Zero-input drift plus response to a bounded input | Spontaneous motion or numerical energy injection |
| Complete coupled excitation | Recurrence, native circulation, shell and weave variables with fixed coefficients | Four labels without their derived mechanisms |
| Interaction necessity | Four individual ablations against the predeclared complete observable contract | Full claimed behavior unchanged when a load-bearing mechanism is removed |
| Boundary behavior | Spatial channel response and complete energy ledger | Forced geometric crossing, unaccounted gain or missing outgoing channels |
| Translation | Directional motion, pinning threshold, deformation and wake controls | Recentered output or imposed trajectory hiding the dynamics |
| Mass Effect | Energy curvature and independent force/acceleration comparison, drag separated | Frequency, norm or fitted target substituted for inertia |
| Numerical convergence | At least a declared sequence of spacing, domain and timestep controls | Persistent spacing sensitivity hidden by a larger box |
| Detector prediction | Declared coupled detector with calibrated observable mapping | Passive amplitude called a collider mass or event count |
| Physical comparison | Frozen model and withheld measurements with matching definitions | Supplied experimental answer used as a stopping condition |

A PASS accepts only its declared scope. FAIL, INCONCLUSIVE and INVALID results stay in the consequence record. No complete physical claim is promoted from a successful program exit.

## What the next loop must inherit

Keep the exact energy and passive response controls. Keep the localized nonlinear branch and its detector trace. Also keep the coupling-off survival, approximately 15% spacing energy shift, shifted-seed branch and missing norm-selection rule. Those observations decide where the next calculation has to go.

The objective is a field law whose excitations, measured responses and classifications arise together under reproducible constraints. That is a stronger result than either an unsupported prediction or a list of unresolved questions, because every next step has a specific observable and a condition that can reject it.

## Constrained native compression follow-up

[The native compression derivation](../../solvers/NATIVE_COMPRESSION_BRIDGE.md) retains displacement and enforces compression as minus its discrete divergence on the twelve-neighbor FCC graph. Ten controls pass (including a conditional stationary-scaling identity): constrained stationarity, zero total compression, reciprocal and reduced force gradients, coupling-off and uniform-density controls, the canonical linear limit, and timestep refinement. This is a constitutive hypothesis, with its coupling terms still assumed. The independently eliminated local compression shortcut fails the periodic divergence constraint. The small-input dynamic run spreads; no self-held localization or complete four-interaction requirement has been established. See the linked code and raw report for scope and the next branch test.

The follow-up also proves an obstruction within this candidate: every stationary state with nonzero displacement is an energy saddle under joint excitation/displacement scaling, since the two-direction Hessian has determinant -16 U². The uniform zero-displacement state is not localized. This excludes stable static localization under this exact real unconstrained law; it does not exclude time-periodic localized recurrence or establish a failure of the complete four-interaction architecture. The next test is a periodic recurrence search and stability controls, rather than another static-minimum search.

## Periodic recurrence screen with retained displacement

[The executed search](../../solvers/PERIODIC_COMPRESSION_SEARCH.md) tests six initial states under the unchanged reciprocal FCC candidate, then adds two localization-refinement controls and three growth-onset timestep controls. No seed passes the declared localized full-state recurrence screen. The completed small coupled seed spreads; enlarging the domain reduces its minimum late localized fraction from about 9.6% to 1.6%. Higher-amplitude endpoints lose numerical energy control and remain invalid for physical interpretation. Smaller timesteps reproduce the earlier growth onset with second-order energy convergence. Raw traces and measured plots are published; phase/velocity seed families and periodic-orbit searches remain open. No clock-rate or translation claim follows from this finite screen.

## Phase/velocity search and radiation-band constraint

[The follow-up experiment](../../solvers/PHASE_VELOCITY_SEARCH.md) adds seven standing, kicked, quadrature, traveling and angular initial cases under the unchanged real reciprocal FCC law. Full-state returns use a time-5 reference, allowing an initial transient. No seed qualifies; two refinement runs preserve failure for the best completed coupled angular case. Enlarging the box reduces its minimum late localized activity from about 13.7% to 2.6%. Numerically invalid amplitude-stop endpoints remain flagged. A separate vacuum-band calculation derives exact scalar/transverse bands and a sampled plus rigorously bounded longitudinal range. There is no low-frequency gap in this candidate, so a periodic orbit must address outgoing radiation channels and its compression harmonics. The next step is bounded periodic-orbit shooting/continuation with nonzero-state and radiation controls, rather than repeated similar seed screens.


### Direct retained-state recurrence solve

The [finite-harmonic One-Wave recurrence solve](../../solvers/PERIODIC_ORBIT_SOLVE.md)
finds three small periodic-box near-recurrences while retaining displacement and
compression. All survive ten fitted periods with controlled energy error; the
smallest state shows approximately fourfold improvement when dt is halved. None
passes the declared localization screen: central activity is 58.8–64.5%, below
80%. The two larger amplitudes also exceed the unprojected harmonic-defect limit.
This advances beyond failed seed launches, but does not establish a Persistent
Mode, Mass Effect or clock. The next bounded calculation is larger-domain and
higher-harmonic continuation of the smallest branch, with zero-mean displacement
and a nonzero-state anchor. Knot, shell, Mirror and Boundary-Tension Weave closure
remain separate missing mechanisms; no node gate is promoted.


### Domain check identifies what the recurrence still lacks

The [domain and harmonic check](../../solvers/RECURRENCE_DOMAIN_CHECK.md) refines
the smallest recurrence to full equation defect below 9e-12, then embeds and
resolves it on 108 FCC sites. Central radius-1 activity falls from 64.55% to
31.07%; even the radius-2 diagnostic falls from 98.55% to 75.05%. Near-periodic
return remains numerically controlled, but localization weakens. A spectral
projection identifies the upper-band eigenspace; its geometry and localization
bounds explain the broad tails. The leading reciprocal compression correction
lowers this branch into the Ground propagation band. No Persistent Mode or Mass
Effect is assigned.

A second exact closure check shows that the current compression law cannot
create curl from zero displacement/velocity curl. C-319/C-320 supply the intended
rotation/path-reorganization handoff, but its full reciprocal work law is absent
from this reduced solver. Simply multiplying the present force by a positive
accessibility tensor produces a nonsymmetric derivative in the current unit
kinetic coordinates. The next physical step is a common energy/force closure
for boundary, rotation and reorganization, preserving C-317 and D-412 rather
than naming this near-linear branch as a complete knot.



### Reciprocal balance and conditional pressure–tension radius lock

The [balance/lock calculation](../../solvers/RECIPROCAL_BALANCE_AND_LOCK.md)
supplies two separately scoped candidate cores. The reciprocal FCC path/circulation
energy passes six work/recovery controls and permits a small timestep-converged
compression-to-curl response. All six trajectories still fail the spatial
return/localization screen. A separate freely moving spherical radius and assumed
cavity recurrence give R_*³=J a_omega/(8 pi sigma_T), with positive averaged
curvature 24 pi sigma_T. Radius remains bounded over 200 time units after ±10%
radius perturbations; removing tension or recurrence loses that lock. Halving dt
improves energy error by four. This is a reduced radial lock, not a self-held
native spatial knot. Carrier confinement and its inverse-radius frequency are
assumed. Next replace that assumption with a computed spatial recurrence and
evolving boundary work law, retaining knot, shell, Mirror and weave coupling.



### Computed spatial pressure replaces the assumed radial carrier

The [spatial pressure and closure map](../../solvers/SPATIAL_BOUNDARY_PRESSURE_AND_GAPS.md)
identifies and supplies the immediate field-to-boundary feedback for a computed
13-site four-role FCC cavity. The moving material metric and stiffness both
contribute to the reciprocal radius force. Under the same action and tension
inputs, the computed spectrum changes the balance radius from 1 to .758813219;
pressure and tension both equal .0263569473. Four 200-unit trajectories remain
bounded, including ±10% radius perturbations and a tighter-tolerance control.

Uniform relative-phase recurrences have nonzero frequencies but zero cycle-averaged radius
pressure. Their energy cannot be assigned to confinement work merely because
they recur. Five implementation/outcome checks pass. The reflecting graph and
self-similar spherical geometry remain prescribed, so this is not emergent Knot
Lock. The report specifies the remaining native-field/skin map, nonspherical
surface dynamics, exterior/Mirror channels, circulation/phase topology, shell
feedback and constitutive calibration in dependency order.


### Current balance/lock work index

[One-Wave lock status](../../solvers/ONE_WAVE_LOCK_STATUS.md) collects the verified
native compression, recurrence, domain, reciprocal path and moving-boundary
results. It identifies the next construction as one native field/closed-skin
work law with geometry derivatives and exterior/Mirror channels. The complete
architecture is retained; reduced radius locks do not promote to spatial Knot
Lock or measured Mass Effect.
