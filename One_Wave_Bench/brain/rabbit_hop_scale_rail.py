"""Bounded 1-12 outward / 12-24 division rail for Rabbit Hopping.

The rail is numerical and label-independent.  A musical-neck or alphabet
adapter may label its addresses separately without redefining this topology.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum


FORWARD_SOURCE_MIN = 1
FORWARD_SOURCE_MAX = 12
DIVISION_ADDRESS_MIN = 12
DIVISION_ADDRESS_MAX = 24


class WrapperSide(IntEnum):
    LOWER = -1
    UPPER = 1


class DivisionRole(str, Enum):
    TOP = "top"
    LOWER_WRAPPER = "lower-wrapper"
    UPPER_WRAPPER = "upper-wrapper"


@dataclass(frozen=True, slots=True)
class ForwardPacket:
    """One complete ``source | doubled top | mandatory wrapper`` packet."""

    source: int
    top: int
    wrapper: int
    wrapper_side: WrapperSide

    @property
    def tuple(self) -> tuple[int, int, int]:
        return self.source, self.top, self.wrapper


@dataclass(frozen=True, slots=True)
class DivisionCandidate:
    """One exact way an outer address points back to the 1-12 rail."""

    outer_address: int
    source: int
    source_top: int
    outer_role: DivisionRole


def forward_pair(source: int) -> tuple[ForwardPacket, ForwardPacket]:
    """Generate both mandatory wrappers for one source in the 1-12 rail."""

    if not isinstance(source, int) or not FORWARD_SOURCE_MIN <= source <= FORWARD_SOURCE_MAX:
        raise ValueError("forward source must be an integer from 1 through 12")
    top = source * 2
    return tuple(
        ForwardPacket(source, top, top + int(side), side)
        for side in WrapperSide
    )


def division_candidates(address: int) -> tuple[DivisionCandidate, ...]:
    """Read an address from 12-24 back toward its exact 1-12 source(s).

    Even addresses are doubled tops and divide directly by two.  Odd addresses
    are shared wrappers: ``address-1`` and ``address+1`` are the neighboring
    even tops, so division returns both connected sources without fractions.
    """

    if not isinstance(address, int) or not DIVISION_ADDRESS_MIN <= address <= DIVISION_ADDRESS_MAX:
        raise ValueError("division address must be an integer from 12 through 24")
    if address % 2 == 0:
        return (
            DivisionCandidate(
                outer_address=address,
                source=address // 2,
                source_top=address,
                outer_role=DivisionRole.TOP,
            ),
        )
    return (
        DivisionCandidate(
            outer_address=address,
            source=(address - 1) // 2,
            source_top=address - 1,
            outer_role=DivisionRole.UPPER_WRAPPER,
        ),
        DivisionCandidate(
            outer_address=address,
            source=(address + 1) // 2,
            source_top=address + 1,
            outer_role=DivisionRole.LOWER_WRAPPER,
        ),
    )


def division_rail() -> tuple[tuple[int, tuple[int, ...]], ...]:
    """Return the complete declared 12-24 division map."""

    return tuple(
        (address, tuple(candidate.source for candidate in division_candidates(address)))
        for address in range(DIVISION_ADDRESS_MIN, DIVISION_ADDRESS_MAX + 1)
    )

