---
node_id: "G-768"
canonical_name: "Anisotropic Signed-Axis Spectrum and Rotating-Axis Scale Test"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Analytic lattice result / mode selection / renormalization boundary"
claim_gate_detail: "YELLOW — static signed-axis spectrum is derived; isotropic 2x recursion is not proven and requires the composed three-orientation coarse-graining map"
metadata_standard: "I-06"
---

# G-768 — Anisotropic Signed-Axis Spectrum and Rotating-Axis Scale Test

## Purpose

Correct the octave/scale bridge without analogy. This node separates what the triangular-lattice operator actually proves from what remains a physical/RG hypothesis.

## 1. Bond geometry and anisotropic operator

Let
[
\delta_a=a(1,0),\quad
\delta_b=a(1/2,\sqrt3/2),\quad
\delta_c=\delta_b-\delta_a=a(-1/2,\sqrt3/2).
]

For the signed-axis test use
[
J_a=+J,\quad J_b=+J,\quad J_c=-J,\qquad J>0,
]
and
[
\mathcal D\psi_i=\sum_{\nu=a,b,c}J_\nu
(\psi_{i+\nu}+\psi_{i-\nu}-2\psi_i).
]

For a plane wave, with (u=k_xa/2) and (v=\sqrt3k_ya/2),
[
\Lambda_J(u,v)=2J[\cos(2u)-2\sin u\sin v-1].
]

This is the operator to use for this signed-axis hypothesis; the isotropic triangular Laplacian must not be used and then corrected verbally afterward.

## 2. Critical spectrum result

The stationary-point calculation gives:
- uniform background: (\Lambda_J(\Gamma)=0);
- global maximum: (\Lambda_{\max}=+J) at the corresponding interior stationary points;
- M-type extreme: (\Lambda_J=-8J) at (u=v=\pi/2) and symmetry-related points.

For
[
\mathbf k_M=(\pi/a,\pi/(\sqrt3a)),
]
the bond phases are
[
\mathbf k_M\cdot\delta_a=\pi,\quad
\mathbf k_M\cdot\delta_b=\pi,\quad
\mathbf k_M\cdot\delta_c=0.
]

Thus the M pattern is anti-phase along (a,b) and in-phase along (c).

In lattice coordinates (\mathbf r_{nm}=n\mathbf a_1+m\mathbf a_2),
[
\psi_{nm}=A(-1)^{n+m}.
]

This is a stripe state, not an isotropically doubled triangular lattice.

## 3. Selection boundary

Do not call the (-8J) state the exchange-energy ground state merely from the Laplacian sign convention. With conventional
[
E=-\sum_{\langle ij\rangle}J_{ij}\psi_i\psi_j,
]
positive (J) favors equal signs and negative (J) favors opposite signs.

The architecture's candidate selection rule is instead gradient/shear-triggered hysteretic switching. That is a physical hypothesis requiring a coercive-threshold model or measurement.

For equal-amplitude neighboring phases,
[
|\Delta\psi|=2|\psi_0||\sin(\theta/2)|.
]
Hence a 120-degree K relation gives (\sqrt3|\psi_0|), while exact anti-phase gives (2|\psi_0|). A threshold-only discrimination window would therefore require a condition such as
[
\sqrt3|\psi_0|<H_c<2|\psi_0|,
]
subject to the actual transfluxor coupling law and units.

## 4. Static signed-axis result

A fixed signed axis does **not** prove
[
\mathbf a_i' = 2\mathbf a_i.
]

It produces directional ordering:
- period (2a) along the two alternating primitive directions;
- in-phase stripes along the remaining direction;
- transverse stripe spacing/period must be treated geometrically rather than relabeled as isotropic octave scaling.

Therefore:

**DISPROVED:** one static (J_c=-J) assignment implies isotropic 2x scale recursion.

**ESTABLISHED FOR THE MODEL:** the M-type stripe candidate has (\psi_{nm}=A(-1)^{n+m}) and a period-two sign modulation along the alternating lattice directions.

## 5. Rotating signed-axis candidate

Let (D_1) be the spatial tensor/operator for one signed-axis orientation and
[
D_2=R_{120}D_1R_{120}^{-1},\qquad
D_3=R_{240}D_1R_{240}^{-1}.
]

The symmetry average
[
\bar D=(D_1+D_2+D_3)/3
]
commutes with the 120-degree rotation. For a real symmetric rank-2 tensor in 2D this constrains
[
\bar D=dI.
]

This establishes restoration of isotropy at the averaged tensor level if the three orientations are sampled symmetrically. It does **not** establish (d=2).

## 6. Decisive RG test

Define the actual coarse-graining maps for the three orientations:
[
\mathcal R_1,\quad\mathcal R_2,\quad\mathcal R_3.
]

Calculate, without inserting 2 as an assumption,
[
\mathcal R_{cycle}=\mathcal R_3\mathcal R_2\mathcal R_1.
]

Interpretation:
- (\mathcal R_{cycle}=2I): isotropic octave scaling derived for this model;
- (\mathcal R_{cycle}=sI, s\neq2): isotropic recursion exists but its natural scale factor is (s);
- (\mathcal R_{cycle}\neq sI): the full three-axis cycle does not produce self-similar isotropic recursion.

The measured/calculated result wins; octave scaling must not be forced.

## 7. Relation to Rabbit Hop and Z12

The internal 12-state grammar and spatial dilation remain separate mathematical structures. No power-of-two modular-closure argument is permitted as evidence for spatial scale doubling.

Likewise, the Pythagorean comma is not derived from (2^n\bmod12). Musical ratio analogies may motivate questions but cannot establish lattice frustration or RG closure.

## Status

**Established:** anisotropic operator; its stated extrema; M stripe phase relation; static signed-axis failure to produce isotropic 2x scaling; rotational averaging restores isotropy at tensor level under symmetric cycling.

**Proposed / requires derivation or measurement:** hysteretic selection of M over competing modes; physical realization of the signed-bond model; the three coarse-graining maps; (\mathcal R_3\mathcal R_2\mathcal R_1=2I).

## Next smallest proof step

Construct (\mathcal R_1,\mathcal R_2,\mathcal R_3) from an explicitly declared block/decimation rule and calculate their composition. Do not assume the answer is 2.
