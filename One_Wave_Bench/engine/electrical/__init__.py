"""
One-Wave Bench — small DC electrical subsystem.

Scope for this batch (see engine/electrical/README.md): DCVoltageSource,
Resistor, Wire, Ground, a real Kirchhoff/Ohm nodal solver, and the
voltage/current/power/energy measurements needed for plain resistive DC
networks. Nothing else -- no MOSFETs, capacitors, inductors, comparators,
batteries-with-internal-resistance, LEDs, magnetics, or macros yet.

This package does not modify engine/run_experiment.py or the D-413 engine.
It is a separate, self-contained addition that a caller can import directly.
"""
from .components import DCVoltageSource, Resistor, Wire, Ground, GROUND
from .circuit import Circuit
from .solver import solve_dc, SolveResult
from . import measurements
from . import energy

__all__ = [
    "DCVoltageSource", "Resistor", "Wire", "Ground", "GROUND",
    "Circuit", "solve_dc", "SolveResult",
    "measurements", "energy",
]
