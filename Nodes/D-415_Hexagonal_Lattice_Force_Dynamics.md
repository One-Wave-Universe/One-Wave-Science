---
node_id: "D-415"
canonical_name: "Hexagonal Lattice Interaction Dynamics"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Lattice Dynamics / Interaction Discretization"
claim_gate_detail: "YELLOW — discrete equations written from C-323 + D-408 + A-115; multi-core numerical validation still open"
metadata_standard: "I-06"
---

# Node D-415: Hexagonal Lattice Interaction Dynamics

**Former title:** Hexagonal Lattice Force Dynamics  
**Reason for rename:** One-Wave has interactions and restoring responses, not forces.

**Dependencies**  
Upstream: D-408 Sixfold 2D Triangular-Hexagonal Lattice, C-323 Displacement Interaction Regimes, A-115 Unified Compression Field, E-532 Bound/Unbound + Finite Wake, E-531 Dual-Harmonic Propagation, A-105 Restoring Response, D-412 Lattice Simulation Standard  
Lateral: D-413 Ground Lattice Orbital Restoring Simulation, D-414 Four-Interaction Shell  
Downstream: multi-core wake tests, core migration, residual spectrum runs

## Purpose

Discretize the continuum interaction stress of C-323 / A-115 onto the native sixfold lattice of D-408 so that:

- local compression-gradient response (gravity view),
- extended / wake compression (dark-matter view),
- oriented residual response (electrical view),
- curvature-saturated short residual,
- bound flag and dual-harmonic free sector

all live on the same sites and the same update.

No forces. Bond objects are **restoring responses**.

## Geometry (from D-408)

Sites form a triangular lattice (hexagonal neighborhoods):

\[
\mathbf{a}_1 = a(1,0),\qquad
\mathbf{a}_2 = a\bigl(\tfrac12,\tfrac{\sqrt{3}}{2}\bigr)
\]

Nearest-neighbor directions:

\[
\mathbf{e}_a = \bigl(\cos\tfrac{2\pi a}{6},\;\sin\tfrac{2\pi a}{6}\bigr),\quad a=0\ldots5
\]

Displacement lives on sites: \(\mathbf{u}_n\).

## Discrete compression

\[
\chi_n = -\sum_{a=0}^{5}\mathbf{e}_a\cdot(\mathbf{u}_{n+a}-\mathbf{u}_n)
\]

\[
(\Delta\chi)_n = \sum_{a=0}^{5}(\chi_{n+a}-\chi_n)
\]

## Bound flag (from E-532)

\[
I_1 = |\mathbf{u}_n|^2,\qquad
I_3 = \Bigl|\sum_{a=0}^{5}(\mathbf{u}_{n+a}-\mathbf{u}_n)\Bigr|^2
\]

\[
\mathrm{bound}_n = \bigl(I_3 > \tfrac12 I_1\bigr)\;\wedge\;\bigl(|\mathbf{u}_n| > u_{\mathrm{floor}}\bigr)
\]

Residual orientation \(C_n\) is nonzero only on bound sites.

## Bond restoring responses (discrete interaction stress)

For each directed bond \(n\to n+a\):

\[
\mathbf{R}_{n,a}
=
K\,\chi_n\,\mathbf{e}_a
+
\mu\,(\mathbf{u}_{n+a}-\mathbf{u}_n)
+
\alpha\,(\chi_{n+a}-\chi_n)\,\mathbf{e}_a
+
\beta\,C_n(\mathbf{C}_n\cdot\mathbf{e}_a)\,[\mathrm{bound}_n]
-
\gamma\,(\Delta\chi)_n\,\mathbf{e}_a
\]

Net restoring response on the site:

\[
\mathbf{R}_n = \sum_{a=0}^{5}\mathbf{R}_{n,a}
\]

Update:

\[
\rho\,\ddot{\mathbf{u}}_n = \mathbf{R}_n
\]

## Dual-harmonic free sector (from E-531)

After the response update, the unbound part of the field is evolved or projected so that

\[
\bigl((H+1)\cdot 2+1\bigr)-\bigl((H+1)\cdot 2-1\bigr)=2
\]

holds site-by-site on unbound sites only. Bound cores are excluded; their wakes re-enter the free sector once unbound.

## How the A-115 views appear on the lattice

| A-115 view | Lattice signature |
|------------|-------------------|
| Gravity (local) | Compact bound core → long-range compression gradient; other cores respond down-gradient |
| Dark-matter behavior (wake) | Extended compression left by motion/rotation of bound structure; same field, larger scale |
| Electrical (oriented residual) | Nonzero \(C_n\) on bound sites → oriented free wake; opposite labels cancel |
| Short residual | Large \(\gamma\) collapses core; discrete orientation cancellation inside core |
| Configuration residual | Off-diagonal rotation of \(C_n\) between nearby minima |

## Minimal working update

```text
for each time step:
    compute χ_n, Δχ_n, Δu_n from current u
    evaluate bound_n from I3 / I1 and u_floor
    zero C_n on unbound sites
    accumulate bond responses R_{n,a} → R_n
    advance u_n, v_n (Verlet or equivalent)
    (optional) dual-harmonic projection on unbound sites only
    record: energy, max |u|, bound count, wake profile, residual drift
```

Every run must satisfy D-412.

## Required first runs

1. Zero-input hold — no spontaneous bound flags, no drift.  
2. Single bound core — flag stable; far compression matches expected local gravity view.  
3. Moving / rotating core — measure extended wake (dark-matter view).  
4. Two cores, opposite C — wake cancellation (oriented residual).  
5. High-γ core — short residual, orientation cancellation.  
6. Rear-compression directed update — core migrates without dissolving the flag.  
7. Free packet — never acquires persistent bound flag; preserves ΔH = 2.

## Failure / falsification

- Spontaneous bound flags on pure free packets.  
- Loss of ΔH = 2 on the free sector under energy-preserving updates.  
- Need for a second substance to produce the extended wake.  
- Re-introduction of force-carrier or Standard Model interaction-list language.

## Status

YELLOW. Discrete restoring responses written from C-323 + A-115 + D-408 + E-531 + E-532. Multi-core numerical validation is the next required work.
