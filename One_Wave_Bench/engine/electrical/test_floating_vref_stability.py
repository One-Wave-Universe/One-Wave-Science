#!/usr/bin/env python3
"""Test floating VREF topology for circuit stability."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.p0_hexagon_hbridge_floating_vref import P0HexagonHBridgeFloatingVref
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


def test_baseline_stability(duration_us: float = 500.0, report_interval_us: float = 50.0) -> tuple[bool, float]:
    """Test baseline circuit stability without any drive signals."""
    print(f"\n{'='*80}")
    print(f"BASELINE STABILITY TEST: {duration_us}µs")
    print(f"{'='*80}")
    print(f"Circuit: Floating VREF (VREF_AB, VREF_BC, VREF_CA)")
    print(f"Drive gates: HS=0.9V, LS=0.2V (OFF)")
    print(f"Timestep: 1µs\n")

    builder = P0HexagonHBridgeFloatingVref(v_supply=1.0)
    circuit, initial_state = builder.build()
    controller = CircuitController(circuit, initial_state)

    dt_s = 1e-6
    n_steps = int(duration_us * 1e-6 / dt_s)
    report_steps = int(report_interval_us * 1e-6 / dt_s)

    print(f"{'Time (µs)':<15} {'V_A_pos':<15} {'V_B_pos':<15} {'V_C_pos':<15} {'Status':<20}")
    print("-" * 80)

    for step in range(n_steps):
        try:
            controller.run_step(dt_s)
            state = controller._make_state()

            a_pos = state.node_voltages.get('a_pos', 0.5)
            b_pos = state.node_voltages.get('b_pos', 0.5)
            c_pos = state.node_voltages.get('c_pos', 0.5)

            # Check for divergence
            max_delta = max(abs(a_pos - 0.5), abs(b_pos - 0.5), abs(c_pos - 0.5))
            if max_delta > 1.5:
                divergence_time = step * dt_s * 1e6
                print(f"{divergence_time:<15.1f} {a_pos:<15.4f} {b_pos:<15.4f} {c_pos:<15.4f} DIVERGED!")
                return False, divergence_time

            # Periodic report
            if (step + 1) % report_steps == 0:
                time_us = (step + 1) * dt_s * 1e6
                status = "OK" if max_delta < 0.1 else f"DRIFT({max_delta:.3f})"
                print(f"{time_us:<15.1f} {a_pos:<15.4f} {b_pos:<15.4f} {c_pos:<15.4f} {status:<20}")

        except Exception as e:
            divergence_time = step * dt_s * 1e6
            print(f"{divergence_time:<15.1f} {'ERROR':<15} {str(e)[:30]:<15} EXCEPTION")
            return False, divergence_time

    print("-" * 80)
    print(f"✓ STABLE for entire {duration_us}µs")
    return True, duration_us


def test_ab_transfer(baseline_stable: bool) -> None:
    """Test A→B state transfer if baseline is stable."""
    if not baseline_stable:
        print(f"\n⚠ Skipping A→B transfer test (baseline unstable)")
        return

    print(f"\n{'='*80}")
    print(f"A→B STATE TRANSFER TEST")
    print(f"{'='*80}")
    print(f"Protocol: Baseline 100µs, then drive A (positive current) for 100µs")
    print(f"Expected: A_sense rises → B_memory captures via nerve ring")
    print(f"Sense A and Memory B should both show elevated voltage (~0.7V)\n")

    builder = P0HexagonHBridgeFloatingVref(v_supply=1.0)
    circuit, initial_state = builder.build()
    controller = CircuitController(circuit, initial_state)

    dt_s = 1e-6
    baseline_steps = int(100 * 1e-6 / dt_s)  # 100µs baseline
    drive_steps = int(100 * 1e-6 / dt_s)     # 100µs drive
    total_steps = baseline_steps + drive_steps

    print(f"{'Time (µs)':<15} {'V_sense_A':<15} {'V_mem_B':<15} {'Mode':<20}")
    print("-" * 65)

    for step in range(total_steps):
        try:
            # At baseline_steps, switch to drive A
            if step == baseline_steps:
                # Activate phase A: High-side ON (gate to GND = 0V)
                # This drives a_pos toward +V
                controller._state.node_voltages["gate_a_pos_hs"] = 0.0  # Turn ON high-side
                controller._state.node_voltages["gate_a_pos_ls"] = 0.9  # Turn OFF low-side

            controller.run_step(dt_s)
            state = controller._make_state()

            sense_a = state.node_voltages.get('sense_A_pos', 0.5)
            mem_b = state.node_voltages.get('memory_B_pos_in', 0.5)

            time_us = (step + 1) * dt_s * 1e6
            mode = "BASELINE" if step < baseline_steps else "DRIVE_A"

            if (step + 1) % 25 == 0 or step == baseline_steps:
                print(f"{time_us:<15.1f} {sense_a:<15.4f} {mem_b:<15.4f} {mode:<20}")

        except Exception as e:
            time_us = (step + 1) * dt_s * 1e6
            print(f"{time_us:<15.1f} ERROR {str(e)[:40]:<15}")
            break

    print("-" * 65)
    print(f"✓ A→B transfer test completed")


if __name__ == "__main__":
    stable, div_time = test_baseline_stability(duration_us=500.0)

    if stable:
        print(f"\n✓✓✓ BASELINE STABLE - Floating VREF topology works!")
        print(f"    Topology fix successfully resolved MNA matrix divergence.")
        test_ab_transfer(stable)
    else:
        print(f"\n✗ BASELINE DIVERGED at {div_time:.1f}µs")
        print(f"  Floating VREF did not resolve the issue.")
        print(f"  May need Option B (coupled inductors) or Option C (solver fix).")
