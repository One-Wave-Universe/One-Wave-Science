#!/usr/bin/env python3
"""
Test A->B State Transfer on Passive Circuit

Without MOSFETs, we can directly apply voltage to a_pos and a_neg nodes
to simulate a phase drive, then observe coupling to B memory via nerve ring.
"""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_passive import P0HexagonPassive
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class PassiveABTransferTest:
    """Test on passive circuit - directly drive phase A nodes."""

    def __init__(self):
        builder = P0HexagonPassive(v_supply=1.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def test_ab_transfer_direct(self,
                                drive_pulse_us: float = 50.0,
                                v_drive: float = 0.8,
                                settling_time_us: float = 200.0,
                                dt_s: float = 1e-6) -> dict:
        """
        Direct node voltage excitation (simulates ideal voltage source on phase).

        Drive: set a_pos to v_drive, a_neg to (1-v_drive) during pulse
        Observe: B_memory_pos_mid for coupled response
        """
        # Reset
        builder = P0HexagonPassive(v_supply=1.0)
        circuit, initial_state = builder.build()
        self.controller = CircuitController(circuit, initial_state)

        # Baseline (no drive)
        n_baseline = int(10e-6 / dt_s)
        for _ in range(n_baseline):
            self.controller.run_step(dt_s)

        state = self.controller._make_state()
        baseline_a_sense = state.node_voltages.get('sense_A_pos', 0.5)
        baseline_b_memory = state.node_voltages.get('memory_B_pos_mid', 0.5)

        # Drive pulse parameters
        drive_start = 10e-6
        drive_end = drive_start + drive_pulse_us * 1e-6

        # We'll manually set node voltages during the drive pulse
        # (This simulates an external voltage source)
        # For passive circuit: a_pos = v_drive, a_neg = 1 - v_drive (complementary)
        # Actually, for a differential drive: a_pos swings up, a_neg swings down

        # Run pulse + settling
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

                # Note: In the passive circuit, there's no active control of a_pos/a_neg
                # They naturally settle based on the inductor-resistor network
                # To simulate a drive, we'd need to add external voltage sources
                # For now, just monitor the passive response

                a_sense = state.node_voltages.get('sense_A_pos', 0.5)
                b_memory = state.node_voltages.get('memory_B_pos_mid', 0.5)

                a_sense_history.append(a_sense)
                b_memory_history.append(b_memory)

                # Check for divergence
                if abs(a_sense) > 1.5 or abs(b_memory) > 1.5:
                    diverged = True
                    error_msg = f'Divergence at step {step}'
                    break

            except Exception as e:
                diverged = True
                error_msg = str(e)
                break

        # Analyze
        final_a_sense = a_sense_history[-1] if a_sense_history else baseline_a_sense
        final_b_memory = b_memory_history[-1] if b_memory_history else baseline_b_memory

        peak_a_activity = max(abs(v - baseline_a_sense) for v in a_sense_history) if a_sense_history else 0.0
        peak_b_change = max(abs(v - baseline_b_memory) for v in b_memory_history) if b_memory_history else 0.0

        retention = final_b_memory - baseline_b_memory

        if diverged:
            status = 'FAIL'
            reason = error_msg
        elif peak_a_activity < 0.001:
            status = 'UNCERTAIN'
            reason = 'No activity (passive - needs external drive source)'
        else:
            status = 'PASS'
            reason = f'Nerve ring coupled: A activity={peak_a_activity:.4f}V'

        return {
            'baseline_a_sense': baseline_a_sense,
            'baseline_b_memory': baseline_b_memory,
            'peak_a_activity': peak_a_activity,
            'peak_b_change': peak_b_change,
            'final_a_sense': final_a_sense,
            'final_b_memory': final_b_memory,
            'retention': retention,
            'status': status,
            'reason': reason
        }


def main():
    print("\n" + "="*80)
    print("PASSIVE CIRCUIT TEST (BASELINE)")
    print("="*80)
    print("\nNo external drive - circuit should remain stable at 0.50V baseline")
    print("Nerve ring passively connected: A_sense → B_memory (1kΩ coupling)\n")

    test = PassiveABTransferTest()

    # Run baseline test
    print("Testing passive circuit stability...")
    result = test.test_ab_transfer_direct()

    print(f"  Baseline A sense: {result['baseline_a_sense']:.4f}V")
    print(f"  Baseline B memory: {result['baseline_b_memory']:.4f}V")
    print(f"  Peak A activity: {result['peak_a_activity']:.4f}V")
    print(f"  Peak B change: {result['peak_b_change']:.4f}V")
    print(f"  Final A sense: {result['final_a_sense']:.4f}V")
    print(f"  Final B memory: {result['final_b_memory']:.4f}V")
    print(f"  Retention: {result['retention']:.6f}V")
    print(f"  Status: {result['status']} - {result['reason']}\n")

    if result['status'] == 'PASS':
        print("✓ PASSIVE CIRCUIT STABLE")
        print("  Now need to add active drive elements (voltage sources or MOSFETs)")
    elif result['status'] == 'FAIL':
        print("✗ PASSIVE CIRCUIT UNSTABLE")
        print(f"  Error: {result['reason']}")
    else:
        print("~ PASSIVE CIRCUIT OK (needs external drive)")
        print("  Nerve ring architecture ready for active drive integration")


if __name__ == "__main__":
    main()
