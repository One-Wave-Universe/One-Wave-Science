# Candidate 01 — Restore + Inertia -> Wave Equation

**Target:** L2 MATH + L3 RECOVERY  
**Source:** `Nodes/A-110a_Wave_Equation_Derivation.md`

## Why this is first

This is the cleanest existing derivation in the repository. It starts from a local restoring relation plus inertia and recovers the standard one-dimensional wave equation.

It is useful as the first proof-chain because it tests whether One-Wave can move from its own definitions to a standard physical equation without fitting the answer afterward.

## Sign convention that must be fixed

The current A-110a text writes

[
R=-alpha,partial_xpsi
]

then

[
partial_xR=-alpha,partial_x^2psi
]

but immediately uses

[
mu,partial_t^2psi=+alpha,partial_x^2psi.
]

That final equation is correct for a stable wave equation only if the force density is defined as the **negative divergence of the restoring quantity**:

[
f=-partial_xR
  =alpha,partial_x^2psi.
]

Equivalently, define a tension/stress variable

[
sigma=alpha,partial_xpsi
]

and use

[
f=partial_xsigma.
]

The convention must be stated explicitly.

## Derivation

Let (psi(x,t)) be the displacement/state field.

Assume a linear local restoring stress

[
sigma=alpha,partial_xpsi,
]

where (alpha>0) has the appropriate stiffness units.

The net force per unit length is the spatial divergence

[
f=partial_xsigma
 =alpha,partial_x^2psi.
]

Let (mu>0) be inertia per unit length. Newton-shaped local balance gives

[
mu,partial_t^2psi
=
alpha,partial_x^2psi.
]

Therefore

[
partial_t^2psi
=
v^2partial_x^2psi,
qquad
v^2=rac{alpha}{mu}.
]

This is the standard 1D wave equation.

For a harmonic trial state

[
psi=Ae^{i(kx-omega t)},
]

substitution gives

[
-omega^2=-v^2k^2,
]

hence

[
omega^2=v^2k^2,
qquad
omega=pm vk.
]

The right- and left-traveling branches are therefore recovered.

## L3 recovery statement

The derivation recovers the ordinary nondispersive 1D wave equation and its linear dispersion relation from the declared restore + inertia assumptions.

That recovery is a mathematical compatibility result. It does **not** establish that every physical field is a One-Wave lattice mode.

## What would make this stronger

1. repair the sign convention in A-110a;
2. derive the continuum equation from the discrete A-114 update by controlled long-wavelength expansion rather than only matching the small-k result;
3. show the exact parameter map between (eta,gamma,c_L) and continuum (alpha,mu);
4. identify the assumptions under which damping vanishes or survives.

## Status

**L2:** essentially PASS after sign convention repair.  
**L3:** PASS for recovery of the standard 1D wave equation under the stated linear assumptions.  
**Novel physical claim:** none yet. This is a foundation/calibration result.
