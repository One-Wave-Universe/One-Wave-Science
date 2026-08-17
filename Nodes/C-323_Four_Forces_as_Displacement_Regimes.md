---
node_id: "C-323"
canonical_name: "Four Forces as Displacement Regimes"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Force Unification / Continuum Stress"
claim_gate_detail: "YELLOW — continuum limits written; lattice discretization and quantitative matching still open"
metadata_standard: "I-06"
---

# Node C-323: Four Forces as Displacement Regimes

**Dependencies**  
Upstream: A-102 Displacement, A-105 Restoring Response, A-106 Pressure Response, C-311 Electric-Magnetic Duality, E-532 Bound/Unbound + Finite Wake, D-408 Sixfold Lattice  
Lateral: C-318 Mass Mechanism, D-414 Four-Interaction Shell (visualization, not this derivation)  
Downstream: hexagonal force dynamics, Maxwell closure from pressure, residual spectrum

## Purpose

Recover the four classical interactions as geometric and energetic regimes of **one** continuum stress built from a single displacement field. No additional fundamental fields are introduced.

## Continuum stress

Displacement field \(\mathbf{u}(\mathbf{x},t)\). Strain, compression, and vorticity:

\[
\varepsilon_{ij} = \tfrac12(\partial_i u_j + \partial_j u_i), \qquad
\theta = \nabla\cdot\mathbf{u}, \qquad
\omega_i = (\nabla\times\mathbf{u})_i
\]

Minimal isotropic stress that already distinguishes bound cores, free wakes, and orientation:

\[
\boxed{
\sigma_{ij}
=
K\,\theta\,\delta_{ij}
+
2\mu\bigl(\varepsilon_{ij}-\tfrac13\theta\delta_{ij}\bigr)
+
\alpha(\partial_i\theta)(\partial_j\theta)
+
\beta\,C_i C_j
-
\gamma(\nabla^2\theta)\,\delta_{ij}
}
\]

- \(K\) bulk modulus (isotropic compression)  
- \(\mu\) shear modulus  
- \(\alpha\) gradient energy of compression  
- \(\beta\) oriented residual stress  
- \(\gamma\) curvature penalty  
- \(C_i\) residual orientation density, nonzero **only** on regions that satisfy the bound criterion (E-532)

Momentum balance:

\[
\partial_j\sigma_{ij} = \rho\,\ddot u_i
\]

## Four regimes

### 1. Gravity — isotropic long-range wake

Far from cores, \(C=0\) and shear averages away. Leading term is bulk compression. Static limit:

\[
K\nabla\theta \approx 0 \quad\Rightarrow\quad \theta \sim \frac{M}{r}
\]

Test cores fall down \(-\nabla\theta\). Pure gradient response to stable displacement (consistent with A-105 / gradient-gravity reading). Finite-wake cutoff exists in principle; for ordinary masses it sits at cosmological scales.

### 2. Electromagnetism — oriented free wake

Bound cores can retain a residual orientation \(C_i\). Outside the core, \(\beta C_i C_j\) sources a free, oriented wake. Longitudinal and transverse projections of the same displacement recover the pressure-field split already in C-311:

\[
\mathbf{E} \sim \nabla P_c, \qquad \mathbf{B} \sim \nabla\times P_c
\]

Static potential again \(1/r\), now carrying an orientation label (charge). Opposite labels cancel the far wake.

### 3. Strong interaction — curvature-saturated core

When the curvature term \(\gamma\nabla^2\theta\) dominates, the core cannot expand. Balance

\[
K\theta \sim \gamma\nabla^2\theta \quad\Rightarrow\quad \text{range}\sim\sqrt{\gamma/K}
\]

yields a short (Yukawa or harder) residual. Discrete orientations of \(C_i\) inside the core must cancel for the core to remain bound; the uncancelled piece is the strong residual. Lattice finite-wake kernels with small \(\sigma\) are the discrete transcription.

### 4. Weak interaction — configuration-changing displacement

A core may sit in more than one local minimum of curvature-plus-orientation energy. The displacement that rotates or tunnels the core between minima is an off-diagonal piece of \(\sigma_{ij}\). The intermediate configuration is only marginally bound, so the associated wake is short-lived and massive. Axial character appears because internal orientation rotation is a pseudovector displacement.

## Summary table

| Regime | Dominant stress content | Range | Orientation |
|--------|-------------------------|-------|-------------|
| Gravity | bulk \(K\theta\) | long | none |
| EM | residual \(\beta C_i C_j\) | long | yes (charge) |
| Strong | curvature \(\gamma\nabla^2\theta\) | short | discrete internal |
| Weak | off-diagonal core rotation | short | axial, changes identity |

## Relation to existing nodes

- **C-311** supplies the EM projection language; this node supplies the stress that sources those projections.  
- **E-532** supplies the bound flag that turns \(C_i\) on or off.  
- **E-531** governs free propagation of wakes after they leave the core; it does not set mass.  
- **D-414** visualizes four *interaction channels* of a bounded wave; this node derives the four *force regimes* from continuum stress. They are complementary, not identical.

## Required next work

1. Discretize \(\sigma_{ij}\) on the D-408 hexagonal lattice (bond forces from \(\theta_n\), shear, gradient energy, \(C_n\), curvature).  
2. Seed tightly bound oriented cores and verify automatic appearance of long-range wake, short-range residual, and core migration.  
3. Close Maxwell homogeneous + inhomogeneous pair from \(\nabla P_c\), \(\nabla\times P_c\) and continuum momentum (upgrade path for C-311).  
4. Quantitative matching of effective couplings and ranges remains open — Yellow until then.

## Failure / falsification

- If no single parameter set of \((K,\mu,\alpha,\beta,\gamma)\) can produce both a long-range isotropic wake and a short-range residual under the same bound flag.  
- If oriented residuals fail to cancel for opposite labels while preserving energy accounting.  
- If lattice transcription of the stress spontaneously violates the dual-harmonic free-sector identity (E-531).

## Status

YELLOW. Continuum limits written and internally consistent with A-105, C-311, E-531, E-532. Lattice discretization and quantitative recovery of observed ranges still required.
