---
node_id: "E-533"
canonical_name: "Moving Finite-Slope Multi-Body Field"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Macro-Scale Applied Extension / Orbital Test Architecture"
claim_gate_detail: "YELLOW — candidate architecture and falsification ladder locked; finite-range boundary law and EM-to-shell coupling law not yet derived from first principles"
metadata_standard: "I-06"
---

# Node E-533: Moving Finite-Slope Multi-Body Field

**Dependencies**
Upstream: A-104 Gradient, A-105 Restoring Response, A-115 Unified Compression Field, E-509 Propagation Limit
Lateral: E-532 Bound vs Unbound Criterion and Finite Wake (same finite-range concept, micro-scale instance), C-313 Lorentz Invariance Conflict (frame audit for any drag term)
Downstream: E-534 Recursive Point-Path-Field Planetary Displacement, full Solar-System ephemeris comparison

## Purpose

Model planetary gravitational influence as an **instantaneous moving network of body-specific finite displacement/slope regions** rather than as infinite independent wells summed to infinity or a stored-memory wake. Every body's active range is a *state output*, recomputed at every timestep, not an assigned cutoff radius.

This node absorbs and consolidates the working history of the finite-wake orbital program: an initial memory/assimilation framing was tested and explicitly retired in favor of the instantaneous moving-range architecture below, which is the current canonical statement.

## Locked architectural rules

1. Every gravitating body has its own moving potential/slope profile.
2. Every profile has a body-specific finite active range; there is no universal planetary cutoff.
3. The active range is determined by slope/potential contrast against the current surrounding reference, not by an arbitrary AU radius.
4. All active regions are recomputed at every timestep as all bodies move.
5. No memory or information-relay term is added to preserve a vanished interaction.
6. Electromagnetic structure is not a direct gravity-like force. Its candidate role is modifying the stability/stiffness/response of the local displacement shell (see EM-shell coupling below).

## Field and slope

For body \(i\), define a candidate displacement potential \(\Phi_i(\mathbf r,t)\) and slope

\[
S_i(\mathbf r,t)=|\nabla\Phi_i(\mathbf r,t)|.
\]

Its active domain is

\[
\Omega_i(t)=\{\mathbf r:\ \Delta S_i(\mathbf r,t)\ \text{remains distinguishable from the current reference}\},
\qquad
\Delta S_i(\mathbf r,t)=S_i(\mathbf r,t)-S_{\rm ref}(\mathbf r,t).
\]

The finite-range boundary \(R_i(t)\) is therefore an **emergent boundary condition of the field state**, not a hand-set cutoff. Candidate boundary tests include gradient contrast, curvature contrast, displacement amplitude, or a combination constrained by the underlying lattice equations — the same family of criteria E-532 uses at micro scale for the bound/unbound flag.

## Orbital update

At body \(i\)'s position, form the instantaneous active slope state from every body whose current domain overlaps that location:

\[
S_{{\rm local},i}(t)=\sum_j I(\mathbf r_i\in\Omega_j(t))\,S_j(\mathbf r_i,t),
\]

with \(I\) an activity indicator (or a smooth boundary weight derived from the finite-range law once known). The relational driver is

\[
\Delta S_i(t)=S_{{\rm local},i}(t)-S_{{\rm ref},i}(t),
\]

and the orbital response is written abstractly as

\[
\boxed{a_i(t)=-F\bigl(\Delta S_i(t),\,K_{i,{\rm eff}}(t)\bigr)}
\]

where \(F\) must ultimately be derived from the One-Wave field dynamics rather than fitted independently per planet.

## EM-shell coupling

The EM hypothesis is shell stabilization/response modulation, not direct magnetic propulsion. For a body with a global intrinsic magnetic shell,

\[
K_{i,{\rm eff}}(t)=K_{i0}\bigl[1+\eta\,C_i(t)\bigr],
\qquad
C_i(t)=G\bigl(B_{\rm sun}(\mathbf r_i,t),\,B_i(t),\,{\rm alignment}_i(t),\,{\rm shell\ geometry}_i(t)\bigr).
\]

Mercury receives an additional term for its deep immersion in the solar magnetic environment:

\[
K_{{\rm Me},{\rm eff}}(t)=K_{{\rm Me}0}\bigl[1+\eta\,C_{\rm Me}(t)+\eta_{\rm SM}\,C_{\rm SM}(t)\bigr].
\]

Mercury's 3:2 spin-orbit resonance remains the standard gravitational/tidal control fact; the EM-shell term is not permitted to relabel it without evidence. Mars (\(C_{{\rm Mars,global}}=0\)) and Venus (\(C_{{\rm Venus,intrinsic}}=0\)) are the no-global-dipole controls. Jupiter, Saturn, Uranus, and Neptune are mandatory falsification cases: a correct shell law must not turn a large magnetic moment into an unobserved orbital correction.

## Test ladder (inherited program)

1. **Two-body control** — Sun-Earth and Earth-Moon separately; recover ordinary bounded orbital behavior.
2. **Relational multi-body system** — represent state via relational edges plus one declared scale reference; no privileged absolute coordinate.
3. **Closure attack** — identify and discard tautological closure identities; keep only non-tautological invariants/predictions.
4. **Jupiter perturbation** — predict timing/sign of Jupiter-induced change before tuning against residuals; compare to a standard ephemeris.
5. **Finite-range derivation** — derive \(R_i(t)\) from the field equations; never choose a cutoff by hand to fit data.
6. **Mercury stress test** — decompose the observed residual as
   \[
   {\rm Observed_{Mercury}}={\rm orbital}+{\rm spin\ resonance}+{\rm planetary\ perturbations}+{\rm solar\ GR/control}+{\rm EM/plasma}+{\rm candidate\ medium\ residual},
   \]
   with the candidate residual specified *before* fitting.

Required full-system test set: Sun, Mercury, Venus, Earth+Moon, Mars, Jupiter, Saturn, Uranus, Neptune, updated every timestep against a standard high-quality ephemeris control.

## Failure / falsification

Reject or revise if:

- a single arbitrary cutoff is required for all planets;
- body-specific ranges must be independently tuned merely to force a match;
- an EM coefficient must be independently tuned per magnetized planet;
- Jupiter's field produces an unobserved giant orbital correction;
- Mars or Venus require a fictitious global intrinsic shell;
- Mercury's extra coupling is defined only after inspecting the residual it explains;
- the formulation merely reconstructs ordinary Cartesian N-body dynamics in disguised coordinates (mathematically useful, but not a distinct physical result).

## Status

YELLOW / candidate architecture. This node locks the moving finite-slope test program for numerical implementation. It does not claim the celestial three-body problem, gravitational non-locality, or an EM-orbital coupling has been established.
