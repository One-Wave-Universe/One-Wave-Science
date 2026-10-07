#!/usr/bin/env python3
"""Simple H-bridge test: verify gate control affects a_pos voltage."""
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

        # Load resistor pulls out toward GND when both switches are off
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


def drive_control(mosfet_id, time_us):
    """
    Simple gate control:
    0-10us: both off (gate_hs=0.9, gate_ls=0.2) -> out will settle to some value
    10-20us: high-side on (gate_hs=0.0) -> out should pull toward +V
    20-30us: both off again
    """
    if mosfet_id == "hs":
        # High-side PMOS: gate low (0V) turns it ON and pulls out to +V
        if 10.0 <= time_us < 20.0:
            return 0.0  # PMOS on
        return 0.9  # PMOS off
    elif mosfet_id == "ls":
        # Low-side NMOS: gate high (0.9V) turns it ON and pulls out to GND
        # Keep it off always in this test
        return 0.2  # NMOS off
    return 0.9  # default: off


print("\n" + "="*70)
print("SIMPLE H-BRIDGE TEST: Can gate control move node voltage?")
print("="*70)
print("Expected: out=0.5V baseline, ~1.0V during 10-20us (HS on), 0.5V after\n")

builder = SimpleHBridgeTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(drive_control)

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Time(us)  out_voltage  Mode")
print("-" * 40)

out_max = 0.5

for step in range(n_steps):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)
        state = controller._make_state()

        out = state.node_voltages.get('out', 0.5)
        out_max = max(out_max, out)

        if (step + 1) % 2 == 0 or time_us >= 9.8:  # Print every 2us, plus around transitions
            if 10.0 <= time_us < 20.0:
                mode = "HS_ON"
            else:
                mode = "OFF"
            print(f"{time_us:7.1f}  {out:7.4f}      {mode}")

        if abs(out) > 2.0:
            print(f"(Diverged at {time_us:.1f}us)")
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("-" * 40)
print(f"Max out voltage: {out_max:.4f}V")
if out_max > 0.7:
    print("SUCCESS: Gate control is working!")
else:
    print("FAILURE: out didn't respond to gate control")

print("="*70 + "\n")
