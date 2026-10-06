# A-115 Galaxy Validation: Derived Source Parameters vs MW Rotation Data

## Executive Summary

**Test Status:** COMPLETE  
**Data Points:** 45 published Milky Way rotation measurements (DR3+ 2023, r=5.25–27.25 kpc)  
**Derived Parameters Tested:** σ_core=0.5, σ_tail=2.0, weight_tail=0.4  
**Physical Model:** Static A-115 compression field (3D radial symmetry)  
**Fitting:** Single free parameter (overall amplitude scale), no parameter fitting  

**Result:** The derived source structure produces systematic disagreement with observed galaxy kinematics.

---

## Validation Procedure

### 1. Derived Source Parameters
Source parameters derived from dimensional amplitude law (A-115 across 2D, 3D, 4D):
- **σ_core = 0.5:** Core power-law scale
- **σ_tail = 2.0:** Exponential tail decay scale
- **weight_tail = 0.4:** Mixing ratio (40% tail, 60% core)
- **Dimension:** 3D
- **Harmonic layer:** 12 (galaxy scale)

These parameters were derived to produce:
- Exterior/Interior acceleration ratio = 0.0391 (from dimensional compensation)
- Universal exterior gravity across dimensions
- Naturally optimal scale for galaxy physics (layer-12)

### 2. Solving Procedure
1. Solve static A-115 equation: $(K_\chi + S_u) \nabla^2 \chi = \nabla \cdot J_r$
2. Extract radial acceleration profile: $a(r) = -\alpha_g \frac{d\chi}{dr}$
3. Convert to circular velocity: $v_c(r) = \sqrt{a(r) \cdot r}$
4. Interpolate to measurement radii (45 points)
5. Fit single amplitude scale parameter
6. Compute error metrics against observed velocities

### 3. Key Technical Discovery
- Initial source form (positive J_r) produced inward acceleration
- Corrected form uses negative source: $J_r = -[(1-w) J_{core} + w J_{tail}]$
- This produces outward acceleration matching galaxy gravity
- The sign indicates the model represents a restoring force from compressed medium

---

## Results

### Best-Fit Parameters
| Parameter | Value |
|-----------|-------|
| Solver amplitude scale | 0.1 (arbitrary units) |
| Fitted velocity scale | 4206 |
| RMS residual | 44.463 km/s |
| Mean absolute error | 38.152 km/s |
| Mean absolute % error | 18.19% |
| χ² (diagnostic) | 18195.4 |

### Error Distribution
The model produces **systematic inward bias**:
- **At r=5.25 kpc:** Predicted v=354, Observed v=227 → Error = -127 km/s (55% too high)
- **At r=10 kpc:** Predicted v=246, Observed v=224 → Error = -22 km/s (10% too high)
- **At r=20 kpc:** Predicted v~210, Observed v~200 → Error = -10 km/s (5% too high)
- **At r=27 kpc:** Predicted v~195, Observed v~176 → Error = -19 km/s (11% too high)

Pattern: Predicted velocity decreases too steeply with radius.

### Physical Interpretation

The derived source structure:
1. ✓ Produces positive outward acceleration (correct direction)
2. ✓ Follows reasonable dimensional scaling
3. ✗ Does NOT match observed galaxy's radial mass distribution
4. ✗ Predicts too much central concentration (high inner velocities)
5. ✗ Falls off too quickly at large radii

**Conclusion:** The amplitude law derivation gives *dimensionally compensated* exterior response ratios but *not* the radial structure needed for galaxies.

---

## Theoretical Interpretation

### What the Derived Parameters Represent
The amplitude law derivation addressed:
- How source amplitude must scale across dimensions to maintain constant exterior gravity
- Why 3D at layer-12 is naturally optimal for galaxy-scale physics
- Dimensional suppression effects (e.g., volume weighting r^(d-1))

**What it did NOT address:**
- How to set the ABSOLUTE SCALE for a galaxy
- What source profile matches observed galactic mass distributions
- Physical calibration (K_χ, α_g, length/time scales)

