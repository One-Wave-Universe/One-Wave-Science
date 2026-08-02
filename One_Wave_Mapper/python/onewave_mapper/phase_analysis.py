"""Multichannel phase, delay, and correlation analysis (Section 13)."""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from scipy.signal import hilbert, coherence as sp_coherence


@dataclass
class DelayEstimate:
    delay_samples: float
    delay_seconds: float
    correlation_coefficient: float

    def to_dict(self) -> dict:
        return asdict(self)


def cross_correlation_delay(x: np.ndarray, y: np.ndarray, sample_rate: float) -> DelayEstimate:
    """Positive delay means y lags x (y is x shifted later in time)."""
    x = x - np.mean(x)
    y = y - np.mean(y)

    correlation = np.correlate(y, x, mode="full")
    lags = np.arange(-len(x) + 1, len(y))
    best_index = int(np.argmax(correlation))

    if 0 < best_index < len(correlation) - 1:
        alpha, beta, gamma = correlation[best_index - 1], correlation[best_index], correlation[best_index + 1]
        denom = alpha - 2 * beta + gamma
        p = 0.5 * (alpha - gamma) / denom if abs(denom) > 1e-15 else 0.0
    else:
        p = 0.0

    delay_samples = float(lags[best_index] + p)
    delay_seconds = delay_samples / sample_rate

    norm = np.sqrt(np.sum(x ** 2) * np.sum(y ** 2))
    correlation_coefficient = float(correlation[best_index] / norm) if norm > 1e-20 else 0.0

    return DelayEstimate(delay_samples=delay_samples, delay_seconds=delay_seconds,
                          correlation_coefficient=correlation_coefficient)


def instantaneous_phase_difference_deg(x: np.ndarray, y: np.ndarray,
                                        trim_fraction: float = 0.25) -> float:
    """Mean phase difference (x relative to y, in degrees) via the analytic signal.

    The first/last trim_fraction of samples are excluded from the average
    to avoid Hilbert-transform edge artifacts.
    """
    analytic_x = hilbert(x)
    analytic_y = hilbert(y)
    phase_x = np.unwrap(np.angle(analytic_x))
    phase_y = np.unwrap(np.angle(analytic_y))

    n = len(x)
    trim = int(n * trim_fraction)
    diff_rad = phase_x[trim: n - trim] - phase_y[trim: n - trim]
    mean_diff_rad = np.angle(np.mean(np.exp(1j * diff_rad)))
    return float(np.rad2deg(mean_diff_rad))


def magnitude_squared_coherence(x: np.ndarray, y: np.ndarray, sample_rate: float,
                                 nperseg: int = 1024) -> tuple[np.ndarray, np.ndarray]:
    nperseg = min(nperseg, len(x), len(y))
    freqs, coh = sp_coherence(x, y, fs=sample_rate, nperseg=nperseg)
    return freqs, coh


def correlation_coefficient(x: np.ndarray, y: np.ndarray) -> float:
    x = x - np.mean(x)
    y = y - np.mean(y)
    denom = np.sqrt(np.sum(x ** 2) * np.sum(y ** 2))
    if denom <= 1e-20:
        return 0.0
    return float(np.sum(x * y) / denom)


def mid_side(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mid = 0.5 * (x + y)
    side = 0.5 * (x - y)
    return mid, side
