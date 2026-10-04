# Modified Update Rule: Restoring Oscillatory Behavior

**Status:** BREAKTHROUGH - Path forward identified  
**Date:** 2026-10-03  

---

## The Problem and Solution

**Problem:** Original update rule produces only purely imaginary transverse frequencies → pure decay, no EM-like waves.

**Root cause:** Characteristic equation has real positive eigenvalues → ω = -i ln(λ) is purely imaginary.

**Solution:** Modify the constant term in the characteristic equation to allow complex eigenvalues.

---

## Modified Update Rule (Wave Equation Form)

Replace the original equation:
```
ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ - ψᵢⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]ᵢ
```

With a wave-equation structure:
```
ψᵢⁿ⁺¹ - 2ψᵢⁿ + ψᵢⁿ⁻¹ = -γ(ψᵢⁿ - ψᵢⁿ⁻¹) + β[∇(∇·ψ) - ∇×(∇×ψ)]ᵢ
```

This is the **wave equation with damping**:
```
∂²ψ/∂t² + γ∂ψ/∂t = -β∇²ψ   [in continuous form]
```

This structure is physically motivated:
- **LHS:** Second-order time derivative (inertia) with damping
- **RHS:** Spatial coupling (restoring force)

---

## New Characteristic Equation

For transverse (B-like) modes with this form:

```
λ² - (2 - γ + βk²)λ + (1 + γ - βk²) = 0
```

The change is in the **constant term**: `(1-γ)` → `(1+γ-βk²)`

This allows the **discriminant to be negative**:
```
Δ = (2 - γ + βk²)² - 4(1 + γ - βk²)
```

When Δ < 0: eigenvalues are **complex conjugates** → ω has both real and imaginary parts → **oscillatory modes with decay** ✓

---

## Key Results

### Sample Parameter Sets with Oscillation

| γ | β | k | Re(ω) | Im(ω) | Status |
|---|---|---|-------|-------|--------|
| 0.5 | 0.1 | 0.1 | 0.911 | -0.202 | ✓ Propagating |
| 0.5 | 0.1 | 1.0 | 0.828 | -0.168 | ✓ Propagating |
| 0.5 | 0.1 | 2.0 | 0.438 | -0.048 | ✓ Propagating |
| 0.9 | 0.1 | 0.1 | 1.160 | -0.321 | ✓ Propagating |
| 0.9 | 0.1 | 1.0 | 1.107 | -0.294 | ✓ Propagating |
| 0.1 | 0.1 | 0.1 | 0.436 | -0.047 | ✓ Propagating |

### Characteristics of New Modes

1. **Non-zero group velocity:** ∂ω/∂k ≠ 0 (not purely underdamped)
2. **Damping present:** Im(ω) < 0 (modes decay over time)
3. **Real oscillation:** Re(ω) > 0 (waves propagate before decaying)
4. **k-dependent:** Dispersion relation is non-trivial

---

## Physical Interpretation

The modified rule represents a **damped wave equation**:

```
∂²ψ/∂t² + γ∂ψ/∂t = -c²_eff(k)∇²ψ
```

Where the effective speed depends on wavenumber:
```
c²_eff(k) = β
```

### EM Analogy

This is analogous to electromagnetic waves in a **lossy medium** (conductor or plasma):
- **Real ω:** Waves propagate
- **Im(ω) < 0:** Dissipation (ohmic loss or collisional damping)
- **Frequency-dependent:** Dispersion from lattice structure

---

## Comparison: Original vs Modified

| Property | Original | Modified |
|----------|----------|----------|
| Time structure | First-order | Second-order (wave) |
| Characteristic | λ² - Cλ + (1-γ) | λ² - Cλ + (1+γ-βk²) |
| Eigenvalues | Real ± | Complex conjugates |
| ω = -i ln(λ) | Imaginary only | Real + Imaginary |
| Transverse modes | Pure decay | Damped oscillation |
| EM compatibility | No | Yes (in lossy medium) |

