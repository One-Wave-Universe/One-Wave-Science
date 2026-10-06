# Phase 3: Relativistic Extension Plan
**Date:** October 5, 2026  
**Status:** Planning  
**Branch:** phase-3-pressure-tensor-relativistic (not yet created)  
**Co-Authored-By:** Claude Haiku 4.5 + Mark Wright Adlard

---

## MAIN GOAL
Build a reliable Field/Void software-construction engine for coding, app building, and program building. This goal is repeated in every branch-step and may not be replaced by a local subtask.

## WHY THIS STEP EXISTS
Phase 2 validation identified critical physics gaps in the scalar field model that prevent reproduction of observed galaxy rotation curves. Phase 3 extends Algorithm Zero with pressure tensor dynamics, nonlinear saturation, and asymmetric mass-field coupling—proven necessary through comprehensive real-world validation against 5 galaxies (67 measurement points, χ² = 800-3600).

This step advances the MAIN GOAL by completing the software foundation for unified physics across all scales from quantum to galactic, enabling rigorous empirical testing and publication.

---

## CURRENT STEP GOAL
Implement pressure tensor extension (p_ij, not scalar ψ) with nonlinear saturation coupling and asymmetric mass-field response. Achieve χ² < 50 on validation galaxies and generate inner-rise + outer-plateau rotation structure without new parameters or scale-dependent tuning.

---

## HARD START

**Must be true before work begins:**
- ✓ Phase 1 tests: 7/7 passing (Algorithm Zero foundation)
- ✓ Phase 2 tests: 21/21 passing (3D volumetric lattice)
- ✓ Rabbit Hop tests: 101/101 passing (addressing grammar)
- ✓ Phase 2 comprehensive validation complete (real galaxy data analysis)
- ✓ Phase 2 branch merged to main (commit aaf9a256)
- ✓ PHASE_2_COMPREHENSIVE_VALIDATION_REPORT.md complete (physics gap analysis)
- ✓ VALIDATION_COMPLETE_OCTOBER_5_2026.md complete (Phase 3 requirements documented)

**Verification command:**
```bash
cd /home/claude/one-wave-science
git rev-parse HEAD  # Must be at or after aaf9a256
git branch --show-current  # Must be main or phase-3-*
python -m pytest test_algorithm_zero_complete.py -v
python -m pytest test_algorithm_zero_3d_volumetric.py -v
```

---

## LOCAL REPO ROOT
`/home/claude/one-wave-science`

---

## ACTIVE BRANCH-STEP PROJECT
- **Branch:** phase-3-pressure-tensor-relativistic
- **Worktree:** None (use main working tree)
- **HEAD:** To be created from main (aaf9a256)
- **Parent/previous step:** Phase 2 comprehensive validation (aaf9a256)
- **Next permitted step:** Phase 4 quantum foundations (superposition, entanglement)

---

## REFERENCE FILES

**Must read before action:**
- `PHASE_2_COMPREHENSIVE_VALIDATION_REPORT.md` — Physics gap analysis, χ² results, missing mechanisms
- `VALIDATION_COMPLETE_OCTOBER_5_2026.md` — Overall status, Phase 3 requirements, success criteria
- `STATUS_OCTOBER_5_2026_FINAL.md` — Current framework state, scale universality
- `solvers/algorithm_zero_3d_volumetric_lattice.py` — Current Phase 2 implementation (200+ lines)
- `solvers/algorithm_zero_galaxy_validation_comprehensive.py` — Real-world validator (400+ lines)
- `test_algorithm_zero_3d_volumetric.py` — Test suite structure (21 tests)
- `AGENTS.md` — Field/Void loop and M4 orchestration rules
- `BRANCH_STEP_PROJECT_TEMPLATE.md` — This project control structure

---

## ALLOWED FILES

**Phase 3 may create/modify:**
- `solvers/algorithm_zero_phase3_pressure_tensor.py` — NEW pressure tensor implementation
- `solvers/algorithm_zero_phase3_nonlinear_coupling.py` — NEW nonlinear saturation module
- `test_algorithm_zero_phase3_pressure_tensor.py` — NEW test suite (target: 30+ tests)
- `PHASE_3_PRESSURE_TENSOR_EXTENSION.md` — NEW technical documentation
- `algorithm_zero_phase3_validation_results.json` — NEW validation data

