#!/usr/bin/env python3
"""CELL_V1 stamp 1 — virtual rails. Not Stage 1 comparator. Not Kitty Hawk."""

VP, VN = 12.0, -12.0
R_LAW = 10_000.0
R_OPEN = 1e12


def i0(r_plus, r_minus):
    return VP / r_plus + VN / r_minus


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
    assert abs(abs(pull_plus) - abs(VN) / R_LAW) < 1e-9
    assert abs(abs(pull_minus) - VP / R_LAW) < 1e-9
    print("  VG held at 0 by definition in this model")
    print("  PASS stamp 1 (ideal mid)")
    print("  copper still owes the same numbers at 50 mA")


if __name__ == "__main__":
    main()
