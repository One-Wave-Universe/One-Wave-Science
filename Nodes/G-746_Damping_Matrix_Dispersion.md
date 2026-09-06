---
id: G-746
title: Damping-Matrix Dispersion and Dual E1 Problems
status: yellow-math-trail
tier: yellow
claim_boundary: exact linear algebra for declared models; not a vacuum derivation; not an a0 closure; not Mass Effect
---

# G-746 — Damping-Matrix Dispersion

**Brick:** Yellow
**Advances:** G-728 E1 (scalar exact + dual problem + matrix characteristic)
**Does not close:** E5, F5, C-322, Hoyle, a0

## 1. Scalar continuum (exact for this PDE)

Model:

\[
\partial_t^2\psi+\gamma\partial_t\psi-c_{\mathrm{eff}}^2\nabla^2\psi+\omega_0^2\psi=0.
\]

Ansatz \(\psi\propto e^{i(kx-\omega t)}\).

Temporal problem (real \(k\)):

\[
\omega^2+i\gamma\omega-\Omega_k^2=0,
\qquad
\Omega_k^2=c_{\mathrm{eff}}^2k^2+\omega_0^2,
\]

\[
\omega_\pm=-\frac{i\gamma}{2}\pm\sqrt{\Omega_k^2-\gamma^2/4}.
\]

If \(\Omega_k^2>\gamma^2/4\) the mode oscillates and decays. If \(\Omega_k^2<\gamma^2/4\) it is overdamped **in time**. That is not spatial evanescence.

Spatial problem (real \(\omega\)):

\[
k(\omega)=\pm\frac{1}{c_{\mathrm{eff}}}\sqrt{\omega^2+i\gamma\omega-\omega_0^2},
\qquad
\ell_{\mathrm{att}}=\frac{1}{|\mathrm{Im}\,k|}.
\]

Group velocity of a propagating branch:

\[
v_g=\frac{d}{dk}\mathrm{Re}\,\omega_+(k).
\]

Critical surfaces: underdamped / critical / overdamped in time; propagating / cutoff in space. Code emits all four receipts separately.

## 2. A-114 discrete update (exact quadratic, general gamma)

A-114 already has the exact characteristic for the 1-D core update and only expanded it for small \(k\), small \(\gamma\). The exact statement is

\[
z^2-(2-\gamma+C)z+(1-\gamma)=0,
\qquad
C=\beta(\cos(k\,dx)-1),
\qquad
z=e^{-i\omega\,dt}.
\]

Roots \(z_\pm\) are exact for that linear discrete rule. \(\omega=i\log(z)/dt\) is in general complex. Persistent Mode (A-112) is the non-decaying case \(|z|=1\), which forces \(\gamma=0\) in this linear model. Finite \(\gamma\) is dissipation into an undeclared bath. That is why E5 may not assign \(\tfrac12\hbar\mathrm{Re}\,\omega\) without extra work.

## 3. Matrix continuum (Field/Void capable)

\[
\ddot{\boldsymbol\psi}+\Gamma\dot{\boldsymbol\psi}+D(k)\boldsymbol\psi=0.
\]

Plane wave \(\boldsymbol\psi\propto e^{\lambda t}e^{ikx}\) with \(\lambda=-i\omega\):

\[
\boxed{\det(\lambda^2 I+\lambda\Gamma+D(k))=0.}
\]

Equivalent \(\omega\) form:

\[
\det(-\omega^2 I-i\omega\Gamma+D(k))=0.
\]

Two-component Field/Void candidate (real symmetric coupling):

\[
\Gamma=
\begin{pmatrix}\gamma_F&\gamma_\times\\ \gamma_\times&\gamma_V\end{pmatrix},
\qquad
D(k)=
\begin{pmatrix}c_F^2k^2+\omega_F^2&\kappa\\ \kappa&c_V^2k^2+\omega_V^2\end{pmatrix}.
\]

Characteristic polynomial in \(\lambda\):

\[
\lambda^4+(\gamma_F+\gamma_V)\lambda^3
+(d_F+d_V+\gamma_F\gamma_V-\gamma_\times^2)\lambda^2
+(\gamma_F d_V+\gamma_V d_F-2\gamma_\times\kappa)\lambda
+(d_F d_V-\kappa^2)=0.
\]

Decoupled limit \(\gamma_\times=\kappa=0\) recovers two independent scalar E1 roots. Coupled limit splits branches; avoided crossings are allowed. No seventh route is created. Two fields × temporal roots are branches of one linear system, not new kernel addresses.

## 4. What this does not do

- Does not fix \(c_{\mathrm{eff}},\omega_0,\gamma,\beta\).
- Does not identify 125 GeV with a zone edge (G-745).
- Does not close E5. Vacuum-mode integrals and Einstein-prefactor closures remain forbidden until an independent \(I_0\) exists and dissipation has a bath model.
- Does not replace Field/Void ontology with matrix entries. \(\Gamma\) and \(D\) are wrappers over the invariant engine.

## Executable

`One_Wave_Bench/logic_core/damping_matrix_dispersion.py`
`One_Wave_Bench/logic_core/test_damping_matrix_dispersion.py`
