---
node_id: "C-323"
canonical_name: "Displacement Interaction Regimes of the Unified Compression Field"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Field Identity / Continuum Interaction Stress"
claim_gate_detail: "YELLOW — continuum form written from A-115; lattice runs and quantitative wake profiles still open"
metadata_standard: "I-06"
---

# Node C-323: Displacement Interaction Regimes of the Unified Compression Field

**Former title:** Four Forces as Displacement Regimes  
**Reason for rename:** One-Wave has no forces and no force-carriers. Interaction language only.

**Dependencies**  
Upstream: A-102 Displacement, A-105 Restoring Response, A-106 Pressure Response, A-115 Unified Compression Field, C-311 Electric-Magnetic Duality, C-318 Four-Interaction Mass-Effect Response, C-322 Mirror-Gate 125 GeV Boundary Response, E-532 Bound/Unbound + Finite Wake  
Lateral: D-408 Sixfold Lattice, D-414 Four-Interaction Shell, D-415 Hexagonal Lattice Force Dynamics (bond *responses*)  
Downstream: hexagonal interaction runs, wake profile derivation, residual spectrum

## Purpose

State the continuum interaction stress of **one** displacement field so that the measurement names already locked in A-115 appear as different views of the same object:

```text
gravity          = local directional response of the compression field
dark matter      = extended / wake contribution of that same field
Mass Effect      = resistance to carrying the full four-interaction recurrence
Mirror-Gate      = local boundary stiffness / finite work to cross orientation basin
```

No second substance. No carrier particles. No Standard Model force list imported as architecture.

## Field variables (from A-115)

Displacement of the One-Wave field away from Ground:

\[
\mathbf{u}(\mathbf{x},t)
\]

Scalar compression:

\[
\chi = -\nabla\cdot\mathbf{u}
\]

- \(\chi > 0\): compression  
- \(\chi < 0\): expression / release  
- \(\chi = 0\): no local volumetric displacement

Restoring response (A-105) is the field pushing back on its own displacement. That push-back is the only interaction content.

## Continuum interaction stress

One stress built from the single displacement field:

\[
\boxed{
\sigma_{ij}
=
K\,\chi\,\delta_{ij}
+
2\mu\bigl(\varepsilon_{ij}-\tfrac13\theta\delta_{ij}\bigr)
+
\alpha(\partial_i\chi)(\partial_j\chi)
+
\beta\,C_i C_j
-
\gamma(\nabla^2\chi)\,\delta_{ij}
}
\]

where \(\theta = \nabla\cdot\mathbf{u} = -\chi\), \(\varepsilon_{ij}\) is strain, and \(C_i\) is residual orientation density nonzero **only** where the bound criterion of E-532 holds.

Net restoring response:

\[
\mathbf{R}_i = \partial_j\sigma_{ij}
\qquad\Rightarrow\qquad
\rho\,\ddot{u}_i = R_i
\]

This is A-105 written in continuum stress form. Nothing is added that is not already a geometric limit of \(\mathbf{u}\) and \(\chi\).

## Measurement views of the same field (A-115 identity)

### Local compression-gradient response (gravity view)

Define

\[
\Phi_{\rm OW} = \alpha_g\,\chi,
\qquad
\mathbf{g}_{\rm OW} = -\nabla\Phi_{\rm OW} = -\alpha_g\nabla\chi.
\]

Nearby bound structure responds to this gradient. That response is the gravity view. No carrier. No separate gravity field. The superfluid is displaced; the gradient of that displacement is what is measured as attraction.

### Extended / wake compression (dark-matter view)

Split for bookkeeping only:

\[
\mathbf{g}_{\rm OW} = \mathbf{g}_{\rm local} + \mathbf{g}_{\rm wake}.
\]

\(\mathbf{g}_{\rm wake}\) is retained or extended compression left by motion and rotation of bound structure through the field — the compression ring of Book 1 Ch12 and Book 5 Ch1. A conventional analysis that does not know the field is continuous would invent an extra density

\[
\rho_{\rm DM,eff} = -\frac{1}{4\pi G_{\rm eff}}\nabla\cdot\mathbf{g}_{\rm wake}.
\]

That density is an observational translation, not a second One-Wave substance. Dark-matter behavior is the push-back of the displaced superfluid at extended range.

