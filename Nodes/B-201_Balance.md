---
node_id: "B-201"
canonical_name: "Equilibrium Balance"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "GREEN (Yellow Audit Open)"
metadata_standard: "I-06"
---

# Node B-201: Equilibrium Balance

## Name Disambiguation

B-201 **Equilibrium Balance** is the scalar equilibrium/imbalance measure. It is distinct from G-709 **Regulated-Response Balance**, which is a feedback-scaled response rule. The two nodes share a historical word but not a mechanism. **Do not merge them.**

Dependencies:
Upstream: External Field (E), Internal Field (I), Resistance (R), Electrical Locking (L)
Note: Primitives E, I, R, L are defined in Books, not here.
Downstream: B-202 Pressure, B-206 Paired Loop, Restoring Response, Imbalance-Driven Dynamics

Definition:
Balance defines the scalar measure of equilibrium between driving and opposing contributions.
It establishes the imbalance quantity from which Pressure is derived.
Balance does not define Pressure, Force, or Response.

Primitives:
E = external field contribution
I = internal field contribution
R = resistance
L = electrical locking

B = (k_E*E + k_I*I) - (k_R*R + k_L*L)
k_E, k_I, k_R, k_L > 0

Mathematics:
B = 0 => Equilibrium
B > 0 => Net Driving Tendency
B < 0 => Net Restoring Tendency

Balance is a scalar measure.
Linear weighting is the Green approximation. Nonlinear forms deferred.

Operational Chain:
Field Primitives => Balance => Pressure

Yellow Audit:
- Coefficients k_E, k_I, k_R, k_L unknown until measurement
- Linear weighting assumed; nonlinear regimes unresolved
- Balance evaluated instantaneously; temporal evolution not specified
- Physical interpretation of primitives E, I, R, L deferred to Books

Future Work:
Measure E, I, R, L independently. Compute B.
Compare calculated Balance with observed system state.
Repeat across equilibrium and nonequilibrium configurations.
