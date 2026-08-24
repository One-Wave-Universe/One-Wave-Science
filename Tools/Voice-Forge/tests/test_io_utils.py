import numpy as np

from tests.helpers import sine_tone
from engine import io_utils


def test_save_load_roundtrip(tmp_path):
    y = sine_tone(freq=220.0, sr=16000, duration=0.3)
    path = str(tmp_path / "tone.wav")
    io_utils.save_wav(path, y, 16000)

    loaded, sr = io_utils.load_audio(path)
    assert sr == 16000
    assert loaded.ndim == 1
    assert len(loaded) == len(y)
    assert np.max(np.abs(loaded - y)) < 1e-3


def test_load_resamples_to_target_sr(tmp_path):
    y = sine_tone(freq=220.0, sr=16000, duration=0.3)
    path = str(tmp_path / "tone.wav")
    io_utils.save_wav(path, y, 16000)

    loaded, sr = io_utils.load_audio(path, target_sr=22050)
    assert sr == 22050
    assert abs(len(loaded) - int(0.3 * 22050)) < 50


def test_peak_normalize():
    y = np.array([0.1, -0.2, 0.05], dtype=np.float32)
    out = io_utils.peak_normalize(y, target_peak=0.9)
    assert np.isclose(np.max(np.abs(out)), 0.9, atol=1e-4)
