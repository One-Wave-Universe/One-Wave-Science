#!/usr/bin/env python3
"""Rabbit Hopping arithmetic proofs.

Implements the locked N-based translator grammar from
ARCHITECTURE_RABBIT_HOPPING_SCALE_TRANSLATOR.md and runs the ten
minimum validation tests as exact-integer checks.

Status of this file: GREEN for the arithmetic grammar only.
Does not claim physical, neural, or astrophysical confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


RouteFamily = Literal["after", "before"]
Wrapper = Literal[-1, 1]


@dataclass(frozen=True)
class Receipt:
    N: int
    family: RouteFamily
    m: int
    wrapper: Wrapper
    sign: int
    inverted: bool
    opposing: bool
    X: int
    packet: tuple[int, int, int]


def invert_N(N: int) -> int:
    return 27 - N


def r_after(N: int, m: int) -> int:
    return 2 * N + m


def r_before(N: int, m: int) -> int:
    return 2 * (N + m)


def recover_after(X: int, m: int, wrapper: Wrapper) -> int:
    return (X - m - wrapper) // 2


def recover_before(X: int, m: int, wrapper: Wrapper) -> int:
    return (X - wrapper) // 2 - m


def make_packet(N: int, X: int, wrapper: Wrapper) -> tuple[int, int, int]:
    return (N, X, X + wrapper)


def hop(
    N: int,
    family: RouteFamily,
    m: int,
    wrapper: Wrapper,
    sign: int = 1,
    inverted: bool = False,
    opposing: bool = False,
) -> Receipt:
    if sign not in (-1, 1):
        raise ValueError("sign must be ±1")
    source = invert_N(N) if inverted else N
    X_core = r_after(source, m) if family == "after" else r_before(source, m)
    X = sign * X_core
    packet = make_packet(source if not opposing else -source, X, wrapper if not opposing else -wrapper)
    return Receipt(
        N=N,
        family=family,
        m=m,
        wrapper=wrapper,
        sign=sign,
        inverted=inverted,
        opposing=opposing,
        X=X,
        packet=packet,
    )


def opposite_parity(a: int, b: int) -> bool:
    return (a % 2) != (b % 2)


def test_01_generate_families() -> None:
    packets = []
    for N in range(1, 27):
        for m in range(0, 6):
            for family in ("after", "before"):
                for w in (-1, 1):
                    packets.append(hop(N, family, m, w))
    assert len(packets) == 26 * 6 * 2 * 2


def test_02_route_identity() -> None:
    for N in range(1, 27):
        for m in range(0, 8):
            assert r_after(N, 2 * m) == r_before(N, m)


def test_03_wrapper_opposite_parity() -> None:
    for N in range(1, 27):
        for m in range(0, 6):
            for family in ("after", "before"):
                X = r_after(N, m) if family == "after" else r_before(N, m)
                assert opposite_parity(X, X - 1)
                assert opposite_parity(X, X + 1)


def test_04_adjacent_nests_share_wrapper() -> None:
    for N in range(1, 26):
        assert r_after(N, 1) == r_before(N + 1, 0) - 1
        left = hop(N, "after", 0, 1)
        right = hop(N + 1, "before", 0, -1)
        assert left.X + 1 == right.X + right.wrapper
        shared = 2 * N + 1
        assert left.packet[2] == shared
        assert right.packet[2] == shared


def test_05_sign_mirrors() -> None:
    for N in range(1, 27):
        for m in (0, 1, 3):
            pos = hop(N, "after", m, 1, sign=1)
            neg = hop(N, "after", m, 1, sign=-1)
            assert pos.X == -neg.X
            assert pos.packet[1] == -neg.packet[1]


def test_06_alphabet_inversion() -> None:
    letters = {chr(64 + i): i for i in range(1, 27)}
    for letter, N in letters.items():
        inv = invert_N(N)
        inv_letter = chr(64 + inv)
        assert invert_N(inv) == N
        assert letters[letter] + letters[inv_letter] == 27
    assert invert_N(1) == 26
    assert invert_N(2) == 25
    assert invert_N(26) == 1


def test_07_division_recovers_N() -> None:
    for N in range(1, 27):
        for m in range(0, 6):
            for w in (-1, 1):
                Xa = r_after(N, m) + w
                Xb = r_before(N, m) + w
                assert recover_after(Xa, m, w) == N
                assert recover_before(Xb, m, w) == N


def test_08_receipts_distinguish_equal_destinations() -> None:
    collisions = 0
    for N in range(1, 27):
        for m in range(1, 5):
            a = hop(N, "after", 2 * m, 1)
            b = hop(N, "before", m, 1)
            assert a.X == b.X
            assert a.family != b.family
            assert a.m != b.m
            collisions += 1
    assert collisions > 0


def test_09_opposing_reverses_wrapper_not_sign() -> None:
    for N in range(1, 27):
        fwd = hop(N, "after", 2, 1, opposing=False)
        rev = hop(N, "after", 2, 1, opposing=True)
        assert fwd.X == rev.X
        assert fwd.packet[2] == fwd.X + 1
        assert rev.packet[2] == rev.X - 1
        assert fwd.sign == rev.sign == 1


def test_10_bad_receipt_fails_visibly() -> None:
    N, m, w = 7, 3, 1
    X = r_after(N, m) + w
    assert recover_after(X, m, w) == N
    assert recover_after(X, m, -w) != N
    assert recover_after(X, m + 1, w) != N
    assert recover_before(X, m, w) != N


def run_all() -> int:
    tests = [
        test_01_generate_families,
        test_02_route_identity,
        test_03_wrapper_opposite_parity,
        test_04_adjacent_nests_share_wrapper,
        test_05_sign_mirrors,
        test_06_alphabet_inversion,
        test_07_division_recovers_N,
        test_08_receipts_distinguish_equal_destinations,
        test_09_opposing_reverses_wrapper_not_sign,
        test_10_bad_receipt_fails_visibly,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} proofs held")
    return failed


if __name__ == "__main__":
    raise SystemExit(run_all())
