---
node_id: "D-415"
canonical_name: "Hexagonal Lattice Force Dynamics"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Lattice Dynamics / Force Discretization"
claim_gate_detail: "YELLOW — discrete equations written from C-323 + D-408; multi-core numerical validation still open"
metadata_standard: "I-06"
---

# Node D-415: Hexagonal Lattice Force Dynamics

**Dependencies**  
Upstream: D-408 Sixfold 2D Triangular-Hexagonal Lattice, C-323 Four Forces as Displacement Regimes, E-532 Bound/Unbound + Finite Wake, E-531 Dual-Harmonic Propagation, A-105 Restoring Response, D-412 Lattice Simulation Standard  
Lateral: D-413 Ground Lattice Orbital Restoring Simulation, D-414 Four-Interaction Shell  
Downstream: multi-core wake tests, core migration, Maxwell lattice closure, residual spectrum runs

## Purpose

Discretize the continuum stress of C-323 onto the native sixfold lattice of D-408 so that the four force regimes, the bound flag, and dual-harmonic free propagation all live on the same sites and the same update.

## Geometry (from D-408)

Sites form a triangular lattice (hexagonal neighborhoods):

\[
\mathbf{a}_1 = a(1,0), \qquad
\mathbf{a}_2 = a\bigl(\tfrac12,\tfrac{\sqrt{3}}{2}\bigr)
\]

Nearest-neighbor directions:

\[
\mathbf{e}_a = \bigl(\cos\tfrac{2\pi a}{6},\;\sin\tfrac{2\pi a}{6}\bigr), \quad a=0\ldots5
\]

Displacement lives on sites: \(\mathbf{u}_n = (u_n^x, u_n^y)\).

## Discrete compression and curl

\[
\theta_n = \sum_{a=0}^{5} \mathbf{e}_a \cdot (\mathbf{u}_{n+a} - \mathbf{u}_n)
\]

\[
\omega_n = \sum_{a=0}^{5} \mathbf{e}_a^\perp \cdot (\mathbf{u}_{n+a} - \mathbf{u}_n)
\]

Discrete Laplacian \(\Delta\theta_n\) uses the standard six-neighbor stencil on the triangular lattice.

## Bound flag (from E-532)

\[
I_1 = |\mathbf{u}_n|^2, \qquad
I_3 = |\Delta\mathbf{u}_n|^2
\]

\[
\mathrm{bound}_n = \bigl(I_3 > \tfrac12 I_1\bigr) \;\wedge\; \bigl(|\mathbf{u}_n| > u_{\mathrm{floor}}\bigr)
\]

Residual orientation \(C_n\) is nonzero only on bound sites; elsewhere \(C_n = 0\).

## Bond forces (discrete stress)

For each oriented bond \(n \to n+a\):

\[
\mathbf{f}_{n,a}
=
K\,\theta_n\,\mathbf{e}_a
+
\mu\,(\mathbf{u}_{n+a}-\mathbf{u}_n)
+
\alpha\,(\theta_{n+a}-\theta_n)\,\mathbf{e}_a
+
\beta\,C_n(\mathbf{C}_n\cdot\mathbf{e}_a)
-
\gamma\,(\Delta\theta)_n\,\mathbf{e}_a
\]

Total force on site \(n\):

\[
\mathbf{f}_n = \sum_{a=0}^{5} \mathbf{f}_{n,a}
\]

Newton update:

\[
\rho\,\ddot{\mathbf{u}}_n = \mathbf{f}_n
\]

(or the first-order / velocity-Verlet form used by the existing D-413 runner).

## Dual-harmonic free sector (from E-531)

After forces are applied, the free (unbound) part of the displacement field is projected or evolved so that the local harmonic index satisfies

\[
\bigl((H+1)\cdot 2+1\bigr) - \bigl((H+1)\cdot 2-1\bigr) = 2
\]

site-by-site. Bound cores are excluded from this projection; their wakes, once outside the core, re-enter the free sector and inherit the identity.

## Four regimes on the lattice

| Regime | How it appears |
|--------|----------------|
| Gravity | Compact bound core, \(C=0\) or averaged → long-range \(1/r\)-like compression; other cores drift down the gradient |
| EM | Nonzero residual \(C_n\) on bound sites → oriented free wake; longitudinal / transverse split recovers C-311 language |
| Strong | Large \(\gamma\) collapses core radius; discrete orientations of \(C_n\) must cancel to stay bound |
| Weak | Two nearby core minima; off-diagonal force rotates \(C_n\) and radiates a short-lived massive wake |

## Minimal working update

```text
for each time step:
    compute θ_n, ω_n, Δθ_n, Δu_n from current u
    evaluate bound_n from I3 / I1 and u_floor
    zero C_n on unbound sites
    accumulate bond forces f_{n,a} → f_n
    advance u_n, v_n (Verlet or equivalent)
    (optional) dual-harmonic projection on unbound sites only
    record: energy, max |u|, bound count, circulation Γ_6, residual drift
```

Every run must satisfy D-412 (energy/work balance, residual drift, failure boundary).

## Required first runs

1. **Zero-input hold** — no spontaneous bound flags, no drift (extends D-413 control).  
2. **Single bound core** — flag stable; far compression falls as expected range.  
3. **Two cores, C = 0** — mutual drift (gravity-like).  
4. **Two cores, opposite C** — wake cancellation test (EM-like).  
5. **High-γ core** — short residual, discrete orientation cancellation (strong-like).  
6. **Rear-compression directed update** — core migrates without dissolving the flag.  
7. **Free packet** — never acquires a persistent bound flag; preserves ΔH = 2.

## Relation to existing simulations

- **D-413** already runs ground-lattice orbital restoring dynamics on the same geometry; D-415 adds the full stress, bound flag, and orientation residual.  
- **D-414** visualizes four interaction *channels* driven by real wave data; D-415 derives four force *regimes* from discrete stress. Complementary, not competitive.

## Failure / falsification

- Spontaneous bound flags on pure free packets under zero-core runs.  
- Loss of ΔH = 2 on the free sector under the same update that preserves energy.  
- No parameter set (K, μ, α, β, γ, σ) produces both long-range isotropic and short-range residual behavior.  
- Opposite orientation labels fail to cancel the far wake while energy accounting remains closed.

## Status

YELLOW. Discrete equations and update rule written directly from C-323 + D-408 + E-531 + E-532. Multi-core numerical validation is the next required work; until those runs exist and pass D-412, the node stays Yellow.
