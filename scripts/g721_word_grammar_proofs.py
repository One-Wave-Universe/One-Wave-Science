#!/usr/bin/env python3
"""G-721a / G-721b word-grammar proofs.

Locked convention: W0=0, W1=01, Wk=W(k-1)W(k-2).
Fibonacci is the special Sturmian case. Phi is a consequence metric.
Does not drive live choice. Does not prove lattice physics.
"""

from __future__ import annotations

import math

PHI = (1.0 + math.sqrt(5.0)) / 2.0
CANONICAL_PREFIX_26 = "01001010010010100101001001"


def fibonacci_words(max_generation: int) -> list[str]:
    words = ["0"]
    if max_generation == 0:
        return words
    words.append("01")
    for _ in range(2, max_generation + 1):
        words.append(words[-1] + words[-2])
    return words


def fibonacci_prefix(length: int) -> str:
    words = fibonacci_words(1)
    while len(words[-1]) < length:
        words.append(words[-1] + words[-2])
    return words[-1][:length]


def branch_from_coordinates(identity: int, even: int, odd: int) -> int:
    n = abs(identity)
    e = abs(even)
    if not 1 <= n <= 26:
        raise ValueError("letter identity out of range")
    anchor = e // 2 - n
    if e % 2 or anchor not in (0, 1):
        raise ValueError("illegal even anchor")
    side = abs(odd) - e
    if side not in (-1, 1):
        raise ValueError("odd must be e\u00b11")
    if identity * even <= 0 or identity * odd <= 0:
        raise ValueError("mirror sign must be shared")
    return 0 if side == -1 else 1


def decode_trace(records: list[tuple[int, int, int]]) -> str:
    return "".join(str(branch_from_coordinates(*r)) for r in records)


def is_balanced(word: str) -> bool:
    for width in range(1, len(word) + 1):
        counts = [word[i : i + width].count("1") for i in range(len(word) - width + 1)]
        if counts and max(counts) - min(counts) > 1:
            return False
    return True


def factor_complexity(word: str, width: int) -> int:
    return len({word[i : i + width] for i in range(len(word) - width + 1)})


def mechanical_word(alpha: float, rho: float, length: int) -> str:
    bits = []
    for t in range(length):
        bits.append(str(int(__import__("math").floor((t + 1) * alpha + rho) - __import__("math").floor(t * alpha + rho))))
    return "".join(bits)


def build_az_route() -> list[tuple[int, int, int]]:
    expected = fibonacci_prefix(26)
    rows = []
    for n, token in enumerate(expected, start=1):
        bit = int(token)
        e = 2 * n
        o = e + (-1 if bit == 0 else 1)
        rows.append((n, e, o))
    return rows


def test_convention_and_prefix() -> None:
    words = fibonacci_words(5)
    assert words[0] == "0"
    assert words[1] == "01"
    assert words[2] == "010"
    assert words[3] == "01001"
    assert words[4] == "01001010"
    assert words[5] == "0100101001001"
    assert fibonacci_prefix(26) == CANONICAL_PREFIX_26


def test_recursion_and_counts() -> None:
    words = fibonacci_words(12)
    for k in range(2, len(words)):
        assert words[k] == words[k - 1] + words[k - 2]
        assert len(words[k]) == len(words[k - 1]) + len(words[k - 2])
        assert words[k].count("0") == words[k - 1].count("0") + words[k - 2].count("0")
        assert words[k].count("1") == words[k - 1].count("1") + words[k - 2].count("1")


def test_az_trace_exact() -> None:
    route = build_az_route()
    expected = fibonacci_prefix(26)
    pos = decode_trace(route)
    neg = decode_trace([(-n, -e, -o) for n, e, o in route])
    rev = decode_trace(list(reversed(route)))
    assert pos == expected
    assert neg == expected
    assert rev == expected[::-1]
    assert len(route) == 26


def test_balance_and_complexity() -> None:
    prefix = fibonacci_prefix(256)
    assert is_balanced(prefix)
    for width in range(1, 13):
        assert factor_complexity(prefix, width) == width + 1


def test_phi_is_consequence_not_generator() -> None:
    words = fibonacci_words(16)
    last = words[-1]
    prev = words[-2]
    length_ratio = len(last) / len(prev)
    zeros, ones = last.count("0"), last.count("1")
    count_ratio = zeros / ones
    assert abs(length_ratio - PHI) / PHI < 0.01
    assert abs(count_ratio - PHI) / PHI < 0.01
    assert last == prev + words[-3]


def test_sturmian_mechanical_word_balance() -> None:
    alpha = 1.0 / (PHI * PHI)
    word = mechanical_word(alpha, 0.0, 128)
    assert set(word) <= {"0", "1"}
    assert is_balanced(word)
    for width in range(1, 10):
        p = factor_complexity(word, width)
        assert p <= width + 1
        assert p >= 2


def test_sturmian_rejects_periodic() -> None:
    periodic = ("01" * 64)
    complexities = [factor_complexity(periodic, w) for w in range(1, 8)]
    assert complexities[-1] <= 2
    assert not all(c == i + 2 for i, c in enumerate(complexities))


def test_token_ops_stay_distinct() -> None:
    route = build_az_route()
    bits = decode_trace(route)
    mirrored = decode_trace([(-n, -e, -o) for n, e, o in route])
    reversed_bits = bits[::-1]
    complemented = "".join("1" if b == "0" else "0" for b in bits)
    assert mirrored == bits
    assert reversed_bits != bits
    assert complemented != bits
    assert complemented != reversed_bits


def test_illegal_packet_fails() -> None:
    raised = False
    try:
        branch_from_coordinates(3, 7, 8)
    except ValueError:
        raised = True
    assert raised
    raised = False
    try:
        branch_from_coordinates(3, 6, 9)
    except ValueError:
        raised = True
    assert raised


def run_all() -> int:
    tests = [
        test_convention_and_prefix,
        test_recursion_and_counts,
        test_az_trace_exact,
        test_balance_and_complexity,
        test_phi_is_consequence_not_generator,
        test_sturmian_mechanical_word_balance,
        test_sturmian_rejects_periodic,
        test_token_ops_stay_distinct,
        test_illegal_packet_fails,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} word-grammar proofs held")
    return failed


if __name__ == "__main__":
    raise SystemExit(run_all())
