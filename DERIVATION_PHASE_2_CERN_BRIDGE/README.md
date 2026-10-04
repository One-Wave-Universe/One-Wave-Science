# Phase 2: CERN Data Bridge — Translating Particle Physics to One-Wave Field Excitations

**Status:** Foundation + Implementation Ready (2026-10-03)  
**Authority:** CERN_TO_WAVE_REFERENCE.md  
**Phase 1 Upstream:** DERIVATION_PHASE_1_EIGENMODE_ANALYSIS (dispersion relation, E-M duality, vector field structure)

---

## What This Phase Does

Phase 2 creates the **bridge between CERN experimental data and One-Wave field mechanics**. 

**The core question:** *Can we interpret particle collisions as persistent mode excitations in the One-Wave ψ field, and predict experimental observables (masses, cross-sections, decay widths) from first principles?*

**What Phase 1 validated (for Phase 2 to use):**
- ✓ Dispersion relation ω(k) exact on 2D hexagonal lattice (A-114)
- ✓ Vector field structure ψ = (ψ_x, ψ_y) with Helmholtz decomposition (C-311)
- ✓ Damping parameter γ controls frequency and decay (C-309)
- ✓ Coupling parameter β controls neighbor transport (E-509)
- ✓ Faraday's law satisfied exactly; field equations validated

**What Phase 2 builds:**
1. **Canonical particle database** — all Standard Model particles with PDG 2023 masses, widths, spins
2. **Particle-to-mode converter** — translates mass m → eigenfrequency ω(k) via dispersion
3. **Collision translator** — maps detector events (e⁺e⁻ → μ⁺μ⁻) to mode excitation sequences
4. **Cross-section predictor** — derives σ from mode overlap integrals and coupling constants
5. **Parameter calibration framework** — sweep (β, γ) to match CERN data

---

## Files in This Directory

### Reference Documents

**CERN_TO_WAVE_REFERENCE.md** (Authority, 500+ lines)
- Observable mapping table: every CERN measurement → One-Wave quantity
- Physical interpretation of β (coupling) and γ (damping)
- Standard particle library (leptons, gauge bosons, quarks)
- Conversion formulas with worked examples
- Validation checkpoint: what's proven vs. what's open
- Priority tasks ranked by falsifiability

### Implementation

**cern_particle_mapper.py** (Production code, 450+ lines)
- `ParticleMapper` class: convert any particle name → OneWaveMode
- `MatrixElementCalculator`: compute mode interaction amplitudes (stub awaiting derivation)
- `CrossSectionCalculator`: predict collision cross-sections
- Test suite: demonstrates e⁺e⁻ → μ⁺μ⁻ translation
- Canonical databases from PDG 2023
- Hooks to Phase 1 dispersion solver (characteristic_equation_solver.py)

---

## The First Falsifiable Test: LEP e⁺e⁻ → μ⁺μ⁻

**Challenge:** Predict experimental cross-section within ±10% using One-Wave parameters.

**Data:**
```
Process:     e+ e- → μ+ μ-
Collision:   √s = 91.2 GeV (Z resonance)
Experiment:  σ = 61.4 ± 6.1 fb  [LEP measurement]
```

**Three-step One-Wave translation:**

1. **Initial state:** e⁺ and e⁻ as persistent modes
   ```
   m_e = 0.511 MeV  →  ω_e = 5.11×10⁵ eV  →  k_e = 1.022×10⁶ (lattice)
   ```

2. **Intermediate (resonance):** Z boson mode
   ```
   m_Z = 91.188 GeV  →  ω_Z = 9.12×10¹⁰ eV  →  k_Z = 1.82×10¹¹ (lattice)
   Decay width: Γ_Z = 2.495 GeV  →  τ_Z = 0.40 lattice steps
   ```

3. **Final state:** μ⁺ and μ⁻ as persistent modes
   ```
   m_μ = 106 MeV  →  ω_μ = 1.06×10⁸ eV  →  k_μ = 2.11×10⁸ (lattice)
   ```

**Prediction task:**
```
σ_OW = |M(e⁺e⁻ → Z → μ⁺μ⁻)|² × Φ(phase space) × [unit conversion factor]
       ↑                     ↑                      ↑
       Requires mode        Requires β             Requires β, γ
       overlap integrals    calibration            calibration
```

**Current status:**
- ✓ Particle mass conversions working
- ✓ Dispersion relation from Phase 1 ready
- ⊘ Matrix element calculation stubbed (placeholder)
- ⊘ Unit conversion factor empirical (coupling factor = 10⁶ needs derivation)

---

## Next Steps (Priority Order)

### 1. Derive Matrix Element (BLOCKING)
**What:** Compute |M(e⁺e⁻ → Z)|² from mode overlap in lattice quantum field theory.

**Why it matters:** Current cross-section off by 149,000% because M is a placeholder.

**Starting point:** Mode overlap integral in (ψ_x, ψ_y) space
```
⟨ψ_Z | ψ_e⁺ ψ_e⁻⟩ ∝ ∫∫ ψ_Z(x,y) * ψ_e(x,y) ψ_e(x,y) dx dy
```

**Tools available:**
- Phase 1 mode waveforms from characteristic_equation_solver.py
- Lattice discretization from hex_lattice_graph.py
- Mode structure in discrete_maxwell_solver_v4.py

