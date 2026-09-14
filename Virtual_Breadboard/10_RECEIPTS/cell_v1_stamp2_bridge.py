#!/usr/bin/env python3
"""CELL_V1 stamp 2 — one dummy winding 1k to G. Ideal switches."""

VP, VN, VG = 12.0, -12.0, 0.0
R_LOAD = 1_000.0
R_LAW = 10_000.0


def i0_law():
    return VP / R_LAW + VN / R_LAW  # 0


def phase(state):
    if state == 1:
        return VP
    if state == -1:
        return VN
    return None  # STAY high-Z


def i0_load(state):
    v = phase(state)
    if v is None:
        return 0.0
    return (v - VG) / R_LOAD


def main() -> None:
    print("CELL_V1 STAMP 2  dummy 1k to G")
    law = i0_law()
    stay = i0_load(0) + law
    plus = i0_load(1) + law
    minus = i0_load(-1) + law
    print(f"  I_0 STAY    {stay:+.4e} A")
    print(f"  I_0 +1      {plus:+.4e} A")
    print(f"  I_0 -1      {minus:+.4e} A")
    assert abs(stay) < 1e-12
    assert abs(plus - 12e-3) < 1e-12
    assert abs(minus + 12e-3) < 1e-12
    print("  VG = 0 held")
    print("  PASS stamp 2 (ideal half-bridge + 1k)")
    print("  50 mA knob still covers 12 mA lean")


if __name__ == "__main__":
    main()
