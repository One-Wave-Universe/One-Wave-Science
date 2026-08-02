"""Interference analysis (Section 14).

Section 14.3's constructive/destructive scores stop short of claiming
perfect physical source separation once signals are already mixed into
one microphone signal, and Section 14.4's isolated-vs-combined comparison
is explicitly labeled an experiment rather than a measurement, because
exact repeatability of human picking is limited.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from onewave_mapper import fft_analyzer
from onewave_mapper.phase_analysis import cross_correlation_delay
from onewave_mapper.envelope import hilbert_envelope


def sum_signal(x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    return x1 + x2


def difference_signal(x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    return x1 - x2


def frequency_dependent_response(x1: np.ndarray, x2: np.ndarray, combined: np.ndarray,
                                  sample_rate: float, fft_size: int | None = None,
                                  significance_fraction: float = 0.01) -> dict:
    """Per-bin comparison of the actual combined spectrum against the
    phase-blind naive sum |X1| + |X2| (Section 14.1).

    By the triangle inequality, |X1 + X2| <= |X1| + |X2| at every bin, so
    db_difference is always <= 0: 0 dB means that frequency combined as
    constructively as physically possible (in phase), and increasingly
    negative values mean deeper destructive cancellation. Bins where
    neither source has significant energy are masked to NaN so noise-floor
    artifacts don't dominate a min/max over the whole spectrum.
    """
    n = fft_size or min(len(x1), len(x2), len(combined))
    spectrum1 = fft_analyzer.compute_spectrum(x1[:n], sample_rate, fft_size=n)
    spectrum2 = fft_analyzer.compute_spectrum(x2[:n], sample_rate, fft_size=n)
    actual_spectrum = fft_analyzer.compute_spectrum(combined[:n], sample_rate, fft_size=n)

    predicted_magnitude = spectrum1.magnitude + spectrum2.magnitude
    predicted_db = 20 * np.log10(np.maximum(predicted_magnitude, 1e-12))
    db_difference = actual_spectrum.magnitude_db - predicted_db

    threshold = significance_fraction * np.max(predicted_magnitude)
    significant = predicted_magnitude >= threshold
    db_difference_masked = np.where(significant, db_difference, np.nan)

    return {
        "freqs_hz": actual_spectrum.freqs_hz,
        "db_difference": db_difference,
        "db_difference_significant": db_difference_masked,
        "predicted_magnitude": predicted_magnitude,
        "actual_spectrum": actual_spectrum,
    }


@dataclass
class BeatResult:
    beat_frequency_hz: float | None
    confidence: float
    stability: float | None
    drift_hz_per_second: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def detect_beats(signal: np.ndarray, sample_rate: float, min_beat_hz: float = 0.2,
                  max_beat_hz: float = 20.0) -> BeatResult:
    """Beat rate from the amplitude-envelope modulation spectrum (Section 14.2)."""
    envelope = hilbert_envelope(signal)
    envelope = envelope - np.mean(envelope)
    n = len(envelope)
    if n < 8:
        return BeatResult(beat_frequency_hz=None, confidence=0.0, stability=None, drift_hz_per_second=None)

    spectrum = np.abs(np.fft.rfft(envelope * np.hanning(n)))
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    mask = (freqs >= min_beat_hz) & (freqs <= max_beat_hz)
    if not np.any(mask):
        return BeatResult(beat_frequency_hz=None, confidence=0.0, stability=None, drift_hz_per_second=None)

    masked_spectrum = spectrum[mask]
    masked_freqs = freqs[mask]
    peak_index = int(np.argmax(masked_spectrum))
    beat_freq = float(masked_freqs[peak_index])
    total_energy = float(np.sum(masked_spectrum))
    confidence = float(masked_spectrum[peak_index] / total_energy) if total_energy > 1e-12 else 0.0

    stability, drift = _beat_stability_and_drift(envelope, sample_rate, min_beat_hz, max_beat_hz)

    return BeatResult(beat_frequency_hz=beat_freq, confidence=confidence,
                       stability=stability, drift_hz_per_second=drift)


def _beat_stability_and_drift(envelope: np.ndarray, sample_rate: float, min_beat_hz: float,
                               max_beat_hz: float, n_windows: int = 4) -> tuple[float | None, float | None]:
    n = len(envelope)
    window_size = n // n_windows
    if window_size < sample_rate / min_beat_hz:
        return None, None

    window_beats = []
    for i in range(n_windows):
        segment = envelope[i * window_size: (i + 1) * window_size]
        segment = segment - np.mean(segment)
        spectrum = np.abs(np.fft.rfft(segment * np.hanning(len(segment))))
        freqs = np.fft.rfftfreq(len(segment), d=1.0 / sample_rate)
        mask = (freqs >= min_beat_hz) & (freqs <= max_beat_hz)
        if not np.any(mask):
            continue
        peak_index = int(np.argmax(spectrum[mask]))
        window_beats.append(freqs[mask][peak_index])

    if len(window_beats) < 2:
        return None, None

    stability = float(1.0 - min(1.0, np.std(window_beats) / (np.mean(window_beats) + 1e-9)))
    window_duration = window_size / sample_rate
    drift, _ = np.polyfit(np.arange(len(window_beats)) * window_duration, window_beats, 1)
    return stability, float(drift)


@dataclass
class InterferenceScores:
    """cancellation_depth_db and reinforcement_gain_db are both derived from
    db_difference <= 0 (Section 14.1's triangle-inequality bound): 0 dB is
    the physical ceiling (perfectly in-phase at that frequency).
    reinforcement_gain_db is how close the best-aligned frequency got to
    that ceiling (closer to 0 is more constructive); cancellation_depth_db
    is how far below it the most destructive frequency fell (larger is
    deeper cancellation)."""
    constructive_score: float
    destructive_score: float
    phase_alignment_score: float
    cancellation_depth_db: float
    reinforcement_gain_db: float
    recurrence_period_seconds: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def interference_scores(x1: np.ndarray, x2: np.ndarray, sample_rate: float) -> InterferenceScores:
    """Constructive/destructive interference scoring (Section 14.3)."""
    combined = x1 + x2
    combined_rms = float(np.sqrt(np.mean(combined ** 2)))
    predicted_rms = float(np.sqrt(np.mean((np.abs(x1) + np.abs(x2)) ** 2)))

    constructive_score = float(np.clip(combined_rms / (predicted_rms + 1e-12), 0.0, 1.0))
    destructive_score = float(1.0 - constructive_score)

    n = min(len(x1), len(x2))
    correlation = float(np.corrcoef(x1[:n], x2[:n])[0, 1]) if n > 1 else 0.0
    phase_alignment_score = float((correlation + 1.0) / 2.0)

    response = frequency_dependent_response(x1, x2, combined, sample_rate)
    significant = response["db_difference_significant"]
    valid = significant[~np.isnan(significant)]
    cancellation_depth_db = float(-np.min(valid)) if valid.size else 0.0
    reinforcement_gain_db = float(np.max(valid)) if valid.size else 0.0

    beats = detect_beats(combined, sample_rate)
    recurrence_period_seconds = 1.0 / beats.beat_frequency_hz if beats.beat_frequency_hz else None

    return InterferenceScores(
        constructive_score=constructive_score,
        destructive_score=destructive_score,
        phase_alignment_score=phase_alignment_score,
        cancellation_depth_db=cancellation_depth_db,
        reinforcement_gain_db=reinforcement_gain_db,
        recurrence_period_seconds=recurrence_period_seconds,
    )


@dataclass
class IsolatedVsCombinedResult:
    delay_a_samples: float
    delay_b_samples: float
    gain_a: float
    gain_b: float
    residual_rms: float
    combined_rms: float
    residual_to_combined_db: float
    is_experiment: bool = True
    notes: str = (
        "Comparison against the real combined recording, not a physical measurement -- "
        "exact repeatability of human picking is limited (Section 14.4)."
    )

    def to_dict(self) -> dict:
        return asdict(self)


def compare_isolated_vs_combined(x_a: np.ndarray, x_b: np.ndarray, x_combined: np.ndarray,
                                  sample_rate: float) -> tuple[IsolatedVsCombinedResult, np.ndarray]:
    """Time-align, level-align, and residual-compare two isolated recordings
    against a real combined recording (Section 14.4). Returns
    (result, residual_signal)."""
    delay_a = cross_correlation_delay(x_combined, x_a, sample_rate)
    delay_b = cross_correlation_delay(x_combined, x_b, sample_rate)

    a_aligned = _shift(x_a, -int(round(delay_a.delay_samples)))
    b_aligned = _shift(x_b, -int(round(delay_b.delay_samples)))

    n = min(len(a_aligned), len(b_aligned), len(x_combined))
    a_aligned, b_aligned, combined = a_aligned[:n], b_aligned[:n], x_combined[:n]

    design = np.stack([a_aligned, b_aligned], axis=1)
    (gain_a, gain_b), *_ = np.linalg.lstsq(design, combined, rcond=None)

    predicted_sum = gain_a * a_aligned + gain_b * b_aligned
    residual = combined - predicted_sum

    residual_rms = float(np.sqrt(np.mean(residual ** 2)))
    combined_rms = float(np.sqrt(np.mean(combined ** 2)))
    residual_to_combined_db = float(20 * np.log10((residual_rms + 1e-12) / (combined_rms + 1e-12)))

    result = IsolatedVsCombinedResult(
        delay_a_samples=delay_a.delay_samples,
        delay_b_samples=delay_b.delay_samples,
        gain_a=float(gain_a),
        gain_b=float(gain_b),
        residual_rms=residual_rms,
        combined_rms=combined_rms,
        residual_to_combined_db=residual_to_combined_db,
    )
    return result, residual


def _shift(signal: np.ndarray, shift_samples: int) -> np.ndarray:
    """Shift signal by shift_samples (positive = delay/later, negative = advance/earlier),
    padding with zeros and keeping the original length."""
    if shift_samples == 0:
        return signal.copy()
    if shift_samples > 0:
        return np.concatenate([np.zeros(shift_samples), signal[:-shift_samples]]) if shift_samples < len(signal) \
            else np.zeros_like(signal)
    shift_samples = -shift_samples
    return np.concatenate([signal[shift_samples:], np.zeros(shift_samples)]) if shift_samples < len(signal) \
        else np.zeros_like(signal)
