---
node_id: "F-601"
canonical_name: "Influence"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-601: Influence

Dependencies:
Upstream: A-112 Persistent Mode
Downstream: F-602 through F-608 (all interaction outcomes)

Definition:
Influence means a change in one bounded state produces a change in another.
Without influence, no interaction can occur.
Influence is the precondition for all nodes in Appendix F.

Influence = nonzero state-to-state dependence

Mathematics:
Assume psi_2 = f(psi_1).
Define alpha = f'(psi_1).
Then: delta_psi_2 = alpha * delta_psi_1

If alpha = 0: no influence. delta_psi_1 produces no change in psi_2.
If alpha != 0 and delta_psi_1 != 0: delta_psi_2 != 0. Influence exists.

Influence = nonzero alpha in the state-to-state dependence function.

Operational Chain:
Persistent Mode => Influence => [Canonical Interaction Outcomes F-602 through F-608]

Yellow Audit:
- Exact function f and coefficient alpha not derived here
- Whether influence is symmetric (alpha_12 = alpha_21) or asymmetric not specified
- Range of influence (local vs nonlocal) not specified here

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.
