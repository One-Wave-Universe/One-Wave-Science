"""Audio file I/O helpers.

Everything downstream in the engine works on mono float32 arrays in
[-1, 1] at an explicit sample rate. Stereo files are downmixed on load;
stereo is only reintroduced deliberately by the finishing chain
(doubler / stereo width).
"""
from __future__ import annotations

import numpy as np
import soundfile as sf


def load_audio(path: str, target_sr: int | None = None) -> tuple[np.ndarray, int]:
    """Load an audio file as mono float32 in [-1, 1].

    If target_sr is given and differs from the file's rate, the signal is
    resampled (via librosa, imported lazily to keep this module cheap for
    callers that only need to write audio).
    """
    y, sr = sf.read(path, dtype="float32", always_2d=False)
    if y.ndim > 1:
        y = y.mean(axis=1).astype(np.float32)
    if target_sr is not None and sr != target_sr:
        import librosa

        y = librosa.resample(y, orig_sr=sr, target_sr=target_sr).astype(np.float32)
        sr = target_sr
    return y, sr


def save_wav(path: str, y: np.ndarray, sr: int) -> None:
    """Write a mono or stereo float array to a 32-bit float WAV file.

    Stereo arrays are expected shaped (n_samples, 2).
    """
    y = np.asarray(y, dtype=np.float32)
    sf.write(path, y, sr, subtype="FLOAT")


def peak_normalize(y: np.ndarray, target_peak: float = 0.98) -> np.ndarray:
    peak = float(np.max(np.abs(y))) if y.size else 0.0
    if peak <= 1e-9:
        return y
    return (y * (target_peak / peak)).astype(np.float32)
