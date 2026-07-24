---
node_id: "F-605"
canonical_name: "Interference"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-605: Interference

Dependencies:
Upstream: F-603 Transfer, F-602 Interaction Differential
Downstream: F-606 Reflection, F-607 Transmission, F-608 Attenuation

Definition:
Interference means phase-dependent combination that can reinforce, reduce, or cancel.
The outcome depends on the phase relationship between the two states.

Interference = choice-combination that can reinforce, reduce, or cancel

Mathematics:
psi_1 = A * cos(omega*t)
psi_2 = A * cos(omega*t + phi)

Combined:
psi_T = 2A * cos(phi/2) * cos(omega*t + phi/2)

Phase outcomes:
phi = 0:   psi_T = 2A*cos(omega*t)     Full reinforcement
phi = pi:  psi_T = 0                    Full cancellation
phi other: partial reinforcement or reduction

Effective amplitude:
A_eff = 2A * |cos(phi/2)|

Firewall:
psi_T = psi_1 + psi_2 is a trace of choice-resolution.
It is not borrowed superposition ontology.
The phase phi is a property of the interaction, not of the states in isolation.

Open: exact physical rule that sets phi in a given interaction not derived here (CCD-04).

Operational Chain:
Transfer + Phase Relationship => Interference => [Reinforcement / Reduction / Cancellation]

Yellow Audit:
- What sets phi in a given interaction not derived (CCD-04)
- Whether phi is fixed or dynamically evolving unresolved
- Full cancellation (phi = pi) in the lattice — whether exact or approximate unresolved

---
