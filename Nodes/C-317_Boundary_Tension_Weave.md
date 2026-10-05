---
node_id: "C-317"
canonical_name: "Boundary-Tension Weave"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Boundary Mechanics / Terminology Anchor"
claim_gate_detail: "YELLOW (geometry and energy forms) / GREEN (full QCD replacement claim)"
metadata_standard: "I-06"
---

# Node C-317: Boundary-Tension Weave

**Standard mapping:** gluon field, gluon excitations, strong-force confinement



**Dependencies**
Upstream: A-112 Persistent Mode, A-116 Three-Dimensional Spherical Default, E-503 Pressure, E-504 Surface, E-505 Coupling, Book 1 Ch2 Proton
Downstream: C-318 Four-Interaction Mass-Effect Response, C-321 Reduced Multi-Center Tension Network, C-322 Mirror-Gate Boundary Response, Book 1 Ch2 Proton, Book 1 Ch6 Nucleus, future quark/proton simulations

## Definition

The **Boundary-Tension Weave** is the continuous 3D surface-and-volume coupling that holds Vortex Phases inside a bounded knot.

A conventionally measured gluon contribution maps to a **Tension-Link excitation**: a local vibration, twist, or coupling mode of this weave. It is not treated as a free messenger bead traveling between independent quarks.

The standard names remain in Gray comparison sections. The One-Wave names describe the proposed mechanism.

## 1. Three-Dimensional Knot Geometry

Let the proton occupy a bounded 3D region \(\Omega_p\) with closed boundary \(\partial\Omega_p\simeq S^2\) in the lowest-energy state.

Let three internal Vortex Phases be

\[
\psi_a(\mathbf x,t),\qquad a\in\{1,2,3\}.
\]

They are phase components of one Three-Vortex Knot, not three independently isolatable objects.

## 2. Weave Energy

Use the candidate energy

\[
E_{\rm weave}=E_{\rm skin}+E_{\rm phase}+E_{\rm twist}.
\]

Surface term:

\[
E_{\rm skin}=\sigma_T\int_{\partial\Omega_p}dA.
\]

Phase-locking term:

\[
E_{\rm phase}
=
\frac{\kappa_T}{2}
\sum_{a<b}
\int_{\Omega_p}|\psi_a-\psi_b|^2\,dV.
\]

Twist/vorticity term:

\[
E_{\rm twist}
=
\frac{\eta_T}{2}
\sum_a
\int_{\Omega_p}|\nabla\times\mathbf v_a|^2\,dV.
\]

The coefficients \(\sigma_T,\kappa_T,\eta_T\) are not derived yet.

## 3. Tension-Link Excitations

Let the spherical boundary deform as

\[
r(\theta,\phi,t)=R_p+\eta(\theta,\phi,t),
\]

with

\[
\eta=\sum_{\ell,m}a_{\ell m}(t)Y_{\ell m}(\theta,\phi).
\]

The amplitudes \(a_{\ell m}\), together with internal phase/twist modes, are the candidate Tension-Link excitation coordinates. The standard gluon spectrum must eventually be reproduced from these eigenmodes; renaming them does not accomplish that derivation.

## 4. Knot Lock / Confinement

If one Vortex Phase is forced away from the bounded knot, the spherical weave forms an elongated neck. Let the neck have approximately fixed radius \(a\), length \(L\), and lateral area

\[
A_{\rm neck}(L)\approx2\pi aL.
\]

With surface-energy density \(\sigma_T\) in joules per square metre,

\[
E_{\rm neck}(L)\approx\sigma_TA_{\rm neck}
=2\pi a\sigma_TL.
\]

Define the effective line tension

\[
\tau_T\equiv2\pi a\sigma_T,
\]

so

\[
E_{\rm neck}(L)=\tau_TL,
\qquad
F_{\rm lock}=\frac{dE_{\rm neck}}{dL}=\tau_T.
\]

The dimensions now close: \([\sigma_T]={\rm J\,m^{-2}}\), \([\tau_T]={\rm J\,m^{-1}}={\rm N}\). The extraction cost does not fall with separation. This is the One-Wave **Knot Lock** candidate.

When the neck energy exceeds a reclosure threshold \(E_{\rm break}\), the expected process is Boundary Reweaving:

\[
E_{\rm neck}\ge E_{\rm break}
\quad\Rightarrow\quad
\text{neck break + new bounded knots}.
\]

The threshold and products are not derived.

## 5. Three-Body Structure

Inside an intact proton, the default is not three literal straight strings. The spherical weave distributes tension over the closed boundary and through the internal volume. C-321 remains responsible for reduced junction/network approximations when three or more separated centers must be modeled.


## 6. Role in Mass Effect and the Mirror Gate

C-317 does not derive Mass Effect by itself. The weave is one of four coupled interactions in C-318.

During translation, the weave must be carried and reclosed with the knot, electrical shell, and Mirror relation. Its diagonal and cross-coupled response contributes to the Mass-Effect tensor.

The weave contributes diagonal and cross terms to the joint Hessian H. Boundary excitation couples and shifts phase through the passive resolvent H−ω²W−iω(BBᵀ+Γ). It does not force a path through a barrier. The carried-profile energy Hessian and the boundary response are computed together in the linked executable replacement.

The surface, phase and twist coefficients above still require derivation. The linear cavity control preserves the four-role coupling structure but does not claim to have derived the nonlinear weave or stable three-vortex profile.

