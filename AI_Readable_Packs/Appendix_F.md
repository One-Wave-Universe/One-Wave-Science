# Appendix F — AI-Readable Canonical Node Pack

Generated from current canonical node files. YAML front matter controls gate and lifecycle.

---

## SOURCE: F-601_Influence.md

---
node_id: "F-601"
canonical_name: "Influence"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-601: Influence

Dependencies:
Upstream: A-112 Persistent Mode
Downstream: F-602 through F-608 (all interaction outcomes)

Definition:
Influence means a change in one bounded state produces a change in another.
Without influence, no interaction can occur.
Influence is the precondition for all nodes in Appendix F.

Influence = nonzero state-to-state dependence

Mathematics:
Assume psi_2 = f(psi_1).
Define alpha = f'(psi_1).
Then: delta_psi_2 = alpha * delta_psi_1

If alpha = 0: no influence. delta_psi_1 produces no change in psi_2.
If alpha != 0 and delta_psi_1 != 0: delta_psi_2 != 0. Influence exists.

Influence = nonzero alpha in the state-to-state dependence function.

Operational Chain:
Persistent Mode => Influence => [Canonical Interaction Outcomes F-602 through F-608]

Yellow Audit:
- Exact function f and coefficient alpha not derived here
- Whether influence is symmetric (alpha_12 = alpha_21) or asymmetric not specified
- Range of influence (local vs nonlocal) not specified here

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.

---

## SOURCE: F-602_Interaction_Differential.md

---
node_id: "F-602"
canonical_name: "Interaction Differential"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-602: Interaction Differential

Dependencies:
Upstream: F-601 Influence, A-103 Differential (canonical definition)
Downstream: F-603 Transfer, F-604 Resonance, F-605 Interference

Note: This node is a downstream specialization of A-103 Differential.
Scope here: difference between two interacting states.
Does not redefine A-103. Cross-reference only.

Definition:
Interaction Differential measures the imbalance between two interacting states.
It is the quantity that drives all subsequent interaction outcomes.

D_psi = psi_1 - psi_2

Interaction Differential = measured imbalance between states

Mathematics:
D_psi = psi_1 - psi_2

If psi_1 = psi_2: D_psi = 0. No differential. No interaction driven by imbalance.
If psi_1 != psi_2: D_psi != 0. Differential exists. Interaction may proceed.

Operational Chain:
Influence => Interaction Differential => [Transfer / Resonance / Interference]

Yellow Audit:
- Scalar differential defined here; vector differential deferred
- Whether D_psi is the only relevant differential or additional components exist unresolved

---

---

## SOURCE: F-603_Transfer.md

---
node_id: "F-603"
canonical_name: "Transfer"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-603: Transfer

Dependencies:
Upstream: F-602 Interaction Differential
Downstream: F-604 Resonance, F-605 Interference, F-608 Attenuation

Definition:
Transfer means reciprocal redistribution of a bounded quantity between states.
The total quantity is conserved. What one gains, the other loses.

Transfer = reciprocal redistribution of a bounded quantity

Mathematics:
Closure assumption: Q_total = Q_1 + Q_2 = constant

Consequence:
dQ_1/dt = -dQ_2/dt
DeltaQ_1 + DeltaQ_2 = 0

If DeltaQ_1 > 0: Q_1 gains, Q_2 loses by the same amount.
If DeltaQ_1 < 0: Q_1 loses, Q_2 gains by the same amount.

Operational Chain:
Interaction Differential => Transfer => [Resonance / Interference / Attenuation / Amplification]

Yellow Audit:
- Exact transfer law beyond ideal closure not derived here
- Physical meaning of Q not fixed — Q may be amplitude, energy, phase, or other quantity
- Whether closure holds exactly or only approximately in the One-Wave lattice unresolved
- Transfer rate not specified

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.

---

## SOURCE: F-604_Resonance.md

---
node_id: "F-604"
canonical_name: "Resonance"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-604: Resonance

Dependencies:
Upstream: F-603 Transfer, F-602 Interaction Differential
Downstream: F-606 Reflection, F-607 Transmission

Definition:
Resonance means aligned-choice reinforcement.
When two states choose the same phase, their combination exceeds either alone.

Resonance = aligned choice producing reinforcement

Mathematics:
Let A_1 > 0, A_2 > 0 (both states are in aligned phase).

Combined amplitude:
A_T = A_1 + A_2

