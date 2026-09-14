---
node_id: "C-324"
canonical_name: "No Entanglement — Detector Map"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Principle / Measurement Mathematics"
claim_gate_detail: "YELLOW — principle frozen as One Wave rule; mapping math is ordinary wave timing, not a new force"
metadata_standard: "I-06"
---

# Node C-324: No Entanglement — Detector Map

Dependencies:
Upstream: A-110 Oscillation, A-103 Differential, B-205 Mirror, B-223 Three Moves, B-224 Two Choices, C-315 Wave Reader V1
Downstream: RABBIT-HOPPING build/CELL0, NO_ENTANGLEMENT.md, Book1 chapter No Entanglement

Definition:
There is no entanglement in this science.
A wave meets a detector or a lens. At that when, the cut is plus or minus.
A brain or a computer stores the sequence of cuts and maps peaks and troughs back along a named path. Distance and placement come from that record.
Two sites affect each other only through a net you can point at.

## Mathematics (ordinary wave + fence)

Traveling oscillation on a named path:

```text
u(x, t) = A cos(k x - ω t + φ)
```

Sign at a detector at location x_d and time t*:

```text
s(t*) = sign( u(x_d, t*) )
s ∈ {+1, 0, -1}
```

0 is stay (inside a dead zone T):

```text
s = +1    if u > T
s =  0    if |u| ≤ T
s = -1    if u < -T
```

That is B-223 three moves on the same cut as B-224 two wells when |u| > T.

### Distance from delay (one path, known speed)

If the same wavefront is cut at x_0 at t_0 and at x_1 at t_1, and the path is connected:

```text
Δt = t_1 - t_0
Δx = v Δt
```

Placement is the ordered list of (x_d, t*, s) along the path. No second copy in the void.

### Two-eye / two-detector baseline

Two detectors on a known baseline B, same wave, delays τ_L and τ_R:

```text
sin θ ≈ (τ_L - τ_R) v / B
```

Direction from time difference. Still no entanglement. The eyes share a head (a net).

### Rejected object

Do not write a state on two distant sites as one inseparable vector with no path. If a claim needs that, it is out of this node.

Operational Chain:
wave on a named path => detector/lens cut => s = +/0/- => memory of (t*, s, site) => map delay to distance/placement

Yellow Audit:
- Rule is policy of this repo (GREEN as policy, YELLOW as physics-versus-lab-QM).
- Mapping math is standard time-of-flight / phase. It does not by itself refute every lab correlation experiment; it refuses to *use* entanglement as a connection with no net.
- Cell-0 T3/T5 is the bench version of a cut plus hold.

Falsifier:
An effect in this repo that has no named net, no current, no receipt, and no detector cut, but is still treated as causal.
