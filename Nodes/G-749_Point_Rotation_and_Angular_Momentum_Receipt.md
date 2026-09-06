---
id: G-749
title: C2 Point Rotation and Angular-Momentum Receipt
status: split-gate
---

# G-749 — C2 Point rotation

## GREEN / rigid-frame bookkeeping

A Point carries an orthonormal frame \(R\in SO(3)\) (planar nest may use \(SO(2)\) as the \(z\)-rotation subgroup).

Body angular velocity \(\boldsymbol\omega\) is the unique vector satisfying

\[
\dot R = R[\boldsymbol\omega]_\times.
\]

Carried angular-momentum receipt, body frame:

\[
\mathbf L = I\boldsymbol\omega
\]

with \(I\) a declared inertia tensor and units \(\mathrm{kg\,m^2}\) for \(I\), \(\mathrm{rad/s}\) for \(\omega\), \(\mathrm{kg\,m^2/s}\) for \(L\).

Parent/child rule: child orientation in Ground is

\[
R_{\mathrm{child}}^{\mathrm{ground}} = R_{\mathrm{parent}}^{\mathrm{ground}} R_{\mathrm{child}}^{\mathrm{parent}}.
\]

Do not add parent \(\boldsymbol\omega\) to child \(\boldsymbol\omega\) as if they lived in one frame. Transport first, then add. That is the start of C8 (no double count).

## YELLOW / not yet physics

- \(I\) is declared, not derived from the hex/pyramid nest
- this is not Path circulation and not Field curl
- six pyramid axes are available frames, not six kernel routes
- no Mass Effect from spin

## Attached nest (G-748)

Default planar Points sit on hexagon vertices plus center. Bipyramid apices are the first out-of-plane Points. C3 must rotate the Path that joins them without writing that rotation into \(R\).

## Next

C3 Path rotation: turning / circulation / curvature of the transported center along an edge of the hex or a pyramid lateral.
