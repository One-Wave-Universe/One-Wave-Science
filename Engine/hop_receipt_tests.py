#!/usr/bin/env python3
"""Hop receipt identities. Bronze-as-grammar. Fail loud."""

def double_then_shift(N, K, s):
    return 2 * N + K + s

def shift_then_double(N, K, s):
    return 2 * (N + K) + s

def invert_N(N):
    return 27 - N

def rebuild_dts(X, K, s):
    return (X - K - s) / 2

def rebuild_std(X, K, s):
    return (X - s) / 2 - K

def check():
    fails = []
    for N in range(1, 27):
        if invert_N(invert_N(N)) != N:
            fails.append(("invert", N))
        for K in range(-3, 4):
            for s in (-1, 1):
                x1 = double_then_shift(N, K, s)
                if rebuild_dts(x1, K, s) != N:
                    fails.append(("rebuild_dts", N, K, s))
                x2 = shift_then_double(N, K, s)
                if rebuild_std(x2, K, s) != N:
                    fails.append(("rebuild_std", N, K, s))
                # same number, different route when 2N+2m = 2(N+m)
                if double_then_shift(N, 2, s) != shift_then_double(N, 1, s):
                    fails.append(("identity", N, s))
                # wrapper parity opposite TOP
                top = 2 * N + K
                if (top + s) % 2 == top % 2:
                    fails.append(("wrapper_parity", N, K, s))
    # dropped receipt cannot rebuild
    X = double_then_shift(5, 2, 1)
    ambiguous = [rebuild_dts(X, K, s) for K in range(-3, 4) for s in (-1, 1)]
    if len(set(ambiguous)) == 1:
        fails.append(("dropped_receipt_should_be_ambiguous", ambiguous))
    return fails

if __name__ == "__main__":
    fails = check()
    if fails:
        print("FAIL", len(fails))
        print(fails[:12])
        raise SystemExit(1)
    print("PASS  hop identities + wrapper parity + dropped-receipt ambiguity")
