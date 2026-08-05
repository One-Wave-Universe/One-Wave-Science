---
node_id: "C-318"
canonical_name: "Four-Interaction Mass-Effect Response"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Mass-Effect Derivation / Imported-Assumption Resolution"
claim_gate_detail: "GREEN (One-Wave mechanism identity) / YELLOW (profiles, response coefficients, and numerical spectrum)"
metadata_standard: "I-06"
---

# Node C-318: Four-Interaction Mass-Effect Response

**Dependencies**  
Upstream: A-109 Inertial Memory, A-112 Persistent Mode, A-115 Unified Compression Field, C-301 Mirror Gate, C-311 Electric-Magnetic Duality, C-317 Boundary-Tension Weave  
Downstream: Book 1 Ch1, Book 1 Ch2, Book 1 Ch14, Book 1 Ch15, C-322, future four-interaction lattice simulation

## Purpose

C-318 defines Mass Effect from One-Wave primitives without importing a scalar potential, Higgs curvature, a conventional particle mass gap, or any speed-ceiling-to-mass shortcut.

A previous draft incorrectly treated propagation status as a source of inertia. That inference was introduced by misunderstanding C-309, not by deriving it from One-Wave primitives. It is false, permanently erased, and prohibited from re-entry under alternate wording.

The former replacement scaffold

```text
V(phi) -> V''(v) -> Omega_0 -> mass gap -> Mass Effect
```

is also removed from canonical One-Wave derivation. It was useful Gray mathematics for showing what a conventional gapped branch looks like, but it did not derive Mass Effect from the architecture already accepted by the repository.

## Canonical Four-Interaction Architecture

A bounded material mode is one recurrent 3D field structure maintained by four interacting parts:

1. **Knot interaction** — internal Three-Vortex geometry, recursive motion, phase relation, and structural resistance.
2. **Electrical-shell interaction** — the pressure/stress shell created by boundary resistance and roll-off.
3. **Mirror-Gate interaction** — the restoring pressure and orientation resistance associated with compression/expression reversal.
4. **Boundary-Tension Weave interaction** — the surface-and-volume confinement that holds and reweaves the bounded knot.

These are four interactions of one field configuration, not four independent forces and not four unrelated energies that may be fitted separately.

Represent the complete bounded state by

\[
\mathbf Z
=
\bigl(
\mathbf Z_K,
\mathbf Z_E,
\mathbf Z_M,
\mathbf Z_T
\bigr),
\]

where the subscripts denote knot, electrical shell, Mirror Gate, and Boundary-Tension Weave structure.

Use the cycle-averaged four-interaction energy

\[
\overline E_4[\mathbf Z]
=
\left\langle
E_K+E_E+E_M+E_T+E_\times
\right\rangle_{\rm cycle}.
\]

The cross-interaction term \(E_\times\) is load-bearing. It contains knot-shell, knot-weave, shell-Mirror, Mirror-weave, and other allowed couplings. Omitting it would quietly turn the four interactions into four isolated mechanisms, which is not the model.

## Hold and Stable Recurrence

Let \(\mathbf q\) collect the allowed internal deformation coordinates of the bounded mode. The stable hold state \(\mathbf q_0\) must satisfy

\[
\nabla_{\mathbf q}\overline E_4(\mathbf q_0)=0,
\]

and

\[
\mathbf H_0
=
\nabla_{\mathbf q}^{2}\overline E_4(\mathbf q_0)
\succ0
\]

on every deformation direction that is not a permitted translation, rotation, or phase shift.

This local condition must be combined with A-112 recurrence:

\[
\|\mathbf Z_{n+k}-\mathbf Z_n\|<\epsilon.
\]

A one-time energy minimum is not enough. The structure must repeatedly rebuild the same coupled relation.

## Mass Effect as Carried-Pattern Resistance

Let \(\mathbf X(t)\) be the center of the complete bounded recurrence. Moving the mode relative to Ground requires the knot, shell, Mirror relation, and weave to be carried and rebuilt together.

For any carried component \(\mathbf Z_a(\mathbf x-\mathbf X(t),t)\), the co-moving update is

\[
D_t\mathbf Z_a
=
\partial_t\mathbf Z_a
-
\dot{\mathbf X}\cdot\nabla\mathbf Z_a.
\]

Let \(\mathbf v=\dot{\mathbf X}\). Expand the cycle-averaged energy of the translated recurrence near rest:

\[
\overline E_4(\mathbf v)
=
\overline E_4(\mathbf 0)
+
\frac12 v_i\,\mathcal M_{ij}\,v_j
+O(|\mathbf v|^3).
\]

The **Mass-Effect tensor** is

