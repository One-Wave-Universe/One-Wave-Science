---
id: G-746
title: E1 Scalar Dual Problem and Matrix Handoff
status: split-gate
claim_boundary: GREEN only for the assumed scalar PDE; YELLOW for lattice identity, matrix physics, and E5
---

# G-746 / E1 — Scalar Dual Problem

Assumed scalar PDE (not asserted to be the One-Wave lattice branch):

\[
\partial_t^2\psi+\gamma\partial_t\psi-c_{\mathrm{eff}}^2\nabla^2\psi+\omega_0^2\psi=0.
\]

## GREEN / EXACT FOR THE ASSUMED SCALAR PDE

Temporal characteristic (real \(k\)):

\[
\omega^2+i\gamma\omega-\Omega_k^2=0,
\qquad
\Omega_k^2=c_{\mathrm{eff}}^2k^2+\omega_0^2.
\]

Exact roots:

\[
\omega_\pm(k)=-\frac{i\gamma}{2}\pm\sqrt{c_{\mathrm{eff}}^2k^2+\omega_0^2-\frac{\gamma^2}{4}}.
\]

Temporal boundaries:

- underdamped: \(\Omega_k^2>\gamma^2/4\)
- critical: \(\Omega_k^2=\gamma^2/4\)
- overdamped: \(\Omega_k^2<\gamma^2/4\)

Overdamped means \(\omega\) is imaginary at real \(k\). It is not spatial evanescence.

Spatial problem (real \(\omega\)):

\[
k(\omega)=\pm\frac{1}{c_{\mathrm{eff}}}\sqrt{\omega^2+i\gamma\omega-\omega_0^2},
\qquad
\ell_{\mathrm{att}}=\frac{1}{|\mathrm{Im}\,k|}.
\]

Underdamped propagating region, analytic group velocity:

\[
v_g=\frac{d\,\mathrm{Re}\,\omega}{dk}
=\frac{c_{\mathrm{eff}}^2k}{\sqrt{c_{\mathrm{eff}}^2k^2+\omega_0^2-\gamma^2/4}}.
\]

These six items are exact inside this linear scalar model. They are a completed scalar benchmark.

## YELLOW / NOT YET PHYSICAL CLOSURE

- whether this scalar PDE is the correct One-Wave lattice branch
- Field/Void matrix structure
- branch coupling
- microscopic origin of \(\gamma\), \(c_{\mathrm{eff}}\), \(\omega_0\)

Matrix handoff (Yellow, not a completed lattice):

\[
\det\!\left[-\omega^2 I-i\omega\Gamma+D(k)\right]=0.
\]

Two-component candidate wrappers exist in code. They do not promote the scalar PDE into the invariant engine.

A-114 discrete quadratic at general \(\gamma\) remains available as a separate exact statement for the 1-D core update rule. Finite \(\gamma\) still implies an undeclared bath.

## E5 remains YELLOW

Blocked by:

1. completed multi-branch / matrix dispersion as physics, not just algebra
2. rigorous treatment of damping / open-system energy
3. independently derived invariant \(I_0\)
4. closure that fixes \(a_0\) without 125 GeV or Hoyle back-fitting

No vacuum-mode integral. No \(c^4\mathcal{R}/(8\pi G)\). No G-745 conversion promoted. G-745 quarantine stands.

## Executable

`One_Wave_Bench/logic_core/damping_matrix_dispersion.py`
