#!/usr/bin/env python3
"""Test PMOS with gate always driven low (always ON)."""
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

        # PMOS with gate always low
        circuit.add(PMOS(id="hs", gate="gate_hs", drain="+V", source="out", Vth=0.4, Rds_on=0.5))
        # Load resistor to ground
        circuit.add(Resistor(id="R_load", a="out", b="GND", ohms=1000.0))

        cap_states = {}
        ind_states = {}

        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "out": 0.5,
        }

        return circuit, {"cap_states": cap_states, "ind_states": ind_states, "voltages": voltages}


def always_low_gate(mosfet_id, time_us):
    """Gate always low -> PMOS should be ON."""
    if mosfet_id == "hs":
        return 0.0  # Always ON
    return 0.0


print("\n" + "="*70)
print("PMOS ALWAYS ON TEST")
print("="*70)
print("Expected: PMOS pulls out toward +V\n")

builder = HBridgeTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(always_low_gate)

dt_s = 1e-6
duration_us = 10.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("Time(us)  out(V)")
print("-" * 25)

for step in range(n_steps):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)
        state = controller._make_state()

        out = state.node_voltages.get('out', 0.5)

        if (step + 1) % 1 == 0:  # Print every step
            print(f"{time_us:7.1f}  {out:7.4f}")

        if abs(out - 1.0) < 0.01:
            print("SUCCESS: out settled to +V!")
            break

        if abs(out) > 2.0:
            print(f"DIVERGED at {time_us:.1f}us")
            break

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("-" * 25)
print("="*70 + "\n")
