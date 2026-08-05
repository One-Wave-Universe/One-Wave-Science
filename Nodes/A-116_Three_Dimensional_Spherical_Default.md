---
node_id: "A-116"
canonical_name: "Three-Dimensional Spherical Default"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Foundation Geometry Rule"
claim_gate_detail: "YELLOW (minimum-surface geometry) / GREEN (universal application)"
metadata_standard: "I-06"
---

# Node A-116: Three-Dimensional Spherical Default

**Dependencies**
Upstream: A-102 Displacement, A-104 Gradient, A-106 Pressure Response, A-107 Bounded Motion, A-112 Persistent Mode, A-113 Projection, E-504 Surface, E-517 Negative Space
Downstream: A-117 Dimensional Integrity, D-409 Twelvefold 3D Coordination, Book 1 Ch1 Particle, Book 1 Ch2 Proton, C-317 Boundary-Tension Weave, C-321 Reduced Multi-Center Tension Network, all physical diagrams

## Purpose

A physical One-Wave structure is three-dimensional and volumetric unless a node explicitly states that it is describing a 2D cross-section, projection, or negative-space layer.

The default stable boundary is spherical or sphere-like. Internal vortices and knots may be topologically complex, but they exist inside a closed 3D envelope.

## Minimum-Surface Derivation

For an isotropic boundary tension \(\sigma>0\), the surface contribution is

\[
E_s=\sigma A.
\]

For fixed enclosed volume \(V\), the isoperimetric inequality gives

\[
A^3\ge 36\pi V^2,
\]

with equality only for a sphere. Therefore

\[
A_{\min}=(36\pi V^2)^{1/3},
\qquad
E_{s,\min}=\sigma(36\pi V^2)^{1/3}.
\]

So an undriven bounded mode with isotropic surface tension has a spherical lowest-energy envelope.

## Deformation

Let the boundary be

\[
r(\theta,\phi,t)=R_0+\eta(\theta,\phi,t).
\]

Expand deformation in spherical harmonics:

\[
\eta(\theta,\phi,t)=\sum_{\ell=0}^{\infty}\sum_{m=-\ell}^{\ell}a_{\ell m}(t)Y_{\ell m}(\theta,\phi).
\]

- \(\ell=0\): breathing/compression mode,
- \(\ell=1\): translation of the center,
- \(\ell\ge2\): genuine shape deformation.

Rotation, anisotropic coupling, collisions, or internal knot tension may excite \(\ell\ge2\), but deformation must be derived rather than assumed from a flat sketch.

## 2D Rule

A 2D diagram may represent:

\[
\Omega_{2D}=\Omega_{3D}\cap P
\]

for a cross-section plane \(P\), or a projection

\[
\Pi:\Omega_{3D}\rightarrow\Omega_{2D}.
\]

Neither operation proves the full physical structure is flat.

The exception is an explicit 2D negative-space model under E-517. Such a model must state whether it is a literal layer, an interaction surface, or only a calculation space.

## Falsification / Failure

This default fails as a universal rule if a stable isolated One-Wave mode is derived with lower energy in a non-spherical topology under isotropic tension and fixed volume, or if the physical theory requires fundamental flat objects without an explicit 2D layer.

## Coordination Boundary

A-116 defines the volumetric/spherical default. D-409 separately defines the current 12:1 close-packed local coordination candidate. A sphere-like boundary does not by itself select FCC, HCP, or any other interior stacking.

## Status Statement

The minimum-surface argument is Yellow mathematics. Applying it to every proton, electron shell, star, and galaxy requires node-specific dynamics and remains Green until those structures are derived.
