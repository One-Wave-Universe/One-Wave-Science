# Phase 6B: Canonical Bridge — Node C-311 and Missing Physics

**Date:** 2026-10-03  
**Status:** STRATEGY FORMULATION  
**Critical Reference:** Node C-311 (Electric-Magnetic Duality) [YELLOW gate]

---

## The Canonical Framework

From Node C-311: Electric-Magnetic Duality:

```
E_vec ~ ∇P_c        (radial component — electric field)
B_vec ~ ∇×P_c       (rotational component — magnetic field)

Where P_c = pressure field (pressure cushion from B-206b)
```

**Key statement from C-311 Future Work:**
> "Formally derive Maxwell's four equations from ∇P_c and ∇×P_c rather than leaving them as a sketch."

**This is exactly the phase we are entering.**

---

## Phase 6A Finding: E-B Frequency Mismatch

Our validation showed:
```
k = 0.5:  ω_E = 0.236   ω_B = 0.805   ratio = 3.41  ✗
```

**Why this happens:**

The characteristic equations are:
```
E: λ² - (2-γ-βk²)λ + (1-γ) = 0
B: λ² - (2-γ+βk²)λ + (1+γ-βk²) = 0
```

Different coefficients → different eigenvalues → different ω's.

**Hypothesis from C-311:** 

If E and B are both projections of the SAME field P_c, they should have the SAME time evolution. The frequency mismatch suggests we have the projection wrong.

---

## Missing Physics: The Coupling Term

### Current One-Wave Structure

```
ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]
       └─ inertia ─┘  └─ damping ─┘  └──────── coupling ────────┘
```

The coupling separates:
- **∇(∇·ψ)** with coefficient +β → acts on E-mode
- **-∇×(∇×ψ)** with coefficient -β → acts on B-mode

Note the MINUS sign in front of the curl term!

### What If the Minus Sign Is Wrong?

**Hypothesis:** The characteristic equations have different structures because there's missing physics in the coupling term.

Currently:
```
∇(∇·ψ) - ∇×(∇×ψ)    [divergence MINUS curl]
```

What if the physics requires:
```
∇(∇·ψ) + γ·∇×(∇×ψ)  [divergence PLUS curl with matching damping]
```

Or:
```
∇(∇·ψ) - ∇×(∇×ψ) + cross-coupling term
```

That could couple E and B through an additional interaction term?

---

## Three Candidate Mechanisms for E-B Coupling

### Option A: Symmetric Coupling

Modify the update rule to couple E and B with a damping-dependent cross term:

```
ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ - ψⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]
                                  + λ_cross[term that couples E↔B]
```

Where λ_cross could be:
- Proportional to γ (damping couples the modes)
- Proportional to β (or a different coupling constant)
- A k-dependent function

**Physics motivation:** In quantum systems, dissipation often creates mode coupling.

### Option B: Modified Characteristic Coefficients

Rather than changing the update rule, recognize that E and B should satisfy:

```
E: λ² - C_E(k)λ + P_E(k) = 0
B: λ² - C_B(k)λ + P_B(k) = 0

With CONSTRAINT: Roots must give ω_E = ω_B at each k
```

This is an **inverse problem**: given the requirement that ω_E = ω_B, what must the characteristic equations be?

Solve for C_E, C_B, P_E, P_B that enforce this.

### Option C: Faraday Coupling as a Constraint

Instead of modifying the rule, impose Maxwell's Faraday law as an additional constraint:

```
∇×E = -∂B/∂t   [must be satisfied alongside the update rule]
```

This couples E and B directly through their time derivatives.

For plane waves:
```
k × A_E e^{iωt} = ω_B A_B e^{iωt}
```

This requires:
```
|k||A_E| = |ω_B||A_B|
```

And frequency matching:
```
ω_E = ω_B
```

**This is a non-local constraint** that might require modifying how we interpret the update rule.

---

## Phase 6B Implementation Plan

### Track 1: Investigate Cross-Coupling Terms (Option A)

**Objective:** Find the minimal coupling term that makes ω_E = ω_B.

**Steps:**
1. Assume coupling term: λ_cross = γ·f(k,β)·[some operator]
2. Derive new characteristic equations with this term
3. Solve for f(k,β) such that eigenvalues match
4. Check if resulting mode dispersion still shows oscillation

**Success criteria:**
- ω_E = ω_B at all k tested
- Transverse modes still propagate in low-k regime
- Faraday's law approximately satisfied

