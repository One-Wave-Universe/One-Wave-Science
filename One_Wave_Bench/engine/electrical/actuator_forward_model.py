#!/usr/bin/env python3
"""
Direct Actuator Forward Model: V_0 = f(gate_voltage)

Empirically measure how gate voltage directly controls V_0, without PID layer.
Build lookup table for direct feedback control.
"""
from __future__ import annotations
import sys
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.p0_ternary_circuit import P0TernaryCircuit
from One_Wave_Bench.engine.electrical.circuit_controller import (
    CircuitController, ControlMode, CircuitState
)


class ActuatorForwardModelBuilder:
    """
    Empirical forward model: sweep gate voltage, measure steady-state V_0.

    Goal: Answer the question: "If I set all gates to X volts, what is V_0?"
    """

    def __init__(self):
        print("Building P0 circuit for forward model...")
        builder = P0TernaryCircuit(v_supply=5.0)
        self.circuit, initial_state = builder.build(supply_mode="single")
        self.controller = CircuitController(self.circuit, initial_state)

    def measure_steady_state_v0(self,
                                gate_voltage: float,
                                settling_time_us: float = 100,
                                dt_s: float = 1e-6) -> Tuple[float, float, float]:
        """
        Set all gates to a fixed voltage and measure steady-state V_0.

        Returns:
            (v_0_final, v_0_min_last_10%, v_0_max_last_10%)
        """
        # Define fixed gate control
        def gate_control(mosfet_id: str, time: float) -> float:
            return gate_voltage

        self.controller.set_gate_control(gate_control)

        # Run settling simulation
        n_steps = int(settling_time_us * 1e-6 / dt_s)
        v_0_history = []

        for step in range(n_steps):
            try:
                self.controller.run_step(dt_s)
                state = self.controller._make_state()
                v_0 = state.node_voltages.get('0', 2.5)
                v_0_history.append(v_0)

                # Safety: if V_0 diverges beyond 10V, stop early
                if v_0 > 10.0 or v_0 < 0.0:
                    print(f"    ⚠ Divergence at step {step}: V_0 = {v_0:.2f}V, stopping")
                    break

            except Exception as e:
                print(f"    ⚠ Error at step {step}: {e}")
                break

        # Extract steady-state from last 10% of samples
        n_steady = max(10, len(v_0_history) // 10)
        steady_samples = v_0_history[-n_steady:]

        v_0_final = steady_samples[-1] if steady_samples else 2.5
        v_0_min = min(steady_samples) if steady_samples else 2.5
        v_0_max = max(steady_samples) if steady_samples else 2.5

        return v_0_final, v_0_min, v_0_max

    def build_forward_model(self) -> Dict[float, Dict]:
        """
        Sweep gate voltage from 0V to 5V in 0.2V steps.
        Measure steady-state V_0 at each point.

        Build lookup table: gate_voltage → (v_0_nominal, v_0_range)
        """
        print("\n" + "="*70)
        print("FORWARD MODEL: Gate Voltage → V_0")
        print("="*70)
        print(f"\nSweeping gate voltage 0.0V to 5.0V in 0.2V steps")
        print(f"Each measurement: 100µs settling time")
        print(f"\nGate_V(V) | V_0_steady(V) | V_0_min(V) | V_0_max(V) | Stability")
        print("-"*70)

        model = {}

        # Test points: 0.0V to 5.0V
        gate_voltages = [v / 10.0 for v in range(0, 51, 2)]  # 0.0, 0.2, 0.4, ..., 5.0

        for gate_v in gate_voltages:
            v_0_final, v_0_min, v_0_max = self.measure_steady_state_v0(gate_v)

            stability = "STABLE" if (v_0_max - v_0_min) < 0.05 else "UNSTABLE"
            if v_0_final > 10.0:
                stability = "DIVERGED"

            model[gate_v] = {
                "v_0_steady": v_0_final,
                "v_0_min": v_0_min,
                "v_0_max": v_0_max,
                "stability": stability
            }

            print(f"{gate_v:5.1f}     | {v_0_final:13.6f} | {v_0_min:10.6f} | {v_0_max:10.6f} | {stability:8s}")

        return model

    def analyze_forward_model(self, model: Dict[float, Dict]):
        """
        Analyze the forward model to extract control insight.
        """
        print("\n" + "="*70)
        print("FORWARD MODEL ANALYSIS")
        print("="*70)

        # Extract data
        gate_vs = sorted(model.keys())
        v_0_values = [model[gv]["v_0_steady"] for gv in gate_vs]
        stability = [model[gv]["stability"] for gv in gate_vs]

        # Find stable region
        stable_indices = [i for i, s in enumerate(stability) if s == "STABLE"]
        if stable_indices:
            stable_gate_vs = [gate_vs[i] for i in stable_indices]
            stable_v_0s = [v_0_values[i] for i in stable_indices]

            print(f"\nStable gate voltage range: {min(stable_gate_vs):.1f}V to {max(stable_gate_vs):.1f}V")
            print(f"Corresponding V_0 range: {min(stable_v_0s):.6f}V to {max(stable_v_0s):.6f}V")

            # Linear fit in stable region
            if len(stable_indices) >= 2:
                x = stable_gate_vs
                y = stable_v_0s
                n = len(x)
                sum_x = sum(x)
                sum_y = sum(y)
                sum_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
                sum_x2 = sum(x_i**2 for x_i in x)

                slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
                intercept = (sum_y - slope * sum_x) / n

                print(f"\nLinear fit (stable region):")
                print(f"  V_0 = {intercept:.6f} + {slope:.6f} × gate_V")
                print(f"  Sensitivity: {slope:.6f} V per volt of gate control")

                # Inverse model for direct control
                if slope != 0:
                    gate_v_for_2_5 = (2.5 - intercept) / slope
                    print(f"\nDirect actuator command (to maintain V_0 = 2.5V):")
                    print(f"  gate_V_command = {gate_v_for_2_5:.6f}V (baseline)")
                    print(f"  gate_V_command = {gate_v_for_2_5:.6f} + (V_0_error / {slope:.6f})")

                    return {
                        "slope": slope,
                        "intercept": intercept,
                        "baseline_gate_v": gate_v_for_2_5,
                        "stable_range": (min(stable_gate_vs), max(stable_gate_vs))
                    }

        # Find unstable/divergent region
        unstable_gate_vs = [gate_vs[i] for i in range(len(gate_vs)) if stability[i] != "STABLE"]
        if unstable_gate_vs:
            print(f"\nUnstable/divergent gate voltage range: {min(unstable_gate_vs):.1f}V to {max(unstable_gate_vs):.1f}V")
            print(f"Circuit cannot be controlled in this region—AVOID these gate voltages")

        return None


def main():
    builder = ActuatorForwardModelBuilder()
    model = builder.build_forward_model()
    analysis = builder.analyze_forward_model(model)

    # Export model
    export_data = {
        "model": {str(k): v for k, v in model.items()},
        "analysis": analysis or {}
    }

    export_path = "/tmp/actuator_forward_model.json"
    with open(export_path, 'w') as f:
        json.dump(export_data, f, indent=2)
    print(f"\n✓ Forward model exported to {export_path}")


if __name__ == "__main__":
    main()
