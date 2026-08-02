import numpy as np

from onewave_mapper import signal_generator
from onewave_mapper.trigger import TriggerEngine, TriggerConfig, TriggerType, TriggerEdge


def test_rising_edge_trigger_finds_expected_number_of_crossings():
    sr = 48000
    freq = 100.0
    duration = 1.0
    sine = signal_generator.sine(freq, duration, sr, amplitude=1.0)

    engine = TriggerEngine(TriggerConfig(
        trigger_type=TriggerType.LEVEL, edge=TriggerEdge.RISING, threshold=0.0, hysteresis=0.05,
    ))
    triggers = engine.find_triggers(sine, sr)

    expected_count = int(freq * duration)
    assert abs(len(triggers) - expected_count) <= 1


def test_trigger_stability_low_jitter_on_stable_periodic_signal():
    sr = 48000
    freq = 220.0
    duration = 2.0
    sine = signal_generator.sine(freq, duration, sr, amplitude=1.0)

    engine = TriggerEngine(TriggerConfig(
        trigger_type=TriggerType.LEVEL, edge=TriggerEdge.RISING, threshold=0.0, hysteresis=0.05,
    ))
    triggers = engine.find_triggers(sine, sr)

    period_samples = sr / freq
    intervals = np.diff(triggers)
    jitter = np.std(intervals - period_samples)
    assert jitter < 0.05  # sub-sample jitter on a clean synthetic tone


def test_holdoff_suppresses_rapid_retriggers():
    sr = 48000
    freq = 1000.0
    sine = signal_generator.sine(freq, 0.1, sr, amplitude=1.0)

    engine = TriggerEngine(TriggerConfig(
        trigger_type=TriggerType.LEVEL, edge=TriggerEdge.RISING, threshold=0.0, hysteresis=0.05,
        holdoff_samples=int(sr / freq * 5),
    ))
    triggers = engine.find_triggers(sine, sr)
    intervals = np.diff(triggers)
    assert np.all(intervals >= int(sr / freq * 5))


def test_zero_crossing_trigger_matches_level_trigger_at_zero_threshold():
    sr = 48000
    sine = signal_generator.sine(300, 0.5, sr, amplitude=1.0)

    zc_engine = TriggerEngine(TriggerConfig(trigger_type=TriggerType.ZERO_CROSSING, edge=TriggerEdge.RISING))
    level_engine = TriggerEngine(TriggerConfig(trigger_type=TriggerType.LEVEL, edge=TriggerEdge.RISING, threshold=0.0))

    assert np.allclose(zc_engine.find_triggers(sine, sr), level_engine.find_triggers(sine, sr))


def test_note_onset_detects_attack():
    sr = 48000
    silence = np.zeros(int(0.2 * sr))
    note = signal_generator.exponential_decay(220, 1.0, sr, decay_tau_seconds=0.3, amplitude=1.0)
    signal = np.concatenate([silence, note])

    engine = TriggerEngine(TriggerConfig(trigger_type=TriggerType.NOTE_ONSET, onset_energy_ratio=3.0))
    onsets = engine.find_triggers(signal, sr)

    assert len(onsets) >= 1
    assert abs(onsets[0] - len(silence)) < sr * 0.05


def test_capture_frame_respects_pre_and_post_samples():
    sr = 48000
    sine = signal_generator.sine(440, 1.0, sr)
    engine = TriggerEngine(TriggerConfig(trigger_type=TriggerType.LEVEL, threshold=0.0))
    trigger_index = 20000.0
    frame, start = engine.capture_frame(sine, trigger_index, pre_samples=100, post_samples=200)
    assert start == 19900
    assert len(frame) == 300
