---
node_id: "A-110a"
canonical_name: "Wave Equation Derivation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Foundation Extension"
claim_gate_detail: "YELLOW — continuum wave equation recovered from A-105 + inertia in 1D; discrete form already in A-114"
metadata_standard: "I-06"
---

# Node A-110a: Wave Equation Derivation

Dependencies:
Upstream: A-103 Differential, A-104 Gradient, A-105 Restoring Response, A-109 Inertial Memory, A-110 Oscillation
Sibling: A-114 Dispersion Relation (discrete update rule)
Downstream: C-324 No Entanglement Detector Map, C-315 Wave Reader

Purpose:
Show how the traveling wave used in C-324 is *derived*, not assumed.
Two tracks: continuum (this node) and lattice update (A-114).
Neither track uses entanglement.

## Track 1 — continuum from restore + inertia

A-104: imbalance is a gradient

```text
G = ∂ψ/∂x
```

A-105 linear restore (special case A = α):

```text
R_OW = -α ∂ψ/∂x
```

On a line, the *net* restore on a small segment is the difference of R_OW at the two ends — that is another derivative:

```text
net restore per length = ∂R_OW/∂x = -α ∂²ψ/∂x²
```

A-109 inertial memory: leftover change wants to keep going. Continuum stand-in:

```text
inertia density · ∂²ψ/∂t²
```

Balance (Newton-shaped, no new name required):

```text
μ ∂²ψ/∂t² = α ∂²ψ/∂x²
```

Set

```text
v² = α / μ
```

and you have the 1D wave equation:

```text
∂²ψ/∂t² = v² ∂²ψ/∂x²
```

General solution on an infinite line (d'Alembert):

```text
ψ(x,t) = f(x - v t) + g(x + v t)
```

Right-going piece is the C-324 traveling wave. A harmonic right-going cut of that family is

```text
ψ = A cos(k x - ω t + φ),    ω = v k
```

That last line is the *non-dispersive* limit. A-114 is the lattice version with possible dispersion.

## Track 2 — lattice (already derived in A-114)

Core update:

```text
ψ_i^{n+1} = ψ_i^n + (1-γ)(ψ_i^n - ψ_i^{n-1}) + β(<ψ_j^n> - ψ_i^n)
```

Plane-wave ansatz → characteristic quadratic → small-k, small-γ:

```text
ω(k) ≈ c_L k √(β/2)
```

Same shape as ω = v k with v = c_L √(β/2). No extra constant invented here.

## Detector (C-324) sits on top, not inside

The equation does not choose + or −.
A fence at (x_d, t*) reads

```text
s = sign_T( ψ(x_d, t*) )
```

Distance on a named path:

```text
Δx = v Δt
```

Two detectors, baseline B:

```text
sin θ ≈ v (τ_L - τ_R) / B
```

If there is no path between the two sites, this formula is not licensed.

## What is established vs open

Established as algebra:
- restore + inertia ⇒ wave equation in 1D linear case
- traveling + and − families
- A-114 small-k match

Open / YELLOW:
- operator A is not proven linear at every scale (A-105 says so)
- β, γ unmeasured on the bench
- 3D / hex lattice not derived in this node
- Cell-0 oscillation may be fight, not this PDE

Falsifier:
A claimed traveling sign change with no restore, no inertia, and no named path.
