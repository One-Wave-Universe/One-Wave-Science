# P0 Ternary Circuit Simulator

Complete simulation, testing, and visualization suite for the P0 ternary three-phase motor drive circuit with virtual ground buffer.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  solver_transient.py                                         │
│  ├─ Modified Nodal Analysis (MNA)                           │
│  ├─ Newton iteration for nonlinear elements                 │
│  ├─ Backward Euler / Trapezoidal integration                │
│  └─ MOSFET + OpAmpBuffer models                             │
└────────────┬────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────┐
│  p0_ternary_circuit.py                                       │
│  ├─ Circuit topology (split or single supply)               │
│  ├─ Three half-bridge phases (U, V, W)                      │
│  ├─ Virtual ground buffer (TLE2426-like)                    │
│  └─ Initial state preparation                               │
└────────────┬────────────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────────────┐
│  circuit_controller.py                                       │
│  ├─ Three operating modes:                                  │
│  │  ├─ VISUALIZATION: Record state history                  │
│  │  ├─ AI_CONTROL: Agent observation + gate control         │
│  │  └─ TEST_EXECUTION: Automated test suite                 │
│  ├─ State recording & measurement extraction                │
│  └─ Test case definition & pass/fail criteria               │
└────────────┬────────────────────────────────────────────────┘
             │
      ┌──────┴───────┐
      │              │
   ┌──▼──┐      ┌───▼────┐
   │ Test│      │  Viz   │
   │Suite│      │ Results│
   └─────┘      └────────┘
```

## Quick Start

### 1. Run Basic Simulation Tests

```bash
python -m pytest One_Wave_Bench/engine/electrical/tests/test_p0_ternary.py -xvs
```

**Expected Output:**
- Virtual ground stability test: ✓ PASSED (V_0 = 2.500V)
- Ternary sequencing test: ✓ PASSED (all gates off, V_0 stable)

### 2. Run All DC Regression Tests

```bash
python -m pytest One_Wave_Bench/engine/electrical/tests/test_dc_regressions.py -xvs
```

**Expected:** 11 tests pass

### 3. Demo All Control Modes

```bash
# Visualization mode only
python One_Wave_Bench/engine/electrical/demo_circuit_controller.py --mode visualization

# AI control mode only
python One_Wave_Bench/engine/electrical/demo_circuit_controller.py --mode ai-control

# Test execution mode only
python One_Wave_Bench/engine/electrical/demo_circuit_controller.py --mode test

# All three modes in sequence
python One_Wave_Bench/engine/electrical/demo_circuit_controller.py --all
```

### 4. Export Simulation Results

```bash
# Run simulation for 1 second and export to JSON
python One_Wave_Bench/engine/electrical/visualization_server.py --run 1.0 --export /tmp/results.json

# This generates:
# - Full state history (time, voltages, currents, MOSFET states)
# - Node voltage time series with statistics
# - Inductor current time series
# - Circuit summary (supply voltage, virtual ground stability, etc.)
```

### 5. Visualize Results

```bash
# Start HTTP server to view results
python One_Wave_Bench/engine/electrical/visualization_server.py --serve /tmp/results.json --port 8000

