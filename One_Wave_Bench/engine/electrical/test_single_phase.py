#!/usr/bin/env python3
"""Test a single phase sense winding in isolation."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import Inductor, NMOS, PMOS, OpAmpBuffer
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class SinglePhaseTest:
    """Absolute minimum: one phase, one sense winding."""

    def __init__(self, r_sense: float):
        self.r_sense = r_sense
        self.v_supply = 1.0

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build single-phase sense winding."""
        circuit = TransientCircuit()

        # Supply and ground
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        # VREF as simple resistor divider (no opamp)
        circuit.add(Resistor(id="R_div_top", a="+V", b="VREF", ohms=100.0))
        circuit.add(Resistor(id="R_div_bottom", a="VREF", b="GND", ohms=100.0))

        # Single phase with H-bridge (unpowered)
        circuit.add(PMOS(
            id="a_pos_HS", gate="gate_a_pos_hs", drain="+V", source="a_pos",
            Vth=0.4, Rds_on=0.5
        ))
        circuit.add(NMOS(
            id="a_pos_LS", gate="gate_a_pos_ls", drain="a_pos", source="GND",
            Vth=0.4, Rds_on=0.5
        ))
        circuit.add(PMOS(
            id="a_neg_HS", gate="gate_a_neg_hs", drain="+V", source="a_neg",
            Vth=0.4, Rds_on=0.5
        ))
        circuit.add(NMOS(
            id="a_neg_LS", gate="gate_a_neg_ls", drain="a_neg", source="GND",
            Vth=0.4, Rds_on=0.5
        ))

        # Single sense winding
        circuit.add(Inductor(
            id="L_A_sense_pos", a="a_pos", b="sense_A_pos",
            henries=10e-6  # 10µH
        ))
        circuit.add(Resistor(
            id="R_A_sense_pos", a="sense_A_pos", b="VREF",
            ohms=self.r_sense
        ))

        circuit.add(Inductor(
            id="L_A_sense_neg", a="VREF", b="sense_A_neg",
            henries=10e-6  # 10µH
        ))
        circuit.add(Resistor(
            id="R_A_sense_neg", a="sense_A_neg", b="a_neg",
            ohms=self.r_sense
        ))

        # Initial state
        ind_states = {
            "L_A_sense_pos": InductorState(id="L_A_sense_pos", current=0.0),
            "L_A_sense_neg": InductorState(id="L_A_sense_neg", current=0.0),
        }

        v_baseline = 0.50
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "VREF": v_baseline,
            "a_pos": v_baseline,
            "a_neg": v_baseline,
            "sense_A_pos": v_baseline,
            "sense_A_neg": v_baseline,
            "gate_a_pos_hs": 0.9,
            "gate_a_pos_ls": 0.2,
            "gate_a_neg_hs": 0.9,
            "gate_a_neg_ls": 0.2,
        }

        return circuit, {
            "cap_states": {},
            "ind_states": ind_states,
            "voltages": voltages
        }


print("\n" + "="*80)
print("SINGLE-PHASE SENSE WINDING: Absolute minimum stability test")
print("="*80)
print("\nCircuit: One phase A with sense winding L=10µH, R=variable")
print("         Star-grounded at VREF = 0.50V (resistor divider)")
print("         H-bridge present but unpowered (gates held off)")
print("         Solver: Backward Euler, dt = 1us\n")

r_sense_values = [100.0, 500.0, 1000.0, 5000.0, 10000.0]

print(f"{'R_sense (Ohms)':<20} {'dt/tau':<15} {'Stability':<20} {'Result (us)':<20}")
print("-" * 75)

for r_sense in r_sense_values:
    tau = 10e-6 / r_sense
    dt_tau = 1e-6 / tau

    builder = SinglePhaseTest(r_sense=r_sense)
    circuit, initial_state = builder.build()
    controller = CircuitController(circuit, initial_state)

    dt_s = 1e-6
    stable = True
    divergence_time = None

    for step in range(500000):  # 500us max
        try:
            controller.run_step(dt_s)
            state = controller._make_state()

            a_sense = state.node_voltages.get('sense_A_pos', 0.5)

            if abs(a_sense - 0.5) > 1.5:  # Diverged from baseline
                divergence_time = step * dt_s * 1e6
                stable = False
                break

        except Exception as e:
            divergence_time = step * dt_s * 1e6
            stable = False
            break

    if stable:
        status = "[STABLE 500us]"
        result = "500.0"
    else:
        status = f"[DIVERGE]"
        result = f"{divergence_time:.0f}"

    print(f"{r_sense:<20.1f} {dt_tau:<15.1f} {status:<20} {result:<20}")

print("="*80 + "\n")
