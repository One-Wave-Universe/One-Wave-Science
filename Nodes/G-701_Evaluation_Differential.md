---
node_id: "G-701"
canonical_name: "Evaluation Differential"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node G-701: Evaluation Differential

Dependencies:
Upstream: A-103 Differential (canonical definition), B-206 Paired Loop (response context)
Downstream: G-702 Evaluation

Note: This node is a downstream specialization of A-103 Differential.
Scope here: difference between current state and response state within the evaluation cycle.
Does not redefine A-103. Cross-reference only.

Definition:
The Evaluation Differential measures the difference between the current state
and the response state. It is the input to Evaluation.

Delta_n = R_n - I_n

Differential measures difference. Differential does not determine action.

Mathematics:
Delta_n = R_n - I_n

If R_n = I_n: Delta_n = 0. No difference. No evaluation signal.
If R_n != I_n: Delta_n != 0. Differential exists. Evaluation proceeds.

Operational Chain:
Current State + Response State => Evaluation Differential => Evaluation

Yellow Audit:
- Whether Delta_n is scalar or vector not specified
- Whether all components of state difference are captured in a single differential unresolved
- Relationship between Delta_n and Threshold value T (B-207) not yet formalized

---
