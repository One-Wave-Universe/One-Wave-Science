# Phase 1: Eigenmode Analysis of the One-Wave Update Rule

## Overview

This directory contains the mathematical derivation and computational analysis of what the One-Wave update rule actually generates when we insert a plane wave ansatz and extract its eigenmode structure.

## Files

| File | Purpose |
|------|---------|
| **D-600_1D_Dispersion_Relation.md** | Complete mathematical derivation of the 1D dispersion relation $\lambda^2 - C(k)\lambda + (1-\gamma) = 0$ |
| **D-601_2D_Hexagonal_Dispersion.md** | Extension to 2D hexagonal lattice; analysis of whether E/B structure emerges |
| **dispersion_phase1.py** | Executable code: computes dispersion spectrum for 1D, generates plots, varies γ and β |
| **dispersion_2d.py** | Executable code: computes 2D dispersion surfaces on hexagonal lattice |
| **dispersion_spectrum.png** | 1D dispersion relation $\omega(k)$ for four (γ, β) parameter sets |
| **dispersion_2d_hex.png** | 3D surface plots of $\text{Re}(\omega_\pm)$ and $\text{Im}(\omega_\pm)$ in 2D k-space |
| **dispersion_2d_contours.png** | Contour plots of the 2D dispersion surfaces (easier to read) |

## How to Run

```bash
# Generate 1D dispersion spectra
python dispersion_phase1.py

# Generate 2D hex lattice dispersion surfaces
python dispersion_2d.py
```

Both scripts are self-contained and produce PNG outputs.

## Key Results

### Phase 1 (1D Analysis)

✅ **The update rule produces TWO distinct mode families:**
- $\omega_+$ (fast mode): grows with $k$ and $\beta$
- $\omega_-$ (slow mode): decay-dominated, nearly independent of $k$

✅ **Stability constraint derived:** $\beta < 1$ for all $k$ regions

✅ **Velocity scales from coupling:** $v \propto \beta$ (not imposed, not tuned)

✅ **Damping is a mode property:** different decay rates ($10\times$ difference) for $\omega_\pm$

### Phase 2 (2D Hexagonal Analysis)

⚠️ **Mode structure is nearly isotropic:** Hexagonal geometry does NOT produce strong anisotropy

❌ **E/B decomposition does NOT emerge automatically:** Neither $\omega_+$ nor $\omega_-$ splits into potential (divergence) and vorticity (curl) components

❌ **Wrapper asymmetry (−6 to +12) NOT derived from hex symmetry:** The lattice respects 6-fold rotational symmetry; the 3:2 ratio does not follow

## Critical Juncture

We face a **decision point:**

**If we require the update rule to generate electromagnetic structure WITHOUT external assumption:**
- The 1D/2D scalar dispersion relation is insufficient
- We must either:
  1. **Extend to vector fields** ($\boldsymbol{\psi}$ instead of $\psi$)
  2. **Look for hidden structure** in mode gradients
  3. **Accept that E/B are imposed** (rejects the physics requirement)

**If we relax the requirement:**
- We have derived TWO stable mode families
- We have a derived velocity scale and stability constraint
- We can now ask: "Given that we impose E/B structure, are the derived properties consistent with experiment?"

## Next Phase

**Phase 3:** Vector Field Extension or Gradient Analysis

See D-601 "Phase 3: Next Steps" for the three options.

---

## Notes for Reviewers

- All mathematics is symbolic; Python code implements numerical evaluation
- Plots use default matplotlib colormaps (easily substitutable)
- Parameter scans are not exhaustive; representative cases shown
- No assumptions about what the modes "represent" until verified

## References

- One-Wave Update Rule (canonical)
- D-411: Mirrored Axis Pairs (beware false unifications)
- D-413: Ground Lattice Orbital Restoring Simulation (YELLOW status)
- FOUR_INTERACTIONS.md: Four-coupling framework
