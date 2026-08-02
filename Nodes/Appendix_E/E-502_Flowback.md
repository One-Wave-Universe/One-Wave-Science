---
node_id: "E-502"
canonical_name: "Flowback"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "GREEN (form) / YELLOW (coefficient)"
metadata_standard: "I-06"
---

# Node E-502: Flowback

Dependencies:
Upstream: A-105 Restoring Response, A-101 Ground / Zero
Downstream: E-506 Stability

Definition:
Flowback is the return tendency of a displaced medium toward equilibrium.
It is the most basic stability mechanism — the field's intrinsic tendency
to undo displacement.

Flowback = restoring return tendency toward ground

Mathematics:
Potential energy of flowback:
V_f(psi) = (1/2) * K_f * psi^2,  K_f > 0

Restoring response from flowback:
R_f = -dV_f/dpsi = -K_f * psi

Sign check:
If psi > 0: R_f = -K_f * psi < 0  (response points back toward zero)
If psi < 0: R_f = -K_f * psi > 0  (response points back toward zero)

Response always points back toward psi = 0.

R_f = -K_f * psi

Operational Chain:
Displacement => Flowback => Restoring Return => Stability

Yellow Audit:
- K_f (flowback stiffness) unknown until measurement
- Whether K_f is constant or displacement-dependent unresolved
- Relationship between K_f and the restoring operator A (A-105) not yet formalized

Future Work:
Measure K_f via Wave Reader.
Apply controlled displacement. Measure return rate.
Determine whether K_f is constant or varies with displacement amplitude.

---
