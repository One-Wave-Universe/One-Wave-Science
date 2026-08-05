---
node_id: "G-705"
canonical_name: "Correction"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node G-705: Correction

Dependencies:
Upstream: G-703 Modulation, G-704 Kabeuchi
Downstream: G-706 Validation, G-707 Persistence A

Definition:
Correction is the application of the modulation signal to update the current state.
It is the mechanism by which evaluation and modulation produce change.

I_{n+1} = I_n + alpha * M(E(Delta_n))

where 0 < alpha < 1 is the update gain.

Mathematics:
I_{n+1} = I_n + alpha * M_n

If M_n = 0: I_{n+1} = I_n. No correction. State unchanged.
If M_n != 0: I_{n+1} != I_n. Correction applied. State updated.

Update gain alpha controls how aggressively the correction is applied:
alpha -> 0: very slow correction. High stability. May miss fast changes.
alpha -> 1: very fast correction. Low stability. May overcorrect.

Relationship to update rule (A-109, A-111):
Correction is the deliberate application of a modulation signal.
The One-Wave update rule is the automatic field-level instantiation of the same concept.
In the update rule: beta_i(<psi_j> - psi_i) is the automatic correction term.
In G-705: alpha * M_n is the deliberate correction term.

Operational Chain:
Modulation => Correction => Updated State => Validation

Yellow Audit:
- alpha not yet specified
- Whether alpha is fixed or adaptive unresolved
- Whether overcorrection (alpha too large) produces instability not yet analyzed
- Inherits Yellow status from G-702 and G-703

---
