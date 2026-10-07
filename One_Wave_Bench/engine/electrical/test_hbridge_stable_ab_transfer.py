#!/usr/bin/env python3
"""
H-Bridge Stable AB Transfer Test

Tests the corrected circuit with R_sense=100Ω for numerical stability.
Uses independent H-bridge gate control and ternary differential geometry
(A, B, C axes at 120° radial orientation) for common-mode noise rejection
and three-point equilibrium without artificial damping.

Expected outcome: Circuit stable for full 200us settling period,
demonstrating A→B state transfer via nerve ring coupling.
"""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_hbridge_stable import P0HexagonHBridgeStable
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class StableABTransferTest:
    """Test A->B state transfer with numerically stable circuit."""

    def __init__(self):
        print("Building P0 hexagon H-bridge with STABLE parameters...")
        print("  R_sense = 100Ω (dt/τ = 10, stable)")
        print("  Independent H-bridge gate control")
        print("  Ternary differential geometry (A/B/C 120° radial)")
        print("  Nerve ring coupling: 10kΩ (A_sense → B_memory)")

        builder = P0HexagonHBridgeStable(v_supply=1.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def test_stability_no_drive(self, duration_us: float = 300.0, dt_s: float = 1e-6) -> bool:
        """Test baseline stability without any drive signal."""
        print(f"\n  Testing stability ({duration_us:.0f}us, no drive)...", end=" ")

        # Reset
        builder = P0HexagonHBridgeStable(v_supply=1.0)
        circuit, initial_state = builder.build()
        controller = CircuitController(circuit, initial_state)

        n_steps = int(duration_us * 1e-6 / dt_s)

        for step in range(min(n_steps, 3000)):
            try:
                controller.run_step(dt_s)
                state = controller._make_state()

                a_sense = state.node_voltages.get('sense_A_pos', 0.5)
                b_memory = state.node_voltages.get('memory_B_pos_in', 0.5)

                # Check bounds (allow wider margin during development)
                if a_sense > 2.0 or a_sense < -1.0 or b_memory > 2.0 or b_memory < -1.0:
                    print(f"DIVERGE at t={(step*dt_s)*1e6:.1f}us (a_sense={a_sense:.3f}V, b_mem={b_memory:.3f}V)")
                    return False

                # Status updates every 500 steps
                if step % 500 == 0 and step > 0:
                    print(f".", end="", flush=True)

            except Exception as e:
                print(f"\nERROR at step {step} ({(step*dt_s)*1e6:.1f}us): {type(e).__name__}: {e}")
                import traceback
                traceback.print_exc()
                return False

        print(" STABLE [OK]")
        return True

    def test_ab_transfer(self,
                         drive_pulse_us: float = 50.0,
                         drive_direction: str = "high",
                         settling_time_us: float = 200.0,
                         dt_s: float = 1e-6) -> dict:
        """Test A->B state transfer via nerve ring coupling."""
        # Reset
        builder = P0HexagonHBridgeStable(v_supply=1.0)
        circuit, initial_state = builder.build()
        controller = CircuitController(circuit, initial_state)

        # Collect baseline (quiescent equilibrium)
        n_baseline = int(10e-6 / dt_s)
        for _ in range(n_baseline):
            controller.run_step(dt_s)

        state = controller._make_state()
        baseline_a_sense = state.node_voltages.get('sense_A_pos', 0.5)
        baseline_b_memory = state.node_voltages.get('memory_B_pos_in', 0.5)

        # Drive pulse timing
        drive_start = 10e-6
        drive_end = drive_start + drive_pulse_us * 1e-6

        def gate_control(mosfet_id: str, time: float) -> float:
            """
            Independent H-bridge gate control.
            HS (PMOS): drain=+V, source=node → gate=0.2V to turn ON, 0.9V to turn OFF
            LS (NMOS): drain=node, source=GND → gate=0.9V to turn ON, 0.2V to turn OFF
            """
            hs_off = 0.9
            ls_off = 0.2
            hs_on = 0.2
            ls_on = 0.9

            # Drive A positive phase
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

            # Drive A negative phase (complementary)
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

            # All other phases: both FETs off
            else:
                return hs_off if "HS" in mosfet_id else ls_off

        controller.set_gate_control(gate_control)

        # Run drive + settling
        total_time_s = settling_time_us * 1e-6
        n_steps = int(total_time_s / dt_s)

        a_sense_history = []
        b_memory_history = []
        diverged = False
        error_msg = ""
        divergence_time = None

        for step in range(n_steps):
            time = 10e-6 + step * dt_s
            try:
                controller.run_step(dt_s)
                state = controller._make_state()

                a_sense = state.node_voltages.get('sense_A_pos', 0.5)
                b_memory = state.node_voltages.get('memory_B_pos_in', 0.5)

                a_sense_history.append(a_sense)
                b_memory_history.append(b_memory)

                # Check bounds
                if a_sense > 1.5 or a_sense < -0.5 or b_memory > 1.5 or b_memory < -0.5:
                    diverged = True
                    divergence_time = time
                    error_msg = f'Divergence at t={time*1e6:.1f}us'
                    break

            except Exception as e:
                diverged = True
                error_msg = f'Exception: {str(e)}'
                break

        # Analyze results
        final_a_sense = a_sense_history[-1] if a_sense_history else baseline_a_sense
        final_b_memory = b_memory_history[-1] if b_memory_history else baseline_b_memory

        peak_a_activity = max(abs(v - baseline_a_sense) for v in a_sense_history) if a_sense_history else 0.0
        peak_b_memory_change = max(abs(v - baseline_b_memory) for v in b_memory_history) if b_memory_history else 0.0
        retention = final_b_memory - baseline_b_memory

        # Determine pass/fail
        if diverged:
            status = 'FAIL'
            reason = error_msg
        elif peak_a_activity > 0.01 and peak_b_memory_change > 0.01 and abs(retention) > 0.005:
            status = 'PASS'
            reason = 'A→B transfer demonstrated, circuit stable'
        elif peak_a_activity > 0.01:
            status = 'UNCERTAIN'
            reason = f'A active ({peak_a_activity:.4f}V) but B coupling weak ({peak_b_memory_change:.4f}V)'
        else:
            status = 'FAIL'
            reason = 'No A activity detected'

        return {
            'baseline_a_sense': baseline_a_sense,
            'baseline_b_memory': baseline_b_memory,
            'peak_a_activity': peak_a_activity,
            'peak_b_memory_change': peak_b_memory_change,
            'final_a_sense': final_a_sense,
            'final_b_memory': final_b_memory,
            'retention': retention,
            'status': status,
            'reason': reason,
            'divergence_time': divergence_time,
            'n_steps_collected': len(a_sense_history)
        }

    def run_test_series(self):
        """Run full test series: stability + A→B transfer."""
        print("\n" + "="*80)
        print("STABLE H-BRIDGE: A→B STATE TRANSFER TEST")
        print("="*80)
        print("\nCircuit parameters:")
        print("  Supply: 1.0V (single-ended)")
        print("  Drive winding: L=100µH, R=5Ω")
        print("  Sense winding: L=10µH, R=100Ω (CRITICAL: dt/τ=10, stable)")
        print("  Memory winding: L=100µH, R=5Ω")
        print("  Nerve ring: 10kΩ (A_sense → B_memory)")
        print("  MOSFET: Vth=0.4V, Rds_on=0.5Ω")
        print("  VREF: 0.50V (1:1 divider from supply)")
        print("  Solver: Backward Euler, dt=1us")
        print("\nTernary geometry:")
        print("  Three differential axes (A, B, C) at 120° radial")
        print("  Common-mode noise rejection via ±pairs (A+/A-, B+/B-, C+/C-)")
        print("  Three-point equilibrium at virtual zero center")
        print("  No artificial damping resistors")

        # Stage 1: Baseline stability
        print("\n" + "-"*80)
        print("STAGE 1: Baseline Stability (no drive signal)")
        print("-"*80)
        stable = self.test_stability_no_drive(duration_us=300.0)

        if not stable:
            print("\n✗ CIRCUIT UNSTABLE - cannot proceed with transfer test")
            return False

        # Stage 2: A→B transfer tests
        print("\n" + "-"*80)
        print("STAGE 2: A→B State Transfer")
        print("-"*80)

        directions = ["high", "low"]
        results = []

        for drive_dir in directions:
            print(f"\nTesting drive direction={drive_dir}...")
            result = self.test_ab_transfer(drive_direction=drive_dir)
            results.append(result)

            print(f"  Baseline A sense: {result['baseline_a_sense']:.4f}V")
            print(f"  Baseline B memory: {result['baseline_b_memory']:.4f}V")
            print(f"  Peak A activity: {result['peak_a_activity']:.4f}V")
            print(f"  Peak B change: {result['peak_b_memory_change']:.4f}V")
            print(f"  Final B memory: {result['final_b_memory']:.4f}V")
            print(f"  Retention Δ: {result['retention']:.6f}V")
            print(f"  Status: {result['status']} - {result['reason']}")
            if result['divergence_time']:
                print(f"  Divergence at: {result['divergence_time']*1e6:.1f}us")
            print(f"  Steps collected: {result['n_steps_collected']}")

        return results


def main():
    test = StableABTransferTest()
    results = test.run_test_series()

    if not results:
        print("\n" + "="*80)
        print("TEST ABORTED")
        print("="*80)
        return

    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)

    passed = sum(1 for r in results if r['status'] == 'PASS')
    uncertain = sum(1 for r in results if r['status'] == 'UNCERTAIN')
    failed = sum(1 for r in results if r['status'] == 'FAIL')

    print(f"\nResults across {len(results)} transfer tests:")
    print(f"  PASS:      {passed}/{len(results)}")
    print(f"  UNCERTAIN: {uncertain}/{len(results)}")
    print(f"  FAIL:      {failed}/{len(results)}")

    if passed > 0:
        print("\n✓ A→B STATE TRANSFER DEMONSTRATED")
        print("  Nerve ring coupling successfully transfers state from A sense to B memory")
        print("  Circuit stable through settling period with true ternary geometry")
    elif uncertain > 0:
        print("\n~ TRANSFER DETECTED BUT WEAK")
        print("  A activity present but B coupling response marginal")
        print("  May need to verify nerve ring impedance or drive amplitude")
    else:
        print("\n✗ NO A→B TRANSFER")
        print("  Check:")
        print("    1. Gate control timing")
        print("    2. Nerve ring continuity and impedance")
        print("    3. Phase initialization voltages")

    print("\n" + "="*80)


if __name__ == "__main__":
    main()
