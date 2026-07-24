---
node_id: "E-501"
canonical_name: "Zero Compression"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "GREEN (definition) / YELLOW (mathematics)"
metadata_standard: "I-06"
---

# Node E-501: Zero Compression

Dependencies:
Upstream: A-101 Ground / Zero
Downstream: E-502 Flowback

Definition:
Zero Compression is the balanced reference state from which compression and expression are measured. It represents a bounded neutral condition rather than the absence of structure.

Core:
Zero Compression = neutral bounded reference state

Operational Chain:
Ground/Zero -> Zero Compression -> Flowback -> Stability

Yellow Audit:
- Exact mathematical formulation deferred.
- Relationship to pressure response and restoring response to be formalized.
- Interaction with B-201 Equilibrium Balance to be derived. The legacy A-05c label is retired.

Future Work:
Connect Zero Compression to the stability window and recursive boundary conditions.

## Dependency Order

Zero Compression (E-501)
-> Flowback (E-502)
-> Pressure Gradient Form (E-503)
-> Surface (E-504)
-> Coupling (E-505)
-> Stability (E-506)
-> Scale-Invariant Loop (E-507)

Also receives:
- E-508 Real Persistence Under Loss

---

## Canonical Persistence Dependency

Real Persistence Under Loss is defined only in E-508. The anonymous embedded duplicate formerly appended to this file was removed.
