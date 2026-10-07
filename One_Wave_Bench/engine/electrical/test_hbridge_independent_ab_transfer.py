#!/usr/bin/env python3
"""
H-Bridge Independent Gate Control Test: A->B State Transfer

Per UPDATED_63, the first hard criterion:
  1. A Drive event
  2. Measurable current/energy reaches B Memory path
  3. A Drive removed and transient dies
  4. B retains a changed magnetic state
  5. Later B probe differs from baseline

This test uses INDEPENDENT high-side and low-side gate signals
to avoid MOSFET shoot-through, solving the 1V supply / 0.4V Vth problem.
"""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_hbridge_independent import P0HexagonHBridgeIndependent
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class IndependentGateABTransferTest:
    """Test A->B state transfer with independent H-bridge gate control."""

    def __init__(self):
        print("Building P0 hexagon H-bridge with independent gate control...")
        builder = P0HexagonHBridgeIndependent(v_supply=1.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def test_ab_transfer(self,
                         drive_pulse_us: float = 50.0,
                         drive_direction: str = "high",
                         settling_time_us: float = 200.0,
                         deadband_us: float = 1.0,
                         dt_s: float = 1e-6) -> dict:
        """
        Test A->B state transfer with proper H-bridge control.

        Independent gate control strategy:
        - gate_a_pos_HS (high-side): LOW (0.2V) to turn ON PMOS, HIGH (0.9V) to turn OFF
        - gate_a_pos_LS (low-side): HIGH (0.9V) to turn ON NMOS, LOW (0.2V) to turn OFF
        - Deadband ensures both never conduct simultaneously

        Drive direction:
        - "high": a_pos driven HIGH (through PMOS to +V), a_neg driven LOW (through NMOS to GND)
        - "low": a_pos driven LOW, a_neg driven HIGH
        """
        # Reset
        builder = P0HexagonHBridgeIndependent(v_supply=1.0)
        circuit, initial_state = builder.build()
        self.controller = CircuitController(circuit, initial_state)

        # Collect baseline
        baseline_data = []
        n_baseline = int(10e-6 / dt_s)
        for _ in range(n_baseline):
            self.controller.run_step(dt_s)

        state = self.controller._make_state()
        baseline_a_sense = state.node_voltages.get('sense_A_pos', 0.5)
        baseline_b_memory = state.node_voltages.get('memory_B_pos_in', 0.5)

        # Drive pulse timing
        drive_start = 10e-6
        drive_end = drive_start + drive_pulse_us * 1e-6
        deadband_s = deadband_us * 1e-6

        def gate_control(mosfet_id: str, time: float) -> float:
            """
            Independent gate control for H-bridge.

            During drive pulse:
            - If drive_direction="high": a_pos_HS=ON (gate low), a_pos_LS=OFF (gate high)
            - If drive_direction="low": a_pos_HS=OFF (gate high), a_pos_LS=ON (gate low)

            At rest: both OFF (gate_HS high, gate_LS low)
            """
            # Neutral state: all FETs off
            hs_off = 0.9  # PMOS gate high = OFF
            ls_off = 0.2  # NMOS gate low = OFF
            hs_on = 0.2   # PMOS gate low = ON
            ls_on = 0.9   # NMOS gate high = ON

            # A phase drive
            if "a_pos_HS" in mosfet_id:
                if drive_start <= time < drive_end:
                    # During drive pulse
                    if drive_direction == "high":
                        return hs_on   # Turn ON PMOS to drive HIGH
                    else:
                        return hs_off  # Keep OFF
                else:
                    return hs_off     # Rest state
            elif "a_pos_LS" in mosfet_id:
                if drive_start <= time < drive_end:
                    # During drive pulse
                    if drive_direction == "high":
                        return ls_off  # Keep OFF (deadband)
                    else:
                        return ls_on   # Turn ON NMOS to drive LOW
                else:
                    return ls_off     # Rest state
            elif "a_neg_HS" in mosfet_id:
                if drive_start <= time < drive_end:
                    # During drive pulse: a_neg drives opposite to a_pos
                    if drive_direction == "high":
                        return hs_off  # Keep OFF
                    else:
                        return hs_on   # Turn ON PMOS to drive HIGH
                else:
                    return hs_off     # Rest state
            elif "a_neg_LS" in mosfet_id:
                if drive_start <= time < drive_end:
                    # During drive pulse
                    if drive_direction == "high":
                        return ls_on   # Turn ON NMOS to drive LOW
                    else:
                        return ls_off  # Keep OFF (deadband)
                else:
                    return ls_off     # Rest state
            else:
                # All other gates at rest (both OFF)
                return hs_off if "HS" in mosfet_id else ls_off

        self.controller.set_gate_control(gate_control)

        # Run drive pulse + settling
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
                    error_msg = f'Divergence at t={time*1e6:.1f}µs: a_sense={a_sense:.4f}V, b_memory={b_memory:.4f}V'
                    break

            except Exception as e:
                diverged = True
                error_msg = f'Exception at step {step}: {str(e)}'
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
            reason = f'No A activity detected'

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
        """Run A->B transfer tests with independent gate control."""
        print("\n" + "="*80)
        print("H-BRIDGE INDEPENDENT GATE CONTROL: A->B STATE TRANSFER TEST")
        print("="*80)
        print("\nGate Strategy: Independent HS/LS control (no shoot-through)")
        print("  gate_HS: 0.2V=ON (PMOS), 0.9V=OFF")
        print("  gate_LS: 0.9V=ON (NMOS), 0.2V=OFF")
        print("  Deadband: prevents simultaneous conduction")
        print("\nSequence: Baseline → A Drive Pulse → Settling → B Memory Probe")
        print("Drive pulse: 50µs")
        print("Settling: 200µs after pulse")
        print("Criterion: B Memory retains measurable change from baseline\n")

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
            print(f"  Final A sense: {result['final_a_sense']:.4f}V")
            print(f"  Final B memory: {result['final_b_memory']:.4f}V")
            print(f"  Retention Δ: {result['retention']:.6f}V")
            print(f"  Status: {result['status']} - {result['reason']}\n")

        return results


def main():
    test = IndependentGateABTransferTest()
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
        print("  Independent gate control successful.")
        print("  Nerve ring ready for full closure (A->B->C->A).")
    elif uncertain > 0:
        print("\n~ TRANSFER DETECTED BUT WEAK")
        print("  Check impedance matching and coupling strength.")
    else:
        print("\n✗ NO A->B TRANSFER")
        print("  Check gate control timing and H-bridge wiring.")


if __name__ == "__main__":
    main()
