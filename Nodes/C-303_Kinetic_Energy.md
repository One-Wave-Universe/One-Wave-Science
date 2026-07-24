---
node_id: "C-303"
canonical_name: "Kinetic Energy"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node C-303: Kinetic Energy

Dependencies:
Upstream: C-302 Momentum
Downstream: C-304 Potential, C-305 Work, C-309 Friction Limit

Definition:
Velocity v encodes rate of displacement.
Kinetic energy encodes motion energy.

K proportional to v^2

Mathematics:
K = (1/2)*m_SM*v^2  (Gray standard form)

One-Wave candidate notation:
K_OW = (1/2)*m_eff*v^2, where m_eff is measured Mass Effect and is not yet derived from bounded geometry.

v -> K

Yellow Audit:
- Mass Effect m_eff not yet derived from One-Wave geometry
- Cross-reference: Book 1 Ch14 and A-115 for the active Mass-Effect program; C-309 is only one inherited constraint, not a completed derivation
