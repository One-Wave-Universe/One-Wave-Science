---
node_id: "C-307"
canonical_name: "Angular Momentum"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "GREEN (foundation) / YELLOW (endpoint needs refinement)"
metadata_standard: "I-06"
---

# Node C-307: Angular Momentum

Dependencies:
Upstream: C-306 Torque
Downstream: C-308 Spin-half

Definition:
Rotation has angular velocity omega.
Mass distribution gives rotational inertia I.
Angular momentum is their product.

L = I * omega

Mathematics:
L = I * omega

For a continuous field:
L = integral r x (rho * v) dV

where rho is field density and v is local field velocity.

In One-Wave context: density and velocity arise from the update rule.
Full derivation deferred.

Yellow Audit:
- Endpoint derivation from One-Wave field geometry not complete
- Relationship between L and spin-half topology (C-308) needs formalization
- Parked for refinement — does not block chapter
