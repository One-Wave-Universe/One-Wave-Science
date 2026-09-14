---
node_id: "C-320"
canonical_name: "Magnetic-Compression Path Coupling"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Field Mechanics / Magnetism-Gravity Bridge"
claim_gate_detail: "GREEN (canonical coupling contract and recovery limits) / BROWN (physical coefficients and observational fit uncalibrated)"
metadata_standard: "I-06"
---

# Node C-320: Magnetic-Compression Path Coupling

**Dependencies**  
Upstream: A-104 Gradient, A-105 Restoring Response, A-115 Unified Compression Field, C-306 Torque, C-307 Angular Momentum, C-319 Magnetic Lattice Reorganization, D-409 Twelvefold 3D Close-Packed Coordination  
Lateral: C-311 Electric-Magnetic Duality, D-401 Flux, E-503 Pressure (Gradient Form), E-505 Coupling  
Downstream: D-413 Ground Lattice Orbital-Restoring Simulation, D-416 Planetary Rotation-Magnetic Coupling Test Matrix, Book 1 Ch12 Gravity, Book 1 Ch13 Electricity/Magnetism

## Purpose

This node is the canonical One-Wave connection between magnetism and gravity/compression. It exists so the relationship cannot be lost inside prose or silently replaced by the statement that magnetism and gravity are the same force.

The locked mechanism hypothesis is:

```text
magnetic rotational state
-> reorganizes lattice pathways (C-319)
-> changes directional accessibility of an existing compression/restoring field
-> changes how the A-115 restoring bias is expressed through the lattice
```

Magnetism is therefore proposed as a **lattice reorganizer**. Gravity remains the compression-gradient/restoring response of A-115.

## 1. Gravity Is Not Modeled as Water Flow

The intended physical picture is closer to **sand moving through a sieve** than water flowing through an empty pipe.

That analogy is limited and operational:

- the lattice provides discrete routes and restrictions;
- displacement/compression changes the loading on those routes;
- the restoring response is biased by which routes are locally accessible;
- changing route organization can redirect or redistribute the response;
- no literal grains, sieve, water, drag fluid, or hidden mechanical ether are asserted.

The useful mathematical idea is **path accessibility**, not ordinary hydrodynamic flow.

## 2. Baseline A-115 Gravity View

A-115 defines scalar compression

\[
\chi=-\nabla\cdot\mathbf u
\]

and the baseline gravity/compression-gradient view

\[
\mathbf g_0=-\alpha_g\nabla\chi.
\]

C-320 does not replace this source law.

## 3. Path-Weighted Restoring Response

C-319 supplies a lattice accessibility tensor

\[
\mathbf K_L=\mathbf I+\kappa_R\mathbf R.
\]

The minimal coupling candidate is

\[
\boxed{
\mathbf g_{\rm OW}
=-\alpha_g\,\mathbf K_L\nabla\chi
}
\]

or, component-wise,

\[
g_i=-\alpha_g K_{L,ij}\partial_j\chi.
\]

This is the precise meaning of the proposed connection:

> magnetism does not become gravity; magnetic reorganization changes the lattice through which the compression/restoring bias is expressed.

The mandatory recovery limit is

\[
\mathbf R\to0
\Rightarrow
\mathbf K_L\to\mathbf I
\Rightarrow
\mathbf g_{\rm OW}\to-\alpha_g\nabla\chi.
\]

If that recovery fails, C-320 is incompatible with A-115.

## 4. Compression Versus Accessibility

These variables must remain separate:

- `chi`: how compressed/displaced the field is;
- `grad(chi)`: the baseline restoring bias;
- `R`: magnetic/rotational lattice reorganization state;
- `K_L`: directional accessibility created from `R`;
- `g_OW`: resulting path-weighted restoring response.

A magnetic field with no compression gradient must not generate an A-115 gravity field through this equation alone:

\[
\nabla\chi=0
\Rightarrow
\mathbf g_{\rm OW}=0.
\]

That hard stop prevents the repo from drifting into "magnetism automatically equals gravity."

## 5. Torque and Rotational Coupling

For an extended bounded structure with local effective load density `rho_eff`, an off-center path-weighted restoring field can generate torque through the ordinary C-306 structure:

\[
\boldsymbol\tau
=\int_V
\mathbf r\times
\left(\rho_{\rm eff}\mathbf g_{\rm OW}\right)
\,dV.
\]

C-307 then owns the angular response.

This gives a testable chain for orbital/rotational locking proposals:

```text
compression gradient
+ magnetic lattice organization
-> anisotropic restoring response
-> distributed off-center response
-> torque
-> rotational/orbital evolution
```

It does not guarantee locking. Locking must emerge dynamically and survive controls.

## 6. D-413 Gravity-Lab Handoff

D-413 is the first runnable reduced laboratory for this coupling.

Current D-413 uses an imposed gravity-like well. The required integration order is:

1. replace the imposed well with an A-115 source-derived `chi` field;
2. reproduce the baseline `K_L = I` gravity controls;
3. add C-319 `R` and `K_L` as a separately switchable magnetic-reorganization channel;
4. compare trajectories, restoring vectors, torque, capture, orbit, and drift with the magnetic channel ON versus OFF;
5. reject the coupling if the effect is only renderer-level, parameter hand-tuning, or an energy-accounting artifact.

## 7. Planetary Boundary

Planetary spin/orbit/magnetic observations are a falsification set, not evidence by resemblance. D-416 owns that comparison.

A single rule must confront, at minimum:

- the Moon's synchronous rotation despite no present global magnetic field;
- Mercury's 3:2 spin-orbit resonance and weak intrinsic field;
- Venus's very slow retrograde rotation and induced rather than intrinsic global field;
- Uranus's strongly tilted and offset magnetic field;
- Neptune's strongly tilted and offset magnetic field.

A theory that can explain only the convenient members of this set is not a planetary coupling law.

## Direct Failure Conditions

C-320 fails in its present form if:

1. the unmagnetized limit does not recover A-115;
2. a gravity-like response appears when `grad(chi)=0` solely because `B` is nonzero;
3. the same fixed coupling law cannot be used across control systems without body-by-body arbitrary switches;
4. the coupling violates work/energy accounting in a closed numerical test;
5. the proposed magnetic term merely refits an imposed trajectory instead of predicting a measurable change;
6. standard tidal/gravitational controls already explain a case and the magnetic term has no independently measurable residual to predict.

## Status

C-320 permanently gives the magnetism-gravity connection one canonical location:

```text
C-311 magnetic rotation
-> C-319 lattice reorganization
-> C-320 path-weighted A-115 compression/restoring response
-> D-413 laboratory
-> D-416 planetary falsification
```

The connection is canonical inside the One-Wave framework, while its physical validity remains an open experimental question.
