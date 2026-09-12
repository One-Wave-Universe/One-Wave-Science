---
node_id: "C-306"
canonical_name: "Torque"
namespace: "NODE"
gate: "GREEN"
lifecycle: "HELD"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "GREEN (foundation) / YELLOW (math weak, parked for refinement)"
metadata_standard: "I-06"
---

# Node C-306: Torque

Dependencies:
Upstream: C-305 Work, A-104 Gradient
Downstream: C-307 Angular Momentum, C-320 Magnetic-Compression Path Coupling, D-413 Ground Lattice Orbital-Restoring Simulation, D-416 Planetary Rotation-Magnetic Coupling Test Matrix

Definition:
Off-center displacement creates rotational preference.
Rotational preference produces torque.

off-center displacement -> rotational preference -> tau

Mathematics:
tau = r x F

where r is the displacement vector from the rotation axis
and F is the applied force.

In One-Wave context:
tau = r x (-A(nabla_psi))

For the magnetic/compression bridge, C-320 may supply a distributed path-weighted restoring response. C-306 remains the authority for converting an off-center distributed response into torque; C-320 does not redefine torque.

Yellow Audit:
- Math form is foundation level only
- Full derivation of torque from One-Wave field geometry deferred
- C-320/D-416 use this node as a mechanics control, not as evidence that magnetic coupling exists
- Parked for refinement — does not block chapter
