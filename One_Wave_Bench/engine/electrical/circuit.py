"""
Circuit -- a plain container of components plus a .solve() entry point.
Owns no physics itself; delegates to solver.solve_dc(). See
components.py for the parts this batch supports.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from .components import DCVoltageSource, Resistor, Wire, Ground
from .solver import solve_dc, SolveResult


@dataclass
class Circuit:
    resistors: list[Resistor] = field(default_factory=list)
    sources: list[DCVoltageSource] = field(default_factory=list)
    wires: list[Wire] = field(default_factory=list)
    grounds: list[Ground] = field(default_factory=list)

    def add(self, component):
        if isinstance(component, Resistor):
            self.resistors.append(component)
        elif isinstance(component, DCVoltageSource):
            self.sources.append(component)
        elif isinstance(component, Wire):
            self.wires.append(component)
        elif isinstance(component, Ground):
            self.grounds.append(component)
        else:
            raise TypeError(
                f"{type(component).__name__} is not one of the components this "
                "batch supports (DCVoltageSource, Resistor, Wire, Ground)."
            )
        return component

    def solve(self) -> SolveResult:
        return solve_dc(self)
