#!/usr/bin/env python3
"""Debug: Check the time values being passed to gate function."""
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


call_log = []

def debug_gate_function(mosfet_id, time):
    """Gate function with detailed logging."""
    if mosfet_id == "hs":
        # Log the time value
        time_us = time * 1e6 if time < 1 else time  # Check if it's in seconds or us

        if len(call_log) < 20:  # Only log first 20 calls
            call_log.append((mosfet_id, time, time_us))

        # Try both interpretations
        if time < 0.001:  # Likely seconds
            if time < 0.00001:  # <10us
                return 0.9  # OFF
            elif time < 0.00002:  # 10-20us
                return 0.0  # ON
            else:
                return 0.9  # OFF
        else:  # Likely already in microseconds
            if time < 10.0:
                return 0.9  # OFF
            elif time < 20.0:
                return 0.0  # ON
            else:
                return 0.9  # OFF
    elif mosfet_id == "ls":
        return 0.2


print("\n" + "="*70)
print("GATE TIMING DEBUG")
print("="*70 + "\n")

builder = HBridgeTest()
circuit, initial_state = builder.build()
controller = CircuitController(circuit, initial_state)
controller.set_gate_control(debug_gate_function)

dt_s = 1e-6
duration_us = 30.0
n_steps = int(duration_us * 1e-6 / dt_s)

print("First 20 gate function calls:")
print("Step  mosfet_id  time(raw)     time*1e6       time_us_check")
print("-" * 65)

for step in range(min(20, n_steps)):
    time_us = (step + 1) * dt_s * 1e6

    try:
        controller.run_step(dt_s)

        if step < len(call_log):
            mid, t_raw, t_us = call_log[step]
            print(f"{step:3d}  {mid:8}  {t_raw:.9f}  {t_us:.4f}  {t_us:.1f}us")

    except Exception as e:
        print(f"ERROR: {e}")
        break

print("\n" + "="*70 + "\n")