# Open browser to http://localhost:8000
# - View summary statistics
# - Download results as JSON
# - View final state
```

## Component Reference

### solver_transient.py

**Core MNA solver with Newton iteration for nonlinear elements**

Key classes:
- `TransientCircuit`: Circuit netlist and solver
- `TransientSolution`: Voltages, currents, and component states after one step
- `CapacitorState`, `InductorState`: Energy storage element state

Key methods:
- `solve_step(...)`: Execute one timestep of transient analysis
  - Takes: initial cap/inductor states, node voltages, timestep, time, gate voltage function
  - Returns: `TransientSolution` with updated states

**Critical fixes (Phase 3 unblocking):**
1. Initialize MNA matrix A and vector b (lines 289-290)
   - Prevents "name 'A' is not defined" NameError
2. Preserve gate voltages across Newton iterations (line 480)
   - Changed `copy()` to `update()` to maintain external gate nodes
3. Enable dynamic Newton iterations for nonlinear convergence (line 286)
   - 3 iterations when opamps present (for current limiting)
4. Implement OpAmpBuffer current limiting (lines 400-429)
   - Calculates excess current and adds dynamic series resistance
   - Prevents divergence during high-current transients

### p0_ternary_circuit.py

**Circuit topology builder for split or single-supply operation**

Key class:
- `P0TernaryCircuit`: Builder pattern for P0 circuit

Methods:
- `build(supply_mode="split" | "single")`: Create circuit and initial state
  - Returns: `(TransientCircuit, initial_state_dict)`

**Circuit configurations:**
1. **Split supply** (+V / -V):
   - PMOS high-side switches, NMOS low-side
   - Power rails tied to ±V
   - Midpoint at 0V (center of differential rails)

2. **Single supply** (0 to +V):
   - NMOS high and low side switches
   - Virtual ground buffer at 2.5V midpoint
   - TLE2426-like unity-gain buffer for stiff midpoint

**Critical fixes (Phase 3 unblocking):**
1. Initialize all phase and winding node voltages (both modes)
   - Prevents Vgs calculation errors (e.g., -2.5V instead of +3.0V)
   - Ensures initial state is complete for MNA solver

### circuit_controller.py

**Unified interface for visualization, AI control, and testing**

Key classes:
- `CircuitController`: Main control interface
- `CircuitState`: Snapshot at one time point
- `TestCase`: Test definition (duration, timestep, gate control, measurements, criteria)
- `TestResult`: Test execution result (pass/fail with measurements)

Operating modes:
1. **VISUALIZATION**
   - Records full state history
   - Suitable for exporting to visualization server
   - Use: `controller.run_simulation(..., mode=ControlMode.VISUALIZATION)`

2. **AI_CONTROL**
   - AI agent observes circuit via pre/post-step hooks
   - Agent receives state snapshots before and after each step
   - Use: `controller.set_ai_hooks(pre_step=..., post_step=...)`

3. **TEST_EXECUTION**
   - Run predefined test cases with pass/fail criteria
   - Automatic measurement extraction and validation
   - Use: `result = controller.run_test(test_case)`

Key methods:
- `set_gate_control(func)`: Set gate voltage function
- `set_ai_hooks(pre_step, post_step)`: Set AI observation hooks
- `run_simulation(duration_s, dt_s, mode)`: Run and return state history
- `run_test(test_case)`: Execute single test
- `run_test_suite(tests)`: Execute multiple tests
- `get_visualization_data()`: Export for visualization

### transient_measurements.py

**Time-series measurement recording and analysis**

Key classes:
- `TimeSeries`: Time-indexed values with statistics
- `TransientMeasurementRecorder`: Collect and analyze measurements

Methods on `TimeSeries`:
- `.min()`, `.max()`, `.mean()`: Basic statistics
- `.steady_state(last_n=100)`: Average of final N samples
- `.rms()`: Root mean square
- `.peak_to_peak()`: Max - Min
- `.energy(dt)`: Integrated value over time
- `.export_csv(filename)`: Export for external analysis

Methods on `TransientMeasurementRecorder`:
- `.record_step(...)`: Record one timestep
- `.get_node_voltage(node_id)`: Get voltage time series
- `.get_differential_voltage(node_a, node_b)`: Get V(A) - V(B)
- `.get_source_power(src_id, source_voltage)`: Get P = V*I
- `.get_mosfet_duty_cycle(mosfet_id)`: On-time / total-time
- `.get_mosfet_switch_count(mosfet_id)`: Count transitions
- `.get_steady_state_deviation(node_id, target)`: Max error in final period

### demo_circuit_controller.py

**Runnable examples of all three control modes**

Demonstrates:
1. Visualization mode: Record 100 µs of state (100 samples)
2. AI control mode: Agent observes and makes decisions
3. Test execution mode: Run automated test suite

Run all or individual modes:
```bash
python demo_circuit_controller.py --all
python demo_circuit_controller.py --mode visualization
python demo_circuit_controller.py --mode ai-control
python demo_circuit_controller.py --mode test
```

### visualization_server.py

**HTTP server for simulation results**

Features:
- Run simulation and export to JSON
- Serve HTML visualization page
- REST API for querying results
- No external dependencies

Commands:
```bash
# Export simulation
python visualization_server.py --run 1.0 --export /tmp/results.json

