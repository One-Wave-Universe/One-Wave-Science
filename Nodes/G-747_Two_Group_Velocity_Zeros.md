---
id: G-747
title: Two Group-Velocity Zeros
status: split-gate
---

# G-747 — Two Group-Velocity Zeros

Do not treat these as one mechanism.

## GREEN / continuum scalar (same PDE as G-746)

Underdamped analytic identities:

\[
v_g=\frac{c_{\mathrm{eff}}^2 k}{\sqrt{c_{\mathrm{eff}}^2k^2+\omega_0^2-\gamma^2/4}},
\qquad
v_p=\frac{\sqrt{c_{\mathrm{eff}}^2k^2+\omega_0^2-\gamma^2/4}}{k},
\qquad
v_g v_p=c_{\mathrm{eff}}^2.
\]

This continuum model has **no Brillouin zone**. \(v_g\to 0\) only at \(k=0\) (massive rest) or when the temporal discriminant vanishes. That cutoff is not a lattice edge and does not define \(a_0\).

## GREEN / A-114 discrete chain at \(\gamma=0\)

\[
\cos(\omega\Delta t)=1+\frac{\beta}{2}\big(\cos(k\Delta x)-1\big).
\]

At the first zone edge \(k=\pi/\Delta x\), \(v_g=0\). Small-\(k\) speed recovers A-114: \(c_L\sqrt{\beta/2}\).

This zero requires a spacing \(\Delta x\) already present in the stencil. It does not derive \(\Delta x\).

## YELLOW / not permitted

- identifying the continuum cutoff with the discrete zone edge
- setting either zero equal to 125 GeV
- feeding either zero into a Hoyle solver
- calling either zero Mass Effect

## Next

C2 Point rotation, or A-114 \(v_g(k)\) at finite \(\gamma\) without renaming decay as evanescence.
