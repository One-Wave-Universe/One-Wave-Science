---
id: G-750
title: Body-Rate Transport Mechanics
status: split-gate
---

# G-750 — Body-rate transport

## GREEN / SO(3) kinematics

Frames: Ground, parent body, child body.

\[
R_{\mathrm{child}}^{\mathrm{ground}}=R_{\mathrm{parent}}^{\mathrm{ground}}R_{\mathrm{child}}^{\mathrm{parent}}.
\]

Body-rate definition:

\[
\dot R=R[\boldsymbol\omega]_\times.
\]

Differentiate the product:

\[
\dot R_g=\dot R_p R_c+R_p\dot R_c
=R_p[\boldsymbol\omega_p]_\times R_c+R_p R_c[\boldsymbol\omega_c]_\times.
\]

Factor \(R_g=R_p R_c\):

\[
\dot R_g=R_g\Big(R_c^{\top}[\boldsymbol\omega_p]_\times R_c+[\boldsymbol\omega_c]_\times\Big).
\]

Adjoint identity \(R^{\top}[\mathbf v]_\times R=[R^{\top}\mathbf v]_\times\) gives the exact compose rule in **child body axes**:

\[
\boxed{\boldsymbol\omega_{g,\mathrm{body}}=\boldsymbol\omega_c+R_c^{\top}\boldsymbol\omega_p.}
\]

Ground-frame rate is the rotation of that vector:

\[
\boldsymbol\omega_{g,\mathrm{ground}}=R_g\boldsymbol\omega_{g,\mathrm{body}}=R_p\boldsymbol\omega_p+R_g\boldsymbol\omega_c.
\]

Same content, two charts. Transport first, then add. Adding \(\boldsymbol\omega_p+\boldsymbol\omega_c\) in mixed axes is illegal.

Planar nest (G-748 hex): all rates along \(\hat z\), \(R_c^{\top}\boldsymbol\omega_p=\boldsymbol\omega_p\), so rates just add. That is a special case, not the 3D law. Bipyramid apices need the full adjoint as soon as a lateral tilts.

## Receipts

- Point rotation remains C2 / G-749.
- This node only fixes how rates move across a nest boundary (start of C8).
- Path circulation is still not this vector.
- \(I\) is still declared. \(\mathbf L=I\boldsymbol\omega\) after transport, in one named frame.

## YELLOW

Which nest edge is a parent/child joint is a modeling choice. Hex center as parent of six vertices is allowed as a convention, not a derivation.