# Serve for viewing
python visualization_server.py --serve /tmp/results.json --port 8000

# Open browser to http://localhost:8000
```

## Testing Framework

### Test Anatomy

A test case defines:
1. **Gate control function**: How gates switch over time
2. **Duration & timestep**: Simulation parameters
3. **Measurements**: What to extract (node voltage, error, duty cycle, etc.)
4. **Pass criteria**: Min/max ranges for each measurement

Example:
```python
test_dc_steady = TestCase(
    name="DC Steady-State (All Gates OFF)",
    description="Verify virtual ground stability",
    duration_us=50.0,
    dt_us=1.0,
    gate_control_func=lambda mosfet_id, t: 0.0,  # All gates off
    measurements={
        "vg_steady": {
            "type": "node_voltage",
            "params": {"node": "0"}  # Virtual ground
        },
        "vg_error": {
            "type": "voltage_error",
            "params": {"node": "0", "target": 2.5}
        }
    },
    pass_criteria={
        "vg_steady": (2.4, 2.6),      # Must be within 2.4-2.6V
        "vg_error": (0.0, 0.1)         # Error must be < 0.1V
    }
)
```

### Running Tests

```python
from circuit_controller import CircuitController, TestCase

# Create controller
controller = CircuitController(circuit, initial_state)

# Define test
test = TestCase(...)

# Run it
result = controller.run_test(test)

# Check results
if result.status == TestStatus.PASSED:
    print("✓ Test passed")
    for meas_id, (min_v, max_v, passed) in result.pass_criteria.items():
        print(f"  {meas_id}: {result.measurements[meas_id]:.6f} ({min_v}-{max_v})")
