---
node_id: "F-603"
canonical_name: "Transfer"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-603: Transfer

Dependencies:
Upstream: F-602 Interaction Differential
Downstream: F-604 Resonance, F-605 Interference, F-608 Attenuation

Definition:
Transfer means reciprocal redistribution of a bounded quantity between states.
The total quantity is conserved. What one gains, the other loses.

Transfer = reciprocal redistribution of a bounded quantity

Mathematics:
Closure assumption: Q_total = Q_1 + Q_2 = constant

Consequence:
dQ_1/dt = -dQ_2/dt
DeltaQ_1 + DeltaQ_2 = 0

If DeltaQ_1 > 0: Q_1 gains, Q_2 loses by the same amount.
If DeltaQ_1 < 0: Q_1 loses, Q_2 gains by the same amount.

Operational Chain:
Interaction Differential => Transfer => [Resonance / Interference / Attenuation / Amplification]

Yellow Audit:
- Exact transfer law beyond ideal closure not derived here
- Physical meaning of Q not fixed — Q may be amplitude, energy, phase, or other quantity
- Whether closure holds exactly or only approximately in the One-Wave lattice unresolved
- Transfer rate not specified

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.
