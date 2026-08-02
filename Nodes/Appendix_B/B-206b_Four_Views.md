---
node_id: "B-206b"
canonical_name: "Four Views — Inward, Outward, Across, Over"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-206b: Four Views — Inward, Outward, Across, Over

Dependencies:
Upstream: B-203 Expression, B-204 Compression, B-205 Mirror, B-206 Paired Loop, E-503 Surface
Downstream: C-301 Mirror Gate, C-308 Spin-half, A-115 Pressure Pulse (unresolved naming conflict — see earlier audit), C-311 Electric-Magnetic Duality, G-711 Gate 7, B-207 Threshold, E-515 Observation Windows

Definition:
The Four Views describe the four directional relationships of a field mode at its boundary.
They are not separate forces.
They are four perspectives of the same boundary interaction.

Inward  = compression toward center
Outward = expression away from center
Across  = motion along the boundary surface
Over    = boundary roll-off event

The Over is the boundary release mechanism.
A field mode presses against the boundary.
Surface tension holds the mode until the boundary threshold is exceeded.
The field then rolls off the boundary rather than snapping directly backward.
The roll-off produces:
- Spin tendency
- Pressure cushion
- Pressure pulse

Mathematics:
Boundary:
r = R

Surface hold energy:
E_s = sigma * A_s

Boundary excess energy:
DeltaE = E_mode - E_s

Boundary hold:
DeltaE <= 0

Roll-off:
DeltaE > 0

Boundary asymmetry:
S_roll = closed_integral psi(R,theta) * d_psi(R,theta)/d_theta * d_theta

Spin tendency exists when:
DeltaE > 0
AND
S_roll != 0

Pressure cushion:
P_c = beta * DeltaE / V_c

Pressure pulse:
d^2P/dt^2 - c_w^2 * nabla^2 P = gamma * DeltaE * delta(r - R) * delta(t - t_0)

Spin-half closure:
psi(theta + 2*pi) = -psi(theta)
psi(theta + 4*pi) = psi(theta)

Operational Chain:
Expression
-> Compression
-> Paired Loop
-> Four Views
-> Inward / Outward / Across / Over
-> Roll-Off
-> Spin Tendency
-> Pressure Cushion
-> Pressure Pulse
-> Mirror Gate

Yellow Audit:
- Boundary threshold defined.
- Excess-energy condition defined.
- Roll-off condition defined.
- Boundary asymmetry defined.
- Spin tendency mathematically conditioned.
- Pressure cushion defined.
- Pressure pulse equation defined.
- Spin-half closure connected.

Still unresolved:
- First-principles derivation of boundary energy.
- Exact surface-tension function.
- Continuous versus discrete roll-off.
- Formal derivation of orientation inversion.
- Complete derivation of charge shell.
- Complete derivation of magnetic curl.
- Experimental validation across scales.
