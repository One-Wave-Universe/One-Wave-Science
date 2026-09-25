"""Shared contracts for visible checkers and mounted learning agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence, Tuple

Coord = Tuple[int, int]


@dataclass(frozen=True)
class Move:
    src: Coord
    dst: Coord


@dataclass(frozen=True)
class WorldConsequence:
    accepted: bool
    before_pixels: Tuple[int, ...]
    after_pixels: Tuple[int, ...]
    actor_side: int
    next_side: int
    terminal: bool
    terminal_fact: str
    move: Move


class AgentPlugin(Protocol):
    name: str

    def choose_move(
        self,
        grayscale: Sequence[int],
        width: int,
        height: int,
        side: int,
    ) -> Move:
        ...

    def observe(self, consequence: WorldConsequence) -> None:
        ...

    def reset_episode(self, side: int) -> None:
        ...