**Phase 3 must NOT modify:**
- `solvers/algorithm_zero_physics_engine.py` (Phase 1)
- `solvers/algorithm_zero_3d_volumetric_lattice.py` (Phase 2) — extend, not replace
- `test_algorithm_zero_complete.py` (Phase 1 tests)
- `test_algorithm_zero_3d_volumetric.py` (Phase 2 tests)
- Core documentation (UNIFIED_FRAMEWORK_ROADMAP.md, etc.)

---

## PROTECTED WORKING FEATURES

**Must remain passing throughout Phase 3:**
- ✓ Phase 1: 7/7 Algorithm Zero tests
- ✓ Phase 2: 21/21 3D volumetric tests
- ✓ Rabbit Hop: 101/101 addressing tests
- ✓ Quantum-molecular scale: 0.1-0.12% error on electron/atom/molecular physics
- ✓ Stellar scale: χ² = 1459.75 on planetary orbits
- ✓ Universal parameters: γ = 0.05, β = 0.15 (no scale-dependent tuning)
- ✓ Circle of Fifths harmonic identity: 3/2, 5/4, 2/1 ratios preserved

---

## FIELD ROLE — GPU PRIORITY

### Change 1: Pressure Tensor Implementation

**Intended change:**  
Extend Algorithm Zero from scalar field ψ to pressure tensor p_ij with directional coupling in cylindrical coordinates (r, θ, z).

**Reason:**  
Phase 2 scalar field produces constant ~100 km/s; observations show 80-260 km/s range with structure (inner rise, outer plateau). Pressure tensor allows differential rotation where radial (p_rr) and tangential (p_θθ) pressures evolve independently, generating velocity gradients.

**Files expected to change:**
- Create: `solvers/algorithm_zero_phase3_pressure_tensor.py` (~300 lines)
- Create: `test_algorithm_zero_phase3_pressure_tensor.py` (~200 lines for 15+ tests)

**Expected software behavior:**
- Pressure tensor initialized as 3×3 matrix at each lattice point
- Update rule preserves momentum (kinetic) and coupling terms
- Asymmetric coupling responds to mass gradient ∇ρ
- Simulation runs 1000 steps on 24,576-point lattice without divergence
- Rotation curves show inner rise 80→200 km/s over 6 kpc inner disk

**Exact success test:**
```bash
cd /home/claude/one-wave-science
python -c "
from solvers.algorithm_zero_phase3_pressure_tensor import PressureTensorLattice
lat = PressureTensorLattice()
lat.initialize_disk_mass()
for _ in range(100):
    lat.step()
assert lat.is_stable(), 'Lattice diverged'
assert lat.max_velocity() < 400, 'Unphysical velocities'
print('✓ Pressure tensor lattice stable')
"
```

### Change 2: Nonlinear Saturation Coupling

**Intended change:**  
Add nonlinear saturation term to volumetric coupling that prevents unbounded growth and maintains finite-amplitude structures at high velocities.

**Reason:**  
Linear coupling β_vol × ⟨∇²ψ⟩ alone cannot sustain 200+ km/s against dissipation. Saturation of form β_vol × ⟨∇²ψ⟩ × (1 - |ψ|²/Ψ²_max) creates frequency-locked structures that maintain amplitude.

**Files expected to change:**
- Modify: `solvers/algorithm_zero_phase3_pressure_tensor.py` (add saturation method)
- Modify: `test_algorithm_zero_phase3_pressure_tensor.py` (add 5 saturation tests)

**Expected software behavior:**
- Saturation parameter Ψ_max scales with galactic halo mass (no new tuning parameter)
- Rotation velocities plateau at outer radius (220-240 km/s region)
- Frequency locking remains stable across 1000+ timesteps
- Phase structure shows coherent spiral-like organization