### Local boundary stiffness (Mirror-Gate / Higgs-scale view)

When the bound recurrence is driven hard enough to approach the first orientation-basin crossing, the finite work required is the Mirror-Gate energy of C-322:

\[
E_{\rm MG}
=
\overline{E}_4(\mathbf{q}_G) - \overline{E}_4(\mathbf{q}_0)
\approx 125\,\mathrm{GeV}
\quad\text{(empirical anchor)}.
\]

This is boundary stiffness of the same compression architecture, not a separate particle excitation. Mass Effect (C-318) is the small-displacement carried-pattern resistance inside the stable basin; Mirror-Gate is the large-deformation work across the basin boundary. Same field, different derivatives.

### Oriented residual response (electrical view)

Bound regions may retain residual orientation \(C_i\). Outside the core, the \(\beta C_i C_j\) term sources an oriented free wake. Longitudinal and transverse projections recover the pressure-field split of C-311:

\[
\mathbf{E}\sim\nabla P_c,
\qquad
\mathbf{B}\sim\nabla\times P_c.
\]

Opposite orientation labels cancel the far wake. No separate electromagnetic substance — oriented residual of the same displacement field.

### Curvature-saturated residual (short-range core view)

When the curvature term \(\gamma\nabla^2\chi\) dominates, the core cannot expand. Balance

\[
K\chi \sim \gamma\nabla^2\chi
\quad\Rightarrow\quad
\text{range}\sim\sqrt{\gamma/K}
\]

gives a short residual. Discrete orientations of \(C_i\) inside the core must cancel for the core to remain bound under E-532; any uncancelled piece is short-range residual interaction of the same field.

### Configuration-changing residual (orientation-flip residual view)

A core may sit in more than one local minimum of curvature-plus-orientation energy. The displacement that rotates the core between minima is an off-diagonal piece of \(\sigma_{ij}\). The intermediate state is only marginally bound; the associated residual is short-lived. This is still the same field changing its own configuration, not a separate interaction species.

## Summary — one field, many measurements

| Measurement name | Geometric content of the same field |
|------------------|-------------------------------------|
| Gravity | local \(\nabla\chi\) response |
| Dark-matter behavior | extended / wake \(\chi\) response |
| Mass Effect | carried four-interaction resistance (C-318) |
| Mirror-Gate (~125 GeV) | finite work across orientation basin (C-322) |
| Electrical response | oriented residual wake (\(C_i\), C-311) |
| Short-range core residual | curvature-saturated \(\chi\) |
| Configuration residual | off-diagonal orientation change |

No row introduces a new substance. Every row is a limit or derivative of \(\mathbf{u}\), \(\chi\), and the bound flag.

## Relation to locked nodes

- **A-115** is the identity claim this node continuum-forms.  
- **C-318** supplies Mass Effect as carried-pattern resistance.  
- **C-322** supplies Mirror-Gate as finite boundary work.  
- **C-311** supplies the oriented pressure projections.  
- **E-532** supplies the bound flag that turns residual orientation on or off.  
- **E-531** governs free propagation of wakes after they leave bound regions; it does not organize mass.  
- **D-414** visualizes interaction channels of a bounded wave; this node states the continuum stress those channels sit inside.

## Required next work

1. Discretize \(\sigma_{ij}\) on D-408 as bond **responses** (D-415 language, not forces).  
2. Derive \(g_{\rm wake}(r)\) from the field equation with coefficients fixed independently of any galaxy fit.  
3. Close the A-115 / C-318 bridge from one stable four-interaction profile to both local Mass-Effect tensor and far-field gravity-source amplitude.  
4. Lattice runs: single bound core, wake profile, opposite-orientation cancellation, high-curvature short residual, rear-compression migration — under D-412 discipline.

## Failure / falsification

- Any coefficient set that requires a second substance to produce the extended wake.  
- Spontaneous bound flags on pure free packets.  
- Failure of opposite orientation labels to cancel the far wake while energy accounting remains closed.  
- Any re-introduction of force-carrier language or Standard Model interaction list as architectural primitives.

## Status

YELLOW. Continuum interaction stress written to match A-115 identity. Lattice discretization and quantitative wake derivation still required. No Standard Model drift permitted in further development of this node.
