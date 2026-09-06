"""3:1 three-winding nerve. Ternary = virtual ground + choice."""

from __future__ import annotations

from dataclasses import dataclass

WINDINGS = ("U", "V", "W")
# (0) = HOLD = virtual ground. That is the whole ternary.
MOVES = ("DOWN", "HOLD", "UP")


@dataclass(frozen=True)
class NerveCommand:
    u: str
    v: str
    w: str
    ground: str = "HOLD"
    source: str = "ADMIN"

    def __post_init__(self) -> None:
        for phase in (self.u, self.v, self.w, self.ground):
            if phase not in MOVES:
                raise ValueError("winding must be DOWN HOLD or UP")


def rest() -> NerveCommand:
    return NerveCommand("HOLD", "HOLD", "HOLD", "HOLD", "ADMIN")


def from_admin(move: str) -> NerveCommand:
    if move not in MOVES:
        raise ValueError("move is DOWN HOLD or UP around virtual ground")
    if move == "HOLD":
        return rest()
    if move == "UP":
        return NerveCommand("UP", "HOLD", "DOWN", "HOLD", "ADMIN")
    return NerveCommand("DOWN", "HOLD", "UP", "HOLD", "ADMIN")


def m4_may_drive() -> bool:
    return False


def ternary_is() -> str:
    return "virtual_ground_plus_choice"