## One-Wave Naming Chain

```text
quark -> Vortex Phase
gluon field -> Boundary-Tension Weave
gluon -> Tension-Link excitation
strong force -> Boundary-Tension Binding
color charge -> Phase Address
confinement -> Knot Lock
hadronization -> Boundary Reweaving
proton -> Three-Vortex Knot
```

## Yellow Audit

- \(\sigma_T,\kappa_T,\eta_T\) and the neck radius \(a\) are unknown.
- The eigenmode spectrum has not been matched to measured gluon/QCD observables.
- Running coupling and short-distance behavior are not derived.
- Boundary Reweaving products and rates are not derived.
- The relationship between the spherical intact-knot model and C-321's reduced junction geometry needs simulation.

## Constructive replacement for the Phase 5 numerical claim

The earlier assigned octave pressures and mixed scale labels do not constitute a derivation of quark masses or validated proton confinement. Their historical text is preserved in [the pinned pre-replacement version](https://github.com/One-Wave-Universe/One-Wave-Science/blob/0f005afb9afc8ac15a1ea061c2900cf3f6b0187c/Nodes/C-317_Boundary_Tension_Weave.md).

The replacement below supplies a runnable native 3D joint operator, energy conservation, phase/power response, carried-profile curvature, coupling ablation and mesh refinement. It has no fitted particle labels. Nonlinear knot formation and the weave's actual constitutive coefficients remain the next physical derivation, with the Bronze tests below providing its acceptance conditions.

## Bronze Requirement

Simulate three coupled vortex fields inside a closed 3D boundary and show stable knot formation, a non-weakening extraction cost, bounded Tension-Link modes, and reclosure after neck break using one fixed parameter set.

## Executable joint-response replacement (2026-10-04)

The four-interaction calculation now runs on D-409's native twelve-neighbor 3D FCC shell. See [the derivation](../solvers/JOINT_RESPONSE_DERIVATION.md), [solver](../solvers/joint_boundary_response.py) and [complete results](../solvers/joint_response_results.json).

One declared joint operator computes exact discrete energy, passive coupling and phase response, boundary-coordinate inertia and carried-profile energy curvature. Eleven tests pass. The 500-step relative energy drift is below 9.38e-14; the maximum lossless power-ledger error is below 1.34e-15. Cross-coupling removal eliminates interaction-port transfer. No measured mass or 125 GeV target is an input.

Refinement from 13 to 55 to 177 sites changes the first spatial frequency from 0.459660896 to 0.632761487 to 0.683984404. These are dimensionless candidate-cavity results. A self-held knot, constitutive coefficients, physical amplitude, absolute units and observable channel mapping remain required before a particle-mass claim. The imposed reflecting cavity is a conservation control, not demonstrated confinement. Boundary ports currently describe interaction coordinates rather than angular bounce, roll-off or spatial scattering distributions.



## Pressure–tension radius-balance candidate (2026-10-05)

The [reduced boundary calculation](../solvers/RECIPROCAL_BALANCE_AND_LOCK.md)
makes the spherical surface energy a reciprocal pressure-work model. Assuming
Omega(R)=a_omega/R for one cavity recurrence, its adiabatic action J gives
U_avg=J a_omega/R+4 pi sigma_T R². Wave and surface pressures match at
R_*³=J a_omega/(8 pi sigma_T), with averaged radial curvature 24 pi sigma_T>0.

The executable evolves the free radius and carrier through the instantaneous
Hamiltonian; R is not clamped and J is not reset. With illustrative fixed inputs,
balanced radius remains .998849–1.001255 over 200 time units. Both ±10% radius
perturbations remain bounded. Removing either tension or recurrence loses the
radius screen; timestep energy error improves by four. See the
[raw results](../solvers/boundary_balance_lock_results.json).

This 3D area-law balance assumes the spatial reflecting carrier and its
inverse-radius frequency. It does not derive confinement, Three-Vortex Knot,
electrical shell or Mirror phase lock. Surface coefficient and boundary kinetic
weight are illustrative, not measured Mass Effect. The result is a quantitative
target for the native evolving-boundary solver, not Bronze completion or a
node-gate promotion.



## Computed spatial pressure and missing interface (2026-10-05)

The [spatial boundary-pressure control](../solvers/SPATIAL_BOUNDARY_PRESSURE_AND_GAPS.md)
replaces the previous assumed carrier coefficient with the native 13-site
four-role reflecting-cavity spectrum. The reciprocal skin force includes both
the field-stiffness derivative and the moving kinetic-metric derivative. With
the previous action and tension inputs, the actual balance radius is .758813219,
not 1; both pressures are .0263569473 and averaged curvature is positive. Four
200-unit runs, including ±10% radius perturbations, stay bounded with accepted-step
energy error below 1e-12. Five controls pass.

Uniform phase recurrences can have nonzero frequency yet zero geometric pressure.
Total recurrence energy is therefore not automatically confinement work. This
control still prescribes the reflecting graph and self-similar spherical shape.
Its four role coordinates are response fixtures, not a derived knot/shell/Mirror/
weave state. Full native field-to-skin mapping, freely deforming closed geometry
and exterior/phase coupling remain the next interface closure. No node metadata
or gate changes; no physical Knot Lock or Mass Effect is assigned.
