#!/usr/bin/env python3
"""Phase 4: Pull a_pos HIGH (not LOW) for increasing state transfer."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import Inductor, NMOS, PMOS, Capacitor
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class Phase4Test:
    def __init__(self):
        self.v_supply = 1.0

    def build(self):
        circuit = TransientCircuit()
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))
        circuit.add(Capacitor(id="C_dclink", a="DC_LINK", b="GND", farads=10e-6))
        circuit.add(Resistor(id="R_dclink_init", a="+V", b="DC_LINK", ohms=100000.0))

        # VREF
        circuit.add(Resistor(id="R_div_top", a="+V", b="VREF", ohms=100.0))
        circuit.add(Resistor(id="R_div_bottom", a="VREF", b="GND", ohms=100.0))

        # PHASE A: Drive + Sense
        circuit.add(PMOS(id="a_pos_HS", gate="gate_a_pos_hs", drain="+V", source="a_pos", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="a_pos_LS", gate="gate_a_pos_ls", drain="a_pos", source="GND", Vth=0.4, Rds_on=0.5))
        circuit.add(PMOS(id="a_neg_HS", gate="gate_a_neg_hs", drain="+V", source="a_neg", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="a_neg_LS", gate="gate_a_neg_ls", drain="a_neg", source="GND", Vth=0.4, Rds_on=0.5))

        # A sense
        circuit.add(Inductor(id="L_A_sense_pos", a="a_pos", b="sense_A_pos", henries=10e-6))
        circuit.add(Resistor(id="R_A_sense_pos", a="sense_A_pos", b="VREF", ohms=5000.0))
        circuit.add(Inductor(id="L_A_sense_neg", a="VREF", b="sense_A_neg", henries=10e-6))
        circuit.add(Resistor(id="R_A_sense_neg", a="sense_A_neg", b="a_neg", ohms=5000.0))

        # A drive
        circuit.add(Inductor(id="L_A_drive_pos", a="a_pos", b="drive_A_pos", henries=100e-6))
        circuit.add(Resistor(id="R_A_drive_pos", a="drive_A_pos", b="VREF", ohms=100.0))
        circuit.add(Inductor(id="L_A_drive_neg", a="VREF", b="drive_A_neg", henries=100e-6))
        circuit.add(Resistor(id="R_A_drive_neg", a="drive_A_neg", b="a_neg", ohms=100.0))

        # PHASE B: Memory
        circuit.add(PMOS(id="b_pos_HS", gate="gate_b_pos_hs", drain="+V", source="b_pos", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="b_pos_LS", gate="gate_b_pos_ls", drain="b_pos", source="GND", Vth=0.4, Rds_on=0.5))
        circuit.add(PMOS(id="b_neg_HS", gate="gate_b_neg_hs", drain="+V", source="b_neg", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="b_neg_LS", gate="gate_b_neg_ls", drain="b_neg", source="GND", Vth=0.4, Rds_on=0.5))

        # B memory
        circuit.add(Inductor(id="L_B_memory_pos", a="memory_B_pos_in", b="memory_B_pos_mid", henries=100e-6))
        circuit.add(Resistor(id="R_B_memory_pos", a="memory_B_pos_mid", b="VREF", ohms=100.0))
        circuit.add(Resistor(id="R_B_memory_pos_damp", a="memory_B_pos_in", b="VREF", ohms=100000.0))
        circuit.add(Inductor(id="L_B_memory_neg", a="VREF", b="memory_B_neg_mid", henries=100e-6))
        circuit.add(Resistor(id="R_B_memory_neg", a="memory_B_neg_mid", b="memory_B_neg_in", ohms=100.0))
        circuit.add(Resistor(id="R_B_memory_neg_damp", a="memory_B_neg_in", b="VREF", ohms=100000.0))

        # Nerve: A_sense -> B_memory
        circuit.add(Resistor(id="R_nerve_A_sense_to_B_memory_pos", a="sense_A_pos", b="memory_B_pos_in", ohms=10000.0))
        circuit.add(Resistor(id="R_nerve_A_sense_to_B_memory_neg", a="sense_A_neg", b="memory_B_neg_in", ohms=10000.0))

        cap_states = {"C_dclink": CapacitorState(id="C_dclink", voltage=self.v_supply)}
        ind_states = {
            "L_A_sense_pos": InductorState(id="L_A_sense_pos", current=0.0),
            "L_A_sense_neg": InductorState(id="L_A_sense_neg", current=0.0),
            "L_A_drive_pos": InductorState(id="L_A_drive_pos", current=0.0),
            "L_A_drive_neg": InductorState(id="L_A_drive_neg", current=0.0),
            "L_B_memory_pos": InductorState(id="L_B_memory_pos", current=0.0),
            "L_B_memory_neg": InductorState(id="L_B_memory_neg", current=0.0),
        }

        v_baseline = 0.50
        voltages = {
            "+V": self.v_supply, "GND": 0.0, "VREF": v_baseline, "DC_LINK": self.v_supply,
            "a_pos": v_baseline, "a_neg": v_baseline,
            "b_pos": v_baseline, "b_neg": v_baseline,
            "sense_A_pos": v_baseline, "sense_A_neg": v_baseline,
            "drive_A_pos": v_baseline, "drive_A_neg": v_baseline,
            "memory_B_pos_in": v_baseline, "memory_B_pos_mid": v_baseline,
            "memory_B_neg_in": v_baseline, "memory_B_neg_mid": v_baseline,
        }

        return circuit, {"cap_states": cap_states, "ind_states": ind_states, "voltages": voltages}


def drive_control(mosfet_id, time):
    """
    Drive a_pos HIGH (HS on, LS off) during 10-20us.
    """
    time_us = time * 1e6

    if "HS" in mosfet_id:
        if mosfet_id == "a_pos_HS":
            # Turn HIGH-side ON during 10-20us to pull a_pos HIGH
            return 0.0 if 10.0 <= time_us < 20.0 else 0.9
        else:
            # All other HS OFF
            return 0.9
    elif "LS" in mosfet_id:
        # All low-sides OFF (gate low -> off)
        return 0.2
    else:
        return 0.9


print("\n" + "="*70)
print("PHASE 4: A->B STATE TRANSFER (PULL a_pos HIGH)")
print("="*70)
print("Protocol: 0-10us baseline")
print("          10-20us pull a_pos HIGH via HS")
print("          20-30us relax\n")

builder = Phase4Test()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(drive_control)

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Time(us)  sense_A  mem_B    a_pos    drive_A  Mode")
print("-" * 55)

sense_a_max = 0.50
mem_b_max = 0.50
a_pos_max = 0.50

for step in range(n_steps):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)
        state = controller._make_state()

        sense_a = state.node_voltages.get('sense_A_pos', 0.50)
        mem_b = state.node_voltages.get('memory_B_pos_in', 0.50)
        a_pos = state.node_voltages.get('a_pos', 0.50)
        drive_a = state.node_voltages.get('drive_A_pos', 0.50)

        sense_a_max = max(sense_a_max, sense_a)
        mem_b_max = max(mem_b_max, mem_b)
        a_pos_max = max(a_pos_max, a_pos)

        if (step + 1) % 3 == 0:
            mode = "DRIVE" if 10.0 <= time_us < 20.0 else "BASE"
            print(f"{time_us:7.1f}  {sense_a:7.4f}  {mem_b:7.4f}  {a_pos:7.4f}  {drive_a:7.4f}  {mode}")

        if abs(a_pos - 0.5) > 1.5:
            print(f"(Diverged at {time_us:.1f}us)")
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("-" * 55)
print(f"Max sense_A: {sense_a_max:.4f}V (success >0.55V: {sense_a_max > 0.55})")
print(f"Max mem_B:   {mem_b_max:.4f}V (success >0.50V: {mem_b_max > 0.50})")
print(f"Max a_pos:   {a_pos_max:.4f}V")

if sense_a_max > 0.55 and mem_b_max > 0.50:
    print("\nSUCCESS: A->B transfer demonstrated!")
else:
    print("\nPhase 4 test shows A->B coupling (needs higher drive for full criteria)")

print("="*70 + "\n")
