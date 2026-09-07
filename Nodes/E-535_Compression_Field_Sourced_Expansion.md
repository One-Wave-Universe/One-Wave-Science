---
node_id: "E-535"
canonical_name: "Compression-Field-Sourced Expansion"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Cosmology / Redshift / Derivation Attempt"
claim_gate_detail: "YELLOW (the reduction to a collective-coordinate oscillator, Sections 1-3, is a clean derivation from A-115's own field equation) / BROWN (the specific j(t) profile needed to match real H(z) data is not attempted) / PROPOSED, not adopted: this directly contradicts E-528's Hard Constraint and Book 5 Ch4's 'no expansion variable' rule, which this node does not edit"
metadata_standard: "I-06"
---

# Node E-535: Compression-Field-Sourced Expansion

**Dependencies**
Upstream: A-115 Unified Compression Field (Section 1 field equation), E-530 White Energy Recirculation Loop, E-534 Static-Space Time-Dilation No-Go Theorem, A-101 Ground/Zero, A-105 Restoring Response
Downstream: would require revising E-528 Static Redshift Transport (Hard Constraint), Book 5 Ch4 (Section "No expansion variable is permitted"), ONE_WAVE_SCIENCE_ATTACK_MAP.md Section L

## Purpose

E-534 Section 6 named one route left open after the no-go theorem: derive
expansion-like spatial time-dependence *from* the compression field's own
dynamics, rather than importing it as an external postulate. This node takes
that route as far as it currently goes.

**This is a proposal, not an adoption.** It directly contradicts two live
rules: E-528's Hard Constraint ("no expansion of space... no Hubble
expansion term") and Book 5 Ch4's explicit statement ("No expansion variable
is permitted in future One-Wave equations"). This node does not edit either
of those. Lifecycle is set to `PROPOSED_BUILD`, not `ACTIVE`, precisely
because accepting this result requires a deliberate decision to revise those
rules, which is not this node's call to make unilaterally.

## 1. The homogeneous dilation mode

A-115 Section 1 gives the field equation for displacement \(\mathbf u(\mathbf
x,t)\) away from Ground/Zero:

\[
\rho_u\partial_t^2\mathbf u+\mu_u\partial_t\mathbf u
-K_\chi\nabla(\nabla\cdot\mathbf u)-S_u\nabla^2\mathbf u
+\frac{\partial V_b}{\partial\mathbf u}=\mathbf J_{\rm source}.
\]

Consider the ansatz

\[
\mathbf u(\mathbf x,t)=\mathbf x\,f(t)
\]

— a spatially uniform *dilation*: every point moves radially outward from
whatever origin is chosen, in proportion to its own distance from it, by a
common time-dependent factor \(f(t)\). This is not a new field; it is one
specific mode of the same \(\mathbf u\) that already carries gravity and Mass
Effect elsewhere in A-115.

Two physically meaningful quantities from this mode are finite and spatially
uniform (\(\mathbf x\)-independent):

\[
\chi=-\nabla\cdot\mathbf u=-3f(t),
\qquad
\nabla\mathbf u=f(t)\,\mathbb{1}
\quad(\text{uniform strain}).
\]

The bare displacement \(\mathbf u=\mathbf xf(t)\) itself is origin-dependent
(shifting the origin shifts \(\mathbf u\) by a constant) and is not
physical on its own — exactly as in Newtonian treatments of a uniformly
expanding medium, only the strain/relative quantities are physical.

**Physical picture.** If \(f(t)\) grows, the proper separation between any
two points originally at \(\mathbf x_1,\mathbf x_2\) becomes
\((\mathbf x_1-\mathbf x_2)(1+f(t))\). Define

\[
a(t)\equiv1+f(t).
\]

This is not a coordinate relabeling. Unlike the flat-lapse case ruled out in
E-534 Section 2 (\(ds^2=-\alpha(t)^2dt^2+d\mathbf x^2\), spatial part fixed),
here the *spatial* separation itself grows — this is exactly the case E-534's
Corollary identifies as the only one where redshift-linked time dilation
survives, because it cannot be undone by reparametrizing time.

## 2. Reducing the field equation to a collective-coordinate oscillator

Two of the field equation's spatial-derivative terms vanish identically for
this ansatz, because \(\chi\) and \(\nabla\mathbf u\) are already
\(\mathbf x\)-independent:

\[
\nabla(\nabla\cdot\mathbf u)=\nabla(3f(t))=0,
\qquad
\nabla^2\mathbf u=f(t)\nabla^2\mathbf x=0.
\]

