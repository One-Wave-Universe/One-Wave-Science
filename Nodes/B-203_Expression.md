---
node_id: "B-203"
canonical_name: "Expression"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-203: Expression

Dependencies:
Upstream: A-102 Displacement, A-110 Oscillation
Downstream: B-204 Compression, B-206 Paired Loop, B-205 Mirror, B-206a Shared Boundary, B-206b Four Views, B-225 Field Cycle (Expansion stage), G-720 No Control But Self-Control (Choice mechanism)

Definition:
Expression is the outward phase of a one-wave oscillation cycle.
The half-cycle in which one system is the transmitter.

Expression = outward displacement phase of the oscillation cycle

Mathematics:
In update rule context:
psi_i^{n+1} > psi_i^n  (expressed step: field amplitude increasing outward)

From Appendix A Proof (A-05b):
Expression Out <-> Compression In

REFINEMENT (checked, consistent, not contradicting): E(psi) = psi +
beta*grad(psi), where beta is a transmission factor — the mirror
mechanism to B-204's compression refinement, adding rather than
subtracting the gradient term. Together, C(psi) and E(psi) give both
directions of B-203/B-204's existing inequality a real, symmetric
mechanism.

Bidirectional pressure exchange:
P = -c^2 * nabla^2_psi

Operational Chain:
Oscillation => Expression <-> Compression => Paired Loop

Yellow Audit:
- Exact phase boundary between Expression and Compression not formalized
- Relationship between Expression amplitude and transmitted information not derived
