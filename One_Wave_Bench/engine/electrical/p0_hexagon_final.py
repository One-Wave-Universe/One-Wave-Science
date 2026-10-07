#!/usr/bin/env python3
"""
P0 Hexagon - Final Implementation

Pointy hexagon, clockwise vertices:
  a+ (top, 12 o'clock)
  b+ (top-right, 2 o'clock)
  c+ (bottom-right, 4 o'clock)
  a- (bottom, 6 o'clock)
  b- (bottom-left, 8 o'clock)
  c- (top-left, 10 o'clock)

All connected to central nucleus V_0.

Three dual-polarity phases:
  A: a+ ↔ nucleus ↔ a- (vertical)
  B: b+ ↔ nucleus ↔ b- (diagonal)
  C: c+ ↔ nucleus ↔ c- (diagonal)

Each vertex: half-bridge with independent PMOS/NMOS gate control.
PMOS high-side (gate = pmos_gate), NMOS low-side (gate = nmos_gate).
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer


class P0HexagonFinal:
    """P0 hexagon with independent PMOS/NMOS gate control."""

    def __init__(self,
                 v_supply: float = 5.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 1.0,
                 buffer_rout: float = 0.1):
        self.v_supply = v_supply
        self.l_winding = winding_inductance
        self.r_winding = winding_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.buffer_rout = buffer_rout

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build P0 hexagon circuit."""
        circuit = TransientCircuit()

        # Single supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

        # Virtual ground (nucleus): low-impedance resistor divider + op-amp buffer
        r_div = 100.0
        circuit.add(Resistor(
            id="R_div_top",
            a="+V",
            b="vg_raw",
            ohms=r_div
        ))
        circuit.add(Resistor(
            id="R_div_bottom",
            a="vg_raw",
            b="GND",
            ohms=r_div
        ))

        # Op-amp buffer: unity gain, very low output impedance, high current capacity
        circuit.add(OpAmpBuffer(
            id="nucleus_buffer",
            v_in="vg_raw",
            v_out="nucleus",
            gnd="GND",
            gain=1.0,
            Rout=self.buffer_rout,
            max_sourcing_mA=500.0,
            max_sinking_mA=500.0
        ))

        # Six hex vertices (pointy hexagon, clockwise)
        # a+ (top), b+ (tr), c+ (br), a- (bottom), b- (bl), c- (tl)
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]

        # Each vertex has complementary half-bridge with independent gate control
        for node in hex_nodes:
            # High-side PMOS (gate controlled independently)
            circuit.add(PMOS(
                id=f"{node}_HS",
                gate=f"gate_{node}_hs",  # Independent high-side gate
                drain="+V",
                source=node,
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side NMOS (gate controlled independently)
            circuit.add(NMOS(
                id=f"{node}_LS",
                gate=f"gate_{node}_ls",  # Independent low-side gate
                drain=node,
                source="GND",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

        # Three phases, each connecting opposite hex vertices through nucleus
        phases = [
            ("A", "a_pos", "a_neg"),  # a+ (top) ↔ nucleus ↔ a- (bottom)
            ("B", "b_pos", "b_neg"),  # b+ (tr) ↔ nucleus ↔ b- (bl)
            ("C", "c_pos", "c_neg"),  # c+ (br) ↔ nucleus ↔ c- (tl)
        ]

        for phase_name, pos_node, neg_node in phases:
            # Positive half: pos_node → nucleus
            circuit.add(Inductor(
                id=f"L_{phase_name}_pos",
                a=pos_node,
                b=f"mid_{phase_name}_pos",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_pos",
                a=f"mid_{phase_name}_pos",
                b="nucleus",
                ohms=self.r_winding
            ))

            # Negative half: nucleus → neg_node
            circuit.add(Inductor(
                id=f"L_{phase_name}_neg",
                a="nucleus",
                b=f"mid_{phase_name}_neg",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase_name}_neg",
                a=f"mid_{phase_name}_neg",
                b=neg_node,
                ohms=self.r_winding
            ))

        # Initial state
        cap_states = {}
        ind_states = {
            "L_A_pos": InductorState(id="L_A_pos", current=0.0),
            "L_A_neg": InductorState(id="L_A_neg", current=0.0),
            "L_B_pos": InductorState(id="L_B_pos", current=0.0),
            "L_B_neg": InductorState(id="L_B_neg", current=0.0),
            "L_C_pos": InductorState(id="L_C_pos", current=0.0),
            "L_C_neg": InductorState(id="L_C_neg", current=0.0),
        }

        v_mid = self.v_supply / 2.0
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "vg_raw": v_mid,
            "nucleus": v_mid,
            # Hex vertices all at midpoint initially
            "a_pos": v_mid,
            "b_pos": v_mid,
            "c_pos": v_mid,
            "a_neg": v_mid,
            "b_neg": v_mid,
            "c_neg": v_mid,
            # Winding midpoints
            "mid_A_pos": v_mid,
            "mid_A_neg": v_mid,
            "mid_B_pos": v_mid,
            "mid_B_neg": v_mid,
            "mid_C_pos": v_mid,
            "mid_C_neg": v_mid,
        }

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }


if __name__ == "__main__":
    print("Building P0 hexagon final circuit...")
    builder = P0HexagonFinal(v_supply=5.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built: {len(circuit.components)} components")
    print(f"  Layout: Pointy hexagon, clockwise a+ b+ c+ a- b- c-")
    print(f"  Nucleus: central V_0 buffered at 2.5V")
    print(f"  Phases: A (vertical), B (diagonal), C (diagonal)")
    print(f"  Gates: Independent PMOS/NMOS control per vertex")
