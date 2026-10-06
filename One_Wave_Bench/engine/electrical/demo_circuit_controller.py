#!/usr/bin/env python3
"""
Demo: Circuit Controller with Visualization, AI Control, and Testing Modes

This demo shows all three modes of the CircuitController:
1. VISUALIZATION: Record live circuit state for WebSocket/visualization
2. AI_CONTROL: AI agent observes and controls gates in real-time
3. TEST_EXECUTION: Automated test suite execution

Usage:
  python demo_circuit_controller.py --mode visualization
  python demo_circuit_controller.py --mode ai-control
  python demo_circuit_controller.py --mode test
  python demo_circuit_controller.py --all
"""
from __future__ import annotations
import sys
import json
import argparse
from pathlib import Path

# Add repo root to path for imports
repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_ternary_circuit import P0TernaryCircuit
from One_Wave_Bench.engine.electrical.circuit_controller import (
    CircuitController, ControlMode, TestCase, CircuitState
)


def demo_visualization_mode():
    """Record circuit state history for visualization."""
    print("\n" + "="*70)
    print("DEMO: VISUALIZATION MODE (Live State Recording)")
    print("="*70)

    # Build P0 circuit
    builder = P0TernaryCircuit(v_supply=5.0)
    circuit, initial_state = builder.build(supply_mode="single")
    controller = CircuitController(circuit, initial_state)

    # Simple gate control: gates stay off for now
    def gate_control_off(mosfet_id: str, time_us: float) -> float:
        return 0.0  # All gates off

    controller.set_gate_control(gate_control_off)

    # Run simulation in visualization mode
    duration_s = 100e-6  # 100 microseconds
    dt_s = 1e-6  # 1 microsecond timesteps

    print(f"\nRunning {duration_s*1e6:.1f}µs simulation with {dt_s*1e6:.1f}µs timesteps")
    state_history = controller.run_simulation(
        duration_s=duration_s,
        dt_s=dt_s,
        mode=ControlMode.VISUALIZATION
    )

    print(f"\nRecorded {len(state_history)} states")
    print(f"Final time: {state_history[-1].time_us:.1f}µs" if state_history else "No states")

    # Show sample state
    if state_history:
        final_state = state_history[-1]
        print(f"\nFinal state snapshot:")
        print(f"  V(+V) = {final_state.node_voltages.get('+V', 0):.3f}V")
        print(f"  V(0) = {final_state.node_voltages.get('0', 0):.3f}V (virtual ground)")
        print(f"  V(GND) = {final_state.node_voltages.get('GND', 0):.3f}V")

    # Export visualization data (format suitable for WebSocket/HTML5)
    viz_data = controller.get_visualization_data()
    print(f"\nVisualization data ready:")
    print(f"  Simulation time: {viz_data['circuit_info']['simulation_time_us']:.1f}µs")
    print(f"  Tracked nodes: {viz_data['measurements_summary']['nodes']}")
    print(f"  Tracked inductors: {viz_data['measurements_summary']['inductors']}")

    return controller


def demo_ai_control_mode():
    """AI agent observes and controls gates in real-time."""
    print("\n" + "="*70)
    print("DEMO: AI CONTROL MODE (Agent Observation & Gate Control)")
    print("="*70)

    # Build P0 circuit
    builder = P0TernaryCircuit(v_supply=5.0)
    circuit, initial_state = builder.build(supply_mode="single")
    controller = CircuitController(circuit, initial_state)

    # AI agent state
    ai_state = {
        "observations": [],
        "gate_decisions": [],
        "vg_target": 2.5,  # Target virtual ground voltage
    }

    # Pre-step hook: AI observes state
    def ai_observe_pre(state: CircuitState) -> None:
        vg = state.node_voltages.get('0', 2.5)
        ai_state["observations"].append({
            "time_us": state.time_us,
            "vg_voltage": vg,
            "vg_error": abs(vg - ai_state["vg_target"]),
        })

    # Post-step hook: AI decides gate control based on observations
    def ai_control_post(state: CircuitState) -> None:
        # Simple proportional control: if V_G is below target, try to raise it
        vg = state.node_voltages.get('0', 2.5)
        error = vg - ai_state["vg_target"]

        # For now, just record the decision
        if len(ai_state["observations"]) > 0:
            obs = ai_state["observations"][-1]
            decision = "HOLD"  # Default: no gate switching yet
            if error > 0.05:
                decision = "LOWER"  # V_G too high
            elif error < -0.05:
                decision = "RAISE"  # V_G too low

            ai_state["gate_decisions"].append({
                "time_us": obs["time_us"],
                "vg_error": obs["vg_error"],
                "decision": decision,
            })

    # Gate control follows AI decisions (for now just off)
    def gate_control_ai(mosfet_id: str, time_us: float) -> float:
        return 0.0  # AI decides gates stay off for DC analysis

    controller.set_gate_control(gate_control_ai)
    controller.set_ai_hooks(pre_step=ai_observe_pre, post_step=ai_control_post)

    # Run simulation in AI control mode
    duration_s = 50e-6  # 50 microseconds
    dt_s = 1e-6  # 1 microsecond timesteps

    print(f"\nRunning AI-controlled simulation ({duration_s*1e6:.1f}µs)")
    controller.run_simulation(
        duration_s=duration_s,
        dt_s=dt_s,
        mode=ControlMode.AI_CONTROL
    )

    # Show AI results
    print(f"\nAI Agent Results:")
    print(f"  Total observations: {len(ai_state['observations'])}")
    print(f"  Total gate decisions: {len(ai_state['gate_decisions'])}")

    if ai_state["observations"]:
        first_obs = ai_state["observations"][0]
        last_obs = ai_state["observations"][-1]
        print(f"\n  Initial V_G error: {first_obs['vg_error']:.6f}V")
        print(f"  Final V_G error: {last_obs['vg_error']:.6f}V")
        print(f"  V_G stability: {'MAINTAINED' if last_obs['vg_error'] < 0.01 else 'DRIFT DETECTED'}")

    return controller, ai_state


def demo_test_execution_mode():
    """Execute automated test suite."""
    print("\n" + "="*70)
    print("DEMO: TEST EXECUTION MODE (Automated Test Suite)")
    print("="*70)

    # Build P0 circuit
    builder = P0TernaryCircuit(v_supply=5.0)
    circuit, initial_state = builder.build(supply_mode="single")
    controller = CircuitController(circuit, initial_state)

    # Define test cases
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

    # Run single test
    print(f"\nExecuting test: {test_dc_steady.name}")
    result = controller.run_test(test_dc_steady)

    # Show result
    print(f"\nTest Result:")
    print(f"  Status: {result.status.value.upper()}")
    print(f"  Message: {result.message}")

    return controller, result


def main():
    parser = argparse.ArgumentParser(
        description="Circuit Controller Demo: Visualization, AI Control, and Testing"
    )
    parser.add_argument(
        "--mode",
        choices=["visualization", "ai-control", "test"],
        help="Run specific demo mode"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all three demo modes in sequence"
    )
    args = parser.parse_args()

    if not args.mode and not args.all:
        parser.print_help()
        print("\nNo mode specified. Use --mode or --all")
        sys.exit(1)

    # Run demos based on arguments
    if args.all or args.mode == "visualization":
        demo_visualization_mode()

    if args.all or args.mode == "ai-control":
        demo_ai_control_mode()

    if args.all or args.mode == "test":
        demo_test_execution_mode()

    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
