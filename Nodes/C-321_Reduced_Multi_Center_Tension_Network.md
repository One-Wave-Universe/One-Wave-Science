---
node_id: "C-321"
canonical_name: "Reduced Multi-Center Tension Network"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Boundary-Tension Reduction / Junction Geometry"
claim_gate_detail: "YELLOW (N=3 reduced geometry) / GREEN (N>3 and nuclear application)"
metadata_standard: "I-06"
---

# Node C-321: Reduced Multi-Center Tension Network

**Dependencies**  
Upstream: C-317 Boundary-Tension Weave, A-112 Persistent Mode, A-116 Three-Dimensional Spherical Default, A-117 Dimensional Integrity, D-409 Twelvefold 3D Close-Packed Coordination  
Downstream: future separated-center simulations; possible nuclear bridge only after an inter-nucleon coupling law is derived

## Scope Correction

C-317 now describes an intact Three-Vortex Knot as a continuous 3D Boundary-Tension Weave. C-321 does not replace that spherical/volumetric geometry with literal strings.

C-321 applies only in a **reduced neck regime** where several spatially separated centers are connected by slender high-tension regions. The connection to C-317 survives if

\[
\frac{a_i}{L_i}\ll1,
\]

where \(a_i\) is neck radius and \(L_i\) is segment length, and if junction-core energy is small compared with the line contribution.

For an intact proton-sized knot, the continuous 3D weave remains primary.

## Reduced Energy

C-317 supplies the line-tension limit

\[
E_i\approx\tau_iL_i.
\]

For a junction at \(\mathbf J\) connected to centers \(\mathbf q_i\), use

\[
E(\mathbf J)
=
\sum_{i=1}^{N}\tau_i|\mathbf J-\mathbf q_i|+E_J,
\]

where \(E_J\) is the unresolved finite junction-core energy.

The stationarity condition is

\[
\nabla_{\mathbf J}E
=
\sum_i\tau_i\widehat{\mathbf e}_i
+
\nabla_{\mathbf J}E_J
=0,
\]

with

\[
\widehat{\mathbf e}_i
=
\frac{\mathbf J-\mathbf q_i}{|\mathbf J-\mathbf q_i|}.
\]

If \(E_J\) is locally position-independent, force balance reduces to

\[
\sum_i\tau_i\widehat{\mathbf e}_i=0.
\]

## Three Equal Tensions

For \(N=3\) and \(\tau_1=\tau_2=\tau_3=\tau_T\), force balance yields

\[
\widehat{\mathbf e}_1+
\widehat{\mathbf e}_2+
\widehat{\mathbf e}_3=0.
\]

Squaring the vector relation gives

\[
\widehat{\mathbf e}_i\cdot\widehat{\mathbf e}_j=-\frac12,
\]

so the three necks meet at \(120^\circ\). This is the Fermat/Torricelli geometry when all triangle angles permit an interior junction.

For unequal tensions,

\[
\cos\theta_{ij}
=
\frac{\tau_k^2-\tau_i^2-\tau_j^2}{2\tau_i\tau_j}.
\]

Thus the junction angles are predictions of derived tensions, not always 120 degrees.

## Delta Versus Y Reduction

For three separated centers,

\[
E_\Delta
=
\tau_T(r_{12}+r_{23}+r_{31}),
\]

while

\[
E_Y
=
\tau_T\min_{\mathbf J}
\left(
|\mathbf J-\mathbf q_1|
+|\mathbf J-\mathbf q_2|
+|\mathbf J-\mathbf q_3|
\right)+E_J.
\]

The previous numerical example remains a valid geometry check for the length minimization, but it does not calibrate \(\tau_T\), derive \(E_J\), or prove literal tube geometry inside an intact knot.

## Nuclear-Scale Warning

C-317 describes confinement among Vortex Phases inside a proton-like knot. That does not automatically provide the force between separate protons and neutrons.

Therefore C-321 must not be used as a carbon-12 binding law until a distinct bridge derives how intact nucleon knots couple to one another. An N=12 Steiner tree of nucleon centers would otherwise be a geometrical exercise attached to the wrong physical interaction.

## Yellow Audit

- derive the neck-regime reduction from the full C-317 field energy;
- derive \(\tau_i\), neck radii, and junction-core energy;
- test when an interior junction is favored over boundary attachment;
- simulate the transition between continuous spherical weave and reduced neck network;
- derive an inter-nucleon coupling law before any nuclear or carbon application;
- treat N>3 topology as open, not as a routine extension of the N=3 result.

## Resolution

The C-317 geometry change does **not** break C-321. It narrows it:

```text
continuous 3D weave -> slender-neck limit -> reduced line-tension network
```

The N=3 Fermat result survives inside that limit. The former claim that it already extends directly to multi-nucleon nuclear binding does not.