```

## State and Initialization

### Initial State Dictionary

The `initial_state` dict from `P0TernaryCircuit.build()` contains:

```python
{
    "cap_states": {},  # Capacitor voltages (empty for now)
    "ind_states": {
        "L_U": InductorState(id="L_U", current=0.0),
        "L_V": InductorState(id="L_V", current=0.0),
        "L_W": InductorState(id="L_W", current=0.0),
    },
    "voltages": {
        # Power supplies
        "+V": 5.0,
        "-V": -5.0 or "GND": 0.0,
        "0": 2.5,  # Virtual ground midpoint (single supply) or 0V (split supply)
        
        # Phase nodes (initialized to midpoint)
        "mid_U": 2.5, "mid_V": 2.5, "mid_W": 2.5,
        
        # Winding return nodes
        "winding_U_return": 2.5,
        "winding_V_return": 2.5,
        "winding_W_return": 2.5,
        
        # For single supply mode
        "vg_raw": 2.5,  # Virtual ground divider output
    }
}
```

### Critical: Complete Node Initialization

The solver needs ALL nodes in `initial_state["voltages"]` to avoid:
- Vgs calculation errors (gate voltage defaults to 0.0 if missing)
- Newton iteration divergence (missing nodes become 0.0 by default)

## Verification Checklist

After changes to solver, circuit, or controller:

1. **Run DC regression tests**
   ```bash
   pytest tests/test_dc_regressions.py -xvs
   ```
   Expected: 11 tests pass

2. **Run P0 ternary tests**
   ```bash
   pytest tests/test_p0_ternary.py -xvs
   ```
   Expected: 2 tests pass (virtual ground stability + ternary sequencing)

3. **Run demo in all modes**
   ```bash
   python demo_circuit_controller.py --all
   ```
   Expected: Visualization (100 states), AI control (50 obs), test (PASSED)

4. **Export and visualize**
   ```bash
   python visualization_server.py --run 0.01 --export /tmp/test.json
   python visualization_server.py --serve /tmp/test.json --port 8000
   ```
   Expected: HTTP server starts, JSON contains valid measurements

## Known Limitations and Next Steps

### Current State (Phase 3 Unblocked)
- ✓ DC steady-state stable
- ✓ Virtual ground at 2.5V maintained
- ✓ All gates off, no dynamic switching
- ✓ Newton iteration converges
- ✓ OpAmpBuffer current limiting works

### Phase 4: Dynamic Gate Switching
- [ ] Implement dead-band comparator model
- [ ] Test gate transition with dI/dt
- [ ] Verify flyback diode operation
- [ ] Validate Trapezoidal integration stability

### Phase 5: Three-Phase Commutation
- [ ] Implement 120° gate sequencing
- [ ] Test rotating field generation
- [ ] Measure winding currents (phase sequencing)
- [ ] Validate motor-equivalent load

### Phase 6: Hardware Integration
- [ ] KiCad schematic generation
- [ ] PCB layout recommendations
- [ ] Bill of materials (BOM)
- [ ] SPICE model verification

### Phase 7: Visualization & UI
- [ ] 3D circuit rendering
- [ ] Real-time waveform display
- [ ] Interactive gate control UI
- [ ] Hardware breadboard viewer

## File Organization

```
One_Wave_Bench/engine/electrical/
├── solver_transient.py              # MNA solver + Newton iteration
├── components.py                    # Basic components (R, L, C, sources)
├── components_extended.py           # Advanced (MOSFET, OpAmp, Diode)
├── p0_ternary_circuit.py            # P0 topology builder
├── circuit_controller.py            # Unified control interface
├── transient_measurements.py        # Time-series recording
├── demo_circuit_controller.py       # Demo of all modes
├── visualization_server.py          # HTTP export server
│
├── tests/
│   ├── test_dc_regressions.py       # DC analysis regression tests (11 tests)
│   └── test_p0_ternary.py           # P0 ternary tests (2 tests)
│
└── README_CIRCUIT_SIMULATION.md     # This file

One_Wave_Bench/hardware/visualization/
└── p0_breadboard_viewer.html        # Three.js 3D visualization
```

## Troubleshooting

### "name 'A' is not defined"
- **Cause:** MNA matrix not initialized in Newton loop
- **Fix:** Ensure solver_transient.py line 289-290 initialize A and b
- **Status:** Fixed in Phase 3 unblocking commit

### "Vgs = -2.5V instead of +3.0V"
- **Cause:** Initial state missing winding node voltages
- **Fix:** Ensure p0_ternary_circuit.py initializes all phase nodes
- **Status:** Fixed in Phase 3 unblocking commit

### Gate voltage lost on iteration 2+
- **Cause:** prev_voltages overwritten by copy() instead of update()
- **Fix:** Ensure solver_transient.py line 480 uses update()
- **Status:** Fixed in Phase 3 unblocking commit

### Simulation diverges during current spike
- **Cause:** OpAmpBuffer current not limited
- **Fix:** Ensure solver_transient.py lines 400-429 implement current limiting
- **Status:** Fixed in Phase 3 unblocking commit

## References

- **MNA Theory:** Modified Nodal Analysis with Gauss-Jordan elimination
- **Newton Iteration:** Nonlinear element convergence via linearization
- **Backward Euler:** First-order accurate, A-stable integration
- **Trapezoidal:** Second-order accurate, conditionally stable (Phase 4+)
- **P0 Circuit:** Three-phase inverter with virtual ground midpoint
- **TLE2426:** Rail splitter / virtual ground buffer reference

## License and Attribution

Part of the One-Wave Physics Bench.
See repository root for license and attribution.
