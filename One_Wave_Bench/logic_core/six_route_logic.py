"""Finite reference model for Updated 43's two-choice/three-move logic.

This module deliberately does not implement commitment amplitudes, phase
memory, magnetic hardware, or consciousness claims. It owns only the exact
finite address space and its validation rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Final, Iterable


class BinaryChoice(IntEnum):
    NO = -1
    YES = 1

    @property
    def one_hot(self) -> tuple[int, int]:
        return (1, 0) if self is BinaryChoice.YES else (0, 1)


class TernaryMove(IntEnum):
    DOWN = -1
    HOLD = 0
    UP = 1


GROUND_ONE_HOT: Final[tuple[int, int]] = (0, 0)
CONFLICT_ONE_HOT: Final[tuple[int, int]] = (1, 1)


@dataclass(frozen=True, slots=True)
class LogicRoute:
    choice: BinaryChoice
    move: TernaryMove

    @property
    def address(self) -> int:
        """Dense stable address in [0, 5]; Ground is not in this space."""
        choice_index = 0 if self.choice is BinaryChoice.NO else 1
        return 3 * choice_index + (int(self.move) + 1)

    @property
    def receipt(self) -> dict[str, object]:
        return {
            "address": self.address,
            "choice": self.choice.name,
            "one_hot": self.choice.one_hot,
            "move": self.move.name,
            "move_value": int(self.move),
        }


def decode_one_hot(bits: tuple[int, int]) -> BinaryChoice:
    """Decode a real binary choice; Ground and conflict are not choices."""
    if bits == (1, 0):
        return BinaryChoice.YES
    if bits == (0, 1):
        return BinaryChoice.NO
    if bits == GROUND_ONE_HOT:
        raise ValueError("Ground (0,0) is not a binary choice")
    if bits == CONFLICT_ONE_HOT:
        raise ValueError("Conflict (1,1) is not a valid binary choice")
    raise ValueError(f"one-hot bits must be binary, got {bits!r}")


def all_routes() -> tuple[LogicRoute, ...]:
    return tuple(
        LogicRoute(choice, move)
        for choice in (BinaryChoice.NO, BinaryChoice.YES)
        for move in (TernaryMove.DOWN, TernaryMove.HOLD, TernaryMove.UP)
    )


def validate_route_space(routes: Iterable[LogicRoute]) -> None:
    routes = tuple(routes)
    if len(routes) != 6:
        raise ValueError(f"expected six routes, got {len(routes)}")
    addresses = {route.address for route in routes}
    if addresses != set(range(6)):
        raise ValueError(f"route addresses must be exactly 0..5, got {sorted(addresses)}")


validate_route_space(all_routes())

