"""The balanced ternary primitive used for dynamic runtime state.

This is deliberately narrow: Ternary models the *dynamic* gate/state axis
(RETURN / HOLD / ADVANCE) used by the transition engine. It is not a
general-purpose replacement for booleans or categorical fields elsewhere
in the schema -- do not force unrelated attributes into -1/0/+1.
"""

from __future__ import annotations

from enum import IntEnum


class Ternary(IntEnum):
    """Balanced ternary state.

    RETURN  (-1): Return / Opposed transition.
    HOLD     (0): Hold / Mirror reference.
    ADVANCE (+1): Advance / Admitted transition.
    """

    RETURN = -1
    HOLD = 0
    ADVANCE = 1


def sgn3(value: float, epsilon: float = 1e-9) -> Ternary:
    """Map a real number onto the balanced-ternary axis.

    Values within `epsilon` of zero are treated as exactly zero (HOLD),
    since floating point accumulation (lambda * M + g, etc.) will rarely
    land on exact 0.0 even when the "true" underlying value is zero.
    """
    if value > epsilon:
        return Ternary.ADVANCE
    if value < -epsilon:
        return Ternary.RETURN
    return Ternary.HOLD
