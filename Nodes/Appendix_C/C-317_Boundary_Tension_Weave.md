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

During forced boundary deformation, the weave contributes signed generalized work to the C-322 gate barrier:

\[
E_{\rm MG}
=
\int_0^{\xi_G}
\left(
P_K+P_E+P_M+P_T+P_\times
\right)d\xi.
\]

Here \(P_T=dE_{\rm weave}/d\xi\) may be positive or negative along a chosen path. A surface-tension term can assist radial contraction while still controlling confinement, equilibrium geometry, and the cross-coupled route to the Mirror Gate. The weave is load-bearing without being declared a positive resisting pressure by definition.

The weave contribution is therefore confinement/stabilization, not the complete mass mechanism and not the complete 125 GeV mechanism.

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

## Bronze Requirement

Simulate three coupled vortex fields inside a closed 3D boundary and show stable knot formation, a non-weakening extraction cost, bounded Tension-Link modes, and reclosure after neck break using one fixed parameter set.
