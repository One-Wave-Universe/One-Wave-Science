#!/usr/bin/env python3
"""Test if higher damping completes transients before solver divergence at 38µs."""
from __future__ import annotations
import sys
from pathlib import Path

repo_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(repo_root))

from One_Wave_Bench.engine.electrical.solver_transient import TransientCircuit, CapacitorState, InductorState
from One_Wave_Bench.engine.electrical.components import DCVoltageSource, Resistor, Ground
from One_Wave_Bench.engine.electrical.components_extended import Inductor, NMOS, PMOS, Capacitor
from One_Wave_Bench.engine.electrical.circuit_controller import CircuitController


class HeavilyDampedPhaseTest:
    """Single phase with very high damping resistances to speed up settling."""

    def __init__(self, r_mult: float = 1.0):
        self.v_supply = 1.0
        self.r_mult = r_mult  # Resistance multiplier

    def build(self) -> tuple[TransientCircuit, dict]:
        circuit = TransientCircuit()
        circuit.add(DCVoltageSource(id="V_supply", pos="+V", neg="GND", volts=self.v_supply))
        circuit.add(Ground(node="GND"))
        circuit.add(Capacitor(id="C_dclink", a="DC_LINK", b="GND", farads=10e-6))
        circuit.add(Resistor(id="R_dclink_init", a="+V", b="DC_LINK", ohms=100000.0))

        circuit.add(Resistor(id="R_div_top", a="+V", b="VREF", ohms=100.0))
        circuit.add(Resistor(id="R_div_bottom", a="VREF", b="GND", ohms=100.0))

        circuit.add(PMOS(id="a_pos_HS", gate="gate_a_pos_hs", drain="+V", source="a_pos", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="a_pos_LS", gate="gate_a_pos_ls", drain="a_pos", source="GND", Vth=0.4, Rds_on=0.5))
        circuit.add(PMOS(id="a_neg_HS", gate="gate_a_neg_hs", drain="+V", source="a_neg", Vth=0.4, Rds_on=0.5))
        circuit.add(NMOS(id="a_neg_LS", gate="gate_a_neg_ls", drain="a_neg", source="GND", Vth=0.4, Rds_on=0.5))

        # SENSE - with HIGH damping
        r_sense = 1000.0 * self.r_mult
        circuit.add(Inductor(id="L_A_sense_pos", a="a_pos", b="sense_A_pos", henries=10e-6))
        circuit.add(Resistor(id="R_A_sense_pos", a="sense_A_pos", b="VREF", ohms=r_sense))
        circuit.add(Inductor(id="L_A_sense_neg", a="VREF", b="sense_A_neg", henries=10e-6))
        circuit.add(Resistor(id="R_A_sense_neg", a="sense_A_neg", b="a_neg", ohms=r_sense))

        # DRIVE - with HIGH damping
        r_drive = 500.0 * self.r_mult
        circuit.add(Inductor(id="L_A_drive_pos", a="a_pos", b="drive_A_pos", henries=100e-6))
        circuit.add(Resistor(id="R_A_drive_pos", a="drive_A_pos", b="VREF", ohms=r_drive))
        circuit.add(Inductor(id="L_A_drive_neg", a="VREF", b="drive_A_neg", henries=100e-6))
        circuit.add(Resistor(id="R_A_drive_neg", a="drive_A_neg", b="a_neg", ohms=r_drive))

        # MEMORY - with HIGH damping
        circuit.add(Inductor(id="L_A_memory_pos", a="memory_A_pos_in", b="memory_A_pos_mid", henries=100e-6))
        circuit.add(Resistor(id="R_A_memory_pos", a="memory_A_pos_mid", b="VREF", ohms=r_drive))
        circuit.add(Resistor(id="R_A_memory_pos_damp", a="memory_A_pos_in", b="VREF", ohms=100000.0))
        circuit.add(Inductor(id="L_A_memory_neg", a="VREF", b="memory_A_neg_mid", henries=100e-6))
        circuit.add(Resistor(id="R_A_memory_neg", a="memory_A_neg_mid", b="memory_A_neg_in", ohms=r_drive))
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
print("HEAVILY DAMPED PHASE TEST: Can we escape 38µs divergence?")
print("="*80)

test_configs = [
    (1.0, "R_sense=1kΩ, R_drive=500Ω"),
    (10.0, "R_sense=10kΩ, R_drive=5kΩ"),
    (100.0, "R_sense=100kΩ, R_drive=50kΩ"),
]

for r_mult, desc in test_configs:
    print(f"\n--- Test: {desc} (mult={r_mult}) ---")
    builder = HeavilyDampedPhaseTest(r_mult=r_mult)
    circuit, initial_state = builder.build()
    controller = CircuitController(circuit, initial_state)

    dt_s = 1e-6
    duration_us = 100.0
    n_steps = int(duration_us * 1e-6 / dt_s)

    max_time = 0
    for step in range(n_steps):
        try:
            controller.run_step(dt_s)
            state = controller._make_state()
            a_pos = state.node_voltages.get('a_pos', 0.5)
            if abs(a_pos - 0.5) > 1.5:
                divergence_time = step * dt_s * 1e6
                print(f"  DIVERGED at {divergence_time:.1f}µs")
                break
            max_time = (step + 1) * dt_s * 1e6
        except Exception as e:
            divergence_time = step * dt_s * 1e6
            print(f"  ERROR at {divergence_time:.1f}µs: {str(e)[:50]}")
            break
    else:
        print(f"  STABLE for {duration_us}µs ✓")

print("\n" + "="*80 + "\n")
