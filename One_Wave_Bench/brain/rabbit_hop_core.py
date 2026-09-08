"""Label-independent Rabbit-Hopping route arithmetic.

This module is the reusable numerical core. Domain adapters (alphabet, music,
neck/fret, memory, lattice, movement) supply labels and domain bounds; they do
not redefine the route math.

A route is computed in two stages:

1. choose a top using operation order and signed integer ``K``;
2. choose exactly one connector ``s`` around that top, ``TOP-1`` or ``TOP+1``.

Canonical routes:

* ORIGINAL: ``TOP = 2N`` (K must be zero)
* DOUBLE_THEN_SHIFT: ``TOP = 2N + K``
* SHIFT_THEN_DOUBLE: ``TOP = 2(N + K)``

Complete numeric packet:

``N | TOP | TOP+s`` where ``s in {-1,+1}``.

Equal numeric destinations do not erase route identity.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum, IntEnum


class RouteFamily(str, Enum):
    ORIGINAL = "N*2"
    DOUBLE_THEN_SHIFT = "N*2+K"
    SHIFT_THEN_DOUBLE = "(N+K)*2"

    # Compatibility aliases for the earlier positive-only naming.
    ASCENDING_AFTER = "N*2+K"
    ASCENDING_BEFORE = "(N+K)*2"


class WrapperSide(IntEnum):
    LOWER = -1
    UPPER = 1


class MirrorPolarity(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


class TraversalDirection(str, Enum):
    FORWARD = "forward"
    REVERSE = "reverse"


@dataclass(frozen=True, slots=True)
class NumericRouteReceipt:
    """A complete label-independent Rabbit-Hop receipt."""

    source_rank: int
    polarity: MirrorPolarity
    route_family: RouteFamily
    k: int
    wrapper: WrapperSide
    traversal: TraversalDirection
    top_address: int
    wrapper_address: int
    vertical_sign: int = 1

    @property
    def tuple(self) -> tuple[int, int, int]:
        return self.source_rank, self.top_address, self.wrapper_address

    @property
    def top_parity(self) -> int:
        return abs(self.top_address) % 2

    @property
    def wrapper_parity(self) -> int:
        return abs(self.wrapper_address) % 2

    def opposed(self) -> "NumericRouteReceipt":
        direction = (
            TraversalDirection.REVERSE
            if self.traversal is TraversalDirection.FORWARD
            else TraversalDirection.FORWARD
        )
        return replace(self, traversal=direction)


def validate_k(route_family: RouteFamily, k: int) -> None:
    if not isinstance(k, int):
        raise TypeError("K must be an integer")
    if route_family is RouteFamily.ORIGINAL and k != 0:
        raise ValueError("the original N*2 route has no offset; use K=0")


def unsigned_top(source_rank: int, route_family: RouteFamily, k: int = 0) -> int:
    """Return the pre-polarity top for a positive domain source rank."""

    if not isinstance(source_rank, int):
        raise TypeError("source_rank must be an integer")
    validate_k(route_family, k)
    if route_family is RouteFamily.ORIGINAL:
        return source_rank * 2
    if route_family is RouteFamily.DOUBLE_THEN_SHIFT:
        return source_rank * 2 + k
    return (source_rank + k) * 2


def numeric_coordinate(
    source_rank: int,
    *,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
    wrapper: WrapperSide = WrapperSide.UPPER,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
    vertical_sign: int = 1,
) -> NumericRouteReceipt:
    """Build a complete ``source | top | wrapper`` numeric receipt.

    ``vertical_sign`` lets an adapter couple its own orientation inversion to
    logical lower/upper while keeping polarity independent. It must be +/-1.
    """

    if vertical_sign not in (-1, 1):
        raise ValueError("vertical_sign must be -1 or +1")
    top = unsigned_top(source_rank, route_family, k)
    sign = int(polarity)
    return NumericRouteReceipt(
        source_rank=sign * source_rank,
        polarity=polarity,
        route_family=route_family,
        k=k,
        wrapper=wrapper,
        traversal=traversal,
        top_address=sign * top,
        wrapper_address=sign * (top + vertical_sign * int(wrapper)),
        vertical_sign=vertical_sign,
    )


def numeric_wrapper_pair(
    source_rank: int,
    *,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
    vertical_sign: int = 1,
) -> tuple[NumericRouteReceipt, NumericRouteReceipt]:
    """Return both mandatory connector receipts around one selected top."""

    return tuple(
        numeric_coordinate(
            source_rank,
            polarity=polarity,
            route_family=route_family,
            k=k,
            wrapper=side,
            traversal=traversal,
            vertical_sign=vertical_sign,
        )
        for side in WrapperSide
    )


def numeric_offset_ladder(
    source_rank: int,
    *,
    route_family: RouteFamily,
    min_k: int,
    max_k: int,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
    vertical_sign: int = 1,
) -> tuple[tuple[NumericRouteReceipt, NumericRouteReceipt], ...]:
    """Materialize an inclusive signed-K ladder for one generalized route."""

    if route_family is RouteFamily.ORIGINAL:
        raise ValueError("the original N*2 route has no K ladder")
    if not isinstance(min_k, int) or not isinstance(max_k, int):
        raise TypeError("min_k and max_k must be integers")
    if min_k > max_k:
        raise ValueError("min_k must be <= max_k")
    return tuple(
        numeric_wrapper_pair(
            source_rank,
            polarity=polarity,
            route_family=route_family,
            k=k,
            traversal=traversal,
            vertical_sign=vertical_sign,
        )
        for k in range(min_k, max_k + 1)
    )


def recover_source_rank(record: NumericRouteReceipt) -> int:
    """Exactly rebuild the positive adapter source rank from a full receipt."""

    unsigned_wrapper = int(record.polarity) * record.wrapper_address
    top = unsigned_wrapper - record.vertical_sign * int(record.wrapper)
    if record.route_family is RouteFamily.ORIGINAL:
        numerator = top
    elif record.route_family is RouteFamily.DOUBLE_THEN_SHIFT:
        # X = 2N + K + s -> N = (X-K-s)/2
        numerator = top - record.k
    else:
        # X = 2(N+K) + s -> N = (X-s)/2-K
        if top % 2:
            raise ValueError("shift-then-double receipt has an invalid odd top")
        return top // 2 - record.k
    if numerator % 2:
        raise ValueError("receipt cannot recover an integer source rank")
    return numerator // 2


def validate_numeric_receipt(record: NumericRouteReceipt) -> None:
    """Recompute and verify one complete receipt."""

    expected = numeric_coordinate(
        abs(record.source_rank),
        polarity=record.polarity,
        route_family=record.route_family,
        k=record.k,
        wrapper=record.wrapper,
        traversal=record.traversal,
        vertical_sign=record.vertical_sign,
    )
    if record != expected:
        raise ValueError("Rabbit-Hop receipt does not match its route fields")
    if recover_source_rank(record) != abs(record.source_rank):
        raise ValueError("Rabbit-Hop receipt does not rebuild its source")
    if record.top_parity == record.wrapper_parity:
        raise ValueError("wrapper parity must oppose top parity")


def connection_addresses(
    left: tuple[NumericRouteReceipt, NumericRouteReceipt],
    right: tuple[NumericRouteReceipt, NumericRouteReceipt],
) -> tuple[int, ...]:
    """Return shared top/wrapper handoff addresses between two route pairs."""

    for pair in (left, right):
        if len(pair) != 2:
            raise ValueError("each selected top must have both wrapper receipts")
        for record in pair:
            validate_numeric_receipt(record)
    left_top = left[0].top_address
    right_top = right[0].top_address
    left_wrappers = {r.wrapper_address for r in left}
    right_wrappers = {r.wrapper_address for r in right}
    points = left_wrappers.intersection(right_wrappers)
    if left_top == right_top:
        points.add(left_top)
    if left_top in right_wrappers:
        points.add(left_top)
    if right_top in left_wrappers:
        points.add(right_top)
    return tuple(sorted(points))
