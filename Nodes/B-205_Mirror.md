---
node_id: "B-205"
canonical_name: "Mirror"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-205: Mirror

Dependencies:
Upstream: B-203 Expression, B-204 Compression
Downstream: C-301 Mirror Gate, B-206a Shared Boundary, B-206b Four Views

Definition:
Mirror is the flip operation between Expression and Compression states.
Mirror is the function.
Mirror Gate (C-301) is the physical location or scale at which Mirror operates.

At the mirror point, what was Expression becomes Compression with a sign change.

M(psi_C, psi_E) -> (psi_E, -psi_C)

Mathematics:
Symplectic rotation:
M = [[0, 1], [-1, 0]]
M^2 = -I

One Mirror application:
M(psi_C, psi_E) = (psi_E, -psi_C)

Two Mirror applications:
M^2(psi_C, psi_E) = (-psi_C, -psi_E) = -(psi_C, psi_E)

Four Mirror applications:
M^4(psi_C, psi_E) = (psi_C, psi_E)

M^4 = I => 4*pi closure

The 4*pi closure follows from SU(2) structure of the S3 fiber.
Cross-reference: C-308 Spin-half.

Operational Chain:
Expression + Compression => Mirror => Mirror Gate (C-301)

Yellow Audit:
- Whether Mirror is forced by One-Wave geometry or defined as a boundary rule remains open (CCD-03)
- Resolution requires geometric derivation of S3 fiber from update rule alone
