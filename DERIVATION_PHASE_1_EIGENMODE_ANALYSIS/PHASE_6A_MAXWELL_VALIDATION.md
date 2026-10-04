# Phase 6A: Maxwell Equation Validation

**Status:** IN PROGRESS  
**Date:** 2026-10-03  
**Objective:** Verify whether modified One-Wave rule can satisfy Maxwell equations

---

## Overview

The modified wave equation produces oscillatory transverse modes in the low-k regime:

$$\partial^2\psi/\partial t^2 + \gamma \partial\psi/\partial t = -\beta \nabla^2\psi$$

**Question:** Can the E and B field components extracted from this rule satisfy the full set of Maxwell equations?

We will test four critical conditions:

1. **Polarization vectors:** E || k (longitudinal), B ⊥ k (transverse)
2. **Faraday's law:** ∇×E = -∂B/∂t
3. **No monopoles:** ∇·B = 0
4. **Plasma frequency relation:** ω_L²(k) = ω_p² + k²c_eff²

---

## Mathematical Framework

### Modified Characteristic Equations

**Transverse (B-like):**
$$\lambda^2 - (2 - \gamma + \beta k^2)\lambda + (1 + \gamma - \beta k^2) = 0$$

**Longitudinal (E-like):**
$$\lambda^2 - (2 - \gamma - \beta k^2)\lambda + (1 - \gamma) = 0$$

### Frequency Extraction

From characteristic equation $\lambda^2 - C(k)\lambda + P(k) = 0$:

$$\lambda = e^{-i\omega}$$

Therefore:
$$\omega = -i \ln(\lambda)$$

For complex $\lambda = |\lambda|e^{i\theta}$:
$$\omega = -i[\ln|\lambda| + i\theta] = \theta - i\ln|\lambda|$$

### Mode Decomposition on 2D Hexagonal Lattice

For vector field $\vec{\psi}$:
- **E-like modes:** $\vec{A}_E \parallel \vec{k}$ (polarization along wavenumber)
- **B-like modes:** $\vec{A}_B \perp \vec{k}$ (polarization perpendicular to wavenumber)

The divergence-curl decomposition is:
$$\vec{\psi} = \nabla(\nabla \cdot \vec{\psi}) - \nabla \times (\nabla \times \vec{\psi})$$

First term: couples with −βk² → E-like  
Second term: couples with +βk² → B-like

---

## Test Plan

### Test 1: Polarization Vectors (Automatic from Vector Form)

**Hypothesis:** Vector field form with div/curl operators automatically enforces E || k and B ⊥ k.

**Method:**
- Extract polarization eigenvectors for E-mode at various k
- Extract polarization eigenvectors for B-mode at various k
- Verify dot products: $\vec{A}_E \cdot \hat{k} = |\vec{A}_E|$, $\vec{A}_B \cdot \hat{k} = 0$

**Expected result:** Polarizations correct within machine precision.

---

### Test 2: Faraday's Law in Discrete Form

**Hypothesis:** If E and B modes are coupled through the curl operator, Faraday's law should hold.

**Discrete form on hexagonal lattice:**
$$(\nabla \times \vec{E})_\text{hex} = -\partial \vec{B}/\partial t$$

**Method:**
- Evaluate curl of E-mode on a hexagonal patch
- Evaluate time derivative of B-mode
- Compare magnitudes and phases

**Challenge:** Discrete curl on hexagonal lattice requires careful staggered-grid implementation.

---

### Test 3: No-Monopole Condition

**Hypothesis:** B-mode is transverse (∇·B = 0 by construction from curl operator).

**Discrete form:**
$$(\nabla \cdot \vec{B})_\text{hex} = 0$$

**Method:**
- Apply discrete divergence to B-mode eigenvector
- Verify result ≈ 0 to machine precision

**Expected result:** Exact to machine precision (algebraic constraint).

---

### Test 4: Plasma Frequency Relation

**Hypothesis:** Longitudinal modes satisfy ω_L²(k) relation analogous to EM plasma.

**Standard EM:**
$$\omega_L^2(k) = \omega_p^2 + k^2 c^2$$

**Modified One-Wave (candidate relation):**
$$\omega_L^2(k) \approx \omega_p^2 + \beta k^2$$

Where $\omega_p$ is the low-k limit of longitudinal frequency.

**Method:**
- Compute $\omega_L(k)$ for k ∈ [0.1, 2.0]
- Extract $\omega_p = \omega_L(k=0)$ (approximate)
- Check if $\omega_L^2(k) - \omega_L^2(0) \approx \beta k^2$

**Expected result:** Linear or power-law dependence; identify the effective coupling relation.

---

## Critical Questions to Address

1. **K-Dependence Attenuation:**
   - Why does oscillation attenuate for k > 1.0?
   - Is this fundamental to the modified form, or does more physics emerge at high k?

2. **Dispersion vs Relativism:**
   - Real EM: ω_trans/k → c (constant)
   - Modified One-Wave: ω_trans/k varies with k (non-relativistic)
   - Is this an effective-theory limit, or missing physics?

3. **Full EM Compatibility:**
   - Can ALL four Maxwell equations be satisfied simultaneously?
   - Or does the modified rule describe an effective field theory?

4. **Physical Interpretation:**
   - If the rule produces damped waves, is this describing a lossy medium or a fundamental theory?
   - Does the superfluid lattice picture explain the damping naturally?

---

## Implementation Strategy

1. **Create maxwell_validation.py** (detailed numerical tests)
   - Function: test_polarization_vectors()
   - Function: test_faraday_law_discrete()
   - Function: test_no_monopole()
   - Function: test_plasma_frequency()

2. **Create hex_lattice_operators.py** (discrete operators)
   - Hexagonal grid construction
   - Discrete curl operator (staggered grid)
   - Discrete divergence operator
   - Discrete Laplacian operator

3. **Analyze results** in each test section
   - Quantify deviation from Maxwell requirements
   - Identify physical interpretation
   - Recommend modifications if needed

4. **Document findings** in PHASE_6A_RESULTS.md

---

## Success Criteria

- **Tier 1 (Critical):**
  - Polarization vectors correct (∠ between prediction and calculation < 1°)
  - No-monopole condition exact (∇·B ≈ 10^{-14})

- **Tier 2 (Important):**
  - Plasma frequency relation identified (R² > 0.95)
  - Faraday's law approximately satisfied (norm error < 5%)

- **Tier 3 (Desirable):**
  - Full Maxwell equations consistent across k
  - Physical interpretation of damping clear
  - Comparison with known EM phenomena established

---

## References

- PHASE_5_SUMMARY_AND_FORWARD_PATH.md: Phase 6 overview
- modified_maxwell_validation.py: Preliminary validation
- CANONICAL_CONSISTENCY_CHECK.md: Alignment with theory
- vector_field_framework.py: Vector field implementation

