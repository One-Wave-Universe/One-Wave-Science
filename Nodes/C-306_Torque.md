---
node_id: "C-306"
canonical_name: "Torque"
namespace: "NODE"
gate: "GREEN"
lifecycle: "HELD"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "GREEN (foundation) / YELLOW (math weak, parked for refinement)"
metadata_standard: "I-06"
---

# Node C-306: Torque

Dependencies:
Upstream: C-305 Work, A-104 Gradient
Downstream: C-307 Angular Momentum

Definition:
Off-center displacement creates rotational preference.
Rotational preference produces torque.

off-center displacement -> rotational preference -> tau

Mathematics:
tau = r x F

where r is the displacement vector from the rotation axis
and F is the applied force.

In One-Wave context:
tau = r x (-A(nabla_psi))

Yellow Audit:
- Math form is foundation level only
- Full derivation of torque from One-Wave field geometry deferred
- Parked for refinement — does not block chapter
