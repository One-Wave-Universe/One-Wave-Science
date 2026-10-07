# P0 Hexagon Transient Stability Analysis: Findings

## Summary
Extensive testing of the P0 hexagon circuit (18-terminal fixture with 3 phases × 3 winding types) reveals a **systemic numerical stability issue in the MNA solver** that persists across multiple circuit topologies and parameter variations.

## Key Findings

### 1. Systemic Divergence Pattern
- **Single-phase drive winding**: Stable with R_drive=200Ω or R_drive=5000Ω (sweet spot at 200Ω)
- **Single-phase sense winding**: Stable with R_sense=4000-5000Ω (sweet spot at 4500Ω)
- **Three-phase drive-only circuit**: Diverges at ~45-50µs regardless of R_drive
- **Three-phase with drive+sense**: Diverges at ~35-45µs regardless of parameters
- **Passive circuit (no MOSFETs)**: Diverges at ~40µs despite removing all active elements
- **Divergence timeline**: Remarkably consistent ~35-50µs window across all multi-phase configurations

### 2. Stability Window Phenomenon (Not dt/τ Dependent)
Testing with single-phase windings revealed a non-monotonic stability relationship:
- Lower R values: Unstable
- **Stable window**: R = 4000-5000Ω (drive) or similar range (sense)
- Higher R values: Unstable again

This suggests **MNA matrix conditioning/singularity** rather than traditional Euler stability criterion (dt/τ >> 1).

### 3. Failed Interventions
The following parameter adjustments provided NO improvement:
- Increasing R_sense from 10Ω to 100Ω to 4500Ω: Still diverges in full circuit
- Reducing inductances (L_drive: 1mH → 100µH): No change
- Adding damping resistors (100kΩ at memory nodes): Made divergence worse
- Removing nerve ring coupling: Still diverges
- Removing memory windings: Still diverges
- Using resistor divider instead of OpAmp buffer for VREF: Still diverges
- Reducing timestep from 1µs to 0.1µs: Diverges even earlier
- Testing passive circuit (no MOSFETs): Still diverges

### 4. Isolation Testing Results

| Circuit Configuration | Duration | Result | Notes |
|---|---|---|---|
| Single-phase drive, R=200Ω | 500µs | ✓ STABLE | Optimal R value |
| Single-phase sense, R=4500Ω | 500µs | ✓ STABLE | Optimal R value |
| Three-phase drive only | 50µs | ✗ DIVERGE @ ~47µs | Consistent with full circuit |
| Three-phase drive+sense | 50µs | ✗ DIVERGE @ ~35-45µs | Earlier than drive alone |
| Passive (no switching) | 100µs | ✗ DIVERGE @ ~40µs | Topology issue, not MOSFET |

### 5. Root Cause Hypothesis
The divergence is most likely caused by one of:

**A) MNA Matrix Ill-Conditioning**
- The star-grounded 3-phase topology with multiple winding levels creates a singular or near-singular matrix
- This manifests as exponential growth in node voltages around t=35-50µs
- Affects single inductors minimally but catastrophically in multi-phase star configuration

**B) Nodal Analysis Accumulation Error**
- The solver correctly handles isolated L-R networks
- But when three phases couple through VREF (via 100Ω divider and 0.1Ω buffer), numerical errors accumulate
- Error propagation triggers around 35-50µs (characteristic of integrator feedback instability)

**C) OpAmp Buffer Interaction**
- The virtual reference (VREF) created by OpAmpBuffer + voltage divider may create feedback instability
- Removing OpAmp doesn't help, suggesting the topology itself is the issue

## Recommendations

1. **Investigate MNA Implementation**
   - Check for matrix singularities in `solver_transient.py` when handling multi-phase star-grounded networks
   - Consider condition number estimation in the Newton iteration

2. **Alternative Circuit Topologies**
   - **Floating reference**: Disconnect VREF into three separate local references (one per phase pair)
   - **Coupled flux instead of voltage**: Use magnetic coupling between inductors instead of electrical node sharing
   - **Voltage source VREF**: Use a stiff voltage source instead of OpAmp buffer

3. **Solver Improvements**
   - Adaptive timestepping to detect when dt becomes too large for effective coupling
   - Explicit handling of star-grounded multi-phase topologies
   - Matrix preconditioning for ill-conditioned systems

4. **Verify SPICE Compatibility**
   - Test same circuit in commercial SPICE (LTSpice, Ngspice) to determine if this is:
     - A known limitation of backward Euler with this topology
     - An implementation issue specific to this solver

## Files for Reference
- `p0_hexagon_hbridge_stable.py`: Full 18-terminal circuit with optimal parameters
- `p0_hexagon_hbridge_stable_no_mem_damp.py`: Variant without memory damping
- `test_vary_r_sense.py`: Parameter sweep showing stability windows
- `test_single_phase.py`: Single-phase isolation test
- Diagnostic test files in same directory

## Next Steps
1. **Short term**: Test topology variations (floating VREF, coupled inductors)
2. **Medium term**: Review/improve MNA solver matrix handling
3. **Long term**: Consider alternative circuit families (transfluxor-based, capacitive coupling)
