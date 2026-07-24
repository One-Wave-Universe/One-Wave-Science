---
node_id: "C-304"
canonical_name: "Potential"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node C-304: Potential

Dependencies:
Upstream: A-102 Displacement, A-105 Restoring Response
Downstream: C-305 Work

Definition:
Compressed displacement stores imbalance.
Stored imbalance is potential energy.

compressed displacement -> stored imbalance -> potential

Mathematics:
V(x) = integral A(s) ds from 0 to x

where A is the restoring response operator (A-105).

For scalar linear case: A(x) = alpha*x
V(x) = (1/2)*alpha*x^2

Potential energy is the stored integral of the restoring response.

Yellow Audit:
- Full potential energy derivation inherits Yellow status of A-105 (A operator form)
