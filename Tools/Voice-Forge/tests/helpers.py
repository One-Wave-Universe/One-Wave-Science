"""Shared synthetic-signal helpers for engine tests. Nothing here depends
on real recordings -- everything is generated so tests are deterministic
and don't require any voice data to be committed."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def sine_tone(freq=150.0, sr=16000, duration=0.6, amp=0.6):
    n = int(sr * duration)
    t = np.arange(n) / sr
    return (amp * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def estimate_f0_autocorr(y, sr, fmin=50.0, fmax=500.0):
    y = y.astype(np.float64) - np.mean(y)
    corr = np.correlate(y, y, mode="full")[len(y) - 1 :]
    min_lag = max(1, int(sr / fmax))
    max_lag = min(len(corr) - 1, int(sr / fmin))
    if max_lag <= min_lag:
        return 0.0
    segment = corr[min_lag:max_lag]
    peak = int(np.argmax(segment)) + min_lag
    if peak <= 0:
        return 0.0
    return sr / peak


def spectral_centroid(y, sr):
    import librosa

    mag = np.abs(librosa.stft(y.astype(np.float32), n_fft=1024, hop_length=256))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=1024)
    weights = mag.sum(axis=1)
    if weights.sum() <= 1e-9:
        return 0.0
    return float(np.sum(freqs * weights) / weights.sum())