\[
\boxed{
\mathcal M_{ij}
=
\left.
\frac{\partial^2\overline E_4}
{\partial v_i\partial v_j}
\right|_{\mathbf v=0}
}
\]

and the measured reaction is

\[
F_i^{\rm applied}
=
\frac{d}{dt}
\left(
\frac{\partial\overline E_4}{\partial v_i}
\right)
\approx
\mathcal M_{ij}a_j
\]

for slow acceleration around the stable branch.

If A-109/C-309 damping is active, the general low-speed reaction is

\[
F_i^{\rm applied}
=
\mathcal M_{ij}a_j
+
\mathcal C_{ij}v_j
+\cdots.
\]

The \(\mathcal C_{ij}v_j\) term is drag/attenuation, not Mass Effect. It must be measured and derived separately. Absorbing velocity drag into \(\mathcal M\) would confuse inertia with friction and would also trigger the C-313 preferred-frame conflict. The Mass-Effect tensor is the acceleration coefficient after the dissipative contribution is separated.

For an isotropic lowest mode,

\[
\boxed{
m_{\rm eff}
=
\frac13\operatorname{Tr}\mathcal M
}
\]

is the scalar Mass Effect.

This is the mechanism statement:

> Mass Effect is the resistance produced when the complete four-interaction recurrence must be displaced, carried, and rebuilt relative to Ground.

It is not a substance stored inside the mode and it is not created by inserting \(E=mc^2\).

## Discrete Bridge to the Core Update Rule

The velocity derivative above is not meant to float above the lattice as decorative calculus. It can be reduced to a one-step carried-pattern calculation.

At lattice cell \(i\) and update \(n\), collect the four coupled state components into

\[
\mathbf Z_i^n
=
(\mathbf Z_{K,i}^n,\mathbf Z_{E,i}^n,\mathbf Z_{M,i}^n,\mathbf Z_{T,i}^n).
\]

A one-step center displacement \(\delta\mathbf X=\mathbf v\Delta t\) changes a stable profile by

\[
\delta_v\mathbf Z_i
=
\mathbf Z_0(\mathbf x_i-\mathbf X-\delta\mathbf X)
-
\mathbf Z_0(\mathbf x_i-\mathbf X)
=
-\Delta t\,v_jD_j\mathbf Z_{0,i}
+O(|\mathbf v|^2),
\]

where \(D_j\) is the actual lattice difference operator, not an assumed continuum derivative.

A-109 supplies state carry-forward, but it does not yet assign joules to that carried difference. The missing bridge is one positive-semidefinite **four-interaction work metric** \(\mathsf W_i\), derived from the memory, pressure, resistance, and boundary update rules:

\[
\Delta E_{\rm carry}
=
\frac{1}{2\Delta t^2}
\sum_i\Delta V\,
(\delta_v\mathbf Z_i)^{\mathsf T}
\mathsf W_i
(\delta_v\mathbf Z_i).
\]

Substitution gives the lattice Mass-Effect tensor directly:

\[
\boxed{
\mathcal M_{jk}
=
\sum_i\Delta V\,
(D_j\mathbf Z_{0,i})^{\mathsf T}
\mathsf W_i
(D_k\mathbf Z_{0,i})
}
\]

or, after a justified continuum limit,

\[
\mathcal M_{jk}
=
\left\langle
\int
(\partial_j\mathbf Z)^{\mathsf T}
\mathsf W(\mathbf Z)
(\partial_k\mathbf Z)
\,dV
\right\rangle_{\rm cycle}.
\]

The block structure of \(\mathsf W\) is load-bearing:

\[
\mathsf W=
\begin{pmatrix}
W_{KK}&W_{KE}&W_{KM}&W_{KT}\\
W_{EK}&W_{EE}&W_{EM}&W_{ET}\\
W_{MK}&W_{ME}&W_{MM}&W_{MT}\\
W_{TK}&W_{TE}&W_{TM}&W_{TT}
\end{pmatrix}.
\]

The diagonal blocks measure the carried response of each interaction. The off-diagonal blocks measure the extra work forced by their coupling. Setting the off-diagonal blocks to zero would quietly turn one bounded architecture into four unrelated mechanisms.

This exposes the exact open step instead of hiding it: the core update currently predicts dimensionless state evolution, but the repository has not yet derived \(\mathsf W\) or its absolute energy scale. Until that bridge exists, the update rule cannot output kilograms or GeV.

Dimensional check:

\[
[\mathcal M_{ij}]
=
\frac{[E]}{[v]^2}
={\rm kg}.
\]

## Separation from the 125 GeV Mirror Gate

Mass Effect and the Mirror-Gate threshold are generated by the same \(\overline E_4\), but they are not the same derivative.

Mass Effect measures local resistance to translation inside the stable basin:

