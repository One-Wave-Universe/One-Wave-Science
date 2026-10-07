#!/usr/bin/env python3
"""
H-Bridge Damped Test: A->B State Transfer

Tests the damped version with parallel resistors at memory
input nodes to prevent inductor ringing.
"""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_hbridge_damped import P0HexagonHBridgeDamped
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class DampedABTransferTest:
    """Test A->B state transfer with damped memory inputs."""

    def __init__(self):
        print("Building P0 hexagon H-bridge with damped memory inputs...")
        builder = P0HexagonHBridgeDamped(
            v_supply=1.0,
            memory_input_damping_ohms=100000.0
        )
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def test_ab_transfer(self,
                         drive_pulse_us: float = 50.0,
                         drive_direction: str = "high",
                         settling_time_us: float = 200.0,
                         dt_s: float = 1e-6) -> dict:
        """Test A->B state transfer with damped circuit."""
        # Reset
        builder = P0HexagonHBridgeDamped(v_supply=1.0)
        circuit, initial_state = builder.build()
        self.controller = CircuitController(circuit, initial_state)

        # Collect baseline
        n_baseline = int(10e-6 / dt_s)
        for _ in range(n_baseline):
            self.controller.run_step(dt_s)

        state = self.controller._make_state()
        baseline_a_sense = state.node_voltages.get('sense_A_pos', 0.5)
        baseline_b_memory = state.node_voltages.get('memory_B_pos_in', 0.5)

        # Drive pulse timing
        drive_start = 10e-6
        drive_end = drive_start + drive_pulse_us * 1e-6

        def gate_control(mosfet_id: str, time: float) -> float:
            """Independent gate control."""
            hs_off = 0.9
            ls_off = 0.2
            hs_on = 0.2
            ls_on = 0.9

            if "a_pos_HS" in mosfet_id:
                if drive_start <= time < drive_end:
                    return hs_on if drive_direction == "high" else hs_off
                else:
                    return hs_off
            elif "a_pos_LS" in mosfet_id:
                if drive_start <= time < drive_end:
                    return ls_off if drive_direction == "high" else ls_on
                else:
                    return ls_off
            elif "a_neg_HS" in mosfet_id:
                if drive_start <= time < drive_end:
                    return hs_off if drive_direction == "high" else hs_on
                else:
                    return hs_off
            elif "a_neg_LS" in mosfet_id:
                if drive_start <= time < drive_end:
                    return ls_on if drive_direction == "high" else ls_off
                else:
                    return ls_off
            else:
                return hs_off if "HS" in mosfet_id else ls_off

        self.controller.set_gate_control(gate_control)

        # Run drive + settling
        total_time_s = settling_time_us * 1e-6
        n_steps = int(total_time_s / dt_s)

        a_sense_history = []
        b_memory_history = []
        diverged = False
        error_msg = ""

        for step in range(n_steps):
            time = 10e-6 + step * dt_s
            try:
                self.controller.run_step(dt_s)
                state = self.controller._make_state()

                a_sense = state.node_voltages.get('sense_A_pos', 0.5)
                b_memory = state.node_voltages.get('memory_B_pos_in', 0.5)

                a_sense_history.append(a_sense)
                b_memory_history.append(b_memory)

                # Check for divergence
                if a_sense > 1.5 or a_sense < -0.5 or b_memory > 1.5 or b_memory < -0.5:
                    diverged = True
                    error_msg = f'Divergence at t={time*1e6:.1f}µs'
                    break

            except Exception as e:
                diverged = True
                error_msg = f'Exception: {str(e)}'
                break

        # Analyze
        final_a_sense = a_sense_history[-1] if a_sense_history else baseline_a_sense
        final_b_memory = b_memory_history[-1] if b_memory_history else baseline_b_memory

        peak_a_activity = max(abs(v - baseline_a_sense) for v in a_sense_history) if a_sense_history else 0.0
        peak_b_memory_change = max(abs(v - baseline_b_memory) for v in b_memory_history) if b_memory_history else 0.0
        retention = final_b_memory - baseline_b_memory

        if diverged:
            status = 'FAIL'
            reason = error_msg
        elif peak_a_activity > 0.01 and peak_b_memory_change > 0.01 and abs(retention) > 0.005:
            status = 'PASS'
            reason = f'A->B transfer demonstrated'
        elif peak_a_activity > 0.01:
            status = 'UNCERTAIN'
            reason = f'A active but B coupling weak'
        else:
            status = 'FAIL'
            reason = f'No A activity'

        return {
            'baseline_a_sense': baseline_a_sense,
            'baseline_b_memory': baseline_b_memory,
            'peak_a_activity': peak_a_activity,
            'peak_b_memory_change': peak_b_memory_change,
            'final_a_sense': final_a_sense,
            'final_b_memory': final_b_memory,
            'retention': retention,
            'status': status,
            'reason': reason
        }

    def run_test_series(self):
        """Run A->B transfer tests."""
        print("\n" + "="*80)
        print("H-BRIDGE DAMPED MEMORY INPUTS: A->B STATE TRANSFER TEST")
        print("="*80)
        print("\nCircuit improvements:")
        print("  Memory input damping: 100kΩ resistors to VREF")
        print("  Reduces inductor transient ringing")
        print("  Improved numerical stability")
        print("\nTesting A->B state transfer...\n")

        directions = ["high", "low"]
        results = []

        for drive_dir in directions:
            print(f"Testing A drive direction={drive_dir}...")
            result = self.test_ab_transfer(drive_direction=drive_dir)
            results.append(result)

            print(f"  Baseline A sense: {result['baseline_a_sense']:.4f}V")
            print(f"  Baseline B memory: {result['baseline_b_memory']:.4f}V")
            print(f"  Peak A activity: {result['peak_a_activity']:.4f}V")
            print(f"  Peak B memory change: {result['peak_b_memory_change']:.4f}V")
            print(f"  Final B memory: {result['final_b_memory']:.4f}V")
            print(f"  Retention Δ: {result['retention']:.6f}V")
            print(f"  Status: {result['status']} - {result['reason']}\n")

        return results


def main():
    test = DampedABTransferTest()
    results = test.run_test_series()

    # Summary
    print("="*80)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    uncertain = sum(1 for r in results if r['status'] == 'UNCERTAIN')
    failed = sum(1 for r in results if r['status'] == 'FAIL')

    print(f"\nSUMMARY:")
    print(f"  PASS: {passed}/{len(results)}")
    print(f"  UNCERTAIN: {uncertain}/{len(results)}")
    print(f"  FAIL: {failed}/{len(results)}")

    if passed > 0:
        print("\n✓ A->B STATE TRANSFER DEMONSTRATED")
    elif uncertain > 0:
        print("\n~ TRANSFER DETECTED BUT WEAK")
    else:
        print("\n✗ NO A->B TRANSFER")
        print("  Check circuit parameters or solver settings.")


if __name__ == "__main__":
    main()
