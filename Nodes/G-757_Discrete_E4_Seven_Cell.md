---
id: G-757
title: Discrete four-interaction energy on the seven-cell
status: yellow
claim_boundary: dimensionless discrete energy and critical-point tests only; not C-322 numerical close; not a0; not proton observables
---

# G-757 — Discrete \(\overline E_4\) on the seven-cell

The HTML bead was a sketch. This node is the first energy that actually lives on D-408 / G-743 geometry.

## State

Sites \(S=\{c\}\cup R\) with \(|R|=6\), center \(c=(0,0)\), ring from `NEIGHBOR_OFFSETS`.

Each site carries amplitude and phase

\[
\psi_i=a_i e^{i\varphi_i},\qquad a_i\ge 0,\quad \varphi_i\in\mathbb R/2\pi\mathbb Z.
\]

Fourteen real coordinates. No extra hidden fields.

Ring edges \(E_R\) are the six cycle edges. Radial edges \(E_c\) join \(c\) to each ring site. Incidence and Laplacian are those of `hex_lattice_graph.py`.

## Dimensionless energy

C-322 scale freedom still holds: multiply \(\overline E_4\) by \(\lambda>0\) and the critical-point *locations* do not move. Units are not chosen here.

\[
\overline E_4
=
E_K+E_E+E_M+E_T+E_\times.
\]

### Knot / circulation \(E_K\)

Wrapped ring circulation

\[
\Gamma
=
\sum_{(i,j)\in E_R}\mathrm{wrap}(\varphi_j-\varphi_i)\in(-\pi,\pi].
\]

For a single-winding target \(\Gamma_\star=\pm 2\pi\) this first slice uses the *small-wrap* quadratic, valid near a chosen branch, not a global topology solver:

\[
E_K
=
\alpha_K\big(\Gamma-\Gamma_\star\big)^2
+
\beta_K\sum_{(i,j)\in E_R}(a_i-a_j)^2
+
\gamma_K\,a_c\sum_{i\in R}(1-\cos(\varphi_i-\varphi_c)).
\]

Third term: center phase locked to the ring (Josephson / XY).

### Electrical shell \(E_E\)

\[
R
=
\frac{\frac16\sum_{i\in R}a_i}{a_c+\varepsilon},\qquad
E_E=\alpha_E(R-R_\star)^2+\delta_E(a_c-1)^2.
\]

\(R_\star\) is a declared shell-to-core ratio, not a measured proton radius.

### Mirror \(E_M\)

Even / odd ring modes (index ring sites \(0\ldots5\) in cycle order):

\[
C=\sum_{k=0}^{5}a_k\cos\frac{2\pi k}{6},\qquad
S=\sum_{k=0}^{5}a_k\sin\frac{2\pi k}{6},\qquad
\theta=\mathrm{atan2}(S,C).
\]

\[
E_M=\alpha_M\sin^2\theta.
\]

This is the *first even* two-well in the dipole angle. \(\theta=0\) and \(\theta=\pi\) are the intended basins. Whether they survive once \(E_K,E_T,E_\times\) are on is a computed fact, not a drawing.

### Weave \(E_T\)

\[
E_T
=
\alpha_T\big(R-R_\star-\kappa(\Gamma-\Gamma_\star)\big)^2
+
\beta_T\sum_{i\in R}(a_i-a_c R_\star)^2.
\]

Shell and circulation are not allowed to drift independently. That is the weave as a penalty, not a fabric picture.

### Cross \(E_\times\)

\[
E_\times
=
\chi\,(a_c-1)\,S.
\]

One declared product. No other hidden crosses in this slice.

## Stationarity

A hold \(\mathbf q_0\) is a point with

\[
\nabla_a\overline E_4=0,\qquad
\nabla_\varphi\overline E_4=0
\]

and Hessian positive-definite on the physical slice that quotients global phase \(\varphi_i\mapsto\varphi_i+\alpha\).

Global phase is a zero mode. Circulation branch is not.

A mirror partner is a second critical point \(\mathbf q_\pi\) with \(\theta\approx\pi\) and comparable \(\overline E_4\).

The gate is **not** assigned here. C-322 still requires a minimum-work path \(\Gamma_{0\to G}\) on this energy, then the first loss of the original basin. That path is not the HTML shove.

## What this slice does not do

- Does not pick \(\alpha_\bullet\) from 125 GeV.
- Does not identify \(\Gamma_\star\) with baryon number or color.
- Does not use damping as mass.
- Does not replace C-318's four named interactions with new ontology; it *discretizes* them on seven sites.

## Next honest calculations (in order)

1. Confirm a symmetric ring (equal \(a_i\), locked phases) is stationary for \(S=C=0\) when \(\chi=0\).
2. Turn on a small dipole seed and see which well it falls into.
3. Finite-difference Hessian at both wells; count unstable modes.
4. Only then a discrete nudged path between wells.
5. Only after a dimensionless barrier exists may anyone talk about \(\mathcal R_G\).
