---
id: G-758
title: Nudged elastic band between seven-cell wells
status: yellow
---

# G-758 — NEB

## Method (Henkelman / Jónsson)

A chain of images \(q_0,\ldots,q_N\) with ends fixed at two holds.

Tangent \(\hat\tau_i\) from the higher-energy neighbor (improved tangent), not the centered difference, or the band kinks.

True force only perpendicular to the path; springs only along it:

\[
F_i = -\nabla E(q_i)\big|_{\perp\hat\tau_i} + k\big(|q_{i+1}-q_i|-|q_i-q_{i-1}|\big)\hat\tau_i.
\]

Climbing image at the current maximum:

\[
F_{\mathrm{climb}} = -\nabla E\big|_{\perp} + (\nabla E\cdot\hat\tau)\hat\tau
\]

(invert the parallel component so that image walks *up* to the saddle).

That saddle is the candidate \(\mathbf q^{\ddagger}\) in C-322. The barrier is \(E(q^{\ddagger})-E(q_0)\), still dimensionless.

## This slice

First band: **amplitudes only** (7-D), phases held at 0, ends `dipole_seed(0.08,0)` and `dipole_seed(0.08,pi)`. Nine images, 250 steps, crude step size.

Wells: \(E=0.01152\).
Highest image found: \(E\approx 0.203\) at image 1, barrier \(\approx 0.191\).

**Not converged.** Energy is not a single clean peak. Images 2–6 still wander. Do not treat 0.191 as \(\Delta\mathcal E_G\).

Still required: gauge-fixed 14-D path (phases wrapped), improved tangent, tighter springs, Hessian at the climbing image (one negative mode if it is a first-order saddle).

No GeV. No a0.
