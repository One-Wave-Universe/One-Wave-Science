# Phase 6B: Implementation Strategy — From Eigenmode to Projection

**Date:** 2026-10-03  
**Status:** READY FOR IMPLEMENTATION  
**Canonical Authority:** Node C-311, Node B-206b, Book 1 Ch13

---

## The Canonical Truth

**Node C-311: Electric-Magnetic Duality** explicitly states:

```
E_vec ~ ∇P_c        (radial component)
B_vec ~ ∇×P_c       (rotational component)
```

Where:
```
P_c = β * ΔE / V_c   [pressure field, from B-206b]
```

**Critical fact:** Both E and B derive from the SAME field P_c.

**Therefore:** E and B MUST evolve with the SAME frequency, because they are projections of a single time-evolving field.

---

## Phase 6A Error: Wrong Interpretation

We treated E and B as:

```
EIGENMODE INTERPRETATION:
  Update rule → Characteristic equation → Two separate eigenvalues λ_E, λ_B
  → Different frequencies ω_E ≠ ω_B
  
RESULT: Faraday's law violated (frequencies don't match)
```

But C-311 requires:

```
PROJECTION INTERPRETATION:
  Update rule → Single mode with frequency ω
  → Project to E: extract E = some function of ψ with frequency ω
  → Project to B: extract B = some other function of ψ with frequency ω
  
RESULT: Same frequency guaranteed because both come from ψ
```

---

## The Key Realization

The characteristic equation we've been using:

```
λ² - (2-γ+βk²)λ + (1+γ-βk²) = 0  [transverse]
```

This has TWO roots: λ₊ and λ₋.

**Current interpretation:** These are two separate modes (one E-like, one B-like).

**Correct interpretation:** These are two solutions of the SAME mode equation. We should pick one and use it to define both E and B.

**The question:** Given one eigenvalue λ, how do we extract E and B?

---

## Solution Path: Extract E and B from Single Mode

### Step 1: Recognize the Mode Structure

For a plane wave on the lattice:
```
ψ(r,t) = A e^{i(k·r - ωt)}
```

The update rule couples:
```
∇(∇·ψ)  → divergence part [relates to E]
∇×(∇×ψ) → curl part [relates to B]
```

Both are derivatives of the SAME field ψ.

### Step 2: Decompose the Amplitude

The amplitude vector A can be decomposed:
```
A = A_∥ + A_⊥

A_∥ ∥ k̂   [longitudinal, relates to E]
A_⊥ ⊥ k̂   [transverse, relates to B]
```

### Step 3: The Unified Mode

**Hypothesis:** There is ONE characteristic equation that governs the full evolution:

```
λ² - C_unified(k)λ + P_unified(k) = 0
```

This single equation has two roots λ₊ and λ₋.

**But:** We don't use them as separate modes. Instead:

- **For ω_E:** Use λ₊ or λ₋ (pick one consistently)
- **For ω_B:** Use the SAME λ (not the other root)
- **Relationship:** E_vec ~ ∇ψ with this ω, B_vec ~ ∇×ψ with same ω

### Step 4: Faraday Coupling

Once both E and B have the same ω, Faraday's law becomes:

```
∇×E = -∂B/∂t

Takes form:  k × ∇ψ ~ ω (∇×ψ)

This is automatically satisfied if E and B are both projections of ψ
with the same ω.
```

---

## Implementation: Three Tracks

### Track A: Unified Mode Extraction

**Objective:** Take existing characteristic equation, use single eigenvalue for both E and B.

**Code structure:**
```python
def unified_mode_extraction(k_mag, gamma, beta):
    """
    Single characteristic equation governing ψ evolution.
    """
    k_sq = k_mag ** 2
    C_k = 2 - gamma - beta * k_sq  # Unified coefficient
    P_k = 1 - gamma                 # Unified constant
    
    # Single eigenvalue (pick the physical one)
    discriminant = C_k**2 - 4*P_k
    lambda_physical = (C_k + np.sqrt(discriminant + 0j)) / 2
    
    omega = -1j * np.log(lambda_physical)
    
    # Extract E and B as PROJECTIONS with same ω
    E_like = extract_E_projection(k_mag, omega, gamma, beta)
    B_like = extract_B_projection(k_mag, omega, gamma, beta)
    
    return omega, E_like, B_like, lambda_physical
```

**Questions to answer:**
1. What is C_unified? Is it C_E, C_B, or something different?
2. What is P_unified? Is it P_E, P_B, or something different?
3. How exactly do we extract E and B from the same ω?

