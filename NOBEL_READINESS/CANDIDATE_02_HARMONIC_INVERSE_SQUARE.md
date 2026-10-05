# Candidate 02 — Harmonic Steady State -> 1/r Potential -> 1/r^2 Gradient

**Target:** L2 MATH + L3 RECOVERY  
**Sources:** `Nodes/D-401_Flux.md`, A-109/A-112 update chain

## Why this is second

D-401 already derives a discrete mean-value condition for a persistent steady state:

[
langlepsi_jangle=psi_i.
]

On a regular isotropic lattice, the continuum limit of the discrete mean-value condition is Laplace's equation away from sources:

[

abla^2Phi=0.
]

That gives a direct route to a standard inverse-square field under spherical symmetry.

This is more physically useful than simply postulating a (1/r^2) law.

## Step 1 — repository result

For a persistent state, D-401 substitutes the steady condition into the update law and obtains, for nonzero coupling,

[
langlepsi_jangle-psi_i=0.
]

Equivalently,

[
sum_{jin N(i)}(psi_j-psi_i)=0.
]

That is the discrete graph/lattice Laplacian:

[
Delta_dpsi_i=0.
]

## Step 2 — continuum limit

For an isotropic regular lattice with spacing (a), Taylor expansion of neighboring values gives

[
Delta_dpsi
=
C a^2
abla^2Phi
+
O(a^4),
]

where (C>0) depends on lattice geometry.

Thus, in the long-wavelength limit,

[

abla^2Phi=0
]

everywhere outside a source region.

## Step 3 — spherical symmetry

Assume a static isolated source and spherical symmetry:

[
Phi=Phi(r).
]

Then

[

abla^2Phi
=
rac{1}{r^2}
rac{d}{dr}
left(
r^2rac{dPhi}{dr}
ight)
=0.
]

Multiply by (r^2):

[
rac{d}{dr}
left(
r^2rac{dPhi}{dr}
ight)
=0.
]

Integrate once:

[
r^2rac{dPhi}{dr}=C_1.
]

Therefore

[
rac{dPhi}{dr}=rac{C_1}{r^2}.
]

Integrate again:

[
Phi(r)=C_0-rac{C_1}{r}.
]

So the gradient magnitude is

[
|
ablaPhi|
=
rac{|C_1|}{r^2}.
]

## L3 recovery statement

A source-free harmonic field plus spherical symmetry necessarily gives a (1/r) potential and a (1/r^2) radial gradient.

This recovers the geometric radial dependence used by Newtonian gravity and electrostatics outside a compact spherical source.

The derivation does **not** yet derive:
- the coupling constant (G);
- why mass is the source;
- the sign of gravitational attraction;
- equivalence of inertial and gravitational mass;
- relativistic corrections;
- the finite-range law proposed elsewhere in One-Wave.

Those remain separate claims.

## Important consequence for D-401

D-401 correctly notes that a pure harmonic condition does **not** produce exponential decay.

This derivation shows what it *does* naturally produce in 3D with spherical symmetry: a (1/r) potential and (1/r^2) gradient.

Therefore the repo should not add a screening/mass term unless a distinct physical reason requires finite-range/exponential behavior.

## Strong next test

Derive the discrete-to-continuum coefficient for the actual One-Wave lattice geometry rather than a generic isotropic lattice.

Then ask whether the same source/boundary rule fixes (C_1) from one conserved quantity. If it does, the result advances from geometric recovery toward a genuine One-Wave field law.

## Status

**L2:** strong candidate; the continuum-limit coefficient for the actual lattice still needs explicit derivation.  
**L3:** standard (1/r) potential and (1/r^2) radial-gradient recovery follows cleanly once the harmonic continuum limit and spherical symmetry are declared.  
**Novel physical claim:** not yet. The potential novelty would have to come from the source law, finite-range boundary rule, or a distinct quantitative prediction.