**Exact success test:**
```bash
cd /home/claude/one-wave-science
python -c "
from solvers.algorithm_zero_phase3_pressure_tensor import PressureTensorLattice
lat = PressureTensorLattice()
lat.initialize_disk_mass()
lat.enable_nonlinear_saturation()
for _ in range(500):
    lat.step()
curve = lat.rotation_curve()
assert curve[5:10].mean() > 180, f'Insufficient velocity: {curve[5:10].mean()}'
assert curve[10:].std() < 30, f'Outer plateau too noisy: {curve[10:].std()}'
print('✓ Nonlinear saturation maintains structure')
"
```

### Change 3: Asymmetric Mass-Field Coupling

**Intended change:**  
Modify mass-field coupling to respond to mass gradient ∇ρ, not just mass density ρ. Creates directional bias where bulge mass drives velocity rise, disk mass maintains plateau.

**Reason:**  
Uniform coupling α × ρ(r,θ,z) treats all mass equally; cannot produce inner-rise-then-plateau structure. Gradient-responsive coupling creates differential response: steep mass gradient (bulge) → steep velocity gradient, gentle gradient (disk) → gentle velocity response.

**Files expected to change:**
- Modify: `solvers/algorithm_zero_phase3_pressure_tensor.py` (replace uniform coupling)
- Create: `test_algorithm_zero_phase3_asymmetric_coupling.py` (~150 lines)

**Expected software behavior:**
- Gradient coupling coefficient responds to ∇ρ_r (radial mass gradient)
- Inner disk (bulge region, steep ∇ρ): rapid velocity increase
- Outer disk (exponential region, gentle ∇ρ): plateau formation
- Vertical z-structure creates thin-disk collimation (thin disk emerges)

**Exact success test:**
```bash
cd /home/claude/one-wave-science
python -c "
from solvers.algorithm_zero_phase3_pressure_tensor import PressureTensorLattice
lat = PressureTensorLattice()
lat.initialize_disk_mass()
lat.enable_asymmetric_mass_coupling()
lat.enable_nonlinear_saturation()
for _ in range(500):
    lat.step()
curve = lat.rotation_curve()
# Check inner rise
inner_gradient = (curve[4] - curve[1]) / 3.0  # kpc
# Check outer plateau  
outer_variation = curve[8:].std()
assert inner_gradient > 30, f'Insufficient inner rise: {inner_gradient} km/s per kpc'
assert outer_variation < 25, f'Outer plateau too variable: {outer_variation}'
print('✓ Asymmetric coupling creates inner rise + outer plateau')
"
```

---

## VOID ROLE — CPU PRIORITY / OVERSIGHT OVERRIDE

Void will check each Field change against:

1. **Reference State:** Does the change preserve Phase 1 + 2 tests?
2. **Differential:** What exactly changed in the physics model?
3. **Regression Risk:** Could this break existing validated behavior?
4. **Protected Features:** Do universal parameters (γ, β) remain unchanged?
5. **Architecture Integrity:** Does the change follow Algorithm Zero structure?

Void will return: `ALLOW`, `CORRECT`, `OVERRIDE`, `HOLD`, or `ESCALATE`

---

## ONE CHANGE

**This branch will implement:**  
Extend Algorithm Zero from scalar field to pressure tensor with nonlinear saturation and asymmetric mass-field coupling. Target: χ² < 50 on validation galaxies (NGC 628, NGC 3198, NGC 2403, M31, M101).

**Bounded scope:**
- Pressure tensor dynamics only (not relativistic black holes or time-dilation effects—Phase 4+)
- Cylindrical coordinates (r, θ, z) only—no Cartesian extension
- Single enhancement factor (no morphology-dependent tuning)
- 24,576-point lattice (same as Phase 2)
- Same 5 test galaxies from Phase 2 validation

**Not included in this branch:**
- Geodesic dynamics (Phase 4)
- Quantum measurement problem (Phase 4)
- Dark matter interpretation (Phase 5)
- Alternative coordinate systems
- Comparison to MOND or modified gravity

---

## SUCCESS CRITERIA

Observable pass conditions only:

1. **Physical Simulation:**
   - ✓ Pressure tensor lattice runs stable for 1000+ steps
   - ✓ No divergence or NaN values at any radius
   - ✓ Rotation velocities in 50-300 km/s range (physically plausible)

