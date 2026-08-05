---
node_id: "F-606"
canonical_name: "Reflection"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-606: Reflection

Dependencies:
Upstream: F-604 Resonance, F-605 Interference
Downstream: F-608 Attenuation

Definition:
Reflection is the rejection and return of an incoming state at a boundary.
At a boundary, an incoming mode splits into reflected and transmitted components.

Reflection = boundary rejection/return

Mathematics:
Boundary split:
A_i = A_r + A_t

where:
A_i = incoming amplitude
A_r = reflected amplitude
A_t = transmitted amplitude

Reflection ratio:
r = A_r / A_i,   0 <= r <= 1

Reflected amplitude:
A_r = r * A_i

Operational Chain:
Boundary Interaction => Reflection + Transmission

Yellow Audit:
- What determines r at a given boundary not yet derived
- Whether r depends on frequency, angle, boundary type, or lattice properties unresolved
- Relationship between r and lattice coupling beta_i not yet formalized

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.