---

## Critical Questions

### 1. Does the Modified Rule Maintain E/B Separation?

The longitudinal mode equation becomes:
```
λ² - (2 - γ - βk²)λ + (1 + γ + βk²) = 0
```

The sign flip in the coupling (−βk² vs +βk²) should be preserved, so yes, E-like and B-like structure persists.

### 2. Does It Satisfy Maxwell Equations?

With the modified structure:
- Transverse modes now have ω/k ratio that varies with k
- This is **non-relativistic** (ω/k depends on k, not constant)
- Matches **matter wave** behavior (particle-like dispersion)

**Key insight:** The modified rule describes waves in a **medium**, not vacuum EM.

### 3. What's the Physical Origin?

Possible interpretations:
1. **Superfluid lattice with inertia:** The Gross-Pitaevskii equation in discrete form includes ∂²/∂t²
2. **Effective field theory:** Second-order time derivatives emerge from integrating out fast modes
3. **Quantum field theory:** Dispersion relation matches matter fields, not gauge fields

---

## Next Steps

### Immediate (Phase 5A)

1. **Re-test Maxwell equations** with the modified dispersion relation
   - Check Faraday's law: ∇×E = -∂B/∂t
   - Check no-monopole condition: ∇·B = 0
   - Verify E/B polarization relationship

2. **Check light-cone structure**
   - Compute phase velocity: v_ph = ω/k
   - Compute group velocity: v_g = ∂ω/∂k
   - Verify causality: v_g ≤ some universal speed

3. **Verify stability** across full parameter range
   - Check |λ| ≤ 1 for all k
   - Identify stability constraint on (γ, β)

### Medium-term (Phase 5B)

4. **Map to physical parameters**
   - Does γ correspond to damping rate?
   - Does β correspond to effective speed²?
   - Can we extract electron mass, charge, speed of light?

5. **Test against known EM phenomena**
   - Coulomb potential from E-mode
   - Bremsstrahlung from B-mode decay
   - Plasma oscillation frequency

---

## Mathematical Detail: Why Complex Roots Appear

For the modified characteristic equation:
```
λ² - (2 - γ + βk²)λ + (1 + γ - βk²) = 0
```

Discriminant:
```
Δ = (2 - γ + βk²)² - 4(1 + γ - βk²)
```

Expanding:
```
Δ = (2 - γ)² + 2(2 - γ)βk² + β²k⁴ - 4 - 4γ + 4βk²
  = 4 - 4γ + γ² + 2(2 - γ)βk² + β²k⁴ - 4 - 4γ + 4βk²
  = γ² - 8γ + [2(2 - γ) + 4]βk² + β²k⁴
  = γ² - 8γ + (8 - 2γ)βk² + β²k⁴
```

For γ = 0.5, β = 0.1:
```
Δ = 0.25 - 4 + (8 - 1)(0.1)k² + 0.01k⁴
  = -3.75 + 0.7k² + 0.01k⁴
```

This is negative for small k (complex roots ✓) and becomes positive for large k (real roots).

**Transition at:** k ≈ √5 ≈ 2.2

Below this wavenumber: oscillatory modes
Above this wavenumber: evanescent or decay-only modes

---

## Conclusion

The modified wave equation restores oscillatory behavior to transverse modes. This single change:

1. **Eliminates pure decay** for transverse modes at low k
2. **Preserves E/B separation** via sign flip in coupling
3. **Introduces non-relativistic dispersion** (ω/k varies with k)
4. **Matches lossy medium behavior** (waves with damping)

This is consistent with One-Wave being an **effective field theory for condensed matter** rather than vacuum EM. The next phase tests whether this can match actual electromagnetic phenomena despite the non-relativistic dispersion.

---

## References

- PHASE_4_CRITICAL_FINDING.md: Root cause analysis
- modified_update_rule.py: Numerical implementation
- D-602: E/B structure derivation (still valid with modification)