### Why the Derived Source Doesn't Work
1. **Source concentration is too high centrally**
  - Power-law core r/(σ_core² + r²)^(3/2) peaks at r=0
  - Exponential tail decays with σ_tail=2.0
  - This creates a very compact mass-energy distribution

2. **Real galaxies have extended disks**
  - Bulge + exponential disk profile
  - Significant mass from r=0 to r=30+ kpc
  - Extended dark matter halo

3. **Mismatch is structural, not just scale**
  - No single amplitude scaling can fix 127 km/s errors at inner radii
  - The radial dependence is fundamentally different

---

## Diagnostic Tests

### Source Profile Analysis
```
At canonical harmonic layer (r=12):
  Source value: 1.06e-8 (highly suppressed at galaxy scale)
  Compression: χ ~ 10^-6 (dimensionless)
  Acceleration: a ~ 10^-2 to 10^0 (depending on amplitude scale)
```

### Amplitude Scaling Behavior
- Doubling amplitude → Proportional velocity increase
- RMS error independent of amplitude (systematic mismatch)
- Scale factors 100-4000 needed to reach observed velocities
  - Indicates dimensionless solver outputs don't directly map to physical units
  - Suggests missing physical calibration constants

---

## What's Needed to Bridge the Gap

### Option 1: Refine the Derived Source
The amplitude law derivation assumed a specific source form. To match galaxies:
1. Vary σ_core, σ_tail, weight_tail specifically for galaxies (not generic)
2. Allow radial dependence: source structure that's different from 2D/3D/4D comparison
3. Trade off universal dimensional compensation for galaxy-specific accuracy

### Option 2: Include Physical Calibration
1. Define physical length scale (e.g., disk scale radius ~3 kpc for MW)
2. Specify K_χ (compression stiffness) from observations
3. Determine α_g (gravity coupling) from galaxy dynamics
4. Map dimensionless solver output → physical units consistently

### Option 3: Investigate Model Assumptions
1. Is static A-115 the right model for galaxy disks?
   - MW is thin disk (~0.3 kpc thick) → 2D, not 3D
   - 3D model may over-estimate central concentration

2. Is the parent-held wake paradigm correct for galaxies?
   - Alternative: evolving waves, time-dependent structure
   - Dark matter as separate system vs. unified field

3. Are there additional physics at galaxy scale?
   - Rotational inertia / angular momentum
   - Feedback from star formation
   - Magnetic fields (referenced in A-115 but not solved here)

---

## Data Quality & References

| Item | Source |
|------|--------|
| Galaxy data | Milky Way DR3+ 2023 rotation curve |
| Data points | 45 published measurements |
| Radius range | 5.25–27.25 kpc |
| Velocity range | 174–231 km/s |
| Mean velocity | 210.5 ± 16.5 km/s |

**References:**
- Sofue et al. (1999): MW rotation curve, ApJ 523, 136
- Battaglia et al. (2005): MW kinematics, MNRAS 364, 433
- DR3+ dataset: Combined HI + stellar kinematics

---

## Conclusion

The derived source parameters (σ_core=0.5, σ_tail=2.0, weight_tail=0.4) are structurally sound for dimensional analysis but do not match observed galaxies without additional refinement.

**Key Findings:**
1. ✓ Amplitude law derivation is correct for dimensional scaling
2. ✗ Derived parameters create too-concentrated central mass profile
3. ✗ Systematic 18–55% velocity overprediction at inner radii
4. ? Model may need galaxy-specific variants or physical calibration
5. ? Alternative models (2D, time-dependent, or feedback) might work better

**Next Steps:**
- [ ] Test 2D variant (galaxy disk approximation)
- [ ] Derive galaxy-specific source parameters via data fitting (exploratory)
- [ ] Establish physical unit system for A-115
- [ ] Compare with competing dark matter models (MOND, CDM, etc.)
- [ ] Investigate time-dependent wake structure
