"""Fundamental frequency detection using multiple independent methods (Section 8.3).

The engine reports confidence and disagreement between methods rather than
forcing a single pitch estimate when the signal is ambiguous or unvoiced.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np


@dataclass
class PitchResult:
    frequency_hz: float | None
    confidence: float
    method: str
    voiced_probability: float
    disagreement_hz: float | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def autocorrelation_pitch(signal: np.ndarray, sample_rate: float,
                           fmin: float = 60.0, fmax: float = 1500.0) -> tuple[float | None, float]:
    """Normalized autocorrelation with parabolic interpolation for sub-sample lag accuracy."""
    signal = signal - np.mean(signal)
    if np.max(np.abs(signal)) < 1e-9:
        return None, 0.0

    min_lag = int(sample_rate / fmax)
    max_lag = int(sample_rate / fmin)
    max_lag = min(max_lag, len(signal) - 1)
    if max_lag <= min_lag:
        return None, 0.0

    full_autocorr = np.correlate(signal, signal, mode="full")
    zero_lag_index = len(full_autocorr) // 2
    autocorr = full_autocorr[zero_lag_index:]
    autocorr = autocorr / (autocorr[0] + 1e-30)

    search = autocorr[min_lag:max_lag]
    if search.size == 0:
        return None, 0.0
    peak_offset = int(np.argmax(search))
    peak_lag = min_lag + peak_offset
    peak_value = float(autocorr[peak_lag])

    if 0 < peak_lag < len(autocorr) - 1:
        alpha = autocorr[peak_lag - 1]
        beta = autocorr[peak_lag]
        gamma = autocorr[peak_lag + 1]
        denom = alpha - 2 * beta + gamma
        p = 0.5 * (alpha - gamma) / denom if abs(denom) > 1e-15 else 0.0
        refined_lag = peak_lag + p
    else:
        refined_lag = float(peak_lag)

    if refined_lag <= 0:
        return None, 0.0

    frequency = sample_rate / refined_lag
    confidence = max(0.0, min(1.0, peak_value))
    return float(frequency), float(confidence)


def zero_crossing_pitch(signal: np.ndarray, sample_rate: float) -> float | None:
    signal = signal - np.mean(signal)
    signs = np.signbit(signal)
    crossings = np.where(np.diff(signs))[0]
    rising_crossings = [i for i in crossings if signal[i] < 0 <= signal[i + 1]]
    if len(rising_crossings) < 2:
        return None
    periods_samples = np.diff(rising_crossings)
    mean_period = np.mean(periods_samples)
    if mean_period <= 0:
        return None
    return float(sample_rate / mean_period)


def detect_pitch(signal: np.ndarray, sample_rate: float, fmin: float = 60.0,
                  fmax: float = 1500.0, min_confidence: float = 0.5) -> PitchResult:
    autocorr_freq, autocorr_confidence = autocorrelation_pitch(signal, sample_rate, fmin, fmax)
    zc_freq = zero_crossing_pitch(signal, sample_rate)

    if autocorr_freq is None:
        return PitchResult(frequency_hz=None, confidence=0.0, method="autocorrelation",
                            voiced_probability=0.0)

    disagreement_hz = abs(autocorr_freq - zc_freq) if zc_freq is not None else None

    voiced_probability = autocorr_confidence
    if disagreement_hz is not None and autocorr_freq > 0:
        relative_disagreement = disagreement_hz / autocorr_freq
        voiced_probability *= max(0.0, 1.0 - min(1.0, relative_disagreement * 4))

    if autocorr_confidence < min_confidence:
        return PitchResult(frequency_hz=None, confidence=autocorr_confidence,
                            method="autocorrelation", voiced_probability=voiced_probability,
                            disagreement_hz=disagreement_hz)

    return PitchResult(
        frequency_hz=autocorr_freq,
        confidence=autocorr_confidence,
        method="autocorrelation",
        voiced_probability=voiced_probability,
        disagreement_hz=disagreement_hz,
    )


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def frequency_to_note(frequency_hz: float, reference_a4_hz: float = 440.0) -> dict:
    if frequency_hz <= 0:
        raise ValueError("frequency_hz must be positive")
    midi_float = 69 + 12 * np.log2(frequency_hz / reference_a4_hz)
    midi_rounded = int(round(midi_float))
    cents_offset = float((midi_float - midi_rounded) * 100)
    note_name = NOTE_NAMES[midi_rounded % 12]
    octave = midi_rounded // 12 - 1
    return {
        "midi_note_float": float(midi_float),
        "note_name": f"{note_name}{octave}",
        "cents_offset": cents_offset,
    }
