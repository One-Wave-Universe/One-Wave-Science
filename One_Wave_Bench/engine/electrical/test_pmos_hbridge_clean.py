#!/usr/bin/env python3
"""H-bridge test: clean initial conditions, no gate voltage initialization."""
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
        # Power supply
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))

        # H-bridge with stronger load to see switching
        circuit.add(PMOS(id="hs", gate="gate_hs", drain="+V", source="out", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="ls", gate="gate_ls", drain="out", source="GND", Vth=0.4, Rds_on=0.5))

        # Smaller load resistor for faster response
        circuit.add(Resistor(id="R_load", a="out", b="GND", ohms=1000.0))

        cap_states = {}
        ind_states = {}

        # Only set node voltages, NOT gate voltages
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "out": 0.5,  # Initial condition for output
        }

        return circuit, {"cap_states": cap_states, "ind_states": ind_states, "voltages": voltages}


def drive_control(mosfet_id, time_us):
    """Gate control."""
    if mosfet_id == "hs":
        # Turn on high-side from 10-20us
        if 10.0 <= time_us < 20.0:
            return 0.0  # Gate low -> PMOS ON
        return 0.9  # Gate high -> PMOS OFF
    elif mosfet_id == "ls":
        # Keep low-side off
        return 0.2  # Gate low -> NMOS OFF


print("\n" + "="*70)
print("H-BRIDGE TEST: Gate control with clean initial conditions")
print("="*70)
print("Load resistor: 1kΩ (smaller for faster response)\n")

builder = HBridgeTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(drive_control)

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Time(us)  out(V)  Status")
print("-" * 40)

for step in range(n_steps):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)
        state = controller._make_state()

        out = state.node_voltages.get('out', 0.5)

        if (step + 1) % 2 == 0 or (9.8 <= time_us <= 10.2) or (19.8 <= time_us <= 20.2):
            if 10.0 <= time_us < 20.0:
                status = "PMOS_ON"
            else:
                status = "OFF"
            print(f"{time_us:7.1f}  {out:7.4f}  {status}")

        if abs(out) > 2.0:
            print(f"(Diverged at {time_us:.1f}us)")
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("-" * 40)
print("="*70 + "\n")