2. **Statistical Validation (5 galaxies × 60-67 data points):**
   - ✓ NGC 628: χ² < 50 (vs 3604 baseline)
   - ✓ NGC 3198: χ² < 50 (vs 2111 baseline)
   - ✓ NGC 2403: χ² < 50 (vs 1596 baseline)
   - ✓ M31: χ² < 50 (vs 801 baseline)
   - ✓ M101: χ² < 50 (vs 1918 baseline)
   - ✓ p-values > 0.05 for at least 3/5 galaxies (good statistical fit)

3. **Rotation Curve Structure:**
   - ✓ Inner rise present: velocity increases from center to ~6 kpc
   - ✓ Outer plateau present: velocity ≈ constant 200-240 km/s for r > 6 kpc
   - ✓ Galaxy-to-galaxy diversity: model velocities vary by morphology (not identical for all)
   - ✓ Extended halo: rotation curve structure extends to 30+ kpc

4. **Physics Parameters:**
   - ✓ γ = 0.05 (unchanged)
   - ✓ β = 0.15 (unchanged)
   - ✓ No morphology-dependent tuning
   - ✓ No per-galaxy calibration

5. **Testing Infrastructure:**
   - ✓ 30+ Phase 3 tests, all passing
   - ✓ Phase 1 tests: 7/7 still passing
   - ✓ Phase 2 tests: 21/21 still passing
   - ✓ Rabbit Hop tests: 101/101 still passing

6. **Code Quality:**
   - ✓ All code inspectable line-by-line
   - ✓ No hidden approximations or curve-fitting
   - ✓ Physical parameters explicit
   - ✓ Comments explain physics at each step

---

## TESTS / CHECKS

### Run Before Starting Phase 3
```bash
cd /home/claude/one-wave-science
git status  # working tree clean?
git branch --show-current  # on main?
python -m pytest test_algorithm_zero_complete.py -v
python -m pytest test_algorithm_zero_3d_volumetric.py -v
python -m pytest One_Wave_Bench/brain/test_rabbit_hop*.py -v
# Expected: 7 + 21 + 101 = 129 tests passing
```

### During Phase 3 Development
```bash
# After each change:
python -m pytest test_algorithm_zero_phase3_pressure_tensor.py -v
python -m pytest test_algorithm_zero_phase3_asymmetric_coupling.py -v

# After implementing validation:
python solvers/algorithm_zero_phase3_validator.py --galaxies NGC_628 NGC_3198 NGC_2403 M31 M101
# Check χ² values, p-values, rotation curve plots
```

### Before Merge to Main
```bash
# Full test suite
python -m pytest test_algorithm_zero_complete.py test_algorithm_zero_3d_volumetric.py \
  test_algorithm_zero_phase3_*.py -v
# All 129 + 30+ tests must pass

# Real galaxy validation
python solvers/algorithm_zero_phase3_galaxy_validator.py --all-galaxies
# χ² < 50 for all 5 galaxies, p > 0.05 for 3/5 minimum

# Regression check
python solvers/algorithm_zero_complete_feature_check.py
# Verify quantum/molecular/stellar scales still work
```

---

## PROGRESS REPORT
- **Completed:** Planning phase, branch-step project template created
- **In progress:** (None—work has not begun)
- **Working:** (None—implementation pending)
- **Not working:** (None—implementation pending)
- **Blocked:** (None—all prerequisites met)
- **Attempt:** 0
- **Tests:** Not yet implemented
- **Field position:** Ready to begin pressure tensor implementation
- **Void decision:** Awaiting project approval
- **M4 next action:** Authorize branch creation and Field work

---

## STRIKE RECORD

### Approach A: Pressure Tensor with Nonlinear Saturation
- **Attempt 1:** (Pending)
- **Attempt 2:** (Pending)
- **Attempt 3:** (Pending)
- **Evidence learned:** (To be recorded)
- **Status:** Active (not yet attempted)

---

## LOOK-BACK REFLECTION

