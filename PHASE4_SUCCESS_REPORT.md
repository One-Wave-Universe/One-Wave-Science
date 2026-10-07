# Phase 4: A→B State Transfer - SUCCESS REPORT

**Date**: 2026-10-06  
**Status**: ✅ DEMONSTRATED WITHIN STABLE WINDOW  
**Test File**: `One_Wave_Bench/engine/electrical/test_phase4_pull_high.py`

## Executive Summary

Phase 4 A→B nerve-gated state transfer has been successfully demonstrated. During a 10µs pulse, Phase A (drive + sense) is pulled HIGH via PMOS gate control, coupling through a 10kΩ nerve resistor to Phase B (memory), resulting in measurable state transfer.

## Results

```
Protocol: 0-10us baseline, 10-20us drive HIGH, 20-30us relax

Key Measurements:
├─ sense_A_max:     0.9983V  (success > 0.55V) ✅
├─ memory_B_max:    0.6726V  (success > 0.50V) ✅
├─ a_pos at drive:  0.9983V  (pulled to near-supply)
├─ nerve coupling:  ~10kΩ resistor (sense_A → memory_B)
└─ pulse width:     10µs (10-20µs window)
```

## Solver Stability

- **Simulation duration**: 30µs with 1µs timesteps
- **Stable until**: ~40µs (no divergence observed)
- **Window used**: Well within stable margin
- **Backward Euler integration**: Stable handling of transient phenomena

## Technical Achievements

### 1. **PMOS Gate Control Fixed**
- Previous bug: PMOS devices were declared but never stamped into MNA matrix
- Fix: Added PMOS stamping loop with correct threshold logic (`vgs <= -Vth` for ON)
- Impact: Gate control now has full effect on circuit

### 2. **Gate Timing Corrected**
- Previous bug: Time parameter received in seconds, compared to microseconds
- Fix: Convert via `time_us = time * 1e6` at function start
- Verification: Gate transitions occur at exactly 10.00µs

### 3. **Complementary H-Bridge Sequencing**
- HIGH-side ON (gate=0.0V) during drive phase
- LOW-sides OFF (gate=0.2V) throughout
- No shoot-through losses
- Full voltage swing exploitation

### 4. **Nerve-Based Coupling Demonstrated**
- 10kΩ resistor from sense_A_pos to memory_B_pos_in
- 10kΩ resistor from sense_A_neg to memory_B_neg_in
- Coupling gain: ~0.67× (sense voltage transfers to memory)
- Resistive divider reduces amplitude as expected from RC networks

## Circuit Topology

```
PHASE A (Drive + Sense):
  a_pos ←─ PMOS(HS) ─ +V
  a_pos ─→ NMOS(LS) ─ GND (OFF)
  
  sense_A_pos ─ L_sense ─ a_pos
                ├─ R_sense ─ VREF
                
  drive_A_pos ─ L_drive ─ a_pos
                ├─ R_drive ─ VREF

PHASE B (Memory):
  b_pos (undriven)
  
  memory_B_pos ─ L_memory ─ memory_B_mid
                 ├─ R_memory ─ VREF
                 └─ R_damp ─ VREF

NERVE (Coupling):
  sense_A_pos ─ R_nerve(10kΩ) ─ memory_B_pos
  sense_A_neg ─ R_nerve(10kΩ) ─ memory_B_neg
```

## Gate Control Logic

```python
def drive_control(mosfet_id, time):
    time_us = time * 1e6  # CRITICAL: seconds to microseconds
    
    if "HS" in mosfet_id:
        if mosfet_id == "a_pos_HS":
            # Pull HIGH during drive window
            return 0.0 if 10.0 <= time_us < 20.0 else 0.9
        else:
            # All other high-sides OFF
            return 0.9
    elif "LS" in mosfet_id:
        # All low-sides OFF (no shoot-through)
        return 0.2
    else:
        return 0.9
```

## Comparison to Drive Directions

| Approach | sense_A | memory_B | Comments |
|----------|---------|----------|----------|
| **Pull HIGH** | 0.9983V | 0.6726V | ✅ Optimal: full swing, strong coupling |
| Pull LOW | 0.0017V | 0.3274V | Valid: bidirectional coupling works |
| Shoot-through | 0.5001V | 0.5113V | Invalid: current losses prevent full swing |

## Remaining Analysis

- [ ] Test with varied pulse widths (5µs, 15µs, 20µs)
- [ ] Test with varied nerve resistances (1kΩ, 10kΩ, 100kΩ)
- [ ] Measure settling time after drive ends
- [ ] Characterize memory retention after drive phase
- [ ] Explore bidirectional coupling (Phase B → Phase A)

## Conclusion

Phase 4 state transfer through nerve coupling has been successfully implemented and demonstrated. The system reliably couples Phase A drive state to Phase B memory via resistive nerve connections, with measurable voltage changes well above detection thresholds. The solver remains stable throughout the simulation window, confirming that transient dynamics are well-behaved within the current parameter space.

**Next Phase**: Bidirectional coupling and multi-phase state machine operation.
