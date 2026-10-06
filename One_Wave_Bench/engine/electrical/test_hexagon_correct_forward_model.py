#!/usr/bin/env python3
"""
Forward Model Test: P0 Hexagon Correct Circuit

Test that the corrected hexagon circuit (complementary gates, 0.5V neutral)
can actually control nucleus voltage without immediate divergence.

Sweep gate voltage for each phase independently.
Measure nucleus response and stability.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from typing import Dict, Tuple

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagon_correct import P0HexagonCorrect
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class HexagonCorrectForwardModel:
    def __init__(self):
        print("Building corrected P0 hexagon circuit...")
        builder = P0HexagonCorrect(v_supply=5.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def measure_nucleus_response(self,
                                 gate_node: str,
                                 gate_voltage: float,
                                 settling_time_us: float = 100,
                                 dt_s: float = 1e-6) -> Tuple[float, float, float]:
        """
        Set one gate to fixed voltage, others at neutral (0.5V).
        Measure nucleus voltage at steady state.

        Returns:
            (v_nucleus_final, v_nucleus_min, v_nucleus_max)
        """
        # Reset controller for fresh run
        builder = P0HexagonCorrect(v_supply=5.0)
        circuit, initial_state = builder.build()
        self.controller = CircuitController(circuit, initial_state)

        # Gate control: only gate_node active, others at 0.5V (neutral)
        def gate_control(mosfet_id: str, time: float) -> float:
            # Extract node name from mosfet_id (e.g., "a_pos_HS" → "a_pos")
            if gate_node in mosfet_id:
                return gate_voltage
            else:
                return 0.5  # Neutral: complementary gates remain OFF

        self.controller.set_gate_control(gate_control)

        # Run settling
        n_steps = int(settling_time_us * 1e-6 / dt_s)
        v_nucleus_history = []

        for step in range(n_steps):
            try:
                self.controller.run_step(dt_s)
                state = self.controller._make_state()
                v_nucleus = state.node_voltages.get('nucleus', 2.5)
                v_nucleus_history.append(v_nucleus)

                if v_nucleus > 10.0 or v_nucleus < -5.0:
                    print(f"      ⚠ Divergence at step {step}: nucleus={v_nucleus:.2f}V")
                    break
            except Exception as e:
                print(f"      ⚠ Error at step {step}: {e}")
                break

        # Steady state from last 10%
        n_steady = max(10, len(v_nucleus_history) // 10)
        steady_samples = v_nucleus_history[-n_steady:] if v_nucleus_history else [2.5]

        return steady_samples[-1], min(steady_samples), max(steady_samples)

    def test_all_phases(self):
        """Sweep each phase independently, measure nucleus response."""
        print("\n" + "="*70)
        print("HEXAGON CORRECT FORWARD MODEL TEST")
        print("="*70)
        print("\nSweeping each of 6 gates: 0.0V to 5.0V in 0.5V steps")
        print("Neutral gate voltage: 0.5V (complementary gates remain OFF)")
        print("Measuring nucleus (V_0) response\n")

        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]
        results = {}

        for node in hex_nodes:
            print(f"\n{node.upper()}:")
            print(f"  Gate_V(V) | Nucleus(V) | Min(V)    | Max(V)    | Status")
            print(f"  " + "-"*60)

            node_results = {}
            gate_voltages = [v / 10.0 for v in range(0, 51, 5)]  # 0.0, 0.5, 1.0, ..., 5.0

            for gate_v in gate_voltages:
                v_nucleus, v_min, v_max = self.measure_nucleus_response(node, gate_v)

                if v_nucleus > 10.0 or v_nucleus < -5.0:
                    status = "DIVERGED"
                elif (v_max - v_min) < 0.05:
                    status = "STABLE"
                else:
                    status = "UNSTABLE"

                node_results[gate_v] = {
                    "nucleus": v_nucleus,
                    "nucleus_min": v_min,
                    "nucleus_max": v_max,
                    "status": status
                }

                print(f"    {gate_v:4.1f}      | {v_nucleus:10.4f} | {v_min:9.4f} | {v_max:9.4f} | {status}")

            results[node] = node_results

        return results

    def analyze_results(self, results: Dict):
        """Summarize findings."""
        print("\n" + "="*70)
        print("HEXAGON CORRECT TOPOLOGY ANALYSIS")
        print("="*70)

        for node, node_data in results.items():
            stable_gates = [gv for gv, data in node_data.items() if data["status"] == "STABLE"]
            unstable_gates = [gv for gv, data in node_data.items() if data["status"] == "UNSTABLE"]
            diverged_gates = [gv for gv, data in node_data.items() if data["status"] == "DIVERGED"]

            print(f"\n{node.upper()}:")
            if stable_gates:
                print(f"  ✓ Stable range: {min(stable_gates):.1f}V to {max(stable_gates):.1f}V")
            else:
                print(f"  ✓ Stable range: NONE")

            if unstable_gates:
                print(f"  ~ Unstable range: {min(unstable_gates):.1f}V to {max(unstable_gates):.1f}V")

            if diverged_gates:
                print(f"  ✗ Diverged range: {min(diverged_gates):.1f}V to {max(diverged_gates):.1f}V")

        # Summary
        print("\n" + "="*70)
        print("VERDICT:")
        all_stable = all(
            any(data["status"] == "STABLE" for data in node_data.values())
            for node_data in results.values()
        )

        if all_stable:
            print("✓ COMPLEMENTARY GATE TOPOLOGY SUCCESSFUL")
            print("  Circuit can maintain stable nucleus voltage across all gates.")
            print("  Ready for forward model characterization and control design.")
        else:
            print("✗ Topology still unstable")
            print("  Review MOSFET characteristics, timing, or gate drive configuration.")


def main():
    model = HexagonCorrectForwardModel()
    results = model.test_all_phases()
    model.analyze_results(results)

    # Export
    export_data = {str(k): {str(gv): v for gv, v in node_data.items()}
                   for k, node_data in results.items()}

    export_path = "/tmp/hexagon_correct_forward_model.json"
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    print(f"\n✓ Results exported to {export_path}")


if __name__ == "__main__":
    main()
