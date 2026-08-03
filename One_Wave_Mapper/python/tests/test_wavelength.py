import pytest

from onewave_mapper import wavelength


def test_wavelength_of_a4_matches_known_value():
    # 440 Hz in dry air at 20C: lambda = 343/440 ~= 0.7795 m
    lam = wavelength.wavelength_meters(440.0)
    assert lam == pytest.approx(343.0 / 440.0, rel=1e-9)
    assert lam == pytest.approx(0.7795, abs=1e-3)


def test_frequency_from_wavelength_round_trip():
    freq = 220.0
    lam = wavelength.wavelength_meters(freq)
    recovered = wavelength.frequency_from_wavelength(lam)
    assert recovered == pytest.approx(freq, rel=1e-9)


def test_speed_of_sound_increases_with_temperature():
    cold = wavelength.speed_of_sound_in_air(0.0)
    warm = wavelength.speed_of_sound_in_air(30.0)
    assert warm > cold
    assert cold == pytest.approx(331.3, abs=0.1)


def test_wavelength_uses_custom_speed_of_sound():
    v = wavelength.speed_of_sound_in_air(35.0)
    lam_custom = wavelength.wavelength_meters(440.0, speed_of_sound_mps=v)
    lam_default = wavelength.wavelength_meters(440.0)
    assert lam_custom != lam_default
    assert lam_custom == pytest.approx(v / 440.0)


def test_wavelength_rejects_nonpositive_frequency():
    with pytest.raises(ValueError):
        wavelength.wavelength_meters(0.0)
    with pytest.raises(ValueError):
        wavelength.wavelength_meters(-100.0)


def test_wave_number_matches_two_pi_over_lambda():
    freq = 500.0
    lam = wavelength.wavelength_meters(freq)
    k = wavelength.wave_number(freq)
    assert k == pytest.approx(2 * 3.141592653589793 / lam, rel=1e-9)
