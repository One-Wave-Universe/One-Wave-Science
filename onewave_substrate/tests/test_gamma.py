"""Gate (Gamma) truth-table and invariant tests.

The table below was derived by hand from the precedence rules documented
in onewave/transition.py (ground input > mirror cancellation > consensus),
independently of the implementation, so this is a real regression test
and not a tautology.
"""

from onewave.ternary import Ternary
from onewave.transition import gamma

R, H, A_ = Ternary.RETURN, Ternary.HOLD, Ternary.ADVANCE

# (field_state, a, b) -> expected gate_result, all 27 combinations.
TRUTH_TABLE = {
    # A == HOLD -> HOLD, for every (F, B)
    (R, H, R): H, (R, H, H): H, (R, H, A_): H,
    (H, H, R): H, (H, H, H): H, (H, H, A_): H,
    (A_, H, R): H, (A_, H, H): H, (A_, H, A_): H,
    # B == HOLD, A != HOLD -> HOLD, for every (F, A)
    (R, R, H): H, (R, A_, H): H,
    (H, R, H): H, (H, A_, H): H,
    (A_, R, H): H, (A_, A_, H): H,
    # A != B (both non-HOLD) -> HOLD (no consensus), for every F
    (R, A_, R): H, (H, A_, R): H, (A_, A_, R): H,
    (R, R, A_): H, (H, R, A_): H, (A_, R, A_): H,
    # A == B == ADVANCE: mirror-cancelled only when F == RETURN
    (R, A_, A_): H,   # mirror cancellation: A opposes F
    (H, A_, A_): A_,
    (A_, A_, A_): A_,
    # A == B == RETURN: mirror-cancelled only when F == ADVANCE
    (A_, R, R): H,    # mirror cancellation: A opposes F
    (H, R, R): R,
    (R, R, R): R,
}


def test_truth_table_full_coverage():
    assert len(TRUTH_TABLE) == 27


def test_truth_table_matches_implementation():
    for (f, a, b), expected in TRUTH_TABLE.items():
        assert gamma(f, a, b) == expected, f"gamma(F={f!r}, A={a!r}, B={b!r})"


def test_gamma_is_deterministic():
    for (f, a, b) in TRUTH_TABLE:
        first = gamma(f, a, b)
        for _ in range(5):
            assert gamma(f, a, b) == first


def test_mirror_cancellation_advance_opposed_by_return_field():
    # A = +1, F = -1 -> HOLD, regardless of B (ground rule already covers
    # B = HOLD; this checks the non-trivial B values too).
    for b in (Ternary.RETURN, Ternary.HOLD, Ternary.ADVANCE):
        assert gamma(Ternary.RETURN, Ternary.ADVANCE, b) == Ternary.HOLD


def test_mirror_cancellation_return_opposed_by_advance_field():
    # A = -1, F = +1 -> HOLD, regardless of B.
    for b in (Ternary.RETURN, Ternary.HOLD, Ternary.ADVANCE):
        assert gamma(Ternary.ADVANCE, Ternary.RETURN, b) == Ternary.HOLD


def test_ground_input_a_hold():
    for f in Ternary:
        for b in Ternary:
            assert gamma(f, Ternary.HOLD, b) == Ternary.HOLD


def test_ground_input_b_hold():
    for f in Ternary:
        for a in Ternary:
            assert gamma(f, a, Ternary.HOLD) == Ternary.HOLD
