from onewave.ternary import Ternary
from onewave.transition import TransitionParams, phi


def test_phi_zero_state_holds():
    params = TransitionParams()
    assert phi(0.0, 0.0, params) == Ternary.HOLD


def test_phi_memory_dominates_when_no_displacement():
    params = TransitionParams(kappa=1.0)
    assert phi(1.0, 0.0, params) == Ternary.ADVANCE
    assert phi(-1.0, 0.0, params) == Ternary.RETURN


def test_phi_displacement_restores_toward_hold():
    # Positive memory can be pulled back to RETURN by a large enough
    # displacement scaled by kappa -- the restoring-force design decision
    # documented in transition.py.
    params = TransitionParams(kappa=1.0)
    assert phi(1.0, 0.0, params) == Ternary.ADVANCE
    assert phi(1.0, 5.0, params) == Ternary.RETURN


def test_phi_kappa_scales_displacement_influence():
    # Same (memory, displacement) pair, different kappa -> different sign.
    small_kappa = TransitionParams(kappa=0.1)
    large_kappa = TransitionParams(kappa=10.0)
    assert phi(1.0, 2.0, small_kappa) == Ternary.ADVANCE  # 1 - 0.1*2 = 0.8 > 0
    assert phi(1.0, 2.0, large_kappa) == Ternary.RETURN   # 1 - 10*2 << 0


def test_phi_uses_both_memory_and_displacement_not_just_one():
    params = TransitionParams(kappa=1.0)
    # Memory alone would say ADVANCE; displacement alone would say RETURN;
    # phi must combine them, not just look at one.
    combined = phi(memory_state=3.0, displacement=3.0, params=params)
    assert combined == Ternary.HOLD  # 3 - 1*3 == 0
