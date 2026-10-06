"""
Circuit Controller — Unified Interface for Visualization, AI Control, and Testing

Provides:
1. Real-time circuit state observation (for visualization)
2. Programmatic gate control (for AI agents)
3. Automated test execution (for validation)

All three modes can run simultaneously or in sequence.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Tuple
from enum import Enum
import json
import time
from datetime import datetime

from .p0_ternary_circuit import P0TernaryCircuit
from .solver_transient import TransientCircuit, CapacitorState, InductorState
from .transient_measurements import TransientMeasurementRecorder


class ControlMode(Enum):
    """Operating modes for the circuit controller."""
    IDLE = "idle"                    # No simulation running
    VISUALIZATION = "visualization"  # Real-time live visualization
    AI_CONTROL = "ai_control"        # AI agent controlling gates
    TEST_EXECUTION = "test_execution" # Automated test sequence


class TestStatus(Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class CircuitState:
    """Snapshot of circuit state at one moment."""
    time_us: float
    node_voltages: Dict[str, float]
    source_currents: Dict[str, float]
    inductor_currents: Dict[str, float]
    mosfet_states: Dict[str, bool]  # id -> is_on
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "time_us": self.time_us,
            "timestamp": self.timestamp,
            "node_voltages": self.node_voltages,
            "source_currents": self.source_currents,
            "inductor_currents": self.inductor_currents,
            "mosfet_states": self.mosfet_states
        }


@dataclass
class TestCase:
    """Single test case definition."""
    name: str
    description: str
    duration_us: float  # simulation duration
    dt_us: float  # timestep
    gate_control_func: Callable[[str, float], float]  # mosfet_id, time -> gate voltage
    measurements: Dict[str, Dict]  # measurement_id -> {"type": "...", "params": {...}, "tolerance": ...}
    pass_criteria: Dict[str, Tuple[float, float]]  # measurement_id -> (min, max)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "duration_us": self.duration_us,
            "dt_us": self.dt_us,
            "measurement_count": len(self.measurements),
            "criteria_count": len(self.pass_criteria)
        }


@dataclass
class TestResult:
    """Result of one test execution."""
    test_name: str
    status: TestStatus
    duration_us: float
    measurements: Dict[str, float]  # measurement_id -> actual_value
    pass_criteria: Dict[str, Tuple[float, float, bool]]  # measurement_id -> (min, max, passed)
    message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "status": self.status.value,
            "duration_us": self.duration_us,
            "measurements": self.measurements,
            "pass_criteria": {
                mid: {
                    "min": minv,
                    "max": maxv,
                    "passed": passed
                }
                for mid, (minv, maxv, passed) in self.pass_criteria.items()
            },
            "message": self.message,
            "timestamp": self.timestamp
        }


class CircuitController:
    """Unified control interface for circuit simulation."""

    def __init__(self, circuit: TransientCircuit, initial_state: dict):
        self.circuit = circuit
        self.initial_state = initial_state

        # Simulation state
        self.cap_states = initial_state["cap_states"].copy()
        self.ind_states = initial_state["ind_states"].copy()
        self.voltages = initial_state["voltages"].copy()
        self.time = 0.0

        # Recording
        self.recorder = TransientMeasurementRecorder()
        self.state_history: List[CircuitState] = []

        # Control
        self.mode = ControlMode.IDLE
        self.gate_control_func: Optional[Callable[[str, float], float]] = None
        self.analog_gate_control_func: Optional[Callable[[CircuitState], Dict[str, float]]] = None

        # AI hooks
        self.pre_step_hook: Optional[Callable[[CircuitState], None]] = None
        self.post_step_hook: Optional[Callable[[CircuitState], None]] = None

    def set_gate_control(self, func: Callable[[str, float], float]) -> CircuitController:
        """Set the gate voltage control function.

        Args:
            func: function(mosfet_id, time_us) -> gate_voltage

        Returns:
            self for chaining
        """
        self.gate_control_func = func
        return self

    def set_analog_gate_control(self, func: Callable[[CircuitState], Dict[str, float]]) -> CircuitController:
        """Set analog gate control function that receives full circuit state.

        Enables feedback-based proportional/integral gate control.
        Gate voltage varies continuously based on virtual ground feedback.

        Args:
            func: function(state: CircuitState) -> {mosfet_id: gate_voltage_0_to_5V}

        Returns:
            self for chaining
        """
        self.analog_gate_control_func = func
        return self

    def set_ai_hooks(self,
                    pre_step: Optional[Callable] = None,
                    post_step: Optional[Callable] = None) -> CircuitController:
        """Set AI agent hooks for observing/controlling simulation.

        Args:
            pre_step: Called before each step with current state
            post_step: Called after each step with new state

        Returns:
            self for chaining
        """
        self.pre_step_hook = pre_step
        self.post_step_hook = post_step
        return self

    def run_step(self, dt_s: float) -> CircuitState:
        """Execute one simulation step and return state snapshot.

        Args:
            dt_s: timestep in seconds

        Returns:
            CircuitState snapshot
        """
        # Call pre-step hook if set
        if self.pre_step_hook:
            current_state = self._make_state()
            self.pre_step_hook(current_state)

        # Determine gate control function to use
        gate_func = self.gate_control_func

        # If analog gate control is set, call it with current state and wrap result
        if self.analog_gate_control_func:
            current_state = self._make_state()
            analog_voltages = self.analog_gate_control_func(current_state)
            # Convert dict {mosfet_id: voltage} to lambda matching solver's (mosfet_id, time) interface
            gate_func = lambda mosfet_id, time: analog_voltages.get(mosfet_id, 0.0)

        # Solve step
        sol = self.circuit.solve_step(
            initial_cap_states=self.cap_states,
            initial_ind_states=self.ind_states,
            initial_voltages=self.voltages,
            dt=dt_s,
            time=self.time,
            gate_voltage_func=gate_func
        )

        # Update state
        self.cap_states = sol.capacitor_states
        self.ind_states = sol.inductor_states
        self.voltages = sol.voltages
        self.time += dt_s

        # Record
        state = self._make_state()
        self.state_history.append(state)
        self.recorder.record_step(
            time=self.time,
            voltages=sol.voltages,
            source_currents=sol.source_currents,
            inductor_states=sol.inductor_states,
            capacitor_states=sol.capacitor_states,
            mosfet_states=sol.mosfet_states
        )

        # Call post-step hook if set
        if self.post_step_hook:
            self.post_step_hook(state)

        return state

    def run_simulation(self,
                       duration_s: float,
                       dt_s: float,
                       mode: ControlMode = ControlMode.VISUALIZATION) -> List[CircuitState]:
        """Run complete simulation and return history.

        Args:
            duration_s: total simulation time
            dt_s: timestep
            mode: ControlMode.VISUALIZATION or TEST_EXECUTION

        Returns:
            List of CircuitState snapshots
        """
        self.mode = mode
        self.state_history = []

        n_steps = int(duration_s / dt_s)
        for step in range(n_steps):
            try:
                self.run_step(dt_s)
            except Exception as e:
                print(f"ERROR at step {step}: {e}")
                break

        self.mode = ControlMode.IDLE
        return self.state_history

    def _make_state(self) -> CircuitState:
        """Create state snapshot from current simulation."""
        return CircuitState(
            time_us=self.time * 1e6,
            node_voltages=self.voltages.copy(),
            source_currents={},  # Would need to track from sol
            inductor_currents={
                ind_id: state.current
                for ind_id, state in self.ind_states.items()
            },
            mosfet_states={}  # Would need to track from sol
        )

    def run_test(self, test: TestCase) -> TestResult:
        """Execute single test case.

        Args:
            test: TestCase definition

        Returns:
            TestResult with measurements and pass/fail status
        """
        self.mode = ControlMode.TEST_EXECUTION
        self.state_history = []

        dt_s = test.dt_us * 1e-6
        n_steps = int(test.duration_us * 1e-6 / dt_s)

        print(f"\n{'='*70}")
        print(f"TEST: {test.name}")
        print(f"{'='*70}")
        print(test.description)
        print(f"Duration: {test.duration_us:.1f}µs, dt: {test.dt_us:.1f}ns")

        # Run simulation
        self.gate_control_func = test.gate_control_func
        for step in range(n_steps):
            try:
                self.run_step(dt_s)
            except Exception as e:
                print(f"ERROR at step {step}: {e}")
                self.mode = ControlMode.IDLE
                return TestResult(
                    test_name=test.name,
                    status=TestStatus.FAILED,
                    duration_us=self.time * 1e6,
                    measurements={},
                    pass_criteria={},
                    message=f"Simulation error: {e}"
                )

        # Evaluate measurements and pass criteria
        measurements = {}
        criteria_results = {}
        all_passed = True

        for meas_id, meas_spec in test.measurements.items():
            try:
                meas_type = meas_spec.get("type")
                params = meas_spec.get("params", {})

                if meas_type == "node_voltage":
                    node = params.get("node")
                    ts = self.recorder.get_node_voltage(node)
                    value = ts.steady_state() if ts else 0.0
                elif meas_type == "voltage_error":
                    node = params.get("node")
                    target = params.get("target", 0.0)
                    ts = self.recorder.get_node_voltage(node)
                    value = abs(ts.steady_state() - target) if ts else float('inf')
                elif meas_type == "mosfet_duty":
                    mosfet = params.get("mosfet")
                    value = self.recorder.get_mosfet_duty_cycle(mosfet)
                else:
                    value = 0.0

                measurements[meas_id] = value

                # Check against criteria
                if meas_id in test.pass_criteria:
                    min_val, max_val = test.pass_criteria[meas_id]
                    passed = min_val <= value <= max_val
                    criteria_results[meas_id] = (min_val, max_val, passed)
                    if not passed:
                        all_passed = False
            except Exception as e:
                print(f"ERROR measuring {meas_id}: {e}")
                measurements[meas_id] = float('nan')
                all_passed = False

        status = TestStatus.PASSED if all_passed else TestStatus.FAILED

        result = TestResult(
            test_name=test.name,
            status=status,
            duration_us=self.time * 1e6,
            measurements=measurements,
            pass_criteria=criteria_results,
            message="All criteria met" if all_passed else "Some criteria failed"
        )

        # Print summary
        print(f"\nMeasurements:")
        for meas_id, value in measurements.items():
            if meas_id in criteria_results:
                minv, maxv, passed = criteria_results[meas_id]
                status_str = "✓" if passed else "✗"
                print(f"  {status_str} {meas_id}: {value:.6f} (range: {minv:.6f} to {maxv:.6f})")
            else:
                print(f"    {meas_id}: {value:.6f}")

        print(f"\nResult: {result.status.value.upper()}")
        print(f"{'='*70}\n")

        self.mode = ControlMode.IDLE
        return result

    def run_test_suite(self, tests: List[TestCase]) -> List[TestResult]:
        """Execute multiple tests in sequence.

        Args:
            tests: List of TestCase definitions

        Returns:
            List of TestResult objects
        """
        results = []
        for test in tests:
            results.append(self.run_test(test))

        # Summary
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        print(f"\n{'='*70}")
        print(f"TEST SUITE SUMMARY: {passed}/{len(results)} PASSED")
        print(f"{'='*70}")
        for r in results:
            status_icon = "✓" if r.status == TestStatus.PASSED else "✗"
            print(f"  {status_icon} {r.test_name}: {r.status.value}")

        return results

    def get_visualization_data(self) -> dict:
        """Get data formatted for visualization (JSON for web client).

        Returns:
            Dict with circuit topology and state history suitable for 3D rendering
        """
        return {
            "circuit_info": {
                "component_count": len([c for c in dir(self.circuit) if c.startswith('_') is False]),
                "simulation_time_us": self.time * 1e6
            },
            "state_history": [s.to_dict() for s in self.state_history[-1000:]],  # Last 1000 steps
            "measurements_summary": {
                "nodes": list(self.recorder.node_voltages.keys()),
                "inductors": list(self.recorder.inductor_currents.keys()),
                "mosfets": list(self.recorder.mosfet_states.keys())
            }
        }

    def export_results(self, base_filename: str) -> None:
        """Export test results and measurements.

        Args:
            base_filename: Base name for output files (without extension)
        """
        # Export time-series data
        self.recorder.export_json(f"{base_filename}_waveforms.json")

        # Export state history
        with open(f"{base_filename}_state_history.json", 'w') as f:
            json.dump(
                [s.to_dict() for s in self.state_history],
                f,
                indent=2
            )

        # Export summary
        with open(f"{base_filename}_summary.txt", 'w') as f:
            f.write(self.recorder.summary())

        print(f"\nResults exported to {base_filename}_*")


# Example usage and test definitions
if __name__ == "__main__":
    # Build P0 circuit
    builder = P0TernaryCircuit(v_supply=5.0)
    circuit, initial_state = builder.build(supply_mode="single")

    # Create controller
    controller = CircuitController(circuit, initial_state)

    # Define a simple test
    def gate_voltage_all_off(mosfet_id: str, t: float) -> float:
        return 0.0

    test_dc_steady = TestCase(
        name="DC Steady-State (All Gates OFF)",
        description="Verify virtual ground stability at V_0 = 2.5V with all MOSFETs off",
        duration_us=50.0,
        dt_us=1.0,
        gate_control_func=gate_voltage_all_off,
        measurements={
            "vg_steady": {
                "type": "node_voltage",
                "params": {"node": "0"}
            },
            "vg_error": {
                "type": "voltage_error",
                "params": {"node": "0", "target": 2.5}
            }
        },
        pass_criteria={
            "vg_steady": (2.4, 2.6),
            "vg_error": (0.0, 0.1)
        }
    )

    # Run test
    result = controller.run_test(test_dc_steady)

    # Export results
    controller.export_results("/tmp/p0_test_results")
