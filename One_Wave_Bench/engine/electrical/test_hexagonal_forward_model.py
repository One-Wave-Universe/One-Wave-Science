#!/usr/bin/env python3
"""
Test hexagonal P0 forward model: gate voltage → nucleus voltage.

Sweep gate voltages for each of the six hex nodes independently.
Measure nucleus voltage response.

This determines if the hexagonal topology fixes the control cliff.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path
from typing import Dict, Tuple

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_hexagonal_circuit import P0HexagonalCircuit
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class HexagonalForwardModel:
    def __init__(self):
        print("Building hexagonal P0 circuit...")
        builder = P0HexagonalCircuit(v_supply=5.0)
        self.circuit, initial_state = builder.build()
        self.controller = CircuitController(self.circuit, initial_state)

    def measure_nucleus_response(self,
                                 gate_node: str,
                                 gate_voltage: float,
                                 settling_time_us: float = 100,
                                 dt_s: float = 1e-6) -> Tuple[float, float, float]:
        """
        Set one gate to fixed voltage, measure nucleus voltage at steady state.

        Returns:
            (v_nucleus_final, v_nucleus_min, v_nucleus_max)
        """
        # Gate control: only gate_node is active, others at 50% (no effect)
        def gate_control(mosfet_id: str, time: float) -> float:
            # Extract node name from mosfet_id (e.g., "A_pos_HS" → "A_pos")
            if gate_node in mosfet_id:
                return gate_voltage
            else:
                return 2.5  # Neutral: no effect on inactive gates

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

                if v_nucleus > 10.0 or v_nucleus < 0.0:
                    print(f"      ⚠ Divergence at step {step}: nucleus={v_nucleus:.2f}V")
                    break
            except Exception as e:
                print(f"      ⚠ Error at step {step}: {e}")
                break

        # Steady state from last 10%
        n_steady = max(10, len(v_nucleus_history) // 10)
        steady_samples = v_nucleus_history[-n_steady:] if v_nucleus_history else [2.5]

        return steady_samples[-1], min(steady_samples), max(steady_samples)

    def test_all_gates(self):
        """Sweep each gate independently, measure nucleus response."""
        print("\n" + "="*70)
        print("HEXAGONAL FORWARD MODEL TEST")
        print("="*70)
        print("\nSweeping each of 6 gates: 0.0V to 5.0V in 0.5V steps")
        print("Measuring nucleus (V_0) response\n")

        hex_nodes = ["A_pos", "B_pos", "C_pos", "A_neg", "B_neg", "C_neg"]
        results = {}

        for node in hex_nodes:
            print(f"\n{node.upper()}:")
            print(f"  Gate_V(V) | Nucleus(V) | Status")
            print(f"  " + "-"*40)

            node_results = {}
            gate_voltages = [v / 10.0 for v in range(0, 51, 5)]  # 0.0, 0.5, 1.0, ..., 5.0

            for gate_v in gate_voltages:
                v_nucleus, v_min, v_max = self.measure_nucleus_response(node, gate_v)

                if v_nucleus > 10.0:
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

                print(f"    {gate_v:4.1f}      | {v_nucleus:10.4f} | {status}")

            results[node] = node_results

        return results

    def analyze_results(self, results: Dict):
        """Summarize findings."""
        print("\n" + "="*70)
        print("HEXAGONAL TOPOLOGY ANALYSIS")
        print("="*70)

        for node, node_data in results.items():
            stable_gates = [gv for gv, data in node_data.items() if data["status"] == "STABLE"]
            diverged_gates = [gv for gv, data in node_data.items() if data["status"] == "DIVERGED"]

            print(f"\n{node.upper()}:")
            if stable_gates:
                print(f"  Stable range: {min(stable_gates):.1f}V to {max(stable_gates):.1f}V")
            else:
                print(f"  Stable range: NONE")

            if diverged_gates:
                print(f"  Diverged range: {min(diverged_gates):.1f}V to {max(diverged_gates):.1f}V")


def main():
    model = HexagonalForwardModel()
    results = model.test_all_gates()
    model.analyze_results(results)

    # Export
    export_data = {str(k): {str(gv): v for gv, v in node_data.items()}
                   for k, node_data in results.items()}

    export_path = "/tmp/hexagonal_forward_model.json"
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    print(f"\n✓ Results exported to {export_path}")


if __name__ == "__main__":
    main()