### Track 2: Inverse Design of Characteristic Equations (Option B)

**Objective:** Determine what characteristic equations would satisfy both oscillation AND frequency matching.

**Steps:**
1. Require: ω_E = ω_B for all k
2. Require: Complex eigenvalues in low-k regime (oscillation)
3. Require: Matches "closest" to original form
4. Solve for coefficients C_E, C_B, P_E, P_B

**Success criteria:**
- Derived equations explicitly couple E and B
- Physical interpretation clear (what mechanism causes this?)
- Testable predictions for other wavenumbers

### Track 3: Discrete Maxwell Solver on Hexagonal Lattice (Option 4B)

**Objective:** Build a full discrete implementation and test Faraday constraint directly.

**Steps:**
1. Implement hex lattice with proper discrete curl/divergence operators
2. Discretize both E and B equations
3. Enforce Faraday's law ∇×E = -∂B/∂t in discrete form
4. Simulate and check if modes couple correctly

**Files to create:**
- `hex_lattice_operators.py` (discrete differential operators)
- `discrete_maxwell_solver.py` (full solver)
- `phase6b_discrete_validation.py` (tests)

---

## Critical Insight from Repository

The canonical node C-311 tells us what should be true:

```
One field P_c
├─ Gradient:  E ~ ∇P_c
└─ Curl:      B ~ ∇×P_c
```

Both E and B come from the SAME field P_c, so they must have the same frequency!

**The solution might be:** 

We need to express both E and B modes not as separate eigenvalues of the same characteristic equation, but as **two projections of a single mode with a unified frequency**.

This is different from eigenmode decomposition. It's a **projection** rather than a **decomposition**.

---

## Distinction: Eigenmode Decomposition vs Field Projection

### Current Approach (Phase 4-6A): Eigenmode Decomposition

```
Update rule → Characteristic equation → Two eigenvalues λ₊, λ₋ → Frequencies ω₊, ω₋

This gives distinct modes with potentially different frequencies.
```

### Canonical Approach (C-311): Field Projection

```
Single field P_c evolves with one frequency ω
├─ Project to E: E_vec = some derivative of P_c
└─ Project to B: B_vec = some other derivative of P_c

Both have the SAME ω because they come from the same field.
```

**This might be the missing physics!**

The question: How do we extract E and B from ψ such that they share the same frequency?

Maybe:
- E = (∂/∂t) of divergence part
- B = (∂/∂t) of curl part

But both ∂/∂t operate on the same field, so same frequency follows.

---

## Next Immediate Steps

1. **Read C-311 fully** in canonical sources
2. **Read B-206b** (pressure cushion mechanism)
3. **Check Books 1 Ch13** (Electricity/Magnetism, explicitly cites C-311)
4. **Implement discrete lattice operators** from hex_lattice_graph.py
5. **Test Faraday constraint** in discrete form
6. **Investigate field projection** vs eigenmode decomposition

---

## Expected Outcome of Phase 6B

**Scenario 1: C-311 Framework Works**
- E and B emerge naturally from ψ with matching frequencies
- Faraday's law satisfied
- All four Maxwell equations derivable from modified One-Wave rule
- **Verdict:** One-Wave IS a reformulation of electromagnetism (effective field theory)

**Scenario 2: Additional Physics Needed**
- E-B coupling requires specific cross-coupling term
- Term has clear physical meaning (damping ↔ inertia coupling)
- All four Maxwell equations derivable with this addition
- **Verdict:** One-Wave + coupling term = electromagnetic theory

**Scenario 3: Fundamental Incompatibility**
- No coupling term can make E and B frequencies match
- Faraday's law cannot be satisfied with the update rule
- **Verdict:** One-Wave describes different physics (superfluid, not EM)

---

## References

- **Node C-311:** Electric-Magnetic Duality (YELLOW gate, active)
- **Node B-206b:** Four Views / Pressure Cushion
- **Book1_Ch13:** Electricity/Magnetism (cites C-311)
- **Phase 6A Results:** Frequency mismatch ω_B/ω_E = 3.41

---

## Commitment

Phase 6B will follow the canonical framework (C-311) rather than inventing ad-hoc coupling terms. We will either:

1. Show C-311's projection works perfectly → One-Wave is EM
2. Find the minimal addition that makes C-311 work → One-Wave + extension is EM
3. Show why C-311 cannot work → One-Wave is something else

**No ambiguity. Clear falsification gates. Canonical authority as the guide.**

