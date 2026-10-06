"""P0 Ternary Circuit Builder

Constructs the canonical P0 three-phase ternary circuit with:
- Power rails (±V or single supply with virtual ground)
- TLE2426-like virtual ground buffer
- Three half-bridges (U, V, W phases)
- Three windings as loads
- Dead-band window comparators (model as threshold triggers)

This is what you actually solder. The circuit model lets you verify:
1. Midpoint stability with virtual ground (should stay at ~0V even under load)
2. Dead-band hysteresis prevents shoot-through
3. Flyback currents don't destroy gates
4. Phase sequencing actually produces the intended field
"""
from __future__ import annotations
from .solver_transient import TransientCircuit, CapacitorState, InductorState
from .components import DCVoltageSource, Resistor, Wire, Ground
from .components_extended import Capacitor, Inductor, NMOS, PMOS, OpAmpBuffer


class P0TernaryCircuit:
    """Builder for the P0 ternary circuit."""

    def __init__(self,
                 v_supply: float = 5.0,
                 gate_drive_impedance: float = 10.0,
                 winding_inductance: float = 1e-3,
                 winding_resistance: float = 5.0,
                 mosfet_rds_on: float = 0.5,
                 mosfet_vth: float = 1.0,
                 buffer_rout: float = 1.0):
        """
        Args:
            v_supply: supply voltage (single positive supply or ±V magnitude)
            gate_drive_impedance: gate drive source impedance (ohms)
            winding_inductance: each phase winding inductance (H)
            winding_resistance: each phase winding resistance (ohms)
            mosfet_rds_on: MOSFET on-state resistance (ohms)
            mosfet_vth: MOSFET threshold voltage (V)
            buffer_rout: virtual ground buffer output impedance (ohms)
        """
        self.v_supply = v_supply
        self.gate_impedance = gate_drive_impedance
        self.l_winding = winding_inductance
        self.r_winding = winding_resistance
        self.rds_on = mosfet_rds_on
        self.vth = mosfet_vth
        self.buffer_rout = buffer_rout

    def build(self, supply_mode: str = "split") -> tuple[TransientCircuit, dict]:
        """Build the P0 circuit.

        Args:
            supply_mode: "split" (+V / -V) or "single" (0 to +V with virtual ground)

        Returns:
            (circuit, initial_state_dict)
            where initial_state_dict contains cap_states, ind_states, voltages
        """
        circuit = TransientCircuit()

        if supply_mode == "split":
            return self._build_split(circuit)
        elif supply_mode == "single":
            return self._build_single(circuit)
        else:
            raise ValueError(f"Unknown supply_mode: {supply_mode}")

    def _build_split(self, circuit: TransientCircuit) -> tuple[TransientCircuit, dict]:
        """Build circuit with ±V split rails.

        +V --- [high FET] --- winding --- [low FET] --- -V
               (tied to phase midpoint)
        """
        # Power supplies
        circuit.add(DCVoltageSource(
            id="V_pos",
            pos="+V",
            neg="0",
            volts=self.v_supply
        ))
        circuit.add(DCVoltageSource(
            id="V_neg",
            pos="0",
            neg="-V",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="0"))

        # Three phases: U, V, W
        for phase in ["U", "V", "W"]:
            # High-side FET (PMOS)
            circuit.add(PMOS(
                id=f"{phase}_HS",
                gate=f"gate_{phase}",
                drain=f"+V",
                source=f"mid_{phase}",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side FET (NMOS)
            circuit.add(NMOS(
                id=f"{phase}_LS",
                gate=f"gate_{phase}",
                drain=f"mid_{phase}",
                source=f"-V",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Winding (inductor + resistor)
            circuit.add(Inductor(
                id=f"L_{phase}",
                a=f"mid_{phase}",
                b=f"winding_{phase}_return",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase}",
                a=f"winding_{phase}_return",
                b="0",
                ohms=self.r_winding
            ))

        # Initial state
        cap_states = {}
        ind_states = {
            "L_U": InductorState(id="L_U", current=0.0),
            "L_V": InductorState(id="L_V", current=0.0),
            "L_W": InductorState(id="L_W", current=0.0),
        }
        voltages = {
            "+V": self.v_supply,
            "-V": -self.v_supply,
            "0": 0.0,
            # Initialize phase and winding nodes for proper MNA
            "mid_U": 0.0,      # Each phase initially at midpoint (0V)
            "mid_V": 0.0,
            "mid_W": 0.0,
            "winding_U_return": 0.0,  # Winding returns initially at centerpoint
            "winding_V_return": 0.0,
            "winding_W_return": 0.0,
        }

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }

    def _build_single(self, circuit: TransientCircuit) -> tuple[TransientCircuit, dict]:
        """Build circuit with single +V supply and TLE2426 virtual ground.

        +V --- [resistor divider] --- 0V (virtual ground buffer) --- GND

        Each phase ties to the virtual ground midpoint:

        +V --- [high FET] --- mid --- [low FET] --- GND
        """
        # Single supply
        circuit.add(DCVoltageSource(
            id="V_supply",
            pos="+V",
            neg="GND",
            volts=self.v_supply
        ))
        circuit.add(Ground(node="GND"))

        # Virtual ground: resistor divider feeding a unity buffer
        # Passive divider: two equal resistors from +V to GND
        r_div = 1000.0  # 1k resistor divider
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

        # TLE2426 or op-amp buffer (unity gain, ~1 ohm output impedance)
        circuit.add(OpAmpBuffer(
            id="VG_buffer",
            v_in="vg_raw",
            v_out="0",
            gnd="GND",
            gain=1.0,
            Rout=self.buffer_rout,
            max_sourcing_mA=100.0,
            max_sinking_mA=100.0
        ))

        # Three phases
        for phase in ["U", "V", "W"]:
            # High-side FET (NMOS, common-source from +V)
            circuit.add(NMOS(
                id=f"{phase}_HS",
                gate=f"gate_{phase}",
                drain=f"+V",
                source=f"mid_{phase}",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Low-side FET (NMOS, common-source to GND)
            circuit.add(NMOS(
                id=f"{phase}_LS",
                gate=f"gate_{phase}",
                drain=f"mid_{phase}",
                source="GND",
                Vth=self.vth,
                Rds_on=self.rds_on
            ))

            # Winding
            circuit.add(Inductor(
                id=f"L_{phase}",
                a=f"mid_{phase}",
                b=f"winding_{phase}_return",
                henries=self.l_winding
            ))
            circuit.add(Resistor(
                id=f"R_{phase}",
                a=f"winding_{phase}_return",
                b="0",  # virtual ground
                ohms=self.r_winding
            ))

        # Initial state
        cap_states = {}
        ind_states = {
            "L_U": InductorState(id="L_U", current=0.0),
            "L_V": InductorState(id="L_V", current=0.0),
            "L_W": InductorState(id="L_W", current=0.0),
        }
        v_mid = self.v_supply / 2.0  # Midpoint voltage (virtual ground)
        voltages = {
            "+V": self.v_supply,
            "GND": 0.0,
            "0": v_mid,  # virtual ground starts at midpoint
            "vg_raw": v_mid,
            # Initialize winding and phase nodes for proper Vgs calculation
            "mid_U": v_mid,      # Each phase initially at midpoint
            "mid_V": v_mid,
            "mid_W": v_mid,
            "winding_U_return": v_mid,  # Winding returns initially at virtual ground
            "winding_V_return": v_mid,
            "winding_W_return": v_mid,
        }

        return circuit, {
            "cap_states": cap_states,
            "ind_states": ind_states,
            "voltages": voltages
        }
