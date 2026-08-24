"""Signal-processing primitives used by the blend and finishing chain.

Two families of functions live here:

* Source-filter tools (whiten / resynthesize / warp_envelope_freq /
  pitch_shift) that let pitch and formants be manipulated independently,
  operating on the (residual, envelope) representation produced by
  ``engine.analysis``.
* Character-finishing tools (EQ, dynamics, saturation, breath, delay,
  reverb, doubler, stereo width) that work directly on a rendered
  waveform, matching the "Character finishing" stage in the Voice Forge
  spec.
"""
from __future__ import annotations

import numpy as np
import librosa
from scipy import signal
from scipy.interpolate import interp1d

from . import analysis

EPS = 1e-8


# ---------------------------------------------------------------------------
# Source-filter (pitch / formant) tools
# ---------------------------------------------------------------------------

def whiten(y: np.ndarray, sr: int, n_fft: int = 1024, hop: int = 256, order: int | None = None):
    """Split y into a flattened excitation ("residual") and its LPC
    spectral envelope. residual = STFT(y) / envelope, phase preserved."""
    stft, env_mag, freqs = analysis.stft_envelope(y, sr, n_fft=n_fft, hop=hop, order=order)
    residual_stft = stft / (env_mag + EPS)
    residual = librosa.istft(residual_stft, hop_length=hop, length=len(y))
    return residual.astype(np.float32), env_mag, freqs


def resize_env_time(env_mag: np.ndarray, n_frames_target: int) -> np.ndarray:
    """Stretch/compress an envelope's time axis to a new frame count."""
    n_freq, n_frames = env_mag.shape
    if n_frames == n_frames_target:
        return env_mag
    if n_frames == 1:
        return np.repeat(env_mag, n_frames_target, axis=1)
    x_old = np.linspace(0.0, 1.0, n_frames)
    x_new = np.linspace(0.0, 1.0, n_frames_target)
    f = interp1d(x_old, env_mag, axis=1, kind="linear", fill_value="extrapolate")
    return f(x_new)


def resynthesize(residual: np.ndarray, env_mag: np.ndarray, sr: int, n_fft: int = 1024,
                  hop: int = 256, length: int | None = None) -> np.ndarray:
    """Rebuild a waveform from an excitation signal and a target envelope."""
    stft_res = librosa.stft(residual, n_fft=n_fft, hop_length=hop, center=True)
    env_resized = resize_env_time(np.abs(env_mag), stft_res.shape[1])
    new_stft = stft_res * env_resized
    if length is None:
        length = len(residual)
    y = librosa.istft(new_stft, hop_length=hop, length=length)
    return y.astype(np.float32)


def warp_envelope_freq(env_mag: np.ndarray, freqs: np.ndarray, ratio: float) -> np.ndarray:
    """Scale formant frequencies by `ratio` (>1 raises them / smaller
    vocal tract, <1 lowers them / larger tract) without touching pitch."""
    if abs(ratio - 1.0) < 1e-6:
        return env_mag
    n_freq, n_frames = env_mag.shape
    warped = np.empty_like(env_mag)
    query = freqs / ratio
    for t in range(n_frames):
        col = env_mag[:, t]
        warped[:, t] = np.interp(query, freqs, col, left=col[0], right=col[-1])
    return warped


def pitch_shift(y: np.ndarray, sr: int, semitones: float) -> np.ndarray:
    if abs(semitones) < 1e-6 or y.size == 0:
        return y
    return librosa.effects.pitch_shift(y.astype(np.float32), sr=sr, n_steps=semitones).astype(np.float32)


def time_stretch_to_ratio(y: np.ndarray, ratio: float) -> np.ndarray:
    """ratio > 1 makes the result longer (slower speech); < 1 shorter."""
    if abs(ratio - 1.0) < 1e-6 or y.size == 0:
        return y
    rate = 1.0 / ratio
    return librosa.effects.time_stretch(y.astype(np.float32), rate=rate).astype(np.float32)


def time_stretch_to_length(y: np.ndarray, target_len: int) -> np.ndarray:
    if len(y) == 0 or target_len <= 0:
        return y
    rate = len(y) / target_len
    if abs(rate - 1.0) < 1e-6:
        return y
    stretched = librosa.effects.time_stretch(y.astype(np.float32), rate=rate)
    return match_length(stretched, target_len)


