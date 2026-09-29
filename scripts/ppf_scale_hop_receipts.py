#!/usr/bin/env python3
"""Point / Path / Field nested scale hops with reconstructable receipts.

Uses the locked Rabbit Hopping N-grammar only as an addressing translator.
Does not claim CELL_V1 hardware, gravity, or consciousness proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

RouteFamily = Literal["after", "before"]
Wrapper = Literal[-1, 1]
Layer = Literal["center", "point", "path", "field", "closure", "resolved"]


@dataclass(frozen=True)
class ScaleReceipt:
    scale: int
    layer: Layer
    N: int
    family: RouteFamily
    m: int
    wrapper: Wrapper
    X: int
    packet: tuple[int, int, int]
    parent_scale: int | None
    parent_N: int | None


def r_after(N: int, m: int) -> int:
    return 2 * N + m


def r_before(N: int, m: int) -> int:
    return 2 * (N + m)


def recover(family: RouteFamily, X: int, m: int, wrapper: Wrapper) -> int:
    if family == "after":
        return (X - m - wrapper) // 2
    return (X - wrapper) // 2 - m


def emit(scale, layer, N, family, m, wrapper, parent_scale, parent_N):
    X = (r_after(N, m) if family == "after" else r_before(N, m)) + wrapper
    packet = (N, X - wrapper, X)
    return ScaleReceipt(scale, layer, N, family, m, wrapper, X, packet, parent_scale, parent_N)


def nest(start_N: int, scales: int):
    receipts = []
    N = start_N
    for scale in range(scales):
        parent_scale = scale - 1 if scale else None
        parent_N = N - 1 if scale else None
        receipts.append(emit(scale, "center", N, "after", 0, 1, parent_scale, parent_N))
        receipts.append(emit(scale, "point", N, "after", 0, 1, scale, N))
        receipts.append(emit(scale, "path", N, "before", 1, -1, scale, N))
        receipts.append(emit(scale, "field", N, "after", 2, 1, scale, N))
        receipts.append(emit(scale, "closure", N, "after", 2, 1, scale, N))
        resolved_N = N + 1
        receipts.append(
            ScaleReceipt(
                scale=scale,
                layer="resolved",
                N=resolved_N,
                family="after",
                m=0,
                wrapper=1,
                X=r_after(resolved_N, 0) + 1,
                packet=(resolved_N, r_after(resolved_N, 0), r_after(resolved_N, 0) + 1),
                parent_scale=scale,
                parent_N=N,
            )
        )
        N = resolved_N
    return receipts


def reconstruct_backward(receipts):
    recovered = []
    for rec in reversed(receipts):
        if rec.layer == "resolved":
            recovered.append(rec.parent_N if rec.parent_N is not None else rec.N - 1)
            continue
        got = recover(rec.family, rec.X, rec.m, rec.wrapper)
        if got != rec.N:
            raise AssertionError(f"reconstruction drift at {rec.layer} scale {rec.scale}")
        recovered.append(got)
    return recovered


def test_chain_length():
    assert len(nest(1, 3)) == 18


def test_resolved_becomes_next_center():
    recs = nest(4, 4)
    by_scale = {}
    for r in recs:
        by_scale.setdefault(r.scale, []).append(r)
    for s in range(3):
        resolved = [r for r in by_scale[s] if r.layer == "resolved"][0]
        nxt = [r for r in by_scale[s + 1] if r.layer == "center"][0]
        assert resolved.N == nxt.N
        assert nxt.parent_N == resolved.parent_N


def test_backward_recovers_original_N():
    start = 7
    recs = nest(start, 5)
    reconstruct_backward(recs)
    centers = [r for r in recs if r.layer == "center"]
    assert centers[0].N == start
    assert centers[-1].N == start + 4


def test_wrong_wrapper_breaks_reconstruction():
    recs = nest(3, 2)
    bad = recs[2]
    drifted = ScaleReceipt(bad.scale, bad.layer, bad.N, bad.family, bad.m, -bad.wrapper, bad.X, bad.packet, bad.parent_scale, bad.parent_N)
    failed = False
    try:
        reconstruct_backward([drifted])
    except AssertionError:
        failed = True
    if not failed:
        got = recover(drifted.family, drifted.X, drifted.m, drifted.wrapper)
        assert got != drifted.N


def test_path_and_point_keep_distinct_receipts():
    recs = nest(5, 1)
    point = next(r for r in recs if r.layer == "point")
    path = next(r for r in recs if r.layer == "path")
    assert (point.family, point.m, point.wrapper) != (path.family, path.m, path.wrapper)


def test_parent_pointers_are_complete_after_first_scale():
    recs = nest(2, 3)
    later = [r for r in recs if r.scale > 0]
    assert all(r.parent_scale is not None and r.parent_N is not None for r in later)


def run_all():
    tests = [
        test_chain_length,
        test_resolved_becomes_next_center,
        test_backward_recovers_original_N,
        test_wrong_wrapper_breaks_reconstruction,
        test_path_and_point_keep_distinct_receipts,
        test_parent_pointers_are_complete_after_first_scale,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} PPF receipt proofs held")
    return failed


if __name__ == "__main__":
    raise SystemExit(run_all())
