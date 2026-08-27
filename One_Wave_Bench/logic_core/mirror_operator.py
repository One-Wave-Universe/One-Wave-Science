"""Mirror candidates for the center-origin six-route architecture.

Mirror is modeled as oscillatory phase evolution.  It never swaps the binary
relation.  The discrete operator is only a projection of the continuous phase
state and must not be mistaken for the physical motion itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import atan2, cos, hypot, pi, sin
from typing import Tuple

from six_route_logic import LogicRoute, TernaryMove


def mirror_route(route: LogicRoute) -> LogicRoute:
    """Finite half-cycle projection: preserve choice, reverse movement."""

    return LogicRoute(route.choice, TernaryMove(-int(route.move)))


@dataclass(frozen=True)
class PhaseState:
    """Normalized oscillator coordinates in one local reference frame."""

    x: float
    v_scaled: float

    @property
    def amplitude(self) -> float:
        return hypot(self.x, self.v_scaled)

    @property
    def phase(self) -> float:
        return atan2(self.v_scaled, self.x)


def rotate_phase(state: PhaseState, delta_phase: float) -> PhaseState:
    """Advance oscillator phase without changing its binary relation.

    ``v_scaled`` is velocity divided by the local angular frequency, allowing
    x and v/omega to share units.  The rotation preserves x^2+(v/omega)^2.
    Damping and drive belong to the later nonlinear oscillator attack.
    """

    c = cos(delta_phase)
    s = sin(delta_phase)
    return PhaseState(
        x=c * state.x - s * state.v_scaled,
        v_scaled=s * state.x + c * state.v_scaled,
    )


def classify_move(state: PhaseState, speed_band: float = 1e-9) -> TernaryMove:
    """Project continuous scaled velocity into DOWN/HOLD/UP."""

    if speed_band < 0.0:
        raise ValueError("speed_band must be nonnegative")
    if state.v_scaled > speed_band:
        return TernaryMove.UP
    if state.v_scaled < -speed_band:
        return TernaryMove.DOWN
    return TernaryMove.HOLD


def at_shared_center(state: PhaseState, center_band: float = 1e-9) -> bool:
    """Detect center residence/crossing independently from net movement."""

    if center_band < 0.0:
        raise ValueError("center_band must be nonnegative")
    return abs(state.x) <= center_band


@dataclass(frozen=True)
class MirrorReceipt:
    before: PhaseState
    after: PhaseState
    delta_phase: float
    amplitude_error: float
    before_move: TernaryMove
    after_move: TernaryMove
    after_at_center: bool


def apply_mirror_phase(
    state: PhaseState,
    delta_phase: float,
    speed_band: float = 1e-9,
    center_band: float = 1e-9,
) -> MirrorReceipt:
    after = rotate_phase(state, delta_phase)
    return MirrorReceipt(
        before=state,
        after=after,
        delta_phase=delta_phase,
        amplitude_error=after.amplitude - state.amplitude,
        before_move=classify_move(state, speed_band),
        after_move=classify_move(after, speed_band),
        after_at_center=at_shared_center(after, center_band),
    )


def canonical_phase_samples(state: PhaseState) -> Tuple[MirrorReceipt, ...]:
    return tuple(apply_mirror_phase(state, angle) for angle in (0.0, pi / 2, pi, 3 * pi / 2, 2 * pi))

