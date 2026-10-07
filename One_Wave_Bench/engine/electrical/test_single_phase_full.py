#!/usr/bin/env python3
"""Test single phase with all three winding types (drive+sense+memory)."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import Inductor, NMOS, PMOS, Capacitor
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class SinglePhaseFullTest:
    """One phase with drive, sense, and memory windings."""

    def __init__(self):
        self.v_supply = 1.0

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build single phase with all three winding types."""
        circuit = TransientCircuit()

        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        circuit.add(Capacitor(id="C_dclink", a="DC_LINK", b="GND", farads=10e-6))
        circuit.add(Resistor(id="R_dclink_init", a="+V", b="DC_LINK", ohms=100000.0))

        # VREF
        circuit.add(Resistor(id="R_div_top", a="+V", b="VREF", ohms=100.0))
        circuit.add(Resistor(id="R_div_bottom", a="VREF", b="GND", ohms=100.0))

        # Phase A H-bridge
        circuit.add(PMOS(id="a_pos_HS", gate="gate_a_pos_hs", drain="+V", source="a_pos", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="a_pos_LS", gate="gate_a_pos_ls", drain="a_pos", source="GND", Vth=0.4, Rds_on=0.5))
        circuit.add(PMOS(id="a_neg_HS", gate="gate_a_neg_hs", drain="+V", source="a_neg", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="a_neg_LS", gate="gate_a_neg_ls", drain="a_neg", source="GND", Vth=0.4, Rds_on=0.5))

        # SENSE winding
        circuit.add(Inductor(id="L_A_sense_pos", a="a_pos", b="sense_A_pos", henries=10e-6))
        circuit.add(Resistor(id="R_A_sense_pos", a="sense_A_pos", b="VREF", ohms=100.0))
        circuit.add(Inductor(id="L_A_sense_neg", a="VREF", b="sense_A_neg", henries=10e-6))
        circuit.add(Resistor(id="R_A_sense_neg", a="sense_A_neg", b="a_neg", ohms=100.0))

        # DRIVE winding
        circuit.add(Inductor(id="L_A_drive_pos", a="a_pos", b="drive_A_pos", henries=100e-6))
        circuit.add(Resistor(id="R_A_drive_pos", a="drive_A_pos", b="VREF", ohms=5.0))
        circuit.add(Inductor(id="L_A_drive_neg", a="VREF", b="drive_A_neg", henries=100e-6))
        circuit.add(Resistor(id="R_A_drive_neg", a="drive_A_neg", b="a_neg", ohms=5.0))

        # MEMORY winding
        circuit.add(Inductor(id="L_A_memory_pos", a="memory_A_pos_in", b="memory_A_pos_mid", henries=100e-6))
        circuit.add(Resistor(id="R_A_memory_pos", a="memory_A_pos_mid", b="VREF", ohms=5.0))
        circuit.add(Resistor(id="R_A_memory_pos_damp", a="memory_A_pos_in", b="VREF", ohms=100000.0))
        circuit.add(Inductor(id="L_A_memory_neg", a="VREF", b="memory_A_neg_mid", henries=100e-6))
        circuit.add(Resistor(id="R_A_memory_neg", a="memory_A_neg_mid", b="memory_A_neg_in", ohms=5.0))
        circuit.add(Resistor(id="R_A_memory_neg_damp", a="memory_A_neg_in", b="VREF", ohms=100000.0))

        cap_states = {"C_dclink": CapacitorState(id="C_dclink", voltage=self.v_supply)}
        ind_states = {
            "L_A_sense_pos": InductorState(id="L_A_sense_pos", current=0.0),
            "L_A_sense_neg": InductorState(id="L_A_sense_neg", current=0.0),
            "L_A_drive_pos": InductorState(id="L_A_drive_pos", current=0.0),
            "L_A_drive_neg": InductorState(id="L_A_drive_neg", current=0.0),
            "L_A_memory_pos": InductorState(id="L_A_memory_pos", current=0.0),
            "L_A_memory_neg": InductorState(id="L_A_memory_neg", current=0.0),
        }

        v_baseline = 0.50
        voltages = {
            "+V": self.v_supply, "GND": 0.0, "VREF": v_baseline, "DC_LINK": self.v_supply,
            "a_pos": v_baseline, "a_neg": v_baseline,
            "sense_A_pos": v_baseline, "sense_A_neg": v_baseline,
            "drive_A_pos": v_baseline, "drive_A_neg": v_baseline,
            "memory_A_pos_in": v_baseline, "memory_A_pos_mid": v_baseline,
            "memory_A_neg_in": v_baseline, "memory_A_neg_mid": v_baseline,
            "gate_a_pos_hs": 0.9, "gate_a_pos_ls": 0.2,
            "gate_a_neg_hs": 0.9, "gate_a_neg_ls": 0.2,
        }

        return circuit, {"cap_states": cap_states, "ind_states": ind_states, "voltages": voltages}


print("\n" + "="*80)
print("SINGLE PHASE, FULL WINDINGS (6 inductors total)")
print("="*80)
print("\nCircuit: Phase A with Drive, Sense, Memory windings\n")

builder = SinglePhaseFullTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)

dt_s = 1e-6
duration_us = 500.0
n_steps = int(duration_us * 1e-6 / dt_s)

print(f"{'Time (µs)':<15} {'V_a_pos':<15} {'Status':<20}")
print("-" * 50)

for step in range(n_steps):
    try:
        controller.run_step(dt_s)
        state = controller._make_state()
        a_pos = state.node_voltages.get('a_pos', 0.5)
        if abs(a_pos - 0.5) > 1.5:
            divergence_time = step * dt_s * 1e6
            print(f"{divergence_time:<15.1f} {a_pos:<15.4f} DIVERGED!")
            break
        if (step + 1) % 50 == 0:
            time_us = (step + 1) * dt_s * 1e6
            delta = abs(a_pos - 0.5)
            status = "OK" if delta < 0.1 else f"DRIFT({delta:.3f})"
            print(f"{time_us:<15.1f} {a_pos:<15.4f} {status:<20}")
    except Exception as e:
        print(f"EXCEPTION: {e}")
        break
else:
    print("-" * 50)
    print(f"✓ STABLE for {duration_us}µs")

print("="*80 + "\n")
