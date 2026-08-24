"""Source-filter analysis: LPC spectral envelopes and pitch estimation.

The engine treats a voice as excitation (residual) * spectral envelope
(formants / vocal-tract shape), estimated per STFT frame via linear
predictive coding. Separating these two lets pitch and formant controls
act independently, and lets references be blended trait-by-trait instead
of as raw waveform crossfades.
"""
from __future__ import annotations

import numpy as np
import librosa
from scipy.signal import freqz

EPS = 1e-8


def lpc_order_for_sr(sr: int) -> int:
    """Rule-of-thumb LPC order: ~2 coefficients per kHz of sample rate,
    enough to resolve formants up to Nyquist without overfitting."""
    order = int(2 + sr / 1000)
    return max(8, order)


def frame_envelope_mag(y_frame: np.ndarray, order: int, n_fft: int) -> np.ndarray:
    """LPC spectral envelope magnitude for one windowed frame, evaluated
    at n_fft//2 + 1 linearly spaced frequency bins."""
    if not np.any(np.abs(y_frame) > 1e-6):
        return np.full(n_fft // 2 + 1, EPS, dtype=np.float64)
    try:
        a = librosa.lpc(y_frame.astype(np.float64), order=order)
    except Exception:
        return np.full(n_fft // 2 + 1, EPS, dtype=np.float64)
    _, h = freqz([1.0], a, worN=n_fft // 2 + 1)
    mag = np.abs(h)
    mag[mag < EPS] = EPS
    return mag


def stft_envelope(
    y: np.ndarray, sr: int, n_fft: int = 1024, hop: int = 256, order: int | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute the STFT of y plus a per-frame LPC envelope estimate.

    Returns (stft_complex[f, t], env_mag[f, t], freqs[f]).
    """
    if order is None:
        order = lpc_order_for_sr(sr)
    stft = librosa.stft(y, n_fft=n_fft, hop_length=hop, center=True)
    n_frames = stft.shape[1]
    win = np.hanning(n_fft)
    env = np.empty((n_fft // 2 + 1, n_frames), dtype=np.float64)
    pad = n_fft // 2
    y_padded = np.pad(y, (pad, pad), mode="constant")
    for t in range(n_frames):
        start = t * hop
        frame = y_padded[start : start + n_fft]
        if frame.shape[0] < n_fft:
            frame = np.pad(frame, (0, n_fft - frame.shape[0]))
        env[:, t] = frame_envelope_mag(frame * win, order, n_fft)
    freqs = np.linspace(0, sr / 2, n_fft // 2 + 1)
    return stft, env, freqs


def estimate_f0_median(y: np.ndarray, sr: int, fmin: float = 60.0, fmax: float = 500.0) -> float:
    """Rough median fundamental frequency, for UI display only (not used
    by the blend/pitch-shift math, which operates relative to the source)."""
    if y.size < sr // 10:
        return 0.0
    try:
        f0, voiced_flag, _ = librosa.pyin(y, sr=sr, fmin=fmin, fmax=fmax)
    except Exception:
        return 0.0
    voiced = f0[voiced_flag] if voiced_flag is not None else f0[~np.isnan(f0)]
    voiced = voiced[~np.isnan(voiced)]
    if voiced.size == 0:
        return 0.0
    return float(np.median(voiced))