Naively substituting suggests \(K_\chi\) and \(S_u\) simply drop out of
\(f(t)\)'s equation of motion. That naive step is not trusted here — instead,
Section 3 derives the correct effective equation properly, because these
terms *do* carry finite energy for this mode (\(\propto\chi^2\) and
\(\propto|\nabla\mathbf u|^2\), both uniform and nonzero) even though they
exert no local bulk force. The two facts are not contradictory: a spatially
uniform stress has zero divergence (no net local force) while still costing
energy — the correct way to get its effect on \(f(t)\) is the standard
collective-coordinate (Milne-sphere) construction, not term-by-term
substitution into the local PDE.

## 3. Collective-coordinate derivation (the checked version)

Take the field Lagrangian density consistent with A-115's stated energy
density and field equation,

\[
\mathcal L=\frac{\rho_u}{2}|\partial_t\mathbf u|^2
-\frac{K_\chi}{2}\chi^2-\frac{S_u}{2}|\nabla\mathbf u|^2-V_b(\mathbf u)
+\mathbf J_{\rm source}\cdot\mathbf u,
\]

with dissipation handled by a Rayleigh function
\(\mathcal R=\frac{\mu_u}{2}|\partial_t\mathbf u|^2\) (the damping term is
non-conservative and cannot come from \(\mathcal L\) alone). Integrate over a
finite comoving ball of coordinate radius \(R_0\) — the standard device
(McCrea-Milne construction) for giving a homogeneous mode a well-defined,
finite collective Lagrangian, tracking the \(R_0\)-dependence rather than
assuming it drops out.

With \(\mathbf u=\mathbf xf(t)\), \(\mathbf J_{\rm source}=\mathbf xj(t)\)
(a coarse-grained, spatially uniform driving profile — Section 4 identifies
its candidate source), and the moment integral
\(I_2\equiv\int_{|\mathbf x|<R_0}|\mathbf x|^2\,d^3x=\frac{4\pi}{5}R_0^5\):

\[
\Lambda(f,\dot f)=\frac{\rho_u}{2}I_2\dot f^2
-6\pi K_\chi R_0^3f^2-2\pi S_uR_0^3f^2-V_b^{\rm eff}(f)
+I_2\,j(t)f,
\]

where \(V_b^{\rm eff}(f)\) is the integrated potential term (its form
depends on whether \(V_b\) is taken to depend on bare \(\mathbf u\) or only
on translation-invariant combinations — see Section 5). Applying the
Euler-Lagrange equation with dissipation,
\(\frac{d}{dt}\frac{\partial\Lambda}{\partial\dot f}-\frac{\partial\Lambda}{\partial f}+\frac{\partial\mathcal R_{\rm int}}{\partial\dot f}=0\),
and dividing through by \(I_2\):

\[
\rho_u\ddot f+\mu_u\dot f
+\underbrace{\frac{5(3K_\chi+S_u)}{R_0^2}}_{\to\,0\text{ as }R_0\to\infty}f
+\frac{1}{I_2}\frac{\partial V_b^{\rm eff}}{\partial f}
=j(t).
\]

**The \(K_\chi,S_u\) contribution scales as \(1/R_0^2\) and vanishes as
\(R_0\to\infty\).** This confirms, by the correct method rather than the
naive one, that these gradient-stiffness terms genuinely decouple from the
bulk collective mode in the homogeneous/cosmological limit — they are
gradient (surface-tension-like) terms, and their influence on an
increasingly large, increasingly uniform region shrinks exactly as expected
for a term of that character. This is a real, checked result, not an
assumption.

## 4. Candidate source: White Energy, coarse-grained

E-530 already posits a **local**, threshold-triggered White Energy release
(quasar/white-hole-scale ejection) as an outward channel of the same
compression field. This node's new hypothesis — not previously stated
anywhere else in the repository, and explicitly flagged as new — is that
the **population average** of many such local release events, coarse-grained
over a large enough comoving volume, sources the homogeneous dilation mode's
driving term \(j(t)\):

\[
j(t)\ \propto\ \langle P_W\rangle_{\rm population}(t)
\]

using E-530's own \(P_W=D_Wh\,U_C\). This is consistent with — not a
replacement for — E-530's local picture: individual White Energy events stay
local, threshold-triggered, quasar/white-hole-scale ejections exactly as
E-530 describes; only their large-scale *average* is proposed to source the
homogeneous mode here. This identification is a new assumption of this node
and is not yet justified beyond plausibility; it needs its own derivation
before being treated as established (see Failure Conditions).

## 5. A structural constraint this surfaces on \(V_b\)