def match_length(y: np.ndarray, target_len: int) -> np.ndarray:
    if len(y) == target_len:
        return y
    if len(y) > target_len:
        return y[:target_len]
    return np.pad(y, (0, target_len - len(y)))


def micro_pitch_jitter(y: np.ndarray, sr: int, amount: float, rate_hz: float = 4.5) -> np.ndarray:
    """Slow +/- cents wobble via variable-rate resampling: a simple
    vibrato / pitch-instability emulator, amount in [0, 1]."""
    if amount <= 0 or y.size == 0:
        return y
    n = len(y)
    t = np.arange(n) / sr
    max_cents = 35.0 * amount
    cents = max_cents * np.sin(2 * np.pi * rate_hz * t)
    rate = 2.0 ** (cents / 1200.0)
    warped_pos = np.cumsum(rate)
    warped_pos *= (n - 1) / warped_pos[-1]
    idx = np.arange(n)
    return np.interp(idx, warped_pos, y).astype(np.float32)


# ---------------------------------------------------------------------------
# EQ (RBJ biquads + Butterworth cuts)
# ---------------------------------------------------------------------------

def _biquad_peak(sr, freq, gain_db, q=1.0):
    A = 10 ** (gain_db / 40.0)
    w0 = 2 * np.pi * freq / sr
    alpha = np.sin(w0) / (2 * q)
    cos_w0 = np.cos(w0)
    b0, b1, b2 = 1 + alpha * A, -2 * cos_w0, 1 - alpha * A
    a0, a1, a2 = 1 + alpha / A, -2 * cos_w0, 1 - alpha / A
    return np.array([b0, b1, b2]) / a0, np.array([1.0, a1 / a0, a2 / a0])


def _biquad_shelf(sr, freq, gain_db, kind="low", slope=1.0):
    A = 10 ** (gain_db / 40.0)
    w0 = 2 * np.pi * freq / sr
    cos_w0, sin_w0 = np.cos(w0), np.sin(w0)
    alpha = sin_w0 / 2 * np.sqrt((A + 1 / A) * (1 / slope - 1) + 2)
    sqrtA = np.sqrt(A)
    if kind == "low":
        b0 = A * ((A + 1) - (A - 1) * cos_w0 + 2 * sqrtA * alpha)
        b1 = 2 * A * ((A - 1) - (A + 1) * cos_w0)
        b2 = A * ((A + 1) - (A - 1) * cos_w0 - 2 * sqrtA * alpha)
        a0 = (A + 1) + (A - 1) * cos_w0 + 2 * sqrtA * alpha
        a1 = -2 * ((A - 1) + (A + 1) * cos_w0)
        a2 = (A + 1) + (A - 1) * cos_w0 - 2 * sqrtA * alpha
    else:
        b0 = A * ((A + 1) + (A - 1) * cos_w0 + 2 * sqrtA * alpha)
        b1 = -2 * A * ((A - 1) + (A + 1) * cos_w0)
        b2 = A * ((A + 1) + (A - 1) * cos_w0 - 2 * sqrtA * alpha)
        a0 = (A + 1) - (A - 1) * cos_w0 + 2 * sqrtA * alpha
        a1 = 2 * ((A - 1) - (A + 1) * cos_w0)
        a2 = (A + 1) - (A - 1) * cos_w0 - 2 * sqrtA * alpha
    return np.array([b0, b1, b2]) / a0, np.array([1.0, a1 / a0, a2 / a0])


def _apply(y, b, a):
    return signal.lfilter(b, a, y).astype(np.float32)


def low_shelf(y, sr, freq, gain_db):
    if abs(gain_db) < 1e-6:
        return y
    b, a = _biquad_shelf(sr, freq, gain_db, kind="low")
    return _apply(y, b, a)


def high_shelf(y, sr, freq, gain_db):
    if abs(gain_db) < 1e-6:
        return y
    b, a = _biquad_shelf(sr, freq, gain_db, kind="high")
    return _apply(y, b, a)


