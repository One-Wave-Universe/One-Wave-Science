import pytest

from physics_engine.harmonic_mirror import DrivenMirror, HarmonicPacket, alphabet_packet, harmonic_packet


def test_harmonic_packet_matches_canons_own_worked_examples():
    # UPDATED_46 section 2: "A- = 1, 4, 3   A+ = 1, 4, 5"
    assert harmonic_packet(1) == HarmonicPacket(identity=1, carrier=4, lower=3, upper=5)
    # "A#- = 2, 6, 5   A#+ = 2, 6, 7"
    assert harmonic_packet(2) == HarmonicPacket(identity=2, carrier=6, lower=5, upper=7)
    # "C- = 3, 8, 7   C+ = 3, 8, 9"
    assert harmonic_packet(3) == HarmonicPacket(identity=3, carrier=8, lower=7, upper=9)
    # "D- = 4,10, 9   D+ = 4,10,11"
    assert harmonic_packet(4) == HarmonicPacket(identity=4, carrier=10, lower=9, upper=11)


def test_harmonic_packet_rejects_identity_below_one():
    with pytest.raises(ValueError):
        harmonic_packet(0)


def test_adjacent_packets_share_an_odd_boundary():
    # canon section 2: "H+(n) = H-(n + 1) ... forms a continuous
    # harmonic route rather than isolated note nodes."
    for n in range(1, 12):
        assert harmonic_packet(n).upper == harmonic_packet(n + 1).lower


def test_alphabet_packet_matches_canons_own_worked_example():
    # UPDATED_46 section 3: "A- = 1 -> 2 -> 1   A+ = 1 -> 2 -> 3"
    minus, plus = alphabet_packet(1)
    assert minus == (1, 2, 1)
    assert plus == (1, 2, 3)


def test_alphabet_packet_general_form_for_b():
    # L-(2) = (3, 4, 3), L+(2) = (3, 4, 5)
    minus, plus = alphabet_packet(2)
    assert minus == (3, 4, 3)
    assert plus == (3, 4, 5)


def test_alphabet_packet_rejects_n_below_one():
    with pytest.raises(ValueError):
        alphabet_packet(0)


def test_driven_mirror_holds_the_fixed_two_unit_width_invariant():
    # canon section 5: "Invariant: H+ - H- = 2 mod 12" -- must hold at
    # every step, not just eventually.
    mirror = DrivenMirror(sigma=0.0)
    for _ in range(1000):
        lower, _sigma, upper = mirror.step()
        assert abs(((upper - lower) % 12.0) - 2.0) < 1e-9


def test_driven_mirror_sigma_uses_the_carrier_phase_before_it_advances():
    """Canon section 5's equations are ordered Sigma(n+1) from phi(n),
    *then* phi(n+1) = phi(n) + 1 -- Sigma must never see the already-
    advanced phase for the same step."""
    mirror = DrivenMirror(sigma=0.0, phase=0.0)
    expected_sigma = (2 * 0.0 + 2 * 0.0 + 2) % 12.0  # sin(phase=0) = 0
    lower, sigma, upper = mirror.step()
    assert sigma == pytest.approx(expected_sigma)
    assert mirror.phase == pytest.approx(1.0)


def test_driven_mirror_stays_within_the_modulus():
    mirror = DrivenMirror(sigma=0.0)
    for _ in range(1000):
        lower, sigma, upper = mirror.step()
        assert 0.0 <= lower < 12.0
        assert 0.0 <= sigma < 12.0
        assert 0.0 <= upper < 12.0


def test_driven_mirror_respects_a_custom_modulus():
    mirror = DrivenMirror(sigma=0.0, modulus=7.0)
    for _ in range(200):
        lower, _sigma, upper = mirror.step()
        assert abs(((upper - lower) % 7.0) - 2.0) < 1e-9
