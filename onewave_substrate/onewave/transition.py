"""Pure ternary transition semantics: Gamma (gate), Phi (field update), T.

Everything in this module is a pure function over immutable dataclasses.
No I/O, no mutation of inputs, no randomness. That is what makes replay()
possible: identical (initial State, ordered (A, B) inputs, params) always
reproduces the identical final State.

    R_{t+1} = T(R_t, A_t, B_t)

Internally:

    g_t        = Gamma(F_t, A_t, B_t)
    Delta_{t+1} = Delta_t + delta_step * g_t
    M_{t+1}     = lambda * M_t + g_t
    F_{t+1}     = Phi(M_{t+1}, Delta_{t+1}) = sgn3(M_{t+1} - kappa * Delta_{t+1})

Design decisions made where the brief's LaTeX was ambiguous, documented
here rather than silently baked in:

* Gamma's dual-ternary consensus rule. A is the proposal, B is the
  confirmation. Precedence, highest first:
    1. Ground input: A == HOLD or B == HOLD -> HOLD.
    2. Mirror cancellation: F != HOLD and A == -F -> HOLD, regardless of B.
       (`A = -F -> g = 0` is a hard invariant per the brief, not merely
       the "no consensus" case below -- it fires even when B agrees with
       A, e.g. A=B=-1 against F=+1 is still cancellation, not RETURN.)
    3. Consensus: A == B -> g = A (the confirmed proposal is admitted,
       ADVANCE or RETURN as signed). A != B (and neither is HOLD, and
       it's not mirror cancellation) -> HOLD: an unconfirmed proposal
       does not move the state.
  This makes Gamma total and deterministic over all 27 (F, A, B)
  combinations -- see tests/test_gamma.py for the full truth table.

* Phi uses a *restoring* sign: F_{t+1} = sgn3(M_{t+1} - kappa * Delta_{t+1}).
  Retained memory (M) pushes the field gradient forward; accumulated
  displacement (Delta) pulls it back toward the local reference, the way
  a restoring force opposes displacement in the rest of the One-Wave
  material (see Nodes/A-105_Restoring_Response.md). This keeps runtime
  state bounded rather than monotonically diverging under a steady g.
"""

from __future__ import annotations

from dataclasses import dataclass

from onewave.ternary import Ternary, sgn3


@dataclass(frozen=True)
class TransitionParams:
    """Configurable constants for the reference transition dynamics."""

    delta_step: float = 1.0
    lam: float = 0.5   # 0 < lambda < 1
    kappa: float = 1.0  # kappa > 0

    def __post_init__(self) -> None:
        if not (0.0 < self.lam < 1.0):
            raise ValueError(f"lambda must satisfy 0 < lambda < 1, got {self.lam}")
        if not (self.kappa > 0.0):
            raise ValueError(f"kappa must satisfy kappa > 0, got {self.kappa}")


@dataclass(frozen=True)
class State:
    """The (F_t, Delta_t, M_t) triple. Event history (h_t) is tracked
    separately as an append-only event log (see events.py) rather than
    embedded in this dataclass, so State stays a small, cheap-to-compare
    value type -- exactly what replay() needs to diff against.
    """

    field_state: Ternary = Ternary.HOLD
    displacement: float = 0.0
    memory_state: float = 0.0


def gamma(field_state: Ternary, a: Ternary, b: Ternary) -> Ternary:
    """Gamma(F, A, B) -> g. See module docstring for the precedence rules."""
    if a == Ternary.HOLD or b == Ternary.HOLD:
        return Ternary.HOLD
    if field_state != Ternary.HOLD and a == -field_state:
        return Ternary.HOLD
    if a != b:
        return Ternary.HOLD
    return Ternary(a)


def phi(memory_state: float, displacement: float, params: TransitionParams) -> Ternary:
    """Phi(M, Delta) -> F. See module docstring for the restoring-sign choice."""
    return sgn3(memory_state - params.kappa * displacement)


def transition(state: State, a: Ternary, b: Ternary, params: TransitionParams) -> tuple[State, Ternary]:
    """R_{t+1} = T(R_t, A_t, B_t). Returns (new_state, gate_result).

    Pure: `state` is never mutated. Callers that need an event record
    build one from (state, a, b, gate_result, new_state) themselves --
    see events.append_event / runtime.apply_transition.
    """
    g = gamma(state.field_state, a, b)
    new_displacement = state.displacement + params.delta_step * int(g)
    new_memory = params.lam * state.memory_state + int(g)
    new_field = phi(new_memory, new_displacement, params)
    new_state = State(
        field_state=new_field,
        displacement=new_displacement,
        memory_state=new_memory,
    )
    return new_state, g