def peaking_eq(y, sr, freq, gain_db, q=1.0):
    if abs(gain_db) < 1e-6:
        return y
    b, a = _biquad_peak(sr, freq, gain_db, q)
    return _apply(y, b, a)


def high_low_cut(y, sr, low_hz=0.0, high_hz=0.0):
    nyq = sr / 2.0
    out = y
    if low_hz and low_hz > 20:
        sos = signal.butter(2, min(0.999, low_hz / nyq), btype="highpass", output="sos")
        out = signal.sosfiltfilt(sos, out).astype(np.float32)
    if high_hz and high_hz < nyq - 100:
        sos = signal.butter(2, high_hz / nyq, btype="lowpass", output="sos")
        out = signal.sosfiltfilt(sos, out).astype(np.float32)
    return out


def nasality(y, sr, amount_db):
    return peaking_eq(y, sr, freq=1000.0, gain_db=amount_db, q=3.0)


# ---------------------------------------------------------------------------
# Character texture
# ---------------------------------------------------------------------------

def waveshape(y, drive, mix=1.0):
    if drive <= 0 or mix <= 0:
        return y
    k = 1.0 + drive * 9.0
    shaped = np.tanh(k * y) / np.tanh(k)
    return ((1 - mix) * y + mix * shaped).astype(np.float32)


def add_rasp(y, amount):
    return waveshape(y, drive=amount, mix=amount)


def saturate(y, drive):
    if drive <= 0:
        return y
    return waveshape(y, drive=drive, mix=min(1.0, 0.3 + 0.7 * drive))


def add_breath(y, sr, amount, seed=0):
    if amount <= 0 or y.size == 0:
        return y
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(len(y)).astype(np.float64)
    nyq = sr / 2.0
    sos = signal.butter(2, [2000 / nyq, min(0.99, 9000 / nyq)], btype="bandpass", output="sos")
    noise = signal.sosfilt(sos, noise)
    env = np.abs(signal.hilbert(y.astype(np.float64)))
    win = max(1, int(sr * 0.02))
    env_smooth = np.convolve(env, np.ones(win) / win, mode="same")
    if env_smooth.max() > 1e-9:
        env_smooth = env_smooth / env_smooth.max()
    noise *= env_smooth
    noise_peak = np.max(np.abs(noise)) + 1e-9
    voice_peak = np.max(np.abs(y)) + 1e-9
    return (y + amount * 0.6 * voice_peak * noise / noise_peak).astype(np.float32)


def articulate(y, sr, amount):
    if amount <= 0 or y.size == 0:
        return y
    hp = high_low_cut(y, sr, low_hz=3000.0, high_hz=0.0)
    deriv = np.diff(hp, prepend=hp[0])
    peak = np.max(np.abs(y)) + 1e-9
    deriv_peak = np.max(np.abs(deriv)) + 1e-9
    return (y + amount * 0.5 * peak * deriv / deriv_peak).astype(np.float32)


def deesser(y, sr, amount, band=(4000.0, 9000.0)):
    if amount <= 0 or y.size == 0:
        return y
    nyq = sr / 2.0
    lo, hi = max(band[0], 100.0), min(band[1], nyq - 100.0)
    if lo >= hi:
        return y
    sos = signal.butter(2, [lo / nyq, hi / nyq], btype="bandpass", output="sos")
    band_sig = signal.sosfilt(sos, y.astype(np.float64))
    env = np.abs(signal.hilbert(band_sig))
    win = max(1, int(sr * 0.005))
    env_smooth = np.convolve(env, np.ones(win) / win, mode="same") + 1e-9
    thresh = np.percentile(env_smooth, 60)
    gain = np.ones_like(env_smooth)
    over = env_smooth > thresh
    gain[over] = (thresh / env_smooth[over]) ** amount
    return (y - band_sig + band_sig * gain).astype(np.float32)


