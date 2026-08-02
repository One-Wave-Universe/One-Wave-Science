"""Resonance detection and ring-down analysis (Section 15).

A resonance is not just a large FFT peak (Section 15) -- candidates are
scored on prominence, persistence across time, decay behavior, and phase
stability, and are left classified as "unknown" unless the caller
supplies domain knowledge, since this engine has no basis on its own to
tell a body resonance from a room resonance (Section 15.1).
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from scipy.signal import butter, filtfilt, hilbert

from onewave_mapper.spectrogram import Spectrogram, compute_spectrogram
from onewave_mapper.envelope import fit_exponential_decay


@dataclass
class ResonanceEvent:
    center_frequency_hz: float
    bandwidth_hz: float
    quality_factor: float
    start_sample: int
    end_sample: int
    peak_level_dbfs: float
    decay_rate_db_per_second: float | None
    phase_stability: float
    persistence_score: float
    coherence_score: float | None
    classification: str
    confidence: float
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def _find_prominent_bins(mean_magnitude: np.ndarray, min_prominence_db: float = 6.0,
                          max_candidates: int = 20) -> list[int]:
    mean_db = 20 * np.log10(np.maximum(mean_magnitude, 1e-12))
    candidates = []
    for i in range(1, len(mean_db) - 1):
        if mean_db[i] > mean_db[i - 1] and mean_db[i] >= mean_db[i + 1]:
            lo = max(0, i - 10)
            hi = min(len(mean_db), i + 11)
            local_floor = np.median(mean_db[lo:hi])
            prominence = mean_db[i] - local_floor
            if prominence >= min_prominence_db:
                candidates.append((prominence, i))
    candidates.sort(reverse=True)
    return [i for _, i in candidates[:max_candidates]]


def _bandwidth_and_q(freqs_hz: np.ndarray, mean_db: np.ndarray, peak_bin: int) -> tuple[float, float]:
    peak_db = mean_db[peak_bin]
    target = peak_db - 3.0

    lo = peak_bin
    while lo > 0 and mean_db[lo] > target:
        lo -= 1
    hi = peak_bin
    while hi < len(mean_db) - 1 and mean_db[hi] > target:
        hi += 1

    bandwidth_hz = max(freqs_hz[hi] - freqs_hz[lo], freqs_hz[1] - freqs_hz[0])
    fc = freqs_hz[peak_bin]
    quality_factor = fc / bandwidth_hz if bandwidth_hz > 0 else float("inf")
    return float(bandwidth_hz), float(quality_factor)


def _phase_stability(spectrogram: Spectrogram, bin_index: int, present_frames: np.ndarray) -> float:
    if present_frames.sum() < 3:
        return 0.0
    phase = spectrogram.phase_rad[bin_index, present_frames]
    unwrapped = np.unwrap(phase)
    increments = np.diff(unwrapped)
    if len(increments) < 2:
        return 0.0
    normalized_std = np.std(increments) / (np.abs(np.mean(increments)) + 1e-9)
    return float(max(0.0, 1.0 - min(1.0, normalized_std)))


def detect_resonances(signal: np.ndarray, sample_rate: float, fft_size: int = 4096,
                       hop_size: int = 1024, min_prominence_db: float = 6.0,
                       persistence_threshold_db: float = -6.0,
                       max_candidates: int = 20) -> list[ResonanceEvent]:
    spectrogram = compute_spectrogram(signal, sample_rate, fft_size=fft_size, hop_size=hop_size)
    if spectrogram.magnitude.shape[1] == 0:
        return []

    mean_magnitude = np.mean(spectrogram.magnitude, axis=1)
    mean_db = 20 * np.log10(np.maximum(mean_magnitude, 1e-12))
    candidate_bins = _find_prominent_bins(mean_magnitude, min_prominence_db, max_candidates)

    events = []
    n_frames = spectrogram.magnitude.shape[1]

    for bin_index in candidate_bins:
        bin_track_db = spectrogram.magnitude_db[bin_index, :]
        peak_db = np.max(bin_track_db)
        present_frames = np.where(bin_track_db >= peak_db + persistence_threshold_db)[0]
        persistence_score = float(len(present_frames) / n_frames)

        bandwidth_hz, quality_factor = _bandwidth_and_q(spectrogram.freqs_hz, mean_db, bin_index)

        peak_frame = int(np.argmax(bin_track_db))
        decay_segment = bin_track_db[peak_frame:]
        decay_rate_db_per_second = None
        if len(decay_segment) >= 2:
            frame_period_seconds = spectrogram.hop_size / sample_rate
            t = np.arange(len(decay_segment)) * frame_period_seconds
            finite = np.isfinite(decay_segment)
            if np.sum(finite) >= 2:
                slope, _ = np.polyfit(t[finite], decay_segment[finite], 1)
                decay_rate_db_per_second = float(slope)

        phase_stability = _phase_stability(spectrogram, bin_index, present_frames)

        confidence = float(np.clip(0.5 * persistence_score + 0.5 * phase_stability, 0.0, 1.0))

        start_sample = int(present_frames[0] * spectrogram.hop_size) if present_frames.size else 0
        end_sample = int(present_frames[-1] * spectrogram.hop_size + spectrogram.fft_size) if present_frames.size else len(signal)
        end_sample = min(end_sample, len(signal))

        events.append(ResonanceEvent(
            center_frequency_hz=float(spectrogram.freqs_hz[bin_index]),
            bandwidth_hz=bandwidth_hz,
            quality_factor=quality_factor,
            start_sample=start_sample,
            end_sample=end_sample,
            peak_level_dbfs=float(peak_db),
            decay_rate_db_per_second=decay_rate_db_per_second,
            phase_stability=phase_stability,
            persistence_score=persistence_score,
            coherence_score=None,
            classification="unknown",
            confidence=confidence,
        ))

    events.sort(key=lambda e: e.peak_level_dbfs, reverse=True)
    return events


def ring_down_analysis(signal: np.ndarray, sample_rate: float, center_frequency_hz: float,
                        bandwidth_hz: float, excitation_end_sample: int | None = None) -> dict:
    """Bandpass-isolate a resonance and analyze its decay (Section 15.3)."""
    nyquist = sample_rate / 2.0
    low = max(1.0, center_frequency_hz - bandwidth_hz) / nyquist
    high = min(nyquist - 1.0, center_frequency_hz + bandwidth_hz) / nyquist
    if not (0 < low < high < 1.0):
        raise ValueError("invalid bandpass range for the given sample rate")

    b, a = butter(4, [low, high], btype="bandpass")
    isolated = filtfilt(b, a, signal)

    start = excitation_end_sample if excitation_end_sample is not None else int(np.argmax(np.abs(isolated)))
    start = max(0, min(start, len(isolated) - 1))

    env = np.abs(hilbert(isolated))
    fit = fit_exponential_decay(env, sample_rate, start_index=start)

    ring_down_segment = isolated[start:]
    analytic = hilbert(ring_down_segment)
    inst_phase = np.unwrap(np.angle(analytic))
    inst_freq = np.diff(inst_phase) / (2 * np.pi) * sample_rate

    early = inst_freq[: max(1, len(inst_freq) // 10)]
    late = inst_freq[-max(1, len(inst_freq) // 10):]
    frequency_drift_hz = float(np.mean(late) - np.mean(early)) if len(inst_freq) > 1 else 0.0

    return {
        "isolated_signal": isolated,
        "envelope": env,
        "start_sample": start,
        "exponential_fit": fit,
        "frequency_drift_hz": frequency_drift_hz,
        "phase_progression_rad": inst_phase,
    }
