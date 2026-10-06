import copy

from onewave.ternary import Ternary
from onewave.transition import State, TransitionParams, gamma, phi, transition


def test_transition_does_not_mutate_input_state():
    before = State(field_state=Ternary.HOLD, displacement=1.0, memory_state=0.5)
    snapshot = copy.deepcopy(before)
    params = TransitionParams()

    transition(before, Ternary.ADVANCE, Ternary.ADVANCE, params)

    assert before == snapshot


def test_transition_returns_new_object():
    state = State()
    params = TransitionParams()
    new_state, _ = transition(state, Ternary.ADVANCE, Ternary.ADVANCE, params)
    assert new_state is not state


def test_transition_is_deterministic():
    state = State(field_state=Ternary.HOLD, displacement=2.0, memory_state=0.3)
    params = TransitionParams(delta_step=1.0, lam=0.6, kappa=0.5)

    r1 = transition(state, Ternary.RETURN, Ternary.RETURN, params)
    r2 = transition(state, Ternary.RETURN, Ternary.RETURN, params)

    assert r1 == r2


def test_transition_matches_manual_composition_of_gamma_and_phi():
    state = State(field_state=Ternary.HOLD, displacement=1.0, memory_state=0.4)
    params = TransitionParams(delta_step=1.0, lam=0.5, kappa=1.0)
    a, b = Ternary.ADVANCE, Ternary.ADVANCE

    new_state, g = transition(state, a, b, params)

    expected_g = gamma(state.field_state, a, b)
    expected_delta = state.displacement + params.delta_step * int(expected_g)
    expected_mem = params.lam * state.memory_state + int(expected_g)
    expected_field = phi(expected_mem, expected_delta, params)

    assert g == expected_g
    assert new_state.displacement == expected_delta
    assert new_state.memory_state == expected_mem
    assert new_state.field_state == expected_field


def test_hold_gate_still_updates_memory_decay_but_not_displacement():
    # A HOLD gate (g=0) leaves displacement unchanged but memory still
    # decays by lambda -- momentum doesn't freeze just because the gate
    # didn't admit a transition this step.
    state = State(field_state=Ternary.HOLD, displacement=3.0, memory_state=2.0)
    params = TransitionParams(lam=0.5)
    new_state, g = transition(state, Ternary.HOLD, Ternary.HOLD, params)
    assert g == Ternary.HOLD
    assert new_state.displacement == 3.0
    assert new_state.memory_state == 1.0


def test_transition_params_validates_lambda_and_kappa():
    import pytest

    with pytest.raises(ValueError):
        TransitionParams(lam=0.0)
    with pytest.raises(ValueError):
        TransitionParams(lam=1.0)
    with pytest.raises(ValueError):
        TransitionParams(kappa=0.0)
    with pytest.raises(ValueError):
        TransitionParams(kappa=-1.0)
