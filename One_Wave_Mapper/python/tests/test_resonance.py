import numpy as np

from onewave_mapper import signal_generator, resonance


def test_detect_resonances_finds_decaying_tone():
    sr = 48000
    signal = signal_generator.exponential_decay(500, 2.0, sr, decay_tau_seconds=0.5, amplitude=1.0)
    events = resonance.detect_resonances(signal, sr, fft_size=4096, hop_size=1024)

    assert len(events) > 0
    top = events[0]
    assert abs(top.center_frequency_hz - 500) < 20
    assert top.decay_rate_db_per_second is not None
    assert top.decay_rate_db_per_second < 0  # decaying, not growing
    assert 0.0 <= top.persistence_score <= 1.0
    assert top.classification == "unknown"


def test_quality_factor_higher_for_narrower_resonance():
    # Exponential-decay linewidth (FWHM) is ~1/(pi*tau), so a longer tau
    # gives a physically narrower resonance; fft_size/hop chosen with
    # enough frequency resolution (Section 8.1) to actually resolve the
    # difference rather than being limited by the analysis window itself.
    sr = 48000
    narrow = signal_generator.exponential_decay(500, 4.0, sr, decay_tau_seconds=2.0, amplitude=1.0)
    wide = signal_generator.exponential_decay(500, 4.0, sr, decay_tau_seconds=0.01, amplitude=1.0)

    narrow_events = resonance.detect_resonances(narrow, sr, fft_size=16384, hop_size=2048)
    wide_events = resonance.detect_resonances(wide, sr, fft_size=16384, hop_size=2048)

    assert narrow_events[0].quality_factor > wide_events[0].quality_factor


def test_ring_down_analysis_recovers_known_tau():
    sr = 48000
    true_tau = 0.4
    signal = signal_generator.exponential_decay(500, 2.0, sr, decay_tau_seconds=true_tau, amplitude=1.0)

    result = resonance.ring_down_analysis(signal, sr, center_frequency_hz=500, bandwidth_hz=100,
                                           excitation_end_sample=0)
    fit = result["exponential_fit"]
    assert fit["tau_seconds"] is not None
    assert abs(fit["tau_seconds"] - true_tau) / true_tau < 0.25


def test_ring_down_analysis_low_frequency_drift_for_stable_tone():
    sr = 48000
    signal = signal_generator.exponential_decay(500, 2.0, sr, decay_tau_seconds=0.5, amplitude=1.0)
    result = resonance.ring_down_analysis(signal, sr, center_frequency_hz=500, bandwidth_hz=100,
                                           excitation_end_sample=0)
    assert abs(result["frequency_drift_hz"]) < 10.0