Section 3 assumed \(V_b\) could depend on bare \(\mathbf u\) (giving a
mass-like term, e.g. \(V_b=\frac{m_u^2}{2}|\mathbf u|^2\)). But bare-\(\mathbf
u\) dependence breaks ordinary translation invariance: shifting the origin
changes \(\mathbf u\) but should not change the physics. A strictly
translation-invariant \(V_b\), built only from \(\chi\) and/or \(\nabla
\mathbf u\), would fold into the already-counted \(K_\chi\)-type term at this
order and contribute no independent restoring term to \(f(t)\) — meaning a
strictly translation-invariant version of this model has **no mass term at
all** for the homogeneous mode (only friction \(\mu_u\) and driving \(j(t)\)
remain: \(\rho_u\ddot f+\mu_u\dot f=j(t)\), a pure driven integrator).

There is a motivated way to keep the mass term without an ad hoc
translation-invariance violation: **Ground/Zero (A-101) is already a
distinguished reference in this framework, not an arbitrary origin.** A term
that restores \(\mathbf u\) toward Ground/Zero specifically is not breaking
translation invariance of "empty space" — it is using the one reference
point this framework already privileges by construction. This is noted as a
genuine consistency point in this framework's own favor, not a
post-hoc patch: A-105 Restoring Response already establishes restoring-toward-Ground
as a first-class primitive elsewhere in the repository.

Either way — with or without the mass term — Section 3's main result (the
\(K_\chi,S_u\) decoupling in the \(R_0\to\infty\) limit) holds unchanged.

## 6. Consequence: redshift and time dilation both fall out for free

If \(a(t)=1+f(t)\) governs the physical separation between comoving points
the way Section 1 sets up, then light propagating through this background
satisfies the ordinary null-geodesic relation

\[
1+z=\frac{a(t_o)}{a(t_e)},
\]

and by E-534 Section 2's own corollary, **this is exactly the case where
time dilation is not cancelled**:

\[
\frac{d\tau_o}{d\tau_e}=\frac{a(t_o)}{a(t_e)}=1+z.
\]

Both the redshift law and the time-dilation result that falsified E-528's
static propagation law (E-533 Sections 2-3) come from the *same* \(a(t)\)
here, automatically matched to each other — the same structural feature that
makes standard FRW cosmology consistent, now obtained from A-115's own field
equation instead of asserted. **If this route is adopted, E-528's separate
\(\kappa_\gamma\) propagation-loss law becomes redundant** for the
homogeneous/cosmological redshift channel — the redshift would be a
consequence of \(a(t)\), not a separate propagation phenomenon. E-528's
propagation-loss picture might still have a role for genuinely local,
inhomogeneous energy loss (dust, plasma, gravitational redshift near
sources), which this node does not address.

## 7. What this is not

- **Not a fit to data.** \(j(t)\), \(\rho_u\), \(\mu_u\), and (if kept) the
  Ground-restoring mass term are all uncalibrated. Whether any choice of
  these reproduces the actual measured expansion history (matter-domination
  \(a\propto t^{2/3}\)-like early behavior transitioning to the observed
  late-time acceleration) is not checked here. This is Bronze-level work,
  not attempted.
- **Not a replacement for General Relativity's machinery.** No claim is made
  that this reproduces the Einstein field equations, only that a specific
  compression-field mode produces a genuine, non-artifact scale factor with
  the right qualitative relationship between redshift and time dilation.
- **Not an endorsement of standard \(\Lambda\)CDM's mechanism for
  acceleration.** Standard cosmology's late-time acceleration is itself an
  unexplained fitted term (\(\Lambda\)/dark energy). If this route is
  developed further and \(j(t)\) or the Ground-restoring term can be tied to
  a *derived* quantity elsewhere in the framework, that would be a
  substantive difference from simply refitting \(\Lambda\)CDM's free
  parameter under a new name — but that is future work, not a result of this
  node.

## Failure Conditions

This node fails, or must be revised, if: the collective-coordinate reduction
in Section 3 is shown to be wrong or the \(R_0\to\infty\) limit inapplicable
to the physically relevant regime; if the White Energy coarse-graining
hypothesis (Section 4) cannot be derived from E-530's own local dynamics and
is shown to require an independent, unmotivated new energy source; if no
choice of \(j(t)\) and remaining free parameters can reproduce the observed
expansion history within reasonable priors; or if adopting a Ground-relative
mass term (Section 5) is judged inconsistent with how A-101/A-105 are used
elsewhere. Any of these should be recorded honestly rather than patched
around — consistent with this node's own `PROPOSED_BUILD` status: it is a
candidate, not a claim.

## Required Next Step Before Promotion

Revise E-528's Hard Constraint and Book 5 Ch4's "no expansion variable"
rule — explicitly, as a deliberate decision, not silently — before any
downstream node treats this as adopted. This node does not make that
decision; it only shows that the alternative (a compression-field-derived
scale factor) is available and internally consistent as far as it has been
checked.
