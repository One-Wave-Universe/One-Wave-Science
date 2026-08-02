---
node_id: "B-204"
canonical_name: "Compression"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-204: Compression

Dependencies:
Upstream: A-102 Displacement, A-110 Oscillation
Downstream: B-203 Expression, B-206 Paired Loop, B-205 Mirror, B-206a Shared Boundary, B-206b Four Views, B-225 Field Cycle (Compression stage), G-720 No Control But Self-Control (Choice mechanism)

Definition:
Compression is the inward phase of a one-wave oscillation cycle.
The half-cycle in which one system is the receiver.

Compression = inward displacement phase of the oscillation cycle

Mathematics:
In update rule context:
psi_i^{n+1} < psi_i^n  (compressed step: field amplitude decreasing inward)

One system's Expression is another system's Compression input.
Compression In <-> Expression Out

REFINEMENT (checked, consistent with the above, not contradicting it):
a precise gradient-driven mechanism for this inequality: C(psi) = psi
- alpha*grad(psi), where alpha is a stabilization factor. This gives
the "decreasing inward" direction an actual driver (a fraction of the
local gradient subtracted each step) rather than just stating the
inequality holds. Structurally matches A-105's real restoring-response
form (R_OW = -A*grad(psi)) — same gradient-opposing shape, applied here
specifically as the Compression mechanism rather than a general
restoring force.

Operational Chain:
Oscillation => Compression <-> Expression => Paired Loop

Yellow Audit:
- Exact phase boundary between Compression and Expression not formalized
- Compression depth (how much is integrated vs rejected) not specified
- Relationship between Compression depth and threshold behavior deferred to Threshold node
