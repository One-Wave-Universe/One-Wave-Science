"""
Measurements read a SolveResult. They never mutate it and never change the
circuit's answer -- see Virtual_Breadboard/00_RULES/measurement_rules.md's
"measurement is separate from simulation behavior" for why that boundary
matters.

Every function here is a plain arithmetic read of already-solved state
(node voltages, source branch currents). None of them re-solve anything or
assume a value -- if the circuit changes, calling these again on a fresh
SolveResult reflects that change automatically.
"""
from __future__ import annotations
from .solver import SolveResult
from .components import Resistor, DCVoltageSource


def node_voltage(result: SolveResult, node: str) -> float:
    """V(node), relative to whichever node the solver used as its 0V
    reference -- see result.reference_node."""
    return result.voltages[node]


def differential_voltage(result: SolveResult, node_a: str, node_b: str) -> float:
    """V(node_a) - V(node_b). Always safe to call regardless of which node
    happens to be the solver's own internal reference."""
    return result.voltages[node_a] - result.voltages[node_b]


def resistor_current(result: SolveResult, r: Resistor) -> float:
    """Real branch current through a resistor via Ohm's law, using the
    resistor's OWN solved terminal voltages. Positive = current flowing
    from r.a to r.b."""
    va = result.voltages[r.a]
    vb = result.voltages[r.b]
    return (va - vb) / r.ohms


def source_current(result: SolveResult, s: DCVoltageSource) -> float:
    """Real source branch current, positive when the source is discharging
    (delivering current out of its own + terminal into the external
    circuit) -- the same convention used by
    Virtual_Breadboard/js/circuit.js's battery model."""
    return result.source_currents[s.id]


def resistor_power(result: SolveResult, r: Resistor) -> float:
    """P = I^2 * R, always >= 0 (a resistor only dissipates)."""
    i = resistor_current(result, r)
    return i * i * r.ohms


def source_power(result: SolveResult, s: DCVoltageSource) -> float:
    """P = V * I. Positive when the source is delivering real power into
    the circuit (discharging); negative would mean something external is
    driving current back into it."""
    return s.volts * source_current(result, s)


def total_resistor_power(result: SolveResult, resistors: list[Resistor]) -> float:
    return sum(resistor_power(result, r) for r in resistors)


def total_source_power(result: SolveResult, sources: list[DCVoltageSource]) -> float:
    return sum(source_power(result, s) for s in sources)
