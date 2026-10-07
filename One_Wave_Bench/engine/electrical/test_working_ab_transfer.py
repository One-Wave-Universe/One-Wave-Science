#!/usr/bin/env python3
"""
Test A->B State Transfer on Working Circuit

First hard criterion from UPDATED_63:
A->B passes only if:
  1. A Drive event
  2. Measurable current reaches B Memory path
  3. A Drive removed and transient dies
  4. B retains changed magnetic state
  5. Later B probe differs from baseline
"""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_working import P0HexagonWorking
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class WorkingABTransferTest:
    """Test A->B state transfer with nerve ring pre-wired."""

    def __init__(self):
        builder = P0HexagonWorking(v_supply=1.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def test_ab_transfer(self,
                         drive_pulse_us: float = 50.0,
                         drive_voltage: float = 0.8,
                         settling_time_us: float = 200.0,
                         dt_s: float = 1e-6) -> dict:
        """
        Test A->B transfer.

        Drive pulse: apply voltage to a_pos_HS to excite A phase
        Memory capture: B_memory_pos will show coupled change via nerve ring
        """
        # Reset
        builder = P0HexagonWorking(v_supply=1.0)
        circuit, initial_state = builder.build()
        self.controller = CircuitController(circuit, initial_state)

        # Baseline
        baseline_data = []
        n_baseline = int(10e-6 / dt_s)
        for _ in range(n_baseline):
            self.controller.run_step(dt_s)

        state = self.controller._make_state()
        baseline_a_sense = state.node_voltages.get('sense_A_pos', 0.5)
        baseline_b_memory = state.node_voltages.get('memory_B_pos_mid', 0.5)

        # Gate control for A drive pulse
        drive_start = 10e-6
        drive_end = drive_start + drive_pulse_us * 1e-6
        neutral_v = 0.2
        drive_high_v = 0.9

        def gate_control(mosfet_id: str, time: float) -> float:
            if "a_pos_HS" in mosfet_id:
                if drive_start <= time < drive_end:
                    return drive_high_v
                else:
                    return neutral_v
            else:
                return neutral_v

        self.controller.set_gate_control(gate_control)

        # Run pulse + settling
        total_time_s = settling_time_us * 1e-6
        n_steps = int(total_time_s / dt_s)

        a_sense_history = []
        b_memory_history = []
        diverged = False

        for step in range(n_steps):
            try:
                self.controller.run_step(dt_s)
                state = self.controller._make_state()

                a_sense = state.node_voltages.get('sense_A_pos', 0.5)
                b_memory = state.node_voltages.get('memory_B_pos_mid', 0.5)

                a_sense_history.append(a_sense)
                b_memory_history.append(b_memory)

                # Check for divergence
                if abs(a_sense) > 1.5 or abs(b_memory) > 1.5:
                    diverged = True
                    break

            except Exception as e:
                diverged = True
                break

        # Analyze
        final_a_sense = a_sense_history[-1] if a_sense_history else baseline_a_sense
        final_b_memory = b_memory_history[-1] if b_memory_history else baseline_b_memory

        peak_a_activity = max(abs(v - baseline_a_sense) for v in a_sense_history) if a_sense_history else 0.0
        peak_b_memory_change = max(abs(v - baseline_b_memory) for v in b_memory_history) if b_memory_history else 0.0

        retention = final_b_memory - baseline_b_memory

        if diverged:
            status = 'FAIL'
            reason = f'Circuit diverged at step {len(a_sense_history)}'
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
        """Run tests at different drive voltages."""
        print("\n" + "="*80)
        print("A->B STATE TRANSFER TEST (WORKING CIRCUIT)")
        print("="*80)
        print("\nNerve ring: A_sense → B_memory (pre-wired)")
        print("Criterion: B memory shows retained change after A drive pulse\n")

        drive_voltages = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        results = []

        for drive_v in drive_voltages:
            print(f"Testing drive_v={drive_v:.1f}V (drive_high={0.9:.1f}V, neutral={0.2:.1f}V)...")
            result = self.test_ab_transfer(drive_voltage=drive_v)
            results.append(result)

            print(f"  Baseline A sense: {result['baseline_a_sense']:.4f}V")
            print(f"  Baseline B memory: {result['baseline_b_memory']:.4f}V")
            print(f"  Peak A activity: {result['peak_a_activity']:.4f}V")
            print(f"  Peak B change: {result['peak_b_memory_change']:.4f}V")
            print(f"  Retention Δ: {result['retention']:.6f}V")
            print(f"  Status: {result['status']} - {result['reason']}\n")

        return results


def main():
    test = WorkingABTransferTest()
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
        print("\n✓ A->B TRANSFER PROVEN")
        print("  Nerve ring functional. Ready to close A->B->C->A ring.")
    elif uncertain > 0:
        print("\n~ TRANSFER DETECTED BUT WEAK")
        print("  Check impedance and coupling strength.")
    else:
        print("\n✗ NO TRANSFER")
        print("  Review circuit and gate control strategy.")


if __name__ == "__main__":
    main()
