#!/usr/bin/env python3
"""Trace gate function calls and output voltage."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import NMOS, PMOS
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class HBridgeTest:
    def __init__(self):
        self.v_supply = 1.0

    def build(self):
        circuit = TransientCircuit()
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        circuit.add(PMOS(id="hs", gate="gate_hs", drain="+V", source="out", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="ls", gate="gate_ls", drain="out", source="GND", Vth=0.4, Rds_on=0.5))
        circuit.add(Resistor(id="R_load", a="out", b="GND", ohms=1000.0))

        cap_states = {}
        ind_states = {}

        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "out": 0.5,
        }

        return circuit, {"cap_states": cap_states, "ind_states": ind_states, "voltages": voltages}


call_times = {}
last_hs_value = None

def drive_control(mosfet_id, time_us):
    """Gate control with tracing."""
    global last_hs_value

    key = (mosfet_id, round(time_us, 1))

    if mosfet_id == "hs":
        if 10.0 <= time_us < 20.0:
            value = 0.0  # ON
        else:
            value = 0.9  # OFF

        # Print when value changes
        if last_hs_value is None or value != last_hs_value:
            last_hs_value = value
            print(f"  [t={time_us:.1f}us] gate_hs changes to {value} {'(ON)' if value == 0.0 else '(OFF)'}")

        return value
    elif mosfet_id == "ls":
        return 0.2  # Always OFF


print("\n" + "="*70)
print("GATE CONTROL TRACING")
print("="*70 + "\n")

builder = HBridgeTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(drive_control)

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Gate control function calls and output:")
out = 0.5
for step in range(n_steps):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)
        state = controller._make_state()
        out = state.node_voltages.get('out', 0.5)

        if abs(time_us - 9.9) < 0.02 or abs(time_us - 10.0) < 0.02 or abs(time_us - 10.2) < 0.02 or abs(time_us - 20.0) < 0.02 or abs(time_us - 20.2) < 0.02:
            print(f"  [t={time_us:.2f}us] output={out:.4f}V")

        if abs(out) > 2.0:
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("\n" + "="*70 + "\n")