def compressor(y, sr, threshold_db=-18.0, ratio=3.0, attack_ms=5.0, release_ms=80.0, makeup_db=0.0):
    if y.size == 0:
        return y
    makeup = 10 ** (makeup_db / 20.0)
    if ratio <= 1.0:
        return (y * makeup).astype(np.float32)
    x = y.astype(np.float64)
    level = np.abs(x)
    att = np.exp(-1.0 / max(1.0, sr * (attack_ms / 1000.0)))
    rel = np.exp(-1.0 / max(1.0, sr * (release_ms / 1000.0)))
    env = np.empty_like(level)
    g = 0.0
    for i in range(level.shape[0]):
        coeff = att if level[i] > g else rel
        g = coeff * g + (1 - coeff) * level[i]
        env[i] = g
    env_db = 20 * np.log10(env + EPS)
    over = env_db - threshold_db
    gain_db = np.where(over > 0, -over * (1 - 1 / ratio), 0.0)
    gain = 10 ** (gain_db / 20.0)
    return (x * gain * makeup).astype(np.float32)


# ---------------------------------------------------------------------------
# Space: delay, reverb, doubler, stereo width
# ---------------------------------------------------------------------------

def delay_fx(y, sr, time_ms=220.0, feedback=0.3, mix=0.0):
    if mix <= 0 or y.size == 0:
        return y
    d = max(1, int(sr * time_ms / 1000.0))
    fb = float(np.clip(feedback, 0.0, 0.95))
    a = np.zeros(d + 1)
    a[0] = 1.0
    a[d] = -fb
    wet = signal.lfilter([1.0], a, y)
    return ((1 - mix) * y + mix * wet).astype(np.float32)


def _comb_filter(x, delay, feedback):
    a = np.zeros(delay + 1)
    a[0] = 1.0
    a[delay] = -feedback
    return signal.lfilter([1.0], a, x)


def _allpass_filter(x, delay, gain=0.5):
    b = np.zeros(delay + 1)
    b[0] = -gain
    b[delay] = 1.0
    a = np.zeros(delay + 1)
    a[0] = 1.0
    a[delay] = -gain
    return signal.lfilter(b, a, x)


def reverb_fx(y, sr, size=0.5, mix=0.3):
    if mix <= 0 or y.size == 0:
        return y
    comb_delays_ms = [29.7, 37.1, 41.1, 43.7]
    fb = 0.6 + 0.35 * float(np.clip(size, 0.0, 1.0))
    wet = np.zeros(len(y))
    for ms in comb_delays_ms:
        d = max(1, int(sr * ms / 1000.0 * (0.5 + size)))
        wet = wet + _comb_filter(y.astype(np.float64), d, fb)
    wet /= len(comb_delays_ms)
    for ms, g in ((5.0, 0.7), (1.7, 0.5)):
        d = max(1, int(sr * ms / 1000.0))
        wet = _allpass_filter(wet, d, g)
    wet = high_low_cut(wet.astype(np.float32), sr, low_hz=0.0, high_hz=8000.0)
    wet_peak = np.max(np.abs(wet)) + EPS
    dry_peak = np.max(np.abs(y)) + EPS
    wet = wet / wet_peak * dry_peak
    return ((1 - mix) * y + mix * wet).astype(np.float32)


def to_stereo(mono: np.ndarray) -> np.ndarray:
    return np.stack([mono, mono], axis=-1).astype(np.float32)


def doubler(mono: np.ndarray, sr: int, amount: float) -> np.ndarray:
    if amount <= 0 or mono.size == 0:
        return to_stereo(mono)
    delay_samples = int(sr * 0.018)
    detuned = pitch_shift(mono, sr, semitones=0.08)
    detuned = match_length(detuned, len(mono))
    left = (1 - amount) * mono + amount * np.pad(detuned, (delay_samples, 0))[: len(mono)]
    right = (1 - amount) * mono + amount * np.pad(detuned, (0, delay_samples))[delay_samples : delay_samples + len(mono)]
    right = match_length(right, len(mono))
    return np.stack([left, right], axis=-1).astype(np.float32)


def stereo_width(stereo: np.ndarray, width: float) -> np.ndarray:
    if abs(width - 1.0) < 1e-6:
        return stereo
    mid = (stereo[:, 0] + stereo[:, 1]) / 2.0
    side = (stereo[:, 0] - stereo[:, 1]) / 2.0 * width
    return np.stack([mid + side, mid - side], axis=-1).astype(np.float32)