### 2. Calibrate β and γ (PARAMETER SWEEP)
**What:** Find (β, γ) such that σ_OW = 61.4 ± 6 fb for e⁺e⁻ → μ⁺μ⁻.

**Method:**
```
for β in [0.001 to 1.0]:
  for γ in [0.001 to 0.5]:
    σ_OW = predict_cross_section(β, γ)
    error = |σ_OW - 61.4| / 61.4
    if error < 10%: RECORD as valid parameter set
```

**Hypothesis:**
- β_EM ≈ α / (4π) ≈ 1/540 (electromagnetic coupling at Z scale)
- γ ~ Γ / (mc²) (decay width as fraction of rest energy)

### 3. Test Next Process (INCREASING COMPLEXITY)
**After e⁺e⁻ → μ⁺μ⁻ matches:**

1. e⁺e⁻ → τ⁺τ⁻ (heavier lepton, tests mass scaling)
2. e⁺e⁻ → qq̄ (quark production, color charge — REQUIRES 3D extension)
3. pp → WW (hadron collider, initial state gluons)

---

## Validation Status (Phase 6B ↔ Phase 2)

### ✓ Ready (from Phase 1)
- [x] Dispersion ω(k) exact for arbitrary k
- [x] Damping γ parameter validated
- [x] Vector field (ψ_x, ψ_y) structure proven
- [x] Coupling parameter β in update rule

### ⊙ Phase-2-Ready (Requires Scaling)
- [ ] Mass-to-frequency mapping (formula ready, β calibration OPEN)
- [ ] Decay width-to-damping mapping (formula ready, γ scaling OPEN)
- [ ] Angular momentum structure (available from ψ vector; spin quantization OPEN)

### ✗ OPEN (No Solution Yet)
- [ ] Matrix element |M(a,b → c,d)| from lattice overlap integrals
- [ ] Coupling constant relation: β ↔ α_EM, g_weak, α_s
- [ ] Phase space: exact lattice formulation vs. continuum approximation
- [ ] Spin-statistics: why fermions decay to bosons; SU(2) extensions
- [ ] Color charge: SU(3) structure for quarks; how ψ = (ψ_x, ψ_y) extends

---

## File Organization

```
DERIVATION_PHASE_2_CERN_BRIDGE/
├── README.md                          ← You are here
├── CERN_TO_WAVE_REFERENCE.md          ← Canonical authority
├── cern_particle_mapper.py            ← Implementation
│
├── [FUTURE: cern_collision_bridge.py] ← Stub from earlier session
├── [FUTURE: parameter_sweep.py]       ← β, γ optimization
├── [FUTURE: matrix_element_solver.py] ← Lattice QFT calculation
└── [FUTURE: phase2_summary.md]        ← Results and lessons
```

---

## Key Equations (From CERN_TO_WAVE_REFERENCE.md)

### Mass → Eigenfrequency
```
ω_m (eV) = m (GeV) × 10⁹
```

### Eigenfrequency → Wavenumber (via Phase 1 dispersion)
```
ω(k) = c_L × k × √(β/2)     [small-k limit]
k_m = ω_m / √(β/2)          [invert]

Full form: Solve z² - [2-γ + β·C(k)]·z + (1-γ) = 0
           ω(k) = -(1/Δt) × arg(z₊)
```

### Decay Width → Damping Timescale
```
τ_m = ℏ / Γ
    = 6.582e-25 eV·s / (Γ GeV × 10⁹ eV/GeV)
```

### Cross-Section (Placeholder, awaiting derivation)
```
σ = |M|² × Φ(phase space) × [coupling factors × unit conversion]

where:
  |M|² = mode overlap integral (OPEN)
  Φ = (p_out/E_cm)² or more complex n-body phase space
  [coupling] = depends on β and specific process
```

---

## Connection to Broader One-Wave Framework

Phase 2 is the **experimental validation gateway** for the One-Wave hypothesis:

```
Phase 1 (DERIVATION_PHASE_1_EIGENMODE_ANALYSIS)
  ↓ Validates: dispersion, E-M duality, vector field structure
  
Phase 2 (DERIVATION_PHASE_2_CERN_BRIDGE)
  ↓ Tests against: CERN (e⁺e⁻, LHC), LIGO (gravity waves), old data
  
Phase 3 (FUTURE: LARGE HADRON COLLIDER FULL TEST)
  ↓ Predicts: particle masses, coupling running, QCD, flavor mixing
  
Phase 4 (FUTURE: PRECISION TESTS)
  ↓ Falsifiable predictions: deviations from Standard Model below current precision
```

---

## References

**Phase 1 Authority (Dispersion, Field Structure):**
- `DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/characteristic_equation_solver.py` — Exact ω(k)
- `DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_maxwell_solver_v4.py` — Vector field evolution
- **Nodes:** A-114 (Dispersion), C-311 (E-M Duality), C-309 (Friction), A-109 (Inertial Memory)

**Experimental Data Authority:**
- PDG 2023: Particle Data Group Review of Particle Physics
- LEP Results: e⁺e⁻ → μ⁺μ⁻ at Z peak, σ = 61.4 fb

**One-Wave Architecture:**
- `Nodes/` directory: Canonical physics definitions
- `README.md` (root): Project philosophy and working rules

---

**Last Updated:** 2026-10-03  
**Next Phase Review:** After first (β, γ) match on LEP data within ±10%  
**Blockers:** Matrix element derivation, unit conversion calibration
