#!/usr/bin/env python3
"""
P0 Hexagonal Transfluxor Circuit

Six nodes on flat-edge hexagon, clockwise: A+, B+, C+, A−, B−, C−
All connected to central nucleus (V_0).

Three phases with dual polarity:
- A phase: A+ ↔ nucleus ↔ A− (state/temperature, DC)
- B phase: B+ ↔ nucleus ↔ B− (rotation/gyro, AC)
- C phase: C+ ↔ nucleus ↔ C− (gradient, RC)

Each outer node has a half-bridge (high/low FET pair).
All phases reference through the nucleus.
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Inductor, NMOS, PMOS, OpAmpBuffer


class P0HexagonalCircuit:
    """Builder for hexagonal P0 transfluxor with six dual-polarity nodes."""

    def __init__(self,
                 v_supply: float = 5.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 1.0,
                 buffer_rout: float = 1.0):
        """
        Args:
            v_supply: supply voltage (single positive supply)
            winding_inductance: each phase winding inductance (H)
            winding_resistance: each phase winding resistance (ohms)
            mosfet_rds_on: MOSFET on-state resistance (ohms)
            mosfet_vth: MOSFET threshold voltage (V)
            buffer_rout: nucleus buffer output impedance (ohms)
        """
        self.v_supply = v_supply
        self.l_winding = winding_inductance
        self.r_winding = winding_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.buffer_rout = buffer_rout

    def build(self) -> tuple[TransientCircuit, dict]:
        """
        Build hexagonal P0 circuit with dual-polarity phases.

        Returns:
            (circuit, initial_state_dict)
        """
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
        r_div = 1000.0
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

        # Op-amp buffer: unity gain, low output impedance
        circuit.add(OpAmpBuffer(
            id="nucleus_buffer",
            v_in="vg_raw",
            v_out="nucleus",  # Central nucleus node
            gnd="GND",
            gain=1.0,
            Rout=self.buffer_rout,
            max_sourcing_mA=100.0,
            max_sinking_mA=100.0
        ))

        # Six hex nodes, clockwise: A+, B+, C+, A−, B−, C−
        hex_nodes = ["A_pos", "B_pos", "C_pos", "A_neg", "B_neg", "C_neg"]

        # Each hex node has a half-bridge (high-side NMOS, low-side NMOS)
        for node in hex_nodes:
            # High-side FET (NMOS, from +V)
            circuit.add(NMOS(
                id=f"{node}_HS",
                gate=f"gate_{node}",
                drain="+V",
                source=node,
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side FET (NMOS, to GND)
            circuit.add(NMOS(
                id=f"{node}_LS",
                gate=f"gate_{node}",
                drain=node,
                source="GND",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

        # Three phases, each connecting opposite hex nodes through nucleus
        phases = [
            ("A", "A_pos", "A_neg"),  # A phase: A+ ↔ nucleus ↔ A−
            ("B", "B_pos", "B_neg"),  # B phase: B+ ↔ nucleus ↔ B−
            ("C", "C_pos", "C_neg"),  # C phase: C+ ↔ nucleus ↔ C−
        ]

        # Each phase has two windings:
        # Winding 1: positive node → nucleus
        # Winding 2: nucleus → negative node
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
            # Hex nodes all start at midpoint
            "A_pos": v_mid,
            "B_pos": v_mid,
            "C_pos": v_mid,
            "A_neg": v_mid,
            "B_neg": v_mid,
            "C_neg": v_mid,
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
    print("Building hexagonal P0 transfluxor circuit...")
    builder = P0HexagonalCircuit(v_supply=5.0)
    circuit, initial_state = builder.build()
    print(f"✓ Circuit built: {len(circuit.components)} components")
    print(f"  Nodes: nucleus, A+, B+, C+, A−, B−, C−")
    print(f"  Phases: A (state), B (rotation), C (gradient)")
    print(f"  Each phase: bidirectional through nucleus")
