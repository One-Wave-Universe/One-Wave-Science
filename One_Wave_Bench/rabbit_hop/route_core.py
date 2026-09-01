"""Canonical reversible rabbit-hop arithmetic.

This module owns only the route/coordinate grammar.  It does not implement
memory completion, motor choice, alphabet semantics, or physical dynamics.

Two operation-order families are retained as different routes even when they
reach the same address:

    DOUBLE_FIRST:  2N + m
    SHIFT_FIRST:   2(N + m)

A wrapper side s in {-1, 0, +1} is applied around the selected center and a
polarity p in {-1, +1} mirrors the entire signed address:

    address = p * (center + s)

The complete receipt is what makes the mapping reversible.  Equal numerical
addresses do not imply equal routes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
import json


class RouteFamily(str, Enum):
    DOUBLE_FIRST = "double_first"
    SHIFT_FIRST = "shift_first"


class Polarity(IntEnum):
    NEGATIVE = -1
    POSITIVE = 1


class WrapperSide(IntEnum):
    LOWER = -1
    CENTER = 0
    UPPER = 1


class Traversal(str, Enum):
    FORWARD = "forward"
    OPPOSING = "opposing"


@dataclass(frozen=True, slots=True)
class HopReceipt:
    source_n: int
    family: RouteFamily
    offset: int
    wrapper: WrapperSide
    polarity: Polarity
    traversal: Traversal
    address: int

    def to_json(self) -> str:
        return json.dumps(
            {
                "address": self.address,
                "family": self.family.value,
                "offset": self.offset,
                "polarity": int(self.polarity),
                "source_n": self.source_n,
                "traversal": self.traversal.value,
                "wrapper": int(self.wrapper),
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_json(cls, payload: str) -> "HopReceipt":
        raw = json.loads(payload)
        required = {
            "address",
            "family",
            "offset",
            "polarity",
            "source_n",
            "traversal",
            "wrapper",
        }
        if set(raw) != required:
            raise ValueError("rabbit-hop receipt has unexpected fields")
        receipt = cls(
            source_n=int(raw["source_n"]),
            family=RouteFamily(raw["family"]),
            offset=int(raw["offset"]),
            wrapper=WrapperSide(int(raw["wrapper"])),
            polarity=Polarity(int(raw["polarity"])),
            traversal=Traversal(raw["traversal"]),
            address=int(raw["address"]),
        )
        validate_receipt(receipt)
        return receipt


def _positive_n(n: int) -> int:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("N must be a positive integer")
    return n


def _integer_offset(offset: int) -> int:
    if not isinstance(offset, int) or isinstance(offset, bool):
        raise ValueError("offset must be an integer")
    return offset


def route_center(n: int, family: RouteFamily, offset: int = 0) -> int:
    """Return the unsigned center before wrapper and polarity are applied."""

    n = _positive_n(n)
    offset = _integer_offset(offset)
    if family is RouteFamily.DOUBLE_FIRST:
        return 2 * n + offset
    if family is RouteFamily.SHIFT_FIRST:
        return 2 * (n + offset)
    raise AssertionError("unreachable")


def route_address(
    n: int,
    family: RouteFamily,
    *,
    offset: int = 0,
    wrapper: WrapperSide = WrapperSide.CENTER,
    polarity: Polarity = Polarity.POSITIVE,
) -> int:
    center = route_center(n, family, offset)
    return int(polarity) * (center + int(wrapper))


def invert_address(
    address: int,
    family: RouteFamily,
    *,
    offset: int = 0,
    wrapper: WrapperSide = WrapperSide.CENTER,
    polarity: Polarity = Polarity.POSITIVE,
) -> int:
    """Recover N by undoing polarity, wrapper, and operation-order offset."""

    offset = _integer_offset(offset)
    unsigned_wrapped = int(polarity) * address
    center = unsigned_wrapped - int(wrapper)

    if family is RouteFamily.DOUBLE_FIRST:
        numerator = center - offset
        if numerator % 2:
            raise ValueError("address is incompatible with DOUBLE_FIRST receipt")
        return _positive_n(numerator // 2)

    if family is RouteFamily.SHIFT_FIRST:
        if center % 2:
            raise ValueError("address is incompatible with SHIFT_FIRST receipt")
        return _positive_n(center // 2 - offset)

    raise AssertionError("unreachable")


def make_receipt(
    n: int,
    family: RouteFamily,
    *,
    offset: int = 0,
    wrapper: WrapperSide = WrapperSide.CENTER,
    polarity: Polarity = Polarity.POSITIVE,
    traversal: Traversal = Traversal.FORWARD,
) -> HopReceipt:
    return HopReceipt(
        source_n=_positive_n(n),
        family=family,
        offset=_integer_offset(offset),
        wrapper=wrapper,
        polarity=polarity,
        traversal=traversal,
        address=route_address(
            n,
            family,
            offset=offset,
            wrapper=wrapper,
            polarity=polarity,
        ),
    )


def validate_receipt(receipt: HopReceipt) -> None:
    expected = make_receipt(
        receipt.source_n,
        receipt.family,
        offset=receipt.offset,
        wrapper=receipt.wrapper,
        polarity=receipt.polarity,
        traversal=receipt.traversal,
    )
    if receipt != expected:
        raise ValueError("rabbit-hop receipt does not match its declared route")
    recovered = invert_address(
        receipt.address,
        receipt.family,
        offset=receipt.offset,
        wrapper=receipt.wrapper,
        polarity=receipt.polarity,
    )
    if recovered != receipt.source_n:
        raise ValueError("rabbit-hop receipt is not reversible")


def mirror_receipt(receipt: HopReceipt) -> HopReceipt:
    """Mirror sign only; alphabet inversion and route opposition remain separate."""

    return make_receipt(
        receipt.source_n,
        receipt.family,
        offset=receipt.offset,
        wrapper=receipt.wrapper,
        polarity=Polarity(-int(receipt.polarity)),
        traversal=receipt.traversal,
    )


def oppose_receipt(receipt: HopReceipt) -> HopReceipt:
    """Reverse traversal identity without silently changing sign or route math."""

    traversal = (
        Traversal.OPPOSING
        if receipt.traversal is Traversal.FORWARD
        else Traversal.FORWARD
    )
    return make_receipt(
        receipt.source_n,
        receipt.family,
        offset=receipt.offset,
        wrapper=receipt.wrapper,
        polarity=receipt.polarity,
        traversal=traversal,
    )


def shared_shift_boundary(
    n: int,
    *,
    offset: int = 0,
    polarity: Polarity = Polarity.POSITIVE,
) -> int:
    """Return 2(N+m)+1 == 2(N+m+1)-1 for adjacent shift-first nests."""

    upper = route_address(
        n,
        RouteFamily.SHIFT_FIRST,
        offset=offset,
        wrapper=WrapperSide.UPPER,
        polarity=polarity,
    )
    lower_next = route_address(
        n,
        RouteFamily.SHIFT_FIRST,
        offset=offset + 1,
        wrapper=WrapperSide.LOWER,
        polarity=polarity,
    )
    if upper != lower_next:
        raise AssertionError("adjacent shift-first nests lost their shared boundary")
    return upper


def wrappers(center: int) -> tuple[int, int, int]:
    """Return X-1, X, X+1 without assigning any domain meaning."""

    return center - 1, center, center + 1
