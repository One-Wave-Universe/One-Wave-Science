#!/usr/bin/env python3
"""Test the full circuit with different R_sense values to find stability boundary."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import Inductor, NMOS, PMOS, OpAmpBuffer, Capacitor
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class MinimalMultiPhaseTest:
    """Minimal multi-phase circuit to isolate sense winding instability."""

    def __init__(self, r_sense: float):
        self.r_sense = r_sense
        self.v_supply = 1.0

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build minimal 3-phase circuit with variable R_sense."""
        circuit = TransientCircuit()

        # Supply and ground
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        # VREF (middle point)
        circuit.add(Resistor(id="R_div_top", a="+V", b="vref_raw", ohms=100.0))
        circuit.add(Resistor(id="R_div_bottom", a="vref_raw", b="GND", ohms=100.0))
        circuit.add(OpAmpBuffer(
            id="vref_buffer", v_in="vref_raw", v_out="VREF", gnd="GND",
            gain=1.0, Rout=0.1, max_sourcing_mA=500.0, max_sinking_mA=500.0
        ))

        # Phase vertices
        phases = ["A", "B", "C"]
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]

        # H-bridges at vertices (but we won't drive them)
        for node in hex_nodes:
            circuit.add(PMOS(
                id=f"{node}_HS", gate=f"gate_{node}_hs", drain="+V", source=node,
                Vth=0.4, Rds_on=0.5
            ))
            circuit.add(NMOS(
                id=f"{node}_LS", gate=f"gate_{node}_ls", drain=node, source="GND",
                Vth=0.4, Rds_on=0.5
            ))

        # Three sense windings only (minimal circuit)
        for i, phase_name in enumerate(phases):
            pos_node = hex_nodes[i]  # a_pos, b_pos, c_pos
            neg_node = hex_nodes[i + 3]  # a_neg, b_neg, c_neg

            # Sense winding pos half
            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_pos",
                a=pos_node, b=f"sense_{phase_name}_pos",
                henries=10e-6  # 10µH
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_pos",
                a=f"sense_{phase_name}_pos", b="VREF",
                ohms=self.r_sense
            ))

            # Sense winding neg half
            circuit.add(Inductor(
                id=f"L_{phase_name}_sense_neg",
                a="VREF", b=f"sense_{phase_name}_neg",
                henries=10e-6  # 10µH
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_sense_neg",
                a=f"sense_{phase_name}_neg", b=neg_node,
                ohms=self.r_sense
            ))

        # Initial state
        cap_states = {}
        ind_states = {}
        for phase_name in phases:
            for half in ["pos", "neg"]:
                ind_id = f"L_{phase_name}_sense_{half}"
                ind_states[ind_id] = InductorState(id=ind_id, current=0.0)

        v_baseline = 0.50
        voltages = {
            "+V": self.v_supply, "GND": 0.0,
            "vref_raw": v_baseline, "VREF": v_baseline,
        }

        for node in hex_nodes:
            voltages[node] = v_baseline
            voltages[f"gate_{node}_hs"] = 0.9
            voltages[f"gate_{node}_ls"] = 0.2

        for phase_name in phases:
            for half in ["pos", "neg"]:
                voltages[f"sense_{phase_name}_{half}"] = v_baseline

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


def test_r_sense(r_sense_ohms: float, duration_us: float = 300.0) -> tuple[bool, float]:
    """Test circuit with given R_sense. Return (stable, divergence_time_us)."""
    builder = MinimalMultiPhaseTest(r_sense=r_sense_ohms)
    circuit, initial_state = builder.build()
    controller = CircuitController(circuit, initial_state)

    n_steps = int(duration_us * 1e-6 / 1e-6)
    dt_s = 1e-6

    for step in range(n_steps):
        try:
            controller.run_step(dt_s)
            state = controller._make_state()

            a_sense = state.node_voltages.get('sense_A_pos', 0.5)
            b_sense = state.node_voltages.get('sense_B_pos', 0.5)
            c_sense = state.node_voltages.get('sense_C_pos', 0.5)

            # Check bounds
            if abs(a_sense - 0.5) > 1.5 or abs(b_sense - 0.5) > 1.5 or abs(c_sense - 0.5) > 1.5:
                divergence_time = step * dt_s * 1e6
                return False, divergence_time

        except Exception as e:
            divergence_time = step * dt_s * 1e6
            return False, divergence_time

    return True, duration_us


# Run test series
print("\n" + "="*80)
print("MINIMAL 3-PHASE SENSE CIRCUIT: Finding R_sense stability boundary")
print("="*80)
print("\nCircuit: Three independent sense windings (L=10µH, R=variable)")
print("         Star-grounded at VREF = 0.50V")
print("         No drive windings, no memory, no nerve ring")
print("         Solver: Backward Euler, dt = 1us\n")

r_sense_values = [10.0, 50.0, 100.0, 500.0, 1000.0, 5000.0, 10000.0]

print(f"{'R_sense (Ohms)':<20} {'dt/tau':<15} {'Stability':<20} {'Divergence (us)':<20}")
print("-" * 75)

for r_sense in r_sense_values:
    tau = 10e-6 / r_sense  # L/R time constant
    dt_tau = 1e-6 / tau
    stable, div_time = test_r_sense(r_sense, duration_us=300.0)

    status = "[STABLE]" if stable else f"[DIVERGE @ {div_time:.0f}us]"
    print(f"{r_sense:<20.1f} {dt_tau:<15.1f} {status:<20} {div_time:<20.1f}")

print("="*80 + "\n")
