#!/usr/bin/env python3
"""Phase 4 A->B state transfer test with corrected gate drive logic."""
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

        # A sense (high damping R=5000 for stability)
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
            "gate_a_pos_hs": 0.9, "gate_a_pos_ls": 0.2,
            "gate_a_neg_hs": 0.9, "gate_a_neg_ls": 0.2,
            "gate_b_pos_hs": 0.9, "gate_b_pos_ls": 0.2,
            "gate_b_neg_hs": 0.9, "gate_b_neg_ls": 0.2,
        }

        return circuit, {"cap_states": cap_states, "ind_states": ind_states, "voltages": voltages}


def drive_control(mosfet_id, time_us):
    """
    Gate control with proper complementary switching.
    0-10us: baseline (all switches off)
    10-20us: drive a_pos HIGH (HS on, LS off) then LOW (HS off, LS on)
    20-30us: back to baseline
    """
    # Baseline: all HS=0.9V (off), all LS=0.2V (off)
    if "HS" in mosfet_id:
        # During 10-12us, pull a_pos HIGH via PMOS (gate=0V turns PMOS on)
        if 10.0 <= time_us < 12.0 and "a_pos_HS" in mosfet_id:
            return 0.0  # PMOS on (pulls a_pos to +V)
        # During 12-20us, pull a_pos LOW via NMOS (gate=0.9V turns NMOS on)
        if 12.0 <= time_us < 20.0 and "a_pos_LS" in mosfet_id:
            return 0.9  # NMOS on (but this is handled below)
        return 0.9  # Default: HS off
    else:  # LS switches
        # During 10-12us keep LS off (gate=0.2V)
        if 10.0 <= time_us < 12.0:
            return 0.2  # LS off
        # During 12-20us, pull a_pos LOW via NMOS (gate=0.9V)
        if 12.0 <= time_us < 20.0 and "a_pos_LS" in mosfet_id:
            return 0.9  # NMOS on (pulls a_pos to GND)
        return 0.2  # Default: LS off


print("\n" + "="*70)
print("PHASE 4: A->B STATE TRANSFER TEST (CORRECTED DRIVE)")
print("="*70)
print("Protocol: 0-10us baseline")
print("          10-12us drive a_pos HIGH")
print("          12-20us drive a_pos LOW")
print("          20-30us baseline\n")

builder = Phase4Test()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(drive_control)

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Time(us)  sense_A  mem_B    a_pos   drive_A  Mode")
print("-" * 60)

sense_a_max = 0.50
mem_b_max = 0.50
drive_a_max = 0.50

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
        drive_a_max = max(drive_a_max, drive_a)

        if (step + 1) % 2 == 0:  # Print every 2us
            if 10.0 <= time_us < 12.0:
                mode = "DRIVE_HIGH"
            elif 12.0 <= time_us < 20.0:
                mode = "DRIVE_LOW"
            else:
                mode = "BASE"
            print(f"{time_us:7.1f}  {sense_a:7.4f}  {mem_b:7.4f}  {a_pos:7.4f}  {drive_a:7.4f}  {mode}")

        if abs(a_pos - 0.5) > 1.5:
            print(f"(Diverged at {time_us:.1f}us - solver limit)")
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("-" * 60)
print(f"Max sense_A:  {sense_a_max:.4f}V")
print(f"Max mem_B:    {mem_b_max:.4f}V")
print(f"Max drive_A:  {drive_a_max:.4f}V")

if sense_a_max > 0.55 and mem_b_max > 0.50:
    print("\nSUCCESS: A->B transfer demonstrated!")
else:
    print("\nLimited response observed")

print("="*70 + "\n")
