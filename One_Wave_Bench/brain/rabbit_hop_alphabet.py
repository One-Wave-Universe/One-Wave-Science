"""Alphabet adapter for the label-independent Rabbit-Hopping route core.

Alphabet-specific responsibilities live here: A-Z / Z-A rank orientation,
whole-run Mirror Gate layout, and coupled logical up/down inversion. Route
arithmetic itself comes from ``rabbit_hop_core`` so alphabet, music, and later
lattice/memory adapters literally use the same implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum

from One_Wave_Bench.brain.rabbit_hop_core import (
    MirrorPolarity,
    NumericRouteReceipt,
    RouteFamily,
    TraversalDirection,
    WrapperSide,
    numeric_coordinate,
    recover_source_rank as recover_numeric_source_rank,
)


class AlphabetOrientation(str, Enum):
    NORMAL = "A-Z:1-26"
    INVERTED = "Z-A:1-26"

    @property
    def letter_run(self) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return alphabet if self is self.NORMAL else alphabet[::-1]

    @property
    def vertical_sign(self) -> int:
        """Side-to-side alphabet inversion also inverts logical up/down."""

        return 1 if self is self.NORMAL else -1


class AlphabetMirrorLayout(str, Enum):
    A_TO_Z_MIRROR_Z_TO_A = "A-Z(0)Z-A"
    Z_TO_A_MIRROR_A_TO_Z = "Z-A(0)A-Z"

    @property
    def letter_runs(self) -> tuple[str, str]:
        forward = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self is self.A_TO_Z_MIRROR_Z_TO_A:
            return forward, forward[::-1]
        return forward[::-1], forward


@dataclass(frozen=True, slots=True)
class RabbitHopCoordinate:
    """One alphabet identity plus a complete numeric route receipt."""

    letter: str
    alphabet_orientation: AlphabetOrientation
    polarity: MirrorPolarity
    route_family: RouteFamily
    k: int
    wrapper: WrapperSide
    traversal: TraversalDirection
    source_rank: int
    top_address: int
    wrapper_address: int

    @property
    def tuple(self) -> tuple[int, int, int]:
        return self.source_rank, self.top_address, self.wrapper_address

    @property
    def top_parity(self) -> int:
        return abs(self.top_address) % 2

    @property
    def wrapper_parity(self) -> int:
        return abs(self.wrapper_address) % 2

    def opposed(self) -> "RabbitHopCoordinate":
        """Reverse traversal without silently changing any other receipt field."""

        direction = (
            TraversalDirection.REVERSE
            if self.traversal is TraversalDirection.FORWARD
            else TraversalDirection.FORWARD
        )
        return replace(self, traversal=direction)


def alphabet_rank(
    letter: str,
    alphabet_orientation: AlphabetOrientation,
) -> int:
    normalized = letter.upper()
    if len(normalized) != 1 or not "A" <= normalized <= "Z":
        raise ValueError("letter must be A through Z")
    return alphabet_orientation.letter_run.index(normalized) + 1


def alphabet_map(
    alphabet_orientation: AlphabetOrientation,
) -> tuple[tuple[str, int], ...]:
    """Map A-to-Z or Z-to-A traversal to the rank run 1-to-26."""

    return tuple(
        (letter, alphabet_rank(letter, alphabet_orientation))
        for letter in alphabet_orientation.letter_run
    )


def mirrored_alphabet_runs(layout: AlphabetMirrorLayout) -> tuple[str, int, str]:
    """Keep Mirror Gate zero between two whole opposing alphabet runs."""

    left, right = layout.letter_runs
    return left, 0, right


def _to_numeric(record: RabbitHopCoordinate) -> NumericRouteReceipt:
    return NumericRouteReceipt(
        source_rank=record.source_rank,
        polarity=record.polarity,
        route_family=record.route_family,
        k=record.k,
        wrapper=record.wrapper,
        traversal=record.traversal,
        top_address=record.top_address,
        wrapper_address=record.wrapper_address,
        vertical_sign=record.alphabet_orientation.vertical_sign,
    )


def coordinate(
    letter: str,
    *,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
    wrapper: WrapperSide = WrapperSide.UPPER,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> RabbitHopCoordinate:
    """Translate one alphabet source through a complete Rabbit-Hop route."""

    rank = alphabet_rank(letter, alphabet_orientation)
    numeric = numeric_coordinate(
        rank,
        polarity=polarity,
        route_family=route_family,
        k=k,
        wrapper=wrapper,
        traversal=traversal,
        vertical_sign=alphabet_orientation.vertical_sign,
    )
    return RabbitHopCoordinate(
        letter=letter.upper(),
        alphabet_orientation=alphabet_orientation,
        polarity=numeric.polarity,
        route_family=numeric.route_family,
        k=numeric.k,
        wrapper=numeric.wrapper,
        traversal=numeric.traversal,
        source_rank=numeric.source_rank,
        top_address=numeric.top_address,
        wrapper_address=numeric.wrapper_address,
    )


def wrapper_pair(
    letter: str,
    *,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> tuple[RabbitHopCoordinate, RabbitHopCoordinate]:
    """Produce the mandatory TOP-1 and TOP+1 packets for one top."""

    return tuple(
        coordinate(
            letter,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
            route_family=route_family,
            k=k,
            wrapper=wrapper,
            traversal=traversal,
        )
        for wrapper in WrapperSide
    )


def offset_ladder(
    letter: str,
    *,
    route_family: RouteFamily,
    min_k: int,
    max_k: int,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> tuple[tuple[RabbitHopCoordinate, RabbitHopCoordinate], ...]:
    """Materialize an inclusive signed-K ladder for either offset route."""

    if route_family is RouteFamily.ORIGINAL:
        raise ValueError("the original N*2 route has no K ladder")
    if not isinstance(min_k, int) or not isinstance(max_k, int):
        raise TypeError("min_k and max_k must be integers")
    if min_k > max_k:
        raise ValueError("min_k must be <= max_k")
    return tuple(
        wrapper_pair(
            letter,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
            route_family=route_family,
            k=k,
            traversal=traversal,
        )
        for k in range(min_k, max_k + 1)
    )


def ascending_ladder(
    letter: str,
    *,
    route_family: RouteFamily,
    max_k: int,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> tuple[tuple[RabbitHopCoordinate, RabbitHopCoordinate], ...]:
    """Compatibility helper for the historical positive ``K=1..max_k`` run."""

    if not isinstance(max_k, int) or max_k < 1:
        raise ValueError("max_k must be an integer >= 1")
    return offset_ladder(
        letter,
        route_family=route_family,
        min_k=1,
        max_k=max_k,
        alphabet_orientation=alphabet_orientation,
        polarity=polarity,
        traversal=traversal,
    )


def all_declared_routes(
    letter: str,
    *,
    max_k: int,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
) -> tuple[tuple[RabbitHopCoordinate, RabbitHopCoordinate], ...]:
    """Return original plus both signed offset families from -max_k..+max_k."""

    if not isinstance(max_k, int) or max_k < 0:
        raise ValueError("max_k must be an integer >= 0")
    return (
        wrapper_pair(
            letter, alphabet_orientation=alphabet_orientation, polarity=polarity,
        ),
        *offset_ladder(
            letter,
            route_family=RouteFamily.DOUBLE_THEN_SHIFT,
            min_k=-max_k,
            max_k=max_k,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
        ),
        *offset_ladder(
            letter,
            route_family=RouteFamily.SHIFT_THEN_DOUBLE,
            min_k=-max_k,
            max_k=max_k,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
        ),
    )


def recover_source_rank(record: RabbitHopCoordinate) -> int:
    """Use the shared numeric inverse then enforce the alphabet domain 1..26."""

    rank = recover_numeric_source_rank(_to_numeric(record))
    if not 1 <= rank <= 26:
        raise ValueError("recovered alphabet rank is outside 1..26")
    return rank


def validate_coordinate(record: RabbitHopCoordinate) -> None:
    expected = coordinate(
        record.letter,
        alphabet_orientation=record.alphabet_orientation,
        polarity=record.polarity,
        route_family=record.route_family,
        k=record.k,
        wrapper=record.wrapper,
        traversal=record.traversal,
    )
    if record != expected:
        raise ValueError("rabbit-hop packet does not match its route receipt")
    if recover_source_rank(record) != abs(record.source_rank):
        raise ValueError("rabbit-hop receipt does not recover its source rank")
    if record.top_parity == record.wrapper_parity:
        raise ValueError("wrapper must have parity opposite its top")


def validate_wrapper_pair(
    pair: tuple[RabbitHopCoordinate, RabbitHopCoordinate]
) -> None:
    if len(pair) != 2:
        raise ValueError("a top must have exactly two wrapper packets")
    lower, upper = pair
    for record in pair:
        validate_coordinate(record)
    shared = (
        "letter", "alphabet_orientation", "polarity", "route_family", "k",
        "traversal", "source_rank", "top_address",
    )
    if any(getattr(lower, field) != getattr(upper, field) for field in shared):
        raise ValueError("wrapper packets must belong to the same top receipt")
    if lower.wrapper is not WrapperSide.LOWER:
        raise ValueError("first packet must be the lower wrapper")
    if upper.wrapper is not WrapperSide.UPPER:
        raise ValueError("second packet must be the upper wrapper")


def connection_addresses(
    left: tuple[RabbitHopCoordinate, RabbitHopCoordinate],
    right: tuple[RabbitHopCoordinate, RabbitHopCoordinate],
) -> tuple[int, ...]:
    """Return shared wrapper/top handoffs, symmetrically in either direction."""

    validate_wrapper_pair(left)
    validate_wrapper_pair(right)
    left_top = left[0].top_address
    right_top = right[0].top_address
    left_wrappers = {record.wrapper_address for record in left}
    right_wrappers = {record.wrapper_address for record in right}
    points = left_wrappers.intersection(right_wrappers)
    if left_top == right_top:
        points.add(left_top)
    if left_top in right_wrappers:
        points.add(left_top)
    if right_top in left_wrappers:
        points.add(right_top)
    return tuple(sorted(points))


def shared_original_bridge(
    letter: str,
    *,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
) -> int:
    """Return the shared original-route wrapper between N and N+1."""

    next_rank = alphabet_rank(letter, alphabet_orientation) + 1
    if next_rank > 26:
        raise ValueError("the last rank has no next original-route bridge")
    next_letter = alphabet_orientation.letter_run[next_rank - 1]
    current_side = (
        WrapperSide.UPPER
        if alphabet_orientation is AlphabetOrientation.NORMAL
        else WrapperSide.LOWER
    )
    next_side = (
        WrapperSide.LOWER
        if alphabet_orientation is AlphabetOrientation.NORMAL
        else WrapperSide.UPPER
    )
    current_upper = coordinate(
        letter,
        alphabet_orientation=alphabet_orientation,
        polarity=polarity,
        route_family=RouteFamily.ORIGINAL,
        wrapper=current_side,
    )
    next_lower = coordinate(
        next_letter,
        alphabet_orientation=alphabet_orientation,
        polarity=polarity,
        route_family=RouteFamily.ORIGINAL,
        wrapper=next_side,
    )
    if current_upper.wrapper_address != next_lower.wrapper_address:
        raise AssertionError("neighboring original packets must share a wrapper")
    return current_upper.wrapper_address