Reinforcement conditions:
A_T > A_1  (combined exceeds first alone)
A_T > A_2  (combined exceeds second alone)

Both conditions hold when A_1 > 0 and A_2 > 0.

Firewall:
Same addition form does not mean standard superposition mechanism.
The equation records the aligned-choice outcome.
It does not import quantum superposition ontology.

Open: why a given interaction resolves as aligned rather than opposed — deferred (CCD-04).

Operational Chain:
Transfer + Aligned Choice => Resonance => [Amplification / Transmission]

Yellow Audit:
- Why a given interaction resolves as aligned (resonant) rather than opposed not derived
- CCD-04 is the selection mechanism question — frontier problem
- Conditions for resonance between specific mode types not yet characterized

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.

---

## SOURCE: F-605_Interference.md

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

---

## SOURCE: F-606_Reflection.md

---
node_id: "F-606"
canonical_name: "Reflection"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-606: Reflection

Dependencies:
Upstream: F-604 Resonance, F-605 Interference
Downstream: F-608 Attenuation

Definition:
Reflection is the rejection and return of an incoming state at a boundary.
At a boundary, an incoming mode splits into reflected and transmitted components.

Reflection = boundary rejection/return

Mathematics:
Boundary split:
A_i = A_r + A_t

where:
A_i = incoming amplitude
A_r = reflected amplitude
A_t = transmitted amplitude

Reflection ratio:
r = A_r / A_i,   0 <= r <= 1

Reflected amplitude:
A_r = r * A_i

Operational Chain:
Boundary Interaction => Reflection + Transmission

Yellow Audit:
- What determines r at a given boundary not yet derived
- Whether r depends on frequency, angle, boundary type, or lattice properties unresolved
- Relationship between r and lattice coupling beta_i not yet formalized

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.

---

## SOURCE: F-607_Transmission.md

---
node_id: "F-607"
canonical_name: "Transmission"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-607: Transmission

Dependencies:
Upstream: F-606 Reflection
Downstream:

Definition:
Transmission is the acceptance and passage of an incoming state through a boundary.
Transmission and reflection are complementary — together they account for all
of the incoming mode.

Transmission = boundary acceptance/passage

Mathematics:
From F-606: A_i = A_r + A_t

Transmission ratio:
t = A_t / A_i = 1 - r

Conservation:
r + t = 1

Transmitted amplitude:
A_t = t * A_i = (1 - r) * A_i

Operational Chain:
Boundary Interaction => Reflection + Transmission => [Attenuation / Amplification / Persistence]

Yellow Audit:
- t = 1 - r follows from closure assumption (A_i = A_r + A_t)
- Whether closure holds exactly in the One-Wave lattice unresolved
- Frequency-dependent transmission not yet characterized

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.

---

## SOURCE: F-608_Attenuation.md

---
node_id: "F-608"
canonical_name: "Attenuation"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Interaction Operators"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node F-608: Attenuation

Dependencies:
Upstream: F-603 Transfer, F-605 Interference, F-606 Reflection
Downstream:

Definition:
Attenuation is the progressive weakening of state strength as it propagates
or interacts. The mode loses amplitude over distance or time.

Attenuation = progressive weakening of state strength

Mathematics:
Proportional decay assumption:
dA/dx = -mu * A,   mu > 0

Solution:
A(x) = A_0 * exp(-mu * x)

Since mu > 0: A(x) < A_0 for x > 0.
Amplitude decreases monotonically with distance.

Attenuation rate mu depends on:
- Lattice resistance gamma
- Coupling strength beta
- Mode frequency

Note: Exponential attenuation follows from the proportional decay assumption.
Proportional decay is an assumption, not a derived result.
Other attenuation forms are possible if proportional decay does not hold.

Operational Chain:
Propagating Mode + Resistance => Attenuation => Reduced Amplitude

Yellow Audit:
- Proportional decay assumption not yet verified for One-Wave lattice
- mu not yet derived from lattice parameters gamma and beta
- Whether attenuation is frequency-dependent unresolved
- Non-exponential attenuation forms not yet ruled out

---


## Updated 32 forward-reference repair

Legacy forward references F-609 Amplification and F-610 Persistence were removed because no canonical files exist. Any future amplification or persistence proposal must be routed through the current F-series, A-112 Persistent Mode, and E-508 Real Persistence Under Loss rather than cited as an existing node.

---

