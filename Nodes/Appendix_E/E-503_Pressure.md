---
node_id: "E-503"
canonical_name: "Pressure (Gradient Form)"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "GREEN (form) / YELLOW (coefficient)"
metadata_standard: "I-06"
---

# Node E-503: Pressure (Gradient Form)

Dependencies:
Upstream: A-104 Gradient, A-106 Pressure Response
Downstream: E-506 Stability, Books (wherever pressure gradient drives dynamics), E-518 Relativistic Energy Density (extension), C-315 Wave Reader V1 (candidate hardware application)

IMPORTANT:
This node is a downstream specialization of A-104 Gradient.
It is distinct from B-202 Pressure (which derives from Balance).
Do not merge these nodes.

B-202 Pressure: derived from imbalance B = f(Balance)
E-503 Pressure (Gradient Form): derived from spatial gradient of psi

Definition:
Pressure (Gradient Form) is the distributed influence created by spatial
displacement imbalance. It arises from the gradient of the field, not from
the scalar balance.

Pressure (Gradient Form) = distributed influence from spatial displacement imbalance

Mathematics:
Pressure energy density:
u_p = (1/2) * K_p * |nabla_psi|^2,  K_p > 0

If nabla_psi = 0: u_p = 0. No pressure gradient.
If nabla_psi != 0: u_p > 0. Pressure gradient exists.

P_psi ~ (1/2) * K_p * |nabla_psi|^2

Operational Chain:
Gradient (A-104) => Pressure (Gradient Form) => Distributed Force => Stability

Yellow Audit:
- K_p (pressure stiffness) unknown until measurement
- Whether K_p is constant or field-dependent unresolved
- Relationship between K_p and restoring operator A (A-105) not yet formalized
- Full 3D gradient expansion deferred

Future Work:
Measure K_p via Wave Reader.
Apply controlled gradient. Measure pressure response.
Connect to stability window (E-506).

---
