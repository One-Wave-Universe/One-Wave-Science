import numpy as np

from tests.helpers import sine_tone, estimate_f0_autocorr
from engine import dsp
from tools.make_sample_voices import synth_voice


def test_whiten_resynthesize_reconstructs_signal():
    sr = 16000
    y = synth_voice(sr, duration=0.8, f0=140.0, formants=[(700, 12, 3.0), (1500, 10, 3.0)], breath=0.0, seed=3)
    residual, env_mag, freqs = dsp.whiten(y, sr, n_fft=1024, hop=256)
    y_rebuilt = dsp.resynthesize(residual, env_mag, sr, n_fft=1024, hop=256, length=len(y))

    assert len(y_rebuilt) == len(y)
    corr = np.corrcoef(y, y_rebuilt)[0, 1]
    assert corr > 0.9


def test_pitch_shift_changes_fundamental():
    sr = 16000
    y = sine_tone(freq=150.0, sr=sr, duration=0.5)
    shifted = dsp.pitch_shift(y, sr, semitones=12.0)  # one octave up

    f0_before = estimate_f0_autocorr(y, sr)
    f0_after = estimate_f0_autocorr(shifted, sr)

    assert f0_before == 0 or abs(f0_before - 150.0) < 10
    assert abs(f0_after - 300.0) < 20
    assert len(shifted) == len(y)


def test_pitch_shift_zero_is_identity():
    y = sine_tone()
    assert np.array_equal(dsp.pitch_shift(y, 16000, 0.0), y)


def test_warp_envelope_freq_moves_formant_peak():
    sr = 16000
    n_fft = 1024
    freqs = np.linspace(0, sr / 2, n_fft // 2 + 1)
    env = np.exp(-0.5 * ((freqs - 1000.0) / 80.0) ** 2).reshape(-1, 1)

    warped = dsp.warp_envelope_freq(env, freqs, ratio=1.5)
    peak_before = freqs[np.argmax(env[:, 0])]
    peak_after = freqs[np.argmax(warped[:, 0])]

    assert abs(peak_after - peak_before * 1.5) < (freqs[1] - freqs[0]) * 2


def test_time_stretch_to_length():
    y = sine_tone(duration=0.4)
    target_len = int(len(y) * 1.5)
    stretched = dsp.time_stretch_to_length(y, target_len)
    assert len(stretched) == target_len


def test_eq_filters_run_and_change_signal():
    sr = 16000
    y = synth_voice(sr, duration=0.5, f0=120.0, formants=[(600, 10, 3.0)], breath=0.0, seed=4)
    boosted = dsp.low_shelf(y, sr, freq=200.0, gain_db=12.0)
    assert boosted.shape == y.shape
    assert not np.allclose(boosted, y)


def test_high_low_cut_removes_energy_outside_band():
    sr = 16000
    n = sr
    t = np.arange(n) / sr
    y = (np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 4000 * t)).astype(np.float32)
    filtered = dsp.high_low_cut(y, sr, low_hz=200.0, high_hz=2000.0)

    import librosa

    mag = np.abs(librosa.stft(filtered, n_fft=1024))
    mag_orig = np.abs(librosa.stft(y, n_fft=1024))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=1024)
    low_before, low_after = mag_orig[freqs < 100].sum(), mag[freqs < 100].sum()
    high_before, high_after = mag_orig[(freqs > 3000) & (freqs < 5000)].sum(), mag[(freqs > 3000) & (freqs < 5000)].sum()
    assert low_after < low_before * 0.05
    assert high_after < high_before * 0.05


def test_compressor_reduces_dynamic_range():
    sr = 16000
    n = sr
    t = np.arange(n) / sr
    loud = np.sin(2 * np.pi * 200 * t) * np.where(t < 0.5, 0.1, 0.9)
    compressed = dsp.compressor(loud.astype(np.float32), sr, threshold_db=-20.0, ratio=6.0)

    quiet_rms_before = np.sqrt(np.mean(loud[: sr // 4] ** 2))
    loud_rms_before = np.sqrt(np.mean(loud[sr // 2 : sr // 2 + sr // 4] ** 2))
    quiet_rms_after = np.sqrt(np.mean(compressed[: sr // 4] ** 2))
    loud_rms_after = np.sqrt(np.mean(compressed[sr // 2 : sr // 2 + sr // 4] ** 2))

    ratio_before = loud_rms_before / (quiet_rms_before + 1e-9)
    ratio_after = loud_rms_after / (quiet_rms_after + 1e-9)
    assert ratio_after < ratio_before


def test_doubler_and_stereo_width_produce_stereo():
    y = sine_tone(duration=0.3)
    stereo = dsp.doubler(y, 16000, amount=0.5)
    assert stereo.shape == (len(y), 2)
    widened = dsp.stereo_width(stereo, width=1.5)
    assert widened.shape == stereo.shape
    assert not np.allclose(widened, stereo)


def test_reverb_and_delay_run_without_error():
    y = sine_tone(duration=0.3)
    wet = dsp.reverb_fx(y, 16000, size=0.5, mix=0.3)
    assert wet.shape == y.shape
    delayed = dsp.delay_fx(y, 16000, time_ms=100.0, feedback=0.3, mix=0.4)
    assert delayed.shape == y.shape
