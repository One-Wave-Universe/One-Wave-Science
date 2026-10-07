#!/usr/bin/env python3
"""Debug: Check if gate control function is being applied."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import Inductor, NMOS, PMOS, Capacitor
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class SimpleHBridgeTest:
    def __init__(self):
        self.v_supply = 1.0

    def build(self):
        circuit = TransientCircuit()
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        # Simple H-bridge with one node to drive
        circuit.add(PMOS(id="hs", gate="gate_hs", drain="+V", source="out", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="ls", gate="gate_ls", drain="out", source="GND", Vth=0.4, Rds_on=0.5))

        # Small load resistor on output
        circuit.add(Resistor(id="R_load", a="out", b="GND", ohms=1000.0))

        cap_states = {}
        ind_states = {}

        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "out": 0.5,
            "gate_hs": 0.9,
            "gate_ls": 0.2,
        }

        return circuit, {"cap_states": cap_states, "ind_states": ind_states, "voltages": voltages}


def drive_control(mosfet_id, time_us):
    """Simple gate control."""
    if mosfet_id == "hs":
        # Turn on high-side from 10-20us
        if 10.0 <= time_us < 20.0:
            return 0.0  # PMOS on
        return 0.9  # PMOS off
    elif mosfet_id == "ls":
        # Keep low-side off always
        return 0.2  # NMOS off


print("\n" + "="*70)
print("SIMPLE H-BRIDGE GATE TEST")
print("="*70 + "\n")

builder = SimpleHBridgeTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(drive_control)

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Time(us)  out     gate_hs  gate_ls")
print("-" * 45)

for step in range(n_steps):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)
        state = controller._make_state()

        out = state.node_voltages.get('out', 0.5)
        gate_hs = state.node_voltages.get('gate_hs', 0.9)
        gate_ls = state.node_voltages.get('gate_ls', 0.2)

        if (step + 1) % 2 == 0:  # Print every 2us
            print(f"{time_us:7.1f}  {out:7.4f}  {gate_hs:7.4f}  {gate_ls:7.4f}")

        if abs(out) > 2.0:
            print(f"(Diverged at {time_us:.1f}us)")
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("-" * 45)
print("="*70 + "\n")
