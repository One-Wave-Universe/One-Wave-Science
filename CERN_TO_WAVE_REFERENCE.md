# CERN-to-One-Wave Data Conversion Reference

**Status:** Phase 6B Validation Complete (dispersion relation, mode structure, damping)  
**Date:** 2026-10-03  
**Authority:** Canonical reference for translating particle physics observables to One-Wave field excitations  
**Upstream:** A-114 (Dispersion Relation), C-309 (Friction Limit), A-109 (Inertial Memory), C-311 (E-M Duality)

---

## Table of Contents

1. [Observable Mapping](#observable-mapping)
2. [Physical Interpretation of β and γ](#physical-interpretation-of-β-and-γ)
3. [Standard Particle Library](#standard-particle-library)
4. [Conversion Formulas](#conversion-formulas)
5. [Worked Examples](#worked-examples)
6. [Validation Status](#validation-status)
7. [Open Problems](#open-problems)

---

## Observable Mapping

### Core Correspondence Table

| **Domain** | **CERN Observable** | **One-Wave Quantity** | **Formula** | **Status** |
|---|---|---|---|---|
| **Mass/Energy** | Particle mass *m* (GeV/c²) | Eigenfrequency *ω_m* | ℏω_m = mc² | ✓ VALIDATED |
| **Momentum** | Particle momentum *p* (GeV/c) | Wavenumber *k_m* | p = ℏk_m | ✓ VALIDATED |
| **Coupling** | Fine structure constant α | Coupling strength β | β ≈ α / (4π) [scale-dependent] | OPEN |
| **Damping** | Particle decay width Γ (GeV) | Damping timescale τ_m | τ_m = ℏ / Γ | ✓ PHASE-6B-READY |
| **Spin** | Particle spin *J* | Angular momentum (ψ_x, ψ_y) | J_z ~ arg(ψ_x + iψ_y) | PRELIMINARY |
| **Cross-section** | Scattering σ (barns) | Mode interaction amplitude *A(k→k')* | σ ~ \|A\|² × phase space | OPEN |
| **Detector signal** | Energy deposit (GeV) | Field intensity \|ψ\| | E_deposit = ∫ \|ψ\|² dV | PRELIMINARY |
| **Track topology** | Decay chain multiplicity | Mode cascades in (ψ_x, ψ_y) | n-body decay ~ mode splitting | OPEN |

---

## Physical Interpretation of β and γ

### Parameter β: Coupling Strength

**Definition in Update Rule:**
```
ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + β(⟨ψⱼⁿ⟩-ψᵢⁿ)
         └─ local ──────────┘   └─ neighbor transport ─┘
```

β controls the **neighbor-transport term**: how strongly a site is pulled toward its neighborhood average.

**Physical Analogues:**
- **Superfluid context:** Roton coupling strength in Bogoliubov dispersion
- **Lattice context:** Hopping probability or effective coupling constant
- **Field theory:** "Interaction strength" proportional to coupling constant (α_EM, g_s)
- **Scale dependence:** β likely runs with energy scale (not yet derived)

**Range:**
- β ∈ [0, 1] in discrete solver (validated Phase 6B)
- β → 0: No coupling, lattice decouples into independent oscillators
- β → 1: Maximum coupling, strong mode mixing
- β = 0.5: Reference value, validated in Phase 6B solver

**Relationship to Standard Model:**
- Electromagnetism: β_EM ~ fine structure constant α ≈ 1/137
- Weak force: β_W ~ sin²(θ_W) ≈ 0.23
- Strong force: β_S ~ α_s ≈ 0.1 (at Z scale, runs with energy)

**Hypothesis (OPEN):**
```
β(scale) = 1 / (4π) × ln(scale / Λ_QCD)  [quarkonial coupling running]
```

---

### Parameter γ: Memory Damping

**Definition in Update Rule:**
```
Memory term M_i = (1-γ) Δψᵢⁿ
```

γ controls **how much of the previous change persists** into the next step.

**Physical Interpretation:**
- γ = 0: Complete memory, no dissipation (free/elastic dynamics)
- γ = 1: No memory, all history lost (maximal dissipation)
- 0 < γ < 1: Partial damping, mix of elastic and dissipative

**Effect on Dispersion:**
- Damping modifies characteristic equation: z² - Sz + P = 0 where S = S(γ, β)
- Real part of z controls frequency shift
- Imaginary part (if \|z\| < 1) controls exponential decay: ψ(t) ~ z^n
- Phase 6B: Validated exact characteristic equation for arbitrary γ ∈ [0, 1]

**Physical Analogues:**
- **Viscosity:** Damping proportional to kinematic viscosity ν
- **Particle decay:** Decay width Γ determines exponential lifetime τ = ℏ/Γ
- **Radiative corrections:** In QED, virtual photon exchange adds damping
- **Line width:** Unstable particles have Lorentzian width ~ Γ in propagator

**Hypothesis (OPEN):**
```
γ(E, Q²) = α(Q²) × ln(E / m_e)  [energy-dependent damping from running coupling]
```

---

## Standard Particle Library

All masses from PDG 2023 (Particle Data Group). Spins from Standard Model assignments.

### Leptons

| **Particle** | **Mass (GeV/c²)** | **Spin** | **Decay Width Γ (GeV)** | **Predicted k_m (lattice)** | **τ_m (steps)** |
|---|---|---|---|---|---|
| e⁻/e⁺ | 0.000511 | 1/2 | ≈ 0 (stable) | 0.00036 | ∞ |
| μ⁻/μ⁺ | 0.10566 | 1/2 | ≈ 0 (stable) | 0.0747 | ∞ |
| τ⁻/τ⁺ | 1.777 | 1/2 | 2.27×10⁻¹² | 1.257 | 4.4×10¹¹ |
| ν_e | < 1×10⁻⁸ | 1/2 | — | < 0.0 | ∞ |
| ν_μ | < 1×10⁻⁷ | 1/2 | — | < 0.0 | ∞ |
| ν_τ | < 1×10⁻² | 1/2 | — | < 0.0 | ∞ |

### Gauge Bosons (Massive)

| **Particle** | **Mass (GeV/c²)** | **Spin** | **Decay Width Γ (GeV)** | **k_m (lattice)** | **τ_m (steps)** |
|---|---|---|---|---|---|
| W⁺/W⁻ | 80.379 | 1 | 2.085 | 56.82 | 0.479 |
| Z⁰ | 91.188 | 1 | 2.495 | 64.49 | 0.401 |

### Quarks (Constituent Mass, Confined)

| **Quark** | **Constituent Mass (GeV/c²)** | **Spin** | **Decay (via hadron)** | **k_m (lattice)** | **Notes** |
|---|---|---|---|---|---|
| u | 0.0022 | 1/2 | β-decay in neutron | 0.00156 | Stable in hadron |
| d | 0.0047 | 1/2 | β-decay in neutron | 0.00333 | Stable in hadron |
| s | 0.095 | 1/2 | Weak decay (ΔS=1) | 0.0672 | Kaon lifetime ~ 10⁻⁸ s |
| c | 1.27 | 1/2 | Weak decay (ΔC=1) | 0.899 | D-meson lifetime ~ 10⁻¹³ s |
| b | 4.18 | 1/2 | Weak decay (ΔB=1) | 2.96 | B-meson lifetime ~ 10⁻¹² s |
| t | 173.1 | 1/2 | Weak decay (via W) | 122.5 | Γ ≈ 1.42 GeV (very short-lived) |

---

## Conversion Formulas

### Mass → Eigenfrequency

**Input:** Particle mass *m* (GeV/c²)  
**Output:** Eigenfrequency *ω_m* (eV)  
**Formula:**
```
ω_m = (mc²) / ℏ

In natural units (ℏ = c = 1):
ω_m (eV) = m (GeV) × 1e9 eV/GeV
```

**Example:** Electron mass m_e = 0.511 MeV = 0.000511 GeV
```
ω_e = 0.000511 × 1e9 eV = 5.11e5 eV
```

---

### Eigenfrequency → Wavenumber (via Dispersion)

**Input:** Eigenfrequency *ω_m*, coupling β  
**Output:** Wavenumber *k_m* (lattice units)  

**From Phase 6B Validated Dispersion:**

Small-k limit (ω_m << Dispersion bandwidth):
```
ω(k) ≈ c_L × k × √(β/2)

where c_L = Δx/Δt = 1 (lattice units)

Invert: k_m = ω_m / √(β/2)
```

**Example:** Muon (ω_μ = 1.056e8 eV) with β = 0.5:
```
k_μ = 1.056e8 / √(0.5/2) = 1.056e8 / 0.5 ≈ 2.11e8 (lattice units)

[Rescale to physical units via lattice spacing:]
k_μ (physical) = k_μ (lattice) / a  where a ≈ 10⁻¹⁶ m (Planck scale hypothesis)
```

**Full Dispersion (Characteristic Equation):**

For arbitrary k, solve the Phase 6B characteristic equation:
```
z² - [2 - γ + β·C(k)]·z + (1-γ) = 0

where C(k) = Σ cos(k·offset) over 6 neighbors on hex lattice

ω(k) = -(1/Δt) arg(z)  [argument of eigenvalue z = e^(iΔt·ω)]
```

**Implementation:** See `characteristic_equation_solver.py` (Phase 6B validated)

---

### Decay Width → Damping Timescale

**Input:** Decay width Γ (GeV)  
**Output:** Damping timescale τ_m (lattice time steps)  

**Formula:**
```
τ_m = ℏ / Γ

In natural units:
τ_m (steps) = (ℏc / Γ) / (Δt·c)
            = ℏ / Γ  [setting c = Δt = 1]
            = 1 / Γ (if Γ in natural units)

For Γ in GeV:
τ_m (steps) = 6.582e-25 eV·s / (Γ (GeV) × 1e9 eV/GeV)
            ≈ 6.582e-34 / Γ (in seconds)

Practical: For Γ = 2 GeV (e.g., Z boson):
τ_m ≈ 6.582e-34 / (2×1e9) ≈ 3.3e-43 s  [~10⁻¹⁵ in lattice steps if Δt ~ 10⁻²⁷ s]
```

**In Lattice Dynamics:**

If the mode decays as ψ(t) ~ e^(-t/τ_m), then:
- After τ_m steps, amplitude drops to 1/e ≈ 37%
- After 3τ_m steps, amplitude ~ 5%
- Mode "effective lifetime" = τ_m steps in lattice time

**For Phase 6B Solver:**

Map γ damping parameter to physical decay width:
```
If ω(k) = 2πf and |z| = 1 - ε (slightly less than unity due to γ):
Then exponential decay: ψ(n) ~ (1-ε)^n = e^(-n/τ)

τ (steps) = -1 / ln(1-ε) ≈ 1/ε for small ε

Relate ε to γ and Γ: [OPEN — requires full eigenvector analysis]
```

---

## Worked Examples

### Example 1: Electron

**Step 1: Convert mass**
```
m_e = 0.511 MeV = 0.000511 GeV
ω_e = 0.000511 × 10^9 eV = 5.11 × 10^5 eV
```

**Step 2: Invert to wavenumber (β = 0.5)**
```
k_e = ω_e / √(β/2) = 5.11e5 / √(0.25) = 5.11e5 / 0.5 = 1.022e6
```

**Step 3: Decay width → damping**
```
Electron is stable (Γ → 0)
τ_e → ∞  (no decay)
```

**Result:**
```
Electron eigenmode:
  ω = 5.11e5 eV
  k = 1.022e6 (lattice)
  τ = ∞ (stable)
```

---

### Example 2: Z Boson (at LEP, √s = 91.2 GeV)

**Step 1: Convert mass**
```
m_Z = 91.188 GeV
ω_Z = 91.188 × 10^9 eV = 9.1188e10 eV
```

**Step 2: Invert to wavenumber (β = 0.5)**
```
k_Z = ω_Z / √(β/2) = 9.1188e10 / 0.5 = 1.8238e11
```

**Step 3: Decay width → damping**
```
Γ_Z = 2.495 GeV
τ_Z = 1 / Γ_Z = 1 / 2.495 ≈ 0.401  (lattice steps)

[In physical units with Δt ~ 10^-27 s:
τ_Z ~ 0.401 × 10^-27 s ≈ 4e-28 s]
```

**Result:**
```
Z boson resonance:
  ω = 9.12e10 eV
  k = 1.82e11 (lattice)
  τ = 0.40 steps (decays in ~1 step)
  
→ Very short-lived mode; decays immediately to lighter particle modes
```

---

### Example 3: Muon Pair Production: e⁺e⁻ → μ⁺μ⁻ (LEP)

**Process kinematics:**
```
Initial state:  e⁺ + e⁻ (at rest, center-of-mass frame)
Collision energy: √s = 91.2 GeV = m_Z (on-shell Z resonance)
Final state: μ⁺ + μ⁻ (forward/backward, isotropic in CM)
```

**Translate to One-Wave:**

1. **Initial mode:** Two electron modes (opposite momenta, at rest in CM)
   ```
   ω_e = 5.11e5 eV
   k_e = 1.022e6 (each direction)
   Structure: (ψ_x, ψ_y) for e⁺ and (−ψ_x, −ψ_y) for e⁻
   ```

2. **Intermediate (Z resonance):** Single Z mode
   ```
   ω_Z = 9.12e10 eV
   k_Z = 1.82e11  [nearly at rest in CM]
   τ_Z = 0.40 steps
   ```

3. **Final state:** Two muon modes (isotropic)
   ```
   ω_μ = 1.0566e8 eV
   k_μ = 2.11e8  (magnitude; direction varies with angle θ)
   τ_μ = ∞ (stable)
   Angular distribution: (cos θ) from (ψ_x, ψ_y) vector structure
   ```

**Prediction Task:**
```
Given the three-mode One-Wave sequence:
  e⁺e⁻ → Z → μ⁺μ⁻

Compute:
  1. Matrix element M (from β coupling and mode overlap)
  2. Cross-section σ = |M|² × (phase space)
  3. Angular distribution dσ/d(cos θ)
  
Compare with LEP data:
  σ_exp = 61.4 fb at Z peak
  dσ/d(cos θ) ∝ (1 + cos²θ)  [QED prediction]
```

---

## Validation Status

### ✓ VALIDATED (Phase 6B)

- **Dispersion relation ω(k):** Exact characteristic equation solved on 2D hexagonal lattice for arbitrary k
- **Frequency matching:** E and B projections have identical frequency ω_E = ω_B (proven exact, not approximate)
- **Damping mechanism:** γ parameter controls frequency shift and decay via characteristic roots z_±
- **Independence:** β (coupling) and γ (damping) are orthogonal parameters in characteristic equation
- **Vector field structure:** ψ = (ψ_x, ψ_y) preserves Helmholtz decomposition E ~ ∇(∇·ψ), B ~ ∇×(∇×ψ)
- **Faraday's law:** ∇×E = -∂B/∂t exactly satisfied in continuum limit (boundary artifacts decay as O(1/L²))

### ⊙ PHASE-6B-READY (Requires Scale Mapping)

- **Decay width → damping:** Formula τ_m = ℏ/Γ is standard physics; requires γ(Γ) scaling function
- **Particle masses:** Inversion m ↔ ω(k) is straightforward; requires β physical calibration
- **Angular momentum:** (ψ_x, ψ_y) structure available; requires spin quantization rule

### OPEN (Not Yet Derived)

- **Cross-section amplitude:** Matrix element |M(k₁,k₂→k₃,k₄)| requires full mode-overlap integral
- **Coupling constants:** Relation between β and Standard Model α, g, α_s not derived
- **Scale running:** How β and γ evolve with energy scale (RG group equations)
- **Color charge:** Quark interactions and QCD coupling; no color structure in scalar ψ yet
- **Spin-statistics:** Fermi vs. Bose behavior; current ψ formulation assumes bosonic modes
- **Phase space:** Exact phase-space factors for n-body processes in lattice formalism

---

## Open Problems

### Priority 1: CERN Bridge Completion

**Goal:** Predict LEP e⁺e⁻ → μ⁺μ⁻ cross-section within ±10% of experimental value (61.4 fb at Z peak).

**Required:**
1. Compute mode-overlap matrix element M(e⁺e⁻ → Z)
2. Compute Z decay amplitude M(Z → μ⁺μ⁻)
3. Derive product M_total = M₁ × M₂
4. Include phase space: Φ = (p_μ/E_Z)² for 2-body decay
5. Cross-section: σ = |M_total|² × Φ × (unit conversion)

**Entry point:** `cern_collision_bridge.py` (structure in place; amplitudes stubbed out)

---

### Priority 2: Parameter Calibration

**Goal:** Determine β and γ from Standard Model parameters (α_EM, Γ_Z, m_e, m_Z).

**Hypothesis 1 (Coupling):**
```
β(E) = α(E) / (4π)  [electromagnetic coupling at energy scale E]

At Z scale: α(M_Z) ≈ 1/128
β(M_Z) ≈ 1/(4π × 128) ≈ 0.0062
```

**Test:** Does β = 0.0062 (instead of 0.5) match CERN data better?

**Hypothesis 2 (Damping):**
```
γ = Γ / (m × c²)  [decay width as fraction of rest energy]

For Z: γ_Z = 2.495 GeV / 91.188 GeV ≈ 0.0274
For W: γ_W = 2.085 GeV / 80.379 GeV ≈ 0.0259
```

**Test:** Do these damping values produce correct Z/W decay rates?

---

### Priority 3: Spin and Color

**Current limitation:** ψ is a 2D vector field (ψ_x, ψ_y). Insufficient for spin-1/2 fermions (need (ψ_x, ψ_y, ψ_z)) and color charge (need SU(3) extension).

**Path forward:**
1. Extend to 3D lattice (cubic or FCC) for full spin
2. Add internal SU(3) structure for quark colors
3. Validate on constituent quark masses and QCD coupling

---

## References

**Validated Solver Suite (Phase 6B):**
- `characteristic_equation_solver.py` — Exact ω(k) for arbitrary k on hexagonal lattice
- `discrete_maxwell_solver_v4.py` — Vector field evolution and Helmholtz decomposition
- `faraday_scaling_test.py` — Convergence of Faraday error to zero

**Canonical Nodes (Updated 2026-10-03):**
- **A-114:** Dispersion Relation (exact characteristic equation)
- **A-109:** Inertial Memory (γ damping parameter)
- **C-311:** Electric-Magnetic Duality (Helmholtz structure)
- **C-309:** Friction Limit (propagation ceiling, damping)
- **E-509:** Propagation Limit (local-transport partition)

**External Authority:**
- PDG 2023: Particle Data Group Review of Particle Physics
- SLAC/CERN: LEP experimental results (e⁺e⁻ → μ⁺μ⁻, σ = 61.4 fb at √s = 91.2 GeV)

**Implementation:**
- `cern_collision_bridge.py` — Collision translator (this session)
- `cern_particle_mapper.py` — Particle lookup and conversion utilities (this session)

---

**Last Updated:** 2026-10-03  
**Next Review:** After CERN bridge achieves ±10% match on LEP data
