"""History-dependent candidate for the five commitment readouts.

The five readouts are derived from a continuous latent commitment coordinate;
they are not five primitive choices.  This is a falsifiable control model, not
yet a physical One-Wave law.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos
from typing import Iterable, Tuple

from six_route_logic import LogicRoute


VALID_LEVELS = (-3, -2, 0, 2, 3)


@dataclass(frozen=True)
class CommitmentParameters:
    retention: float = 0.92
    gain: float = 0.24
    partial_enter: float = 0.40
    partial_exit: float = 0.28
    full_enter: float = 0.82
    full_exit: float = 0.68
    limit: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.retention <= 1.0:
            raise ValueError("retention must be in [0,1]")
        if self.gain <= 0.0 or self.limit <= 0.0:
            raise ValueError("gain and limit must be positive")
        if not (0.0 <= self.partial_exit < self.partial_enter
                < self.full_exit < self.full_enter <= self.limit):
            raise ValueError("thresholds must satisfy exit/enter hysteresis ordering")


@dataclass(frozen=True)
class CommitmentState:
    latent: float = 0.0
    level: int = 0

    def __post_init__(self) -> None:
        if self.level not in VALID_LEVELS:
            raise ValueError(f"invalid commitment level: {self.level}")


@dataclass(frozen=True)
class CommitmentReceipt:
    before: CommitmentState
    after: CommitmentState
    route_address: int
    differential: float
    phase_error: float
    phase_lock: float
    signed_drive: float


def phase_lock(phase_error: float) -> float:
    """Bounded alignment: one at zero error, zero at opposite phase."""

    return 0.5 * (1.0 + cos(phase_error))


def _read_level(latent: float, previous: int, p: CommitmentParameters) -> int:
    """Schmitt-style five-state readout with separate entry and exit gates."""

    # Retain full commitment until its lower exit threshold is crossed.
    if previous == 3 and latent >= p.full_exit:
        return 3
    if previous == -3 and latent <= -p.full_exit:
        return -3

    # Full entry takes priority over partial-state retention.
    if latent >= p.full_enter:
        return 3
    if latent <= -p.full_enter:
        return -3

    # Retain partial commitment through its hysteresis band.
    if previous in (2, 3) and latent >= p.partial_exit:
        return 2
    if previous in (-2, -3) and latent <= -p.partial_exit:
        return -2

    if latent >= p.partial_enter:
        return 2
    if latent <= -p.partial_enter:
        return -2
    return 0


def read_commitment_level(
    latent: float,
    previous: int = 0,
    parameters: CommitmentParameters = CommitmentParameters(),
) -> int:
    """Public deterministic readout for threshold and noise audits."""

    if previous not in VALID_LEVELS:
        raise ValueError(f"invalid previous commitment level: {previous}")
    return _read_level(latent, previous, parameters)


def update_commitment(
    state: CommitmentState,
    route: LogicRoute,
    differential: float,
    phase_error: float,
    parameters: CommitmentParameters = CommitmentParameters(),
) -> CommitmentReceipt:
    """Advance one receipt.

    Candidate semantics: movement sign is oriented through the binary relation.
    UP reinforces the selected relation, DOWN retracts/reverses it, and HOLD
    contributes no new drive while retention carries prior state. Differential
    magnitude is bounded to one. This semantic choice must be compared with
    absolute-axis and energy-gradient alternatives before canonization.
    """

    bounded_differential = min(abs(differential), 1.0)
    lock = phase_lock(phase_error)
    signed_drive = int(route.choice) * int(route.move) * bounded_differential * lock
    latent = parameters.retention * state.latent + parameters.gain * signed_drive
    latent = max(-parameters.limit, min(parameters.limit, latent))
    level = _read_level(latent, state.level, parameters)
    after = CommitmentState(latent=latent, level=level)
    return CommitmentReceipt(
        before=state,
        after=after,
        route_address=route.address,
        differential=differential,
        phase_error=phase_error,
        phase_lock=lock,
        signed_drive=signed_drive,
    )


def run_history(
    initial: CommitmentState,
    inputs: Iterable[Tuple[LogicRoute, float, float]],
    parameters: CommitmentParameters = CommitmentParameters(),
) -> Tuple[CommitmentReceipt, ...]:
    receipts = []
    state = initial
    for route, differential, phase_error in inputs:
        receipt = update_commitment(state, route, differential, phase_error, parameters)
        receipts.append(receipt)
        state = receipt.after
    return tuple(receipts)