\[
\mathcal M_{ij}
=
\partial_{v_i}\partial_{v_j}\overline E_4\big|_{0}.
\]

The Mirror Gate measures finite work along a boundary-changing path from the hold state to the first orientation-flip threshold:

\[
E_{\rm Gate}
=
\overline E_4(\mathbf q_G)
-
\overline E_4(\mathbf q_0).
\]

Therefore

\[
\boxed{
m_{\rm eff}\neq E_{\rm Gate}/c^2
}
\]

as a mechanism statement. A later numerical conversion may compare energy and measured inertia, but it may not replace either derivation.

## Executable Derivation Path

A valid numerical test must:

1. construct one stable 3D recurrent profile \(\mathbf Z_0\);
2. keep all four interactions and their cross-couplings active;
3. translate the profile at several small velocities without changing coefficients;
4. measure \(\overline E_4(\mathbf v)-\overline E_4(0)\);
5. extract \(\mathcal M_{ij}\) from the quadratic response;
6. accelerate the profile and independently verify \(\mathbf F\approx\mathcal M\mathbf a\);
7. compare the resulting Mass Effect only after the model is fixed.

## Absolute-Energy Identifiability Result

The repository does not yet contain a microscopic energy normalization. Write

\[
E_{\rm physical}
=
\varepsilon_{\rm lat}\,\mathcal E_{\rm dimensionless}.
\]

The missing scale is not merely an inconvenient coefficient. The current normalized update has a global energy-scale freedom:

\[
\mathsf W_i\rightarrow\lambda\mathsf W_i
\]

implies

\[
\mathcal M_{ij}\rightarrow\lambda\mathcal M_{ij},
\qquad
E_{\rm MG}\rightarrow\lambda E_{\rm MG},
\]

while the dimensionless state trajectory, recurrence geometry, and gate location are unchanged. Therefore the present update rule cannot identify an absolute value in kilograms or GeV. That is a mathematical no-go result for the current parameterization, not a failure of persistence.

What the simulation **can** predict before absolute calibration is a scale-free relation. Let

\[
v_{\rm lat}=\frac{\Delta x}{\Delta t},
\qquad
\widetilde m
=
\frac{m_{\rm eff}v_{\rm lat}^2}{\varepsilon_{\rm lat}},
\qquad
\Delta\mathcal E_G
=
\frac{E_{\rm MG}}{\varepsilon_{\rm lat}}.
\]

Then

\[
\boxed{
\mathcal R_G
=
\frac{E_{\rm MG}}{m_{\rm eff}v_{\rm lat}^2}
=
\frac{\Delta\mathcal E_G}{\widetilde m}
}
\]

is independent of the unknown global energy scale, provided both quantities come from the same fixed four-interaction model. If a later derivation identifies \(v_{\rm lat}\) with measured \(c\), then \(E_{\rm MG}/(m_{\rm eff}c^2)\) may be used as a comparison ratio. It is still not the causal mass mechanism.

Two honest numerical routes remain:

1. **Prediction route:** fix \(\varepsilon_{\rm lat}\) from one independent microscopic observable, then predict the gate energy before comparing it with 125 GeV.
2. **Calibration route:** use 125 GeV to fix \(\varepsilon_{\rm lat}\), then make no claim to have predicted 125 GeV; instead predict masses, other thresholds, and release-channel relations without refitting.

This is the present quantitative boundary. It is specific and executable.

## Yellow Audit

Resolved:

- the false speed-ceiling shortcut is permanently removed;
- scalar-potential curvature is removed from canonical mass derivation;
- Mass Effect is defined as the four-interaction carried-pattern response;
- internal knot, electrical shell, Mirror Gate, Boundary-Tension Weave, and cross-couplings are all load-bearing;
- Mass Effect and the 125 GeV gate are separated as two derivatives of one architecture;
- dimensions close;
- inertial response is separated from velocity drag.

Open:

- derive the stable 3D profiles \(\mathbf Z_a\);
- derive the work metric \(\mathsf W\) from the discrete update rule;
- choose and document either the independent-calibration route or the 125-GeV calibration route;
- compute a Mass-Effect spectrum without per-object fitting;
- prove that a gapless traveling light mode remains available while bounded recurrent modes have nonzero carried-pattern response;
- derive the damping tensor separately and satisfy the C-313 frame test.

## Direct Failure Conditions

The mechanism fails if:

- any of the four interactions can be removed without changing the derived Mass Effect;
- cross-couplings are replaced by unrelated fitted constants;
- every measured mass is used to retune \(\mathsf W\);
- translation changes only a label and does not require field reconstruction;
- or one fixed rule cannot produce both stable recurrence and the measured inertial response.
