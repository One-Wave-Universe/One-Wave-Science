"""Complete mirrored-alphabet rabbit-hop coordinate family for G-721."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, Enum


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
    sign = int(polarity)
    even_unsigned = 2 * (n + int(anchor))
    odd_unsigned = even_unsigned + int(odd_side)
    return RabbitHopCoordinate(
        letter.upper(), orientation, polarity, anchor, odd_side,
        sign * n, sign * even_unsigned, sign * odd_unsigned,
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
    current_upper = coordinate(
        letter, orientation=orientation, polarity=polarity,
        anchor=EvenAnchor.CURRENT, odd_side=OddSide.UPPER,
    )
    next_lower = coordinate(
        letter, orientation=orientation, polarity=polarity,
        anchor=EvenAnchor.NEXT, odd_side=OddSide.LOWER,
    )
    if current_upper.odd != next_lower.odd:
        raise AssertionError("adjacent even anchors must share their middle odd address")
    return current_upper.odd

