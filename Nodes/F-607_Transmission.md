---
node_id: "F-607"
canonical_name: "Transmission"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-607: Transmission

Dependencies:
Upstream: F-606 Reflection
Downstream:

Definition:
Transmission is the acceptance and passage of an incoming state through a boundary.
Transmission and reflection are complementary — together they account for all
of the incoming mode.

Transmission = boundary acceptance/passage

Mathematics:
From F-606: A_i = A_r + A_t

Transmission ratio:
t = A_t / A_i = 1 - r

Conservation:
r + t = 1

Transmitted amplitude:
A_t = t * A_i = (1 - r) * A_i

Operational Chain:
Boundary Interaction => Reflection + Transmission => [Attenuation / Amplification / Persistence]

Yellow Audit:
- t = 1 - r follows from closure assumption (A_i = A_r + A_t)
- Whether closure holds exactly in the One-Wave lattice unresolved
- Frequency-dependent transmission not yet characterized

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.
