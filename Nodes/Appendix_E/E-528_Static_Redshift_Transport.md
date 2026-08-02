---
node_id: "E-528"
canonical_name: "Static Redshift Transport"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Field Propagation / Redshift Replacement"
claim_gate_detail: "YELLOW (transport equation) / GREEN (tired-light identification)"
metadata_standard: "I-06"
---

# Node E-528: Static Redshift Transport

**Dependencies**
Upstream: A-104 Gradient, A-115 Unified Compression Field, E-509 Propagation Limit, C-311 Electric-Magnetic Duality
Downstream: Book 1 Ch7 Photon, Book 1 Ch9 No Observer Effect, Book 5 cosmic transport, E-529, E-530

## Hard Constraint

One-Wave contains no expansion of space. This node must not use a cosmological scale factor, Hubble expansion term, or wavelength stretching by metric expansion.

## Propagation Law

Let \(\ell\) be path length through a static field background and let \(E_\gamma=h\nu\) be the Propagating Light Mode energy. Use

\[
\frac{dE_\gamma}{d\ell}=-\kappa_\gamma(\mathbf x,\nu,\chi,\nabla\chi)E_\gamma.
\]

Then

\[
E_{\rm obs}=E_{\rm em}\exp\left[-\int_0^D\kappa_\gamma(\ell)d\ell\right],
\]

and

\[
1+z=\frac{E_{\rm em}}{E_{\rm obs}}
=\exp\left[\int_0^D\kappa_\gamma(\ell)d\ell\right].
\]

For constant \(\kappa_\gamma\),

\[
z=e^{\kappa_\gamma D}-1\approx\kappa_\gamma D
\]

when \(\kappa_\gamma D\ll1\).

For a pure redshifting channel rather than absorption, the mode count is conserved along the ray:

\[
\frac{dN_\gamma}{d\ell}=0.
\]

Because \(E_\gamma=h\nu\),

\[
\frac{d\nu}{d\ell}=-\kappa_\gamma\nu.
\]

The model therefore changes the oscillation frequency of each surviving Propagating Light Mode while transferring the missing energy into the field.

## Compression Dependence Candidate

A first non-negative coefficient form is

\[
\kappa_\gamma
=
\kappa_0
+
\kappa_\chi\chi^2
+
\kappa_g|\nabla\chi|^2.
\]

This avoids making the sign of compression alone produce negative attenuation. The form is a candidate, not a derivation.

## Energy Accounting

For light energy density \(u_\gamma\) propagating at local speed \(c_L\),

\[
Q_{\gamma\to\chi}=c_L\kappa_\gamma u_\gamma.
\]

The field receives exactly what the light loses:

\[
\partial_tu_\gamma+\nabla\cdot\mathbf J_\gamma=-Q_{\gamma\to\chi},
\]

\[
\partial_tu_\chi+\nabla\cdot\mathbf J_\chi=+Q_{\gamma\to\chi}+\cdots.
\]

## Failure Tests

The model must not merely fit a distance-redshift curve. It must also address:

- frequency dependence or independence,
- angular-image blurring,
- spectral-line broadening,
- energy conservation,
- redshift-correlated transient-duration behavior without metric time stretching,
- gravitational/compression dependence,
- consistency with the same coefficient across different paths.

If the required interaction scatters light enough to destroy observed image sharpness, or if the lost energy has no field destination, this candidate fails.
