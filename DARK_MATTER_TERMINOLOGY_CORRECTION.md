# Dark Matter Terminology Correction Directive

**Effective Immediately Across All Repos and Nodes**

## Core Physics Correction

**Old interpretation:** Dark matter is a separate exotic particle species (~85% of universe's matter).

**CORRECT interpretation (from A-115 and Book 5 Ch1):**
- **Dark matter = Extended Compression Effect** (official One-Wave term)
- **Mathematically: g_wake** (the wake contribution to gravitational acceleration)
- **Physically: compression ring** from galaxy displacement through superfluid field
- **Pressure relation: P_displacement = volume_displaced**
- It is NOT a separate particle—it is the field's pressure response to displacement
- No cascade inheritance, no special mechanism—just: displacement creates pressure

## Repository Authority

The correct definition comes directly from:
1. **A-115 Unified Compression Field** (Section 3: Extended Compression / Dark-Matter View)
2. **Book 5, Chapter 1: Galaxies and the Extended Compression Effect**

Both define dark matter as the "Extended Compression Effect" (g_wake) from galaxy motion through the superfluid field.

## Terminology Mapping (Systematic Replacement)

### Core Terms

| Old Terminology | NEW Official Term | Physical Meaning |
|---|---|---|
| dark matter | **Extended Compression Effect** | Compression ring (g_wake) from galaxy displacement |
| dark matter halo | **compression ring** or **g_wake region** | Extended compression from galaxy motion |
| dark matter particle | (remove entirely) | No such thing; only pressure field response |
| missing mass | **extended compression field** | Field's response at galactic scale (R_ring ~ R_gravity) |

### Variable Names (Consistent Replacement)

| Old Pattern | NEW Pattern | Context |
|---|---|---|
| `dark_matter_*` | `extended_compression_*` | Measures of compression effect strength |
| `dark_matter_volume` | `extended_compression_volume` | Volume of high-pressure regions |
| `dark_matter_halo` | `extended_compression_effect` | Name in data structures |
| `dark_matter_signature` | `extended_compression_signature` | Observable measure of effect |
| `dm2_*` | Keep as-is | Standard physics notation for neutrino masses |

### Descriptive Phrases in Comments

| Old | NEW |
|---|---|
| "dark matter halo" | "Extended Compression Effect" or "compression ring (g_wake)" |
| "displaced superfluid energy" | "Extended Compression Effect" or "compression ring" |
| "cascade-inherited displacement" | "compression ring from galaxy motion" |
| "superfluid displacement signature" | "extended_compression_signature" |

## Why This Terminology

The official term "Extended Compression Effect" appears in:
- **A-115, Section 3, line 152:** "In One-Wave this is the **Extended Compression Effect**, not unseen particulate matter."
- **Book 5 Ch1, line 51:** "The **Extended Compression Effect** is the One-Wave name for the 'extra' gravity conventionally attributed to dark matter"

Using this terminology ensures consistency with the authoritative repository sources and prevents confusion with incorrect interpretations (cascade inheritance, generic superfluid energy, etc.).

## Physics Summary (A-115 / Book 5 Ch1)

```
When galaxy moves through superfluid ψ field:
  
  Displacement creates compression ring around moving structure
  Compression creates pressure field (like water wave around boat)
  
  At atomic scale: R_ring << R_gravity (negligible)
  At galactic scale: R_ring ~ R_gravity (measurable)
  
  Observed in: rotation curves, lensing, structure formation
  Mathematical form: g_0 = g_local + g_wake
  
  Pressure = volume displaced (P = V_displaced)
```

## Files Corrected

### Reference Documents
- [x] DARK_MATTER_COMPLETE_NODE_CHAPTER_REFERENCE.md (FIXED)

### Solver Files
- [x] solvers/unified_phase_solver.py (FIXED)
- [x] solvers/standard_model_mysteries_unified.py (FIXED)
- [x] solvers/galaxy_rotation_cascade_wake_validator.py (FIXED)
- [x] solvers/algorithm_zero_emergence.py (FIXED)
- [x] Nodes/D-415_Hexagonal_Lattice_Interaction_Dynamics/simulate_d415.py (FIXED)

### Remaining Files (follow same pattern)
- [ ] solvers/galaxy_rotation_validator.py
- [ ] solvers/galaxy_rotation_inherited_rotation_field.py
- [ ] solvers/galaxy_rotation_constant_inherited_velocity.py
- [ ] solvers/algorithm_zero_galaxy_validation_comprehensive.py
- [ ] solvers/neutrino_mass_solver.py
- [ ] solvers/three_body_solver.py
- [ ] solvers/w2_gravity_emergence.py
- [ ] solvers/satellite_galaxy_validator_clean_systems.py
- [ ] solvers/satellite_galaxy_velocity_validator.py
- [ ] Books/Book5_Macro/Book5_Ch1_Galaxies_and_Dark_Matter.md
- [ ] Status documents (STATUS_*, PHASE_2_*, ALGORITHM_*, INTEGRATION_*)

## Verification Command

```bash
grep -r "dark.matter\|dark_matter\|Dark Matter\|Dark matter" /home/claude/one-wave-science \
  --include="*.py" --include="*.md" \
  | grep -v "dm2_" \
  | grep -v "Extended Compression Effect" \
  | grep -v "DARK_MATTER_TERMINOLOGY_CORRECTION" \
  | grep -v "^Binary"
```

Should return: Only references in context of Standard Model conventions or comparisons.

---

**Implementation Date:** October 5, 2026  
**Authority:** A-115 and Book 5 Ch1 (authoritative repository definitions)  
**Status:** In progress — correcting all references across codebase
