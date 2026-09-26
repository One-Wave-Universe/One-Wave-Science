#!/usr/bin/env python3
"""CELL_V1 stamp 1 — 5 V supply with 2.5 V buffered virtual ground."""

VP, VG, VN = 5.0, 2.5, 0.0
R_LAW = 10_000.0
R_OPEN = 1e12


def i0(r_plus, r_minus):
    return (VP - VG) / r_plus + (VN - VG) / r_minus


def main() -> None:
    both = i0(R_LAW, R_LAW)
    pull_plus = i0(R_OPEN, R_LAW)
    pull_minus = i0(R_LAW, R_OPEN)
    print("CELL_V1 STAMP 1  rails + law")
    print(f"  I_0 both 10k     {both:+.4e} A")
    print(f"  I_0 pull +10k    {pull_plus:+.4e} A")
    print(f"  I_0 pull -10k    {pull_minus:+.4e} A")
    assert abs(both) < 1e-12
    assert pull_plus < 0
    assert pull_minus > 0
    assert abs(abs(pull_plus) - (VG - VN) / R_LAW) < 1e-9
    assert abs(abs(pull_minus) - (VP - VG) / R_LAW) < 1e-9
    print("  NET_G = 2.5 V absolute / 0 V relative")
    print("  PASS stamp 1 (ideal buffered virtual ground)")
    print("  copper still owes the same numbers at a 10-20 mA supply limit")


if __name__ == "__main__":
    main()
