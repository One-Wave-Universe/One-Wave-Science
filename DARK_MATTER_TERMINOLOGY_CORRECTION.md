# Dark Matter Terminology Correction Directive

**Effective Immediately Across All Repos and Nodes**

## Core Physics Correction

**Old interpretation:** Dark matter is a separate exotic particle species (~85% of universe's matter).

**Correct interpretation:** 
- Dark matter observations are manifestations of **displaced superfluid energy**
- What we measure as "dark matter" is the superfluid's pressure response to mass concentrations
- It is NOT a separate particle—it is the field itself in a displaced state
- The superfluid can be compressed (high pressure → apparent dark matter) or rarefied (low pressure → apparent dark energy)

## Terminology Mapping (Systematic Replacement)

### Core Terms

| Old Terminology | New Terminology | Physical Meaning |
|---|---|---|
| dark matter | displaced superfluid energy | Compression of the superfluid field around masses |
| dark matter halo | extended displaced energy region | The superfluid's extended response to galaxy mass |
| dark matter particle | (remove entirely) | No such thing; only field configurations |
| dark energy | superfluid expansion / superfluid rarefaction | Low-pressure regions where field expands |
| dark energy acceleration | superfluid expansion effect | The field's tendency to flow from high→low pressure |

### Descriptive Phrases

| Old | New | Context |
|---|---|---|
| "dark matter explained by..." | "displaced superfluid energy arises from..." | When explaining observations |
| "dark matter halo surrounds..." | "extended displaced energy surrounds..." | Spatial distribution |
| "dark matter makes up..." | "displaced superfluid energy comprises..." | Mass/energy budget |
| "missing dark matter" | "unexpected superfluid displacement" | When observations diverge from predictions |

### Code/Variable Names

| Old | New |
|---|---|
| `dark_matter_signature` | `superfluid_displacement_signature` |
| `dark_matter_view` | `displaced_superfluid_energy_view` |
| `dark_energy_magnitude` | `superfluid_expansion_magnitude` |
| `dm2_*` (neutrino mass-squared) | Keep as-is; this is standard physics notation |

## Files Requiring Comprehensive Fix

### Critical Documentation (Highest Priority)
- [ ] DARK_MATTER_COMPLETE_NODE_CHAPTER_REFERENCE.md
- [ ] Books/Book5_Macro/Book5_Ch1_Galaxies_and_Dark_Matter.md
- [ ] PHASE_2_COMPREHENSIVE_VALIDATION_REPORT.md
- [ ] GRAVITY_WAKE_NESTING_ROTATION_CASCADE.md
- [ ] README.md

### Node Documentation
- [ ] Nodes/A-115_Unified_Compression_Field.md
- [ ] Nodes/C-323_Four_Forces_as_Displacement_Regimes.md
- [ ] Nodes/D-415_Hexagonal_Lattice_Interaction_Dynamics/README.md

### Solver Files (Python)
- [ ] solvers/galaxy_rotation_cascade_wake_validator.py ✓ (DONE)
- [ ] solvers/galaxy_rotation_validator.py
- [ ] solvers/galaxy_rotation_inherited_rotation_field.py
- [ ] solvers/galaxy_rotation_constant_inherited_velocity.py
- [ ] solvers/algorithm_zero_emergence.py
- [ ] solvers/algorithm_zero_galaxy_validation_comprehensive.py
- [ ] solvers/unified_phase_solver.py ✓ (DONE)
- [ ] solvers/standard_model_mysteries_unified.py ✓ (DONE)
- [ ] solvers/neutrino_mass_solver.py
- [ ] solvers/three_body_solver.py
- [ ] solvers/w2_gravity_emergence.py
- [ ] solvers/satellite_galaxy_validator_clean_systems.py
- [ ] solvers/satellite_galaxy_velocity_validator.py

### Status/Summary Documents
- [ ] STATUS_OCTOBER_5_2026_FINAL.md
- [ ] PHASE_2_DIAGNOSTIC_BREAKTHROUGH.md
- [ ] ALGORITHM_ZERO_STATUS.md
- [ ] INTEGRATION_SESSION_SUMMARY_OCT5_2026.md

## Execution Plan

**Phase 1:** Fix all critical documentation (DARK_MATTER_COMPLETE_NODE_CHAPTER_REFERENCE.md first, as it's the canonical reference)

**Phase 2:** Fix all node documentation files

**Phase 3:** Systematically go through all solver Python files

**Phase 4:** Fix all status/summary documents

**Phase 5:** Verify no remaining "dark matter" references (except in historical context or Standard Model neutrino mass notation)

## Verification Command

```bash
grep -r "dark.matter\|dark_matter\|Dark Matter\|Dark matter" /home/claude/one-wave-science \
  --include="*.py" --include="*.md" \
  | grep -v "dm2_" \
  | grep -v "DARK_MATTER_TERMINOLOGY_CORRECTION"
```

Should return: 0 results (except for Standard Model constants like dm2_31)

## Why This Matters

This correction aligns the codebase with the **fundamental One-Wave insight**: there are no separate exotic particles. All phenomena emerge from a single superfluid field and its configurations. What we observe as "dark matter" is simply displaced superfluid energy—measurable pressure deviations in the field.

This is not a cosmetic change. It reflects the correct physics and ensures the entire framework is internally consistent.

---

**Implementation Date:** October 5, 2026  
**Directive:** All nodes, chapters, solvers must reflect this terminology by end of session