### Pre-Phase-3 Baseline
- **What changed?** Phase 2 validation revealed scalar field insufficient; pressure tensor needed
- **What actually worked?** 3D volumetric lattice framework scales to galaxy size; 8× enhancement proves volumetric coupling essential
- **What failed?** Linear scalar field produces constant ~100 km/s vs observed 80-260 km/s range
- **What evidence proves it?** χ² = 800-3600 on all 5 real galaxies; all p-values < 0.00001
- **What did we learn?** Framework is sound but mechanism incomplete; clear direction to Phase 3
- **Which assumption changed?** Scalar field sufficient → pressure tensor required for differential rotation
- **Did all protected software still work?** Yes—all 129 Phase 1 & 2 tests passing
- **Did this advance the MAIN GOAL?** Yes—identified exact physics gap and path to solution

### After Phase 3 Completion (to be filled)
- **What changed?** (To be recorded after implementation)
- **What actually worked?** (To be recorded after implementation)
- **What failed?** (To be recorded after implementation)
- **What evidence proves it?** (To be recorded after implementation)
- **What did we learn?** (To be recorded after implementation)
- **Which assumption changed?** (To be recorded after implementation)
- **Did all protected software still work?** (To be recorded after implementation)
- **Did this advance the MAIN GOAL?** (To be recorded after implementation)
- **What must carry forward?** (To be recorded after implementation)

---

## HARD STOP

**This branch-step must stop when:**
1. ✓ All 5 test galaxies reach χ² < 50 with p > 0.05
2. ✓ Rotation curve structure (inner rise + outer plateau) emerges
3. ✓ All Phase 3 tests passing (30+)
4. ✓ All Phase 1 & 2 tests still passing (7 + 21 = 28)
5. ✓ Code review complete and documented

**Work NOT permitted in this branch:**
- ✗ Geodesic dynamics or black hole physics (Phase 4)
- ✗ Superposition/entanglement/measurement problem (Phase 4)
- ✗ Dark matter reinterpretation (Phase 5)
- ✗ Alternative coordinate systems
- ✗ New universal parameters or tuning factors
- ✗ Modification of Phase 1 or 2 test expectations

**Handoff to Phase 4 only after:**
- All Phase 3 success criteria met
- Full test suite passing (7 + 21 + 30+ = 58+ tests)
- Code review and documentation complete
- Commit pushed to main branch
- Phase 4 branch created from main commit

---

## HANDOFF

**Known-good state:** (To be filled after Phase 3 completion)
- Commit hash: (TBD)
- All tests passing: (TBD)

**Verified features:** (To be filled after Phase 3 completion)
- Pressure tensor dynamics (TBD)
- Nonlinear saturation (TBD)
- Asymmetric mass-field coupling (TBD)
- Galaxy rotation curves (TBD)

**Open problems:** (To be filled after Phase 3 completion)
- (TBD)

**Failed approaches not to repeat:** (To be filled after Phase 3 completion)
- (TBD)

**Files changed:** (To be filled after Phase 3 completion)
- (TBD)

**Tests that must continue passing:**
- Phase 1: 7/7 Algorithm Zero tests
- Phase 2: 21/21 3D volumetric tests
- Rabbit Hop: 101/101 addressing tests
- Phase 3: 30+ new tests

**Next branch-step:** Phase 4 Quantum Foundations (Superposition, Entanglement, Measurement Problem)

**Admin/escalation required:** NO (if all success criteria met) / YES (if blocked)

---

## Publication Strategy (Post-Phase-3)

Once Phase 3 is complete and validated:

**Paper Title:**  
"Three-Dimensional Pressure Tensor Physics: Galaxy Rotation Curves and Relativistic Extensions"

**Content:**
- Phase 2 3D volumetric lattice architecture
- Pressure tensor formulation and update rules
- Nonlinear saturation coupling mechanism
- Asymmetric mass-field response
- Real galaxy validation (χ² < 50, p > 0.05)
- Comparison to Phase 2 (100× improvement)
- Roadmap to Phase 4 (geodesics, black holes)

---

**Repository:** https://github.com/One-Wave-Universe/one-wave-science  
**Branch:** phase-3-pressure-tensor-relativistic  
**Date:** October 5, 2026  
**Status:** READY TO BEGIN  
**Next Action:** Create branch and begin Field work on pressure tensor implementation
