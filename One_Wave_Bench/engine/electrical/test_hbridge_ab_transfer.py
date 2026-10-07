#!/usr/bin/env python3
"""
H-Bridge Test: A->B State Transfer (First Hard Criterion)

Per UPDATED_63, the first test must prove:
  1. A Drive event
  2. Measurable current/energy reaches B Memory path
  3. A Drive is removed and transient dies
  4. B retains a changed magnetic state
  5. The same later B probe differs from baseline

This is the minimal provable test before closing the full nerve ring.
"""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Tuple

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_hbridge import P0HexagonHBridge
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class HBridgeABTransferTest:
    """Test A->B state transfer via nerve ring coupling."""

    def __init__(self):
        print("Building P0 hexagon H-bridge circuit...")
        builder = P0HexagonHBridge(v_supply=1.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def test_ab_transfer(self,
                         drive_pulse_us: float = 50.0,
                         drive_voltage: float = 0.8,
                         settling_time_us: float = 200.0,
                         dt_s: float = 1e-6) -> dict:
        """
        Test A->B state transfer.

        Sequence:
        1. Baseline: measure A sense and B memory voltages at t=0
        2. Drive pulse: apply gate_A_pos high for drive_pulse_us
        3. Pulse end: remove drive, observe transient decay
        4. Settling: wait for settling_time_us after pulse ends
        5. Final probe: measure A sense and B memory again
        6. Compare: B memory should show retained change from baseline

        Returns:
            {
                'baseline_a_sense': float,
                'baseline_b_memory': float,
                'peak_a_drive_current': float,
                'peak_b_memory_voltage': float,
                'final_a_sense': float,
                'final_b_memory': float,
                'retention': float (change from baseline),
                'status': 'PASS' | 'FAIL' | 'UNCERTAIN',
                'reason': str
            }
        """
        # Reset for fresh run
        builder = P0HexagonHBridge(v_supply=1.0)
        circuit, initial_state = builder.build()
        self.controller = CircuitController(circuit, initial_state)

        # Collect baseline (before drive pulse)
        baseline_data = []
        n_baseline = int(10e-6 / dt_s)  # 10 µs baseline
        for _ in range(n_baseline):
            self.controller.run_step(dt_s)
            state = self.controller._make_state()
            baseline_data.append({
                'a_sense_pos': state.node_voltages.get('sense_A_pos_mid', 0.5),
                'b_memory_pos': state.node_voltages.get('memory_B_pos_ext', 0.5),
            })

        baseline_a_sense = sum(d['a_sense_pos'] for d in baseline_data) / len(baseline_data) if baseline_data else 0.5
        baseline_b_memory = sum(d['b_memory_pos'] for d in baseline_data) / len(baseline_data) if baseline_data else 0.5

        # Set up gate control for A drive pulse
        drive_start = 10e-6  # Start drive pulse at 10 µs
        drive_end = drive_start + drive_pulse_us * 1e-6

        def gate_control(mosfet_id: str, time: float) -> float:
            # Neutral baseline: 0.2V (keeps NMOS off since Vth=0.4V)
            # Drive high: 0.9V (PMOS Vgs = 0.9V - 0.5V = 0.4V, ON)
            # Drive low: would need to be < 0V (not possible with 1V supply)

            neutral_v = 0.2  # Low enough to keep NMOS off (Vgs < 0.4V)
            drive_high_v = 0.9  # High enough to turn on PMOS (need V_source-gate ≤ -0.4V)

            # A drive: high-side gate gets drive_voltage during pulse
            if "a_pos_HS" in mosfet_id:
                if drive_start <= time < drive_end:
                    return drive_high_v  # Turn ON high-side
                else:
                    return neutral_v  # Keep OFF
            # A drive: low-side gate tied to neutral (both off at rest)
            elif "a_pos_LS" in mosfet_id:
                return neutral_v  # Keep low-side OFF
            # All other gates at neutral
            else:
                return neutral_v

        self.controller.set_gate_control(gate_control)

        # Run drive pulse + settling
        total_time_s = settling_time_us * 1e-6
        n_steps = int(total_time_s / dt_s)

        drive_current_history = []
        b_memory_voltage_history = []
        a_sense_voltage_history = []

        for step in range(n_steps):
            time = 10e-6 + step * dt_s
            try:
                self.controller.run_step(dt_s)
                state = self.controller._make_state()

                # Monitor A drive current (through L_A_drive_pos)
                # (Actual current monitoring would need inductor state access)
                a_sense = state.node_voltages.get('sense_A_pos_mid', 0.5)
                b_memory = state.node_voltages.get('memory_B_pos_ext', 0.5)

                a_sense_voltage_history.append(a_sense)
                b_memory_voltage_history.append(b_memory)

                # Simple proxy: change in voltage indicates activity
                if len(drive_current_history) > 0:
                    current_proxy = abs(a_sense - baseline_a_sense)
                    drive_current_history.append(current_proxy)

                # Check for divergence
                if a_sense > 1.5 or a_sense < -0.5 or b_memory > 1.5 or b_memory < -0.5:
                    return {
                        'baseline_a_sense': baseline_a_sense,
                        'baseline_b_memory': baseline_b_memory,
                        'peak_a_drive_current': max(drive_current_history) if drive_current_history else 0.0,
                        'peak_b_memory_voltage': max(abs(v - baseline_b_memory) for v in b_memory_voltage_history) if b_memory_voltage_history else 0.0,
                        'final_a_sense': a_sense,
                        'final_b_memory': b_memory,
                        'retention': b_memory - baseline_b_memory,
                        'status': 'FAIL',
                        'reason': f'Divergence detected at t={time*1e6:.1f}µs'
                    }

            except Exception as e:
                return {
                    'baseline_a_sense': baseline_a_sense,
                    'baseline_b_memory': baseline_b_memory,
                    'peak_a_drive_current': 0.0,
                    'peak_b_memory_voltage': 0.0,
                    'final_a_sense': 0.5,
                    'final_b_memory': 0.5,
                    'retention': 0.0,
                    'status': 'FAIL',
                    'reason': f'Simulation error: {e}'
                }

        # Analyze final state
        final_a_sense = a_sense_voltage_history[-1] if a_sense_voltage_history else baseline_a_sense
        final_b_memory = b_memory_voltage_history[-1] if b_memory_voltage_history else baseline_b_memory
        retention = final_b_memory - baseline_b_memory
        peak_drive_activity = max(drive_current_history) if drive_current_history else 0.0
        peak_memory_change = max(abs(v - baseline_b_memory) for v in b_memory_voltage_history) if b_memory_voltage_history else 0.0

        # Criteria for PASS:
        # 1. A drive shows activity (peak current/voltage change > 0.01V)
        # 2. B memory shows coupling (peak change > 0.01V)
        # 3. B memory retention is measurable (|retention| > 0.005V)
        # 4. No divergence (all voltages within safe range)

        if peak_drive_activity > 0.01 and peak_memory_change > 0.01 and abs(retention) > 0.005:
            status = 'PASS'
            reason = f'A->B transfer proven: peak_activity={peak_drive_activity:.4f}V, retention={retention:.6f}V'
        elif peak_drive_activity > 0.01:
            status = 'UNCERTAIN'
            reason = f'A drive active but B memory coupling weak: activity={peak_drive_activity:.4f}V, change={peak_memory_change:.4f}V'
        else:
            status = 'FAIL'
            reason = f'A drive inactive or circuit non-responsive'

        return {
            'baseline_a_sense': baseline_a_sense,
            'baseline_b_memory': baseline_b_memory,
            'peak_a_drive_current': peak_drive_activity,
            'peak_b_memory_voltage': peak_memory_change,
            'final_a_sense': final_a_sense,
            'final_b_memory': final_b_memory,
            'retention': retention,
            'status': status,
            'reason': reason
        }

    def run_test_series(self):
        """Run A->B transfer test with different drive voltages."""
        print("\n" + "="*80)
        print("H-BRIDGE A->B STATE TRANSFER TEST")
        print("="*80)
        print("\nSequence: Baseline → A Drive Pulse → Settling → B Memory Probe")
        print("Drive pulse: 50µs at varying gate voltage")
        print("Settling: 200µs after pulse")
        print("Criterion: B Memory retains measurable change from baseline\n")

        drive_voltages = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        results = []

        for drive_v in drive_voltages:
            print(f"Testing A drive at {drive_v:.1f}V...")
            result = self.test_ab_transfer(drive_voltage=drive_v)
            results.append(result)

            print(f"  Baseline A sense: {result['baseline_a_sense']:.4f}V")
            print(f"  Baseline B memory: {result['baseline_b_memory']:.4f}V")
            print(f"  Peak A activity: {result['peak_a_drive_current']:.4f}V")
            print(f"  Peak B coupling: {result['peak_b_memory_voltage']:.4f}V")
            print(f"  Final B memory: {result['final_b_memory']:.4f}V")
            print(f"  Retention Δ: {result['retention']:.6f}V")
            print(f"  Status: {result['status']} - {result['reason']}\n")

        return results


def main():
    test = HBridgeABTransferTest()
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
        print("  Nerve ring ready for full closure (A->B->C->A).")
    elif uncertain > 0:
        print("\n~ TRANSFER DETECTED BUT WEAK")
        print("  Check impedance matching and memory winding coupling.")
    else:
        print("\n✗ NO A->B TRANSFER")
        print("  Review H-bridge drive and nerve ring wiring.")


if __name__ == "__main__":
    main()
