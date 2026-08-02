---
node_id: "C-305"
canonical_name: "Work"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node C-305: Work

Dependencies:
Upstream: C-304 Potential, A-105 Restoring Response
Downstream: C-306 Torque, C-307 Angular Momentum

Definition:
Force applied over displacement produces work.

W = integral F dx

Mathematics:
W = integral F(x) dx from x_0 to x_1

In One-Wave context: F = R_OW = -A(nabla_psi)
W = integral (-A(nabla_psi)) dx

Yellow Audit:
- Inherits Yellow status of A-105 operator form
