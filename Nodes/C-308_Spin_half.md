---
node_id: "C-308"
canonical_name: "Spin-half"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "GREEN (internal topology chain valid)"
metadata_standard: "I-06"
---

# Node C-308: Spin-half

Dependencies:
Upstream: C-301 Mirror Gate, B-205 Mirror, C-307 Angular Momentum
Downstream: All spin-related object nodes in Books

Definition:
Spin-half emerges from the 4*pi closure produced by repeated Mirror crossings.

Mirror state:
m = +1  (expressed)
m = -1  (compressed)

Mirror crossing flips state: m -> -m

Mathematics:
One loop (2*pi):
(theta, m) -> (theta + 2*pi, -m)
psi(theta + 2*pi) = -psi(theta)

Two loops (4*pi):
(theta + 2*pi, -m) -> (theta + 4*pi, m)
psi(theta + 4*pi) = psi(theta)

compressed <-> expressed -> 4*pi closure -> spin-half

The state picks up a sign under 2*pi rotation and returns to itself under 4*pi rotation.
This is the defining property of a spin-half system.

Neutron Two-Shell Model (parked pending CCD-02):
Inner shell:  R+ = 0.7331 fm
Outer shell:  R- = 0.8409 fm
Shell width:  sigma = 0.210 fm
These values pass charge form factor sanity checks internally.
Full derivation blocked pending CCD-02.

Operational Chain:
Mirror Gate => 4*pi closure => Spin-half

Yellow Audit:
- Ratio interpretation psi_C/psi_E parked explicitly (CCD-02)
- CCD-02 blocks kappa+/- (equilibrium stiffness) derivation pending E_opp(R)
- Both parked items do not block the topology chain
- They have named addresses and will be resolved when proton boundary work is complete
