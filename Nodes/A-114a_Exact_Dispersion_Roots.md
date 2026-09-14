---
node_id: "A-114a"
canonical_name: "Exact Dispersion Roots"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Foundation Extension"
claim_gate_detail: "YELLOW — algebra of the A-114 characteristic polynomial; no new bench data"
metadata_standard: "I-06"
---

# Node A-114a: Exact Dispersion Roots

Upstream: A-114. Downstream: A-110a, C-324.

Characteristic equation from the core update (A-114):

```text
z^2 - S z + P = 0
S = 2 - γ + C
P = 1 - γ
C = β (cos(θ) - 1)
θ = k Δx
```

Exact roots:

```text
z_± = [ S ± sqrt(S² - 4P) ] / 2
```

Discriminant:

```text
Δ = S² - 4P = γ² + 2(2-γ)C + C²
```

Special case γ = 0:

```text
P = 1
S = 2 + C
Δ = C(C + 4)
z_± = 1 + C/2 ± sqrt(C(C+4)) / 2
```

Because C ∈ [-2β, 0], sign of Δ depends on β and θ.

If z = exp(-i ω Δt) and |z| = 1:

```text
ω Δt = -arg(z)
```

If |z| < 1 the mode decays. If |z| > 1 it grows (unstable update).

Product of roots is P = 1-γ. For undamped standing oscillation you need γ = 0 so |z+ z-| = 1, and Δ ≤ 0 or a unimodular pair.

Small-k recovery (A-114): θ → 0, γ → 0, ω ≈ c_L k sqrt(β/2).

Falsifier: a claimed ω that is not arg(z)/Δt for a root of this quadratic on a named lattice.
