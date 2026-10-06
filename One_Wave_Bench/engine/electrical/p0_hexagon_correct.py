#!/usr/bin/env python3
"""
P0 Hexagon Circuit - Correct Topology

Six vertices (pointy corners), clockwise from top:
  a+ (top)
  b+ (top-right)
  c+ (bottom-right)
  a- (bottom)
  b- (bottom-left)
  c- (top-left)

All connect to central nucleus (V_0).

Three phases (opposite diagonal pairs):
  A: a+ ↔ nucleus ↔ a- (top ↔ bottom, vertical)
  B: b+ ↔ nucleus ↔ b- (top-right ↔ bottom-left)
  C: c+ ↔ nucleus ↔ c- (bottom-right ↔ top-left)

Complementary gates (PMOS high-side, NMOS low-side).
Neutral gate voltage: 0.5V (keeps both FETs OFF).
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer


class P0HexagonCorrect:
    """P0 hexagon with correct topology and complementary gates."""

    def __init__(self,
                 v_supply: float = 5.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 1.0,
                 buffer_rout: float = 1.0):
        self.v_supply = v_supply
        self.l_winding = winding_inductance
        self.r_winding = winding_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.buffer_rout = buffer_rout

    def build(self) -> tuple[TransientCircuit, dict]:
        """Build correct P0 hexagon circuit."""
        circuit = TransientCircuit()

        # Single supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

        # Virtual ground (nucleus): resistor divider + op-amp buffer
        r_div = 100.0  # Low impedance for stable buffer regulation
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

        circuit.add(OpAmpBuffer(
            id="nucleus_buffer",
            v_in="vg_raw",
            v_out="nucleus",
            gnd="GND",
            gain=1.0,
            Rout=0.1,  # Very low output impedance for regulation
            max_sourcing_mA=500.0,  # High current capacity
            max_sinking_mA=500.0
        ))

        # Six hex vertices (clockwise): a+ (top), b+ (tr), c+ (br), a- (bottom), b- (bl), c- (tl)
        hex_nodes = ["a_pos", "b_pos", "c_pos", "a_neg", "b_neg", "c_neg"]

        # Each vertex has complementary half-bridge (PMOS high, NMOS low)
        for node in hex_nodes:
            # High-side PMOS (gate low = ON, gate high = OFF)
            circuit.add(PMOS(
                id=f"{node}_HS",
                gate=f"gate_{node}",
                drain="+V",
                source=node,
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side NMOS (gate high = ON, gate low = OFF)
            circuit.add(NMOS(
                id=f"{node}_LS",
                gate=f"gate_{node}",
                drain=node,
                source="GND",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

        # Three phases, each connecting opposite hex vertices through nucleus
        phases = [
            ("A", "a_pos", "a_neg"),  # a+ ↔ nucleus ↔ a-
            ("B", "b_pos", "b_neg"),  # b+ ↔ nucleus ↔ b-
            ("C", "c_pos", "c_neg"),  # c+ ↔ nucleus ↔ c-
        ]

        for phase_name, pos_node, neg_node in phases:
            # Positive half: pos_node to nucleus
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

            # Negative half: nucleus to neg_node
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
            "c_neg": v_mid,
            "a_pos": v_mid,
            "b_pos": v_mid,
            "c_pos": v_mid,
            "a_neg": v_mid,
            "b_neg": v_mid,
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
    print("Building correct P0 hexagon circuit...")
    builder = P0HexagonCorrect(v_supply=5.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built: {len(circuit.components)} components")
    print(f"  Topology: 6 vertices + nucleus")
    print(f"  Gate control: complementary (PMOS/NMOS)")
    print(f"  Neutral voltage: 0.5V (both FETs OFF)")
