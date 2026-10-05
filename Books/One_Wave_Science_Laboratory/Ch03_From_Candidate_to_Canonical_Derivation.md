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
