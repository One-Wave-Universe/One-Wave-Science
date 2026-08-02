"""Envelope and transient analysis (Section 11)."""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from scipy.signal import hilbert


@dataclass
class EnvelopeMeasurements:
    attack_time_seconds: float | None
    peak_time_seconds: float
    decay_20db_seconds: float | None
    decay_40db_seconds: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def hilbert_envelope(signal: np.ndarray) -> np.ndarray:
    return np.abs(hilbert(signal))


def rms_envelope(signal: np.ndarray, sample_rate: float, window_ms: float = 10.0) -> np.ndarray:
    window_samples = max(1, int(sample_rate * window_ms / 1000.0))
    squared = np.square(signal)
    kernel = np.ones(window_samples) / window_samples
    mean_square = np.convolve(squared, kernel, mode="same")
    return np.sqrt(mean_square)


def peak_envelope(signal: np.ndarray, sample_rate: float, window_ms: float = 10.0) -> np.ndarray:
    window_samples = max(1, int(sample_rate * window_ms / 1000.0))
    absolute = np.abs(signal)
    n = len(signal)
    out = np.empty(n)
    for i in range(n):
        lo = max(0, i - window_samples // 2)
        hi = min(n, i + window_samples // 2 + 1)
        out[i] = np.max(absolute[lo:hi])
    return out


def measure_envelope(envelope: np.ndarray, sample_rate: float,
                      attack_threshold_fraction: float = 0.9) -> EnvelopeMeasurements:
    if envelope.size == 0:
        raise ValueError("cannot measure an empty envelope")

    peak_value = np.max(envelope)
    peak_index = int(np.argmax(envelope))
    peak_time_seconds = peak_index / sample_rate

    attack_threshold = attack_threshold_fraction * peak_value
    above_threshold = np.where(envelope[: peak_index + 1] >= attack_threshold)[0]
    attack_time_seconds = float(above_threshold[0] / sample_rate) if above_threshold.size else None

    decay_20db_seconds = _time_to_decay_db(envelope, sample_rate, peak_index, peak_value, 20.0)
    decay_40db_seconds = _time_to_decay_db(envelope, sample_rate, peak_index, peak_value, 40.0)

    return EnvelopeMeasurements(
        attack_time_seconds=attack_time_seconds,
        peak_time_seconds=peak_time_seconds,
        decay_20db_seconds=decay_20db_seconds,
        decay_40db_seconds=decay_40db_seconds,
    )


def _time_to_decay_db(envelope: np.ndarray, sample_rate: float, peak_index: int,
                       peak_value: float, decay_db: float) -> float | None:
    if peak_value <= 1e-12:
        return None
    target = peak_value * 10 ** (-decay_db / 20.0)
    tail = envelope[peak_index:]
    below = np.where(tail <= target)[0]
    if below.size == 0:
        return None
    return float(below[0] / sample_rate)


def fit_exponential_decay(envelope: np.ndarray, sample_rate: float,
                           start_index: int = 0) -> dict:
    """Fit envelope[start_index:] ~ A * exp(-t / tau) via a log-linear least-squares fit."""
    segment = envelope[start_index:]
    segment = np.maximum(segment, 1e-12)
    t = np.arange(len(segment)) / sample_rate
    log_amplitude = np.log(segment)

    valid = segment > (np.max(segment) * 1e-4)
    if np.sum(valid) < 2:
        return {"tau_seconds": None, "amplitude": None, "r_squared": None}

    slope, intercept = np.polyfit(t[valid], log_amplitude[valid], 1)
    tau_seconds = -1.0 / slope if slope < 0 else None
    amplitude = float(np.exp(intercept))

    predicted = intercept + slope * t[valid]
    residuals = log_amplitude[valid] - predicted
    ss_res = np.sum(residuals ** 2)
    ss_tot = np.sum((log_amplitude[valid] - np.mean(log_amplitude[valid])) ** 2)
    r_squared = float(1 - ss_res / ss_tot) if ss_tot > 1e-20 else None

    return {"tau_seconds": tau_seconds, "amplitude": amplitude, "r_squared": r_squared}
