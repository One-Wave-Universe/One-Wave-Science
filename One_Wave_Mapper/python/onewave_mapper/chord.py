"""Chord and interval analysis (Section 18).

Reports both conventional note/interval names and raw frequency
relationships side by side (Section 18.1) rather than collapsing to
musical labels alone. The two-pitch detector uses iterative harmonic-sieve
scoring and spectral peeling (Section 18.3) -- a simplified but real
polyphonic pitch estimate, not a lookup table.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from onewave_mapper import fft_analyzer, pitch as pitch_module


@dataclass
class ChordEvent:
    detected_fundamentals: list
    candidate_notes: list
    confidence_per_note: list
    frequency_ratios: list
    pairwise_intervals: list
    shared_harmonics: list
    beat_components: list
    intermodulation_candidates: list

    def to_dict(self) -> dict:
        return asdict(self)


def interval_ratio(f1_hz: float, f2_hz: float) -> float:
    return f2_hz / f1_hz


def cents_interval(f1_hz: float, f2_hz: float) -> float:
    return float(1200 * np.log2(f2_hz / f1_hz))


def beat_frequency(f1_hz: float, f2_hz: float) -> float:
    return abs(f2_hz - f1_hz)


def shared_harmonics(f1_hz: float, f2_hz: float, max_harmonic: int = 16,
                      tolerance_cents: float = 50.0) -> list[dict]:
    """Frequencies where n*f1 nearly coincides with m*f2 (Section 18.1/18.2)."""
    matches = []
    for n in range(1, max_harmonic + 1):
        freq_n = n * f1_hz
        for m in range(1, max_harmonic + 1):
            freq_m = m * f2_hz
            if freq_n <= 0 or freq_m <= 0:
                continue
            deviation_cents = abs(1200 * np.log2(freq_n / freq_m))
            if deviation_cents <= tolerance_cents:
                matches.append({
                    "n": n, "m": m,
                    "frequency_hz": float((freq_n + freq_m) / 2),
                    "deviation_cents": float(deviation_cents),
                })
    return matches


def intermodulation_candidates(f1_hz: float, f2_hz: float, max_order: int = 3,
                                nyquist_hz: float | None = None) -> list[dict]:
    """m*f1 +/- n*f2 products for small m, n (Section 19). Labeled as
    possible products only -- not guaranteed identifications."""
    candidates = []
    for m in range(1, max_order + 1):
        for n in range(1, max_order + 1):
            for sign in (1, -1):
                freq = m * f1_hz + sign * n * f2_hz
                if freq <= 0:
                    continue
                if nyquist_hz is not None and freq >= nyquist_hz:
                    continue
                candidates.append({"m": m, "n": n, "sign": sign, "frequency_hz": float(freq)})
    return candidates


def sethares_roughness(f1_hz: float, f2_hz: float, amplitude1: float = 1.0,
                        amplitude2: float = 1.0) -> float:
    """Sethares (1993) sensory-dissonance model for a pair of partials.

    This is a descriptive roughness metric, not a claim about perceived
    consonance for any particular listener (Section 18.1).
    """
    f_min = min(f1_hz, f2_hz)
    f_diff = abs(f2_hz - f1_hz)
    s = 0.24 / (0.0207 * f_min + 18.96)
    amplitude_min = min(amplitude1, amplitude2)
    return float(amplitude_min * (np.exp(-3.5 * s * f_diff) - np.exp(-5.75 * s * f_diff)))


def harmonic_series_roughness(f1_hz: float, f2_hz: float, n_partials: int = 6) -> float:
    """Total roughness summed over all partial pairs of two harmonic series
    with 1/n amplitude rolloff."""
    total = 0.0
    for i in range(1, n_partials + 1):
        a_i = 1.0 / i
        for j in range(1, n_partials + 1):
            a_j = 1.0 / j
            total += sethares_roughness(i * f1_hz, j * f2_hz, a_i, a_j)
    return total


def analyze_interval(f1_hz: float, f2_hz: float, reference_a4_hz: float = 440.0) -> dict:
    note1 = pitch_module.frequency_to_note(f1_hz, reference_a4_hz)
    note2 = pitch_module.frequency_to_note(f2_hz, reference_a4_hz)
    return {
        "frequencies_hz": [f1_hz, f2_hz],
        "note_names": [note1["note_name"], note2["note_name"]],
        "ratio": interval_ratio(f1_hz, f2_hz),
        "cents": cents_interval(f1_hz, f2_hz),
        "beat_frequency_hz": beat_frequency(f1_hz, f2_hz),
        "shared_harmonics": shared_harmonics(f1_hz, f2_hz),
        "roughness": harmonic_series_roughness(f1_hz, f2_hz),
    }


def _harmonic_sieve_score(freqs_hz: np.ndarray, magnitude: np.ndarray, f0: float,
                           max_harmonics: int, tolerance_hz: float) -> float:
    score = 0.0
    nyquist = freqs_hz[-1]
    for n in range(1, max_harmonics + 1):
        expected = n * f0
        if expected >= nyquist:
            break
        mask = np.abs(freqs_hz - expected) <= tolerance_hz
        if np.any(mask):
            score += np.max(magnitude[mask]) / n
    return score


def detect_pitches(signal: np.ndarray, sample_rate: float, n_notes: int = 2, fmin: float = 80.0,
                    fmax: float = 1000.0, resolution_hz: float = 2.0, max_harmonics: int = 10,
                    min_separation_hz: float = 20.0, fft_size: int = 16384) -> dict:
    """N-note polyphonic pitch estimate via iterative harmonic-sieve scoring
    and spectral peeling (Section 18.3): find the strongest candidate
    fundamental, zero out its harmonics from a residual spectrum, then
    repeat against the residual for each remaining note. Confidence is
    scored against the *original* spectrum's total energy, since the
    residual shrinks with each peel and isn't a fair common denominator.
    """
    if n_notes < 1:
        raise ValueError("n_notes must be at least 1")

    spectrum = fft_analyzer.compute_spectrum(signal, sample_rate, window="hann", fft_size=fft_size)
    tolerance_hz = max(spectrum.bin_spacing_hz * 2, 3.0)
    total_energy = float(np.sum(spectrum.magnitude))

    candidate_f0s = np.arange(fmin, fmax, resolution_hz)
    residual_magnitude = spectrum.magnitude.copy()

    found_freqs: list[float] = []
    found_scores: list[float] = []

    for _ in range(n_notes):
        scores = np.array([
            _harmonic_sieve_score(spectrum.freqs_hz, residual_magnitude, f0, max_harmonics, tolerance_hz)
            if all(abs(f0 - f) >= min_separation_hz for f in found_freqs) else -np.inf
            for f0 in candidate_f0s
        ])

        best_index = int(np.argmax(scores))
        f0 = float(candidate_f0s[best_index])
        score = float(scores[best_index])
        found_freqs.append(f0)
        found_scores.append(score)

        for n in range(1, max_harmonics + 1):
            expected = n * f0
            mask = np.abs(spectrum.freqs_hz - expected) <= tolerance_hz
            residual_magnitude[mask] = 0.0

    confidences = [float(np.clip(s / (total_energy + 1e-9), 0.0, 1.0)) for s in found_scores]

    return {
        "fundamentals_hz": found_freqs,
        "confidences": confidences,
        "scores": found_scores,
    }


def detect_two_pitches(signal: np.ndarray, sample_rate: float, fmin: float = 80.0,
                        fmax: float = 1000.0, resolution_hz: float = 2.0,
                        max_harmonics: int = 10, min_separation_hz: float = 20.0,
                        fft_size: int = 16384) -> dict:
    """Two-note case of detect_pitches, kept as a named entry point since
    Section 18.3 introduces two-note detection before generalizing further."""
    return detect_pitches(signal, sample_rate, n_notes=2, fmin=fmin, fmax=fmax,
                           resolution_hz=resolution_hz, max_harmonics=max_harmonics,
                           min_separation_hz=min_separation_hz, fft_size=fft_size)


def build_chord_event(fundamentals_hz: list[float], confidences: list[float],
                       reference_a4_hz: float = 440.0, nyquist_hz: float | None = None) -> ChordEvent:
    notes = [pitch_module.frequency_to_note(f, reference_a4_hz)["note_name"] for f in fundamentals_hz]

    pairwise_intervals = []
    shared = []
    beats = []
    intermod = []
    ratios = []

    for i in range(len(fundamentals_hz)):
        for j in range(i + 1, len(fundamentals_hz)):
            f1, f2 = fundamentals_hz[i], fundamentals_hz[j]
            pairwise_intervals.append({"pair": [i, j], "cents": cents_interval(f1, f2)})
            ratios.append({"pair": [i, j], "ratio": interval_ratio(f1, f2)})
            shared.extend(shared_harmonics(f1, f2))
            beats.append({"pair": [i, j], "beat_frequency_hz": beat_frequency(f1, f2)})
            intermod.extend(intermodulation_candidates(f1, f2, nyquist_hz=nyquist_hz))

    return ChordEvent(
        detected_fundamentals=fundamentals_hz,
        candidate_notes=notes,
        confidence_per_note=confidences,
        frequency_ratios=ratios,
        pairwise_intervals=pairwise_intervals,
        shared_harmonics=shared,
        beat_components=beats,
        intermodulation_candidates=intermod,
    )
