---
node_id: "C-302"
canonical_name: "Momentum"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node C-302: Momentum

Dependencies:
Upstream: A-111 Recursion, A-112 Persistent Mode
Downstream: C-303 Kinetic Energy

Definition:
Wave number k encodes spatial frequency.
Momentum encodes motion tendency.
Higher k => higher p.

p proportional to k

Mathematics:
For a wave mode with spatial frequency k:
p ~ hbar * k  (standard relation, not yet derived from One-Wave geometry alone)

k -> p

Parked Dependency — CCD-01:
Full derivation of S_min = hbar (the minimum action quantum) is blocked
pending Harmonic Shell geometry (D-405).
This does not block the proportionality statement p proportional to k.
It blocks the derivation of the constant of proportionality.

Operational Chain:
Persistent Mode => k => Momentum

Yellow Audit:
- Constant of proportionality not yet derived from One-Wave geometry alone
- CCD-01 parked explicitly
