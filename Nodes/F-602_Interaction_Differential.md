---
node_id: "F-602"
canonical_name: "Interaction Differential"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-602: Interaction Differential

Dependencies:
Upstream: F-601 Influence, A-103 Differential (canonical definition)
Downstream: F-603 Transfer, F-604 Resonance, F-605 Interference

Note: This node is a downstream specialization of A-103 Differential.
Scope here: difference between two interacting states.
Does not redefine A-103. Cross-reference only.

Definition:
Interaction Differential measures the imbalance between two interacting states.
It is the quantity that drives all subsequent interaction outcomes.

D_psi = psi_1 - psi_2

Interaction Differential = measured imbalance between states

Mathematics:
D_psi = psi_1 - psi_2

If psi_1 = psi_2: D_psi = 0. No differential. No interaction driven by imbalance.
If psi_1 != psi_2: D_psi != 0. Differential exists. Interaction may proceed.

Operational Chain:
Influence => Interaction Differential => [Transfer / Resonance / Interference]

Yellow Audit:
- Scalar differential defined here; vector differential deferred
- Whether D_psi is the only relevant differential or additional components exist unresolved

---
