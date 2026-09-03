"""Locked rabbit-hopping addressing and system-communication translator.

There are exactly three currently declared routes: one original route and two
ascending K routes.  Every route produces a top address and every complete
packet ends with either the top-minus-one or top-plus-one wrapper.

The same fully attributed address receipt can cross a system boundary without
losing its source, top, wrapper, route family, K, polarity, or direction.

Division here only verifies that a fully attributed receipt can mechanically
recover its source rank.  The broader meaning/job of division remains open.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, IntEnum


class AlphabetOrientation(str, Enum):
    NORMAL = "A-Z:1-26"
    INVERTED = "Z-A:1-26"

    @property
    def letter_run(self) -> str:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return alphabet if self is self.NORMAL else alphabet[::-1]

    @property
    def vertical_sign(self) -> int:
        """Side-to-side inversion also inverts logical up/down."""

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


class MirrorPolarity(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


class RouteFamily(str, Enum):
    ORIGINAL = "N*2"
    ASCENDING_AFTER = "N*2+K"
    ASCENDING_BEFORE = "(N+K)*2"


class WrapperSide(IntEnum):
    LOWER = -1
    UPPER = 1


class TraversalDirection(str, Enum):
    FORWARD = "forward"
    REVERSE = "reverse"


@dataclass(frozen=True, slots=True)
class RabbitHopCoordinate:
    """One complete ``source | top | wrapper`` address receipt."""

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


def _validate_route_k(route_family: RouteFamily, k: int) -> None:
    if not isinstance(k, int):
        raise TypeError("K must be an integer")
    if route_family is RouteFamily.ORIGINAL:
        if k != 0:
            raise ValueError("the original N*2 route has no K; use K=0")
    elif k < 1:
        raise ValueError("ascending routes require K >= 1")


def _unsigned_top(source_rank: int, route_family: RouteFamily, k: int) -> int:
    if route_family is RouteFamily.ORIGINAL:
        return source_rank * 2
    if route_family is RouteFamily.ASCENDING_AFTER:
        return source_rank * 2 + k
    return (source_rank + k) * 2


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
    """Produce one complete address packet while preserving its route."""

    _validate_route_k(route_family, k)
    rank = alphabet_rank(letter, alphabet_orientation)
    top = _unsigned_top(rank, route_family, k)
    sign = int(polarity)
    return RabbitHopCoordinate(
        letter=letter.upper(),
        alphabet_orientation=alphabet_orientation,
        polarity=polarity,
        route_family=route_family,
        k=k,
        wrapper=wrapper,
        traversal=traversal,
        source_rank=sign * rank,
        top_address=sign * top,
        wrapper_address=(
            sign * (top + alphabet_orientation.vertical_sign * int(wrapper))
        ),
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
    """Produce the mandatory lower and upper wrappers for one top."""

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


def ascending_ladder(
    letter: str,
    *,
    route_family: RouteFamily,
    max_k: int,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> tuple[tuple[RabbitHopCoordinate, RabbitHopCoordinate], ...]:
    """Materialize K=1..max_k for one of the two ascending routes."""

    if route_family is RouteFamily.ORIGINAL:
        raise ValueError("the original route is not an ascending K ladder")
    if not isinstance(max_k, int) or max_k < 1:
        raise ValueError("max_k must be an integer >= 1")
    return tuple(
        wrapper_pair(
            letter,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
            route_family=route_family,
            k=k,
            traversal=traversal,
        )
        for k in range(1, max_k + 1)
    )


def all_declared_routes(
    letter: str,
    *,
    max_k: int,
    alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
) -> tuple[tuple[RabbitHopCoordinate, RabbitHopCoordinate], ...]:
    """Return original, after-ascending, and before-ascending packets."""

    return (
        wrapper_pair(
            letter, alphabet_orientation=alphabet_orientation, polarity=polarity,
        ),
        *ascending_ladder(
            letter,
            route_family=RouteFamily.ASCENDING_AFTER,
            max_k=max_k,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
        ),
        *ascending_ladder(
            letter,
            route_family=RouteFamily.ASCENDING_BEFORE,
            max_k=max_k,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
        ),
    )


def recover_source_rank(record: RabbitHopCoordinate) -> int:
    """Mechanically invert a complete receipt; division's larger role is open."""

    unsigned_wrapper = int(record.polarity) * record.wrapper_address
    top = (
        unsigned_wrapper
        - record.alphabet_orientation.vertical_sign * int(record.wrapper)
    )
    if record.route_family is RouteFamily.ORIGINAL:
        numerator = top
    elif record.route_family is RouteFamily.ASCENDING_AFTER:
        numerator = top - record.k
    else:
        if top % 2:
            raise ValueError("before-ascending receipt has an invalid odd top")
        rank = top // 2 - record.k
        if not 1 <= rank <= 26:
            raise ValueError("recovered alphabet rank is outside 1..26")
        return rank
    if numerator % 2:
        raise ValueError("receipt cannot mechanically recover an integer rank")
    rank = numerator // 2
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
