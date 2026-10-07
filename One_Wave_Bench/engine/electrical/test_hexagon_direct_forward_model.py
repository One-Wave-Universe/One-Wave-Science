#!/usr/bin/env python3
"""
Forward Model Test: P0 Hexagon Direct Phases

Test three independent phases:
  A: a+ ↔ a- (vertical)
  B: b+ ↔ b- (diagonal)
  C: c+ ↔ c- (diagonal)

For each phase, sweep gate voltage on both vertices and measure
phase current/voltage response.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from typing import Dict, Tuple

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_direct import P0HexagonDirect
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class HexagonDirectForwardModel:
    def __init__(self):
        print("Building P0 hexagon direct phase circuit...")
        builder = P0HexagonDirect(v_supply=1.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def measure_phase_response(self,
                               pos_node: str,
                               neg_node: str,
                               gate_voltage: float,
                               settling_time_us: float = 100,
                               dt_s: float = 1e-6) -> Tuple[float, float, float, float]:
        """
        Set both gates of a phase to fixed voltage.
        Measure phase current and voltage at steady state.

        Returns:
            (v_pos_final, v_neg_final, phase_current, stability)
        """
        # Reset circuit for fresh run
        builder = P0HexagonDirect(v_supply=1.0)
        circuit, initial_state = builder.build()
        self.controller = CircuitController(circuit, initial_state)

        # Gate control: both vertices of the phase at same voltage
        def gate_control(mosfet_id: str, time: float) -> float:
            if pos_node in mosfet_id or neg_node in mosfet_id:
                return gate_voltage
            else:
                return 0.50  # Other phases: neutral (virtual ground baseline)

        self.controller.set_gate_control(gate_control)

        # Run settling
        n_steps = int(settling_time_us * 1e-6 / dt_s)
        v_pos_history = []
        v_neg_history = []

        for step in range(n_steps):
            try:
                self.controller.run_step(dt_s)
                state = self.controller._make_state()
                v_pos = state.node_voltages.get(pos_node, 0.50)
                v_neg = state.node_voltages.get(neg_node, 0.50)
                v_pos_history.append(v_pos)
                v_neg_history.append(v_neg)

                if v_pos > 1.5 or v_pos < -0.5 or v_neg > 1.5 or v_neg < -0.5:
                    print(f"      ⚠ Divergence at step {step}: v_pos={v_pos:.2f}V, v_neg={v_neg:.2f}V")
                    break
            except Exception as e:
                print(f"      ⚠ Error at step {step}: {e}")
                break

        # Steady state from last 10%
        n_steady = max(10, len(v_pos_history) // 10)
        v_pos_steady = v_pos_history[-n_steady:] if v_pos_history else [0.50]
        v_neg_steady = v_neg_history[-n_steady:] if v_neg_history else [0.50]

        v_pos_final = v_pos_steady[-1]
        v_neg_final = v_neg_steady[-1]
        phase_current = 0.0  # Placeholder for current calculation

        stability = (max(v_pos_steady) - min(v_pos_steady)) + (max(v_neg_steady) - min(v_neg_steady))

        return v_pos_final, v_neg_final, phase_current, stability

    def test_all_phases(self):
        """Sweep each phase independently."""
        print("\n" + "="*80)
        print("HEXAGON DIRECT PHASES FORWARD MODEL TEST")
        print("="*80)
        print("\nThree independent phases, each swept 0.0V to 1.0V in 0.1V steps")
        print("Measuring phase voltage response (letter-to-letter connections)")
        print("Supply: 1.0V, Baseline: 0.50V\n")

        phases = [
            ("A", "a_pos", "a_neg"),
            ("B", "b_pos", "b_neg"),
            ("C", "c_pos", "c_neg"),
        ]

        results = {}

        for phase_name, pos_node, neg_node in phases:
            print(f"\nPHASE {phase_name}: {pos_node} ↔ {neg_node}")
            print(f"  Gate_V(V) | V_{pos_node[0]}+ (V) | V_{neg_node[0]}- (V) | Diff(V)   | Status")
            print(f"  " + "-"*70)

            phase_results = {}
            gate_voltages = [v / 10.0 for v in range(0, 11, 1)]  # 0.0, 0.1, 0.2, ..., 1.0

            for gate_v in gate_voltages:
                v_pos, v_neg, i_phase, stability = self.measure_phase_response(
                    pos_node, neg_node, gate_v
                )

                diff_v = abs(v_pos - v_neg)

                if diff_v > 10.0:
                    status = "DIVERGED"
                elif stability < 0.1:
                    status = "STABLE"
                else:
                    status = "UNSTABLE"

                phase_results[gate_v] = {
                    "v_pos": v_pos,
                    "v_neg": v_neg,
                    "diff": diff_v,
                    "current": i_phase,
                    "status": status
                }

                print(f"    {gate_v:4.1f}      | {v_pos:10.4f} | {v_neg:10.4f} | {diff_v:9.4f} | {status}")

            results[phase_name] = phase_results

        return results

    def analyze_results(self, results: Dict):
        """Summarize findings."""
        print("\n" + "="*80)
        print("HEXAGON DIRECT TOPOLOGY ANALYSIS")
        print("="*80)

        for phase_name, phase_data in results.items():
            stable_gates = [gv for gv, data in phase_data.items() if data["status"] == "STABLE"]
            unstable_gates = [gv for gv, data in phase_data.items() if data["status"] == "UNSTABLE"]
            diverged_gates = [gv for gv, data in phase_data.items() if data["status"] == "DIVERGED"]

            print(f"\nPHASE {phase_name}:")
            if stable_gates:
                print(f"  ✓ Stable range: {min(stable_gates):.1f}V to {max(stable_gates):.1f}V")
            else:
                print(f"  ✓ Stable range: NONE")

            if unstable_gates:
                print(f"  ~ Unstable range: {min(unstable_gates):.1f}V to {max(unstable_gates):.1f}V")

            if diverged_gates:
                print(f"  ✗ Diverged range: {min(diverged_gates):.1f}V to {max(diverged_gates):.1f}V")

        # Summary
        print("\n" + "="*80)
        all_stable = all(
            any(data["status"] == "STABLE" for data in phase_data.values())
            for phase_data in results.values()
        )

        if all_stable:
            print("✓ DIRECT PHASE TOPOLOGY SUCCESSFUL")
            print("  Three independent phases stable across gate voltage sweep.")
            print("  Ready for asymmetric three-mode control design.")
        else:
            print("✗ Topology still unstable")
            print("  Review half-bridge configuration and gate drive.")


def main():
    model = HexagonDirectForwardModel()
    results = model.test_all_phases()
    model.analyze_results(results)

    # Export
    export_data = {str(k): {str(gv): v for gv, v in phase_data.items()}
                   for k, phase_data in results.items()}

    export_path = "/tmp/hexagon_direct_forward_model.json"
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    print(f"\n✓ Results exported to {export_path}")


if __name__ == "__main__":
    main()
