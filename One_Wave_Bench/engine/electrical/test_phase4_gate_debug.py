#!/usr/bin/env python3
"""Debug: Add prints to gate control function to verify it's called."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import NMOS, PMOS
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class SimpleHBridgeTest:
    def __init__(self):
        self.v_supply = 1.0

    def build(self):
        circuit = TransientCircuit()
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        # H-bridge
        circuit.add(PMOS(id="hs", gate="gate_hs", drain="+V", source="out", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="ls", gate="gate_ls", drain="out", source="GND", Vth=0.4, Rds_on=0.5))

        # Load resistor
        circuit.add(Resistor(id="R_load", a="out", b="GND", ohms=10000.0))

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


gate_call_count = {}

def drive_control(mosfet_id, time_us):
    """Gate control with debug prints."""
    key = (mosfet_id, int(time_us / 5))  # Group by 5us windows
    if key not in gate_call_count:
        gate_call_count[key] = 0
        # Print on first call in each window
        if mosfet_id == "hs":  # Only print for HS to reduce output
            print(f"  [t={time_us:.1f}us] gate_hs called")
    gate_call_count[key] += 1

    if mosfet_id == "hs":
        if 10.0 <= time_us < 20.0:
            return 0.0  # ON
        return 0.9  # OFF
    elif mosfet_id == "ls":
        return 0.2  # OFF
    return 0.9


print("\n" + "="*70)
print("GATE CONTROL DEBUG TEST")
print("="*70 + "\n")

builder = SimpleHBridgeTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)

print("Setting gate control function...")
controller.set_gate_control(drive_control)
print("Gate control set.\n")

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Running simulation...")
print("Time(us)  out")
print("-" * 20)

for step in range(n_steps):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)
        state = controller._make_state()

        out = state.node_voltages.get('out', 0.5)

        if (step + 1) % 5 == 0:
            print(f"{time_us:7.1f}  {out:7.4f}")

        if abs(out) > 2.0:
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("-" * 20)
print(f"\nGate function was called {sum(gate_call_count.values())} times total")
print("="*70 + "\n")
