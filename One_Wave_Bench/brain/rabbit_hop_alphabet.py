"""Alphabet/G-721 adapter over the canonical rabbit-hop route core.

The alphabet is one consumer of rabbit hopping, not the definition of rabbit
hopping itself.  Generic route arithmetic lives in
`One_Wave_Bench.rabbit_hop.route_core`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum

from One_Wave_Bench.rabbit_hop.route_core import (
    Polarity,
    RouteFamily,
    WrapperSide,
    route_address,
    route_center,
    shared_shift_boundary,
)


class AlphabetOrientation(str, Enum):
    A_TO_Z = "A-Z"
    Z_TO_A = "Z-A"


class MirrorPolarity(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


class EvenAnchor(IntEnum):
    CURRENT = 0
    NEXT = 1


class OddSide(IntEnum):
    LOWER = -1
    UPPER = 1


@dataclass(frozen=True, slots=True)
class RabbitHopCoordinate:
    letter: str
    orientation: AlphabetOrientation
    polarity: MirrorPolarity
    anchor: EvenAnchor
    odd_side: OddSide
    identity: int
    even: int
    odd: int

    @property
    def tuple(self) -> tuple[int, int, int]:
        return self.identity, self.even, self.odd

    @property
    def side_bit(self) -> int:
        return 0 if self.odd_side is OddSide.LOWER else 1


def alphabet_rank(letter: str, orientation: AlphabetOrientation) -> int:
    normalized = letter.upper()
    if len(normalized) != 1 or not "A" <= normalized <= "Z":
        raise ValueError("letter must be A through Z")
    forward = ord(normalized) - 64
    return forward if orientation is AlphabetOrientation.A_TO_Z else 27 - forward


def coordinate(
    letter: str,
    *,
    orientation: AlphabetOrientation = AlphabetOrientation.A_TO_Z,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    anchor: EvenAnchor = EvenAnchor.CURRENT,
    odd_side: OddSide = OddSide.UPPER,
) -> RabbitHopCoordinate:
    n = alphabet_rank(letter, orientation)
    core_polarity = Polarity(int(polarity))
    offset = int(anchor)
    even = route_address(
        n,
        RouteFamily.SHIFT_FIRST,
        offset=offset,
        wrapper=WrapperSide.CENTER,
        polarity=core_polarity,
    )
    odd = route_address(
        n,
        RouteFamily.SHIFT_FIRST,
        offset=offset,
        wrapper=WrapperSide(int(odd_side)),
        polarity=core_polarity,
    )
    return RabbitHopCoordinate(
        letter.upper(),
        orientation,
        polarity,
        anchor,
        odd_side,
        int(polarity) * n,
        even,
        odd,
    )


def coordinate_family(
    letter: str,
    *,
    orientation: AlphabetOrientation = AlphabetOrientation.A_TO_Z,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
) -> tuple[RabbitHopCoordinate, ...]:
    """Return current-lower/current-upper/next-lower/next-upper."""

    return tuple(
        coordinate(
            letter,
            orientation=orientation,
            polarity=polarity,
            anchor=anchor,
            odd_side=side,
        )
        for anchor in (EvenAnchor.CURRENT, EvenAnchor.NEXT)
        for side in (OddSide.LOWER, OddSide.UPPER)
    )


def validate_coordinate(record: RabbitHopCoordinate) -> None:
    expected = coordinate(
        record.letter,
        orientation=record.orientation,
        polarity=record.polarity,
        anchor=record.anchor,
        odd_side=record.odd_side,
    )
    if record != expected:
        raise ValueError("rabbit-hop coordinate does not match its declared packet")


def shared_odd_bridge(
    letter: str,
    *,
    orientation: AlphabetOrientation = AlphabetOrientation.A_TO_Z,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
) -> int:
    n = alphabet_rank(letter, orientation)
    bridge = shared_shift_boundary(
        n,
        offset=0,
        polarity=Polarity(int(polarity)),
    )
    current_upper = coordinate(
        letter,
        orientation=orientation,
        polarity=polarity,
        anchor=EvenAnchor.CURRENT,
        odd_side=OddSide.UPPER,
    )
    next_lower = coordinate(
        letter,
        orientation=orientation,
        polarity=polarity,
        anchor=EvenAnchor.NEXT,
        odd_side=OddSide.LOWER,
    )
    if bridge != current_upper.odd or bridge != next_lower.odd:
        raise AssertionError("alphabet adapter lost canonical shared boundary")
    return bridge