### Track B: Discrete Lattice Operators

**Objective:** Implement proper discrete curl/divergence on hexagonal lattice.

**Using:** hex_lattice_graph.py infrastructure

```python
def hex_divergence(vector_field, lattice):
    """Discrete divergence on 2D hexagonal lattice."""
    pass

def hex_curl(vector_field, lattice):
    """Discrete curl on 2D hexagonal lattice."""
    pass

def hex_gradient(scalar_field, lattice):
    """Discrete gradient on 2D hexagonal lattice."""
    pass
```

**Test:** Show that ∇·(∇×F) ≡ 0 exactly on the lattice.

### Track C: Direct Maxwell Solver

**Objective:** Solve full Maxwell equations on hexagonal lattice with the modified rule.

```python
def discrete_maxwell_solver():
    """
    Solve:  ψⁿ⁺¹ = 2ψⁿ - ψⁿ⁻¹ - γ(ψⁿ-ψⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]
    
    Extract: E = some projection of ψ
             B = some other projection of ψ
    
    Verify:  Faraday's law ∇×E = -∂B/∂t holds
             No-monopole ∇·B = 0 holds exactly
             Polarization E∥k, B⊥k holds
             Plasma frequency relation holds
    """
    pass
```

---

## Critical Test: Can We Make ω_E = ω_B?

### The Actual Test

Given:
```
Phase 6A data: k=0.5, ω_E = 0.236, ω_B = 0.805, ratio = 3.41
```

**Question:** Does this ratio disappear if we:
1. Use the same characteristic equation for both?
2. Use the same eigenvalue λ for both?
3. Extract E and B correctly as projections?

**If yes:** One-Wave can satisfy Maxwell equations

**If no:** Additional physics is needed (cross-coupling term)

---

## Mathematical Clarity Needed

### Current Confusion

The original update rule separates:
```
∇(∇·ψ)  with coefficient +β
∇×(∇×ψ) with coefficient -β
```

This leads to DIFFERENT characteristic equations:
```
E: λ² - (2-γ-βk²)λ + (1-γ) = 0
B: λ² - (2-γ+βk²)λ + (1+γ-βk²) = 0
```

### Possible Resolution

**Option 1:** The separation is real, but E and B modes should evolve together via constraint.

**Option 2:** The separation is artificial. There's ONE true characteristic equation, and we've been misidentifying it.

**Option 3:** The update rule needs modification to make E and B frequencies match.

---

## Expected Behavior if Projection Works

If we correctly extract E and B as projections with unified frequency:

```
1. Faraday's law: ∇×E = -∂B/∂t   ✓ (automatic from projections)

2. No-monopole: ∇·B = 0          ✓ (B = ∇×(something), so div is zero)

3. Polarization: E∥k, B⊥k        ✓ (guaranteed by vector decomposition)

4. Plasma frequency: ω_L²(k) ~ ω_p² + βk²  ✓ (should follow from modified rule)

5. Light-like limit: ω/k → const  ✗ (won't hold; this is non-relativistic)
```

---

## Failure Modes and Their Meaning

### If ω_E Still ≠ ω_B After Projection Fix

**Meaning:** The modified One-Wave rule cannot satisfy Maxwell equations.

**Next step:** Investigate what coupling term would fix this.

### If ω_E = ω_B But Faraday Doesn't Hold

**Meaning:** Frequency matching isn't enough; need explicit Faraday constraint.

**Next step:** Add Faraday as a coupled constraint equation.

### If All Conditions Hold Except Light-like Limit

**Meaning:** One-Wave describes an effective theory (waves in medium), not vacuum EM.

**Verdict:** SUCCESS - describe condensed-matter EM analogue.

---

## Success Criteria for Phase 6B

### Tier 1 (Must Have)
- ✓ Implement unified mode extraction
- ✓ Show whether ω_E = ω_B with projection interpretation
- ✓ Discrete curl/divergence operators working

### Tier 2 (Should Have)
- ✓ Full discrete Maxwell solver running
- ✓ Faraday's law tested explicitly
- ✓ Clear statement of what works/doesn't work

### Tier 3 (Nice to Have)
- ✓ Identify required coupling term if needed
- ✓ Physical interpretation of why term exists
- ✓ Falsification path forward

---

## Next Immediate Action

**Implement Track A:** Unified mode extraction

Test the hypothesis: if E and B come from the same mode with the same frequency, do all Maxwell conditions follow?

This is the critical question that will determine the fate of the modified One-Wave rule.

