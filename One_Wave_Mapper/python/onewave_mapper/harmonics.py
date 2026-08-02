"""Harmonic tracking against a detected fundamental (Section 12).

Spectral peaks are not assumed to be harmonics automatically -- each
candidate is classified and only accepted within a frequency tolerance of
n * f0.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from onewave_mapper.fft_analyzer import Spectrum


@dataclass
class HarmonicTrack:
    harmonic_number: int
    expected_frequency_hz: float
    measured_frequency_hz: float | None
    amplitude: float | None
    phase_rad: float | None
    deviation_cents: float | None
    confidence: float

    def to_dict(self) -> dict:
        return asdict(self)


def track_harmonics(spectrum: Spectrum, fundamental_hz: float, max_harmonics: int = 32,
                     search_fraction: float = 0.06) -> list[HarmonicTrack]:
    """search_fraction: fractional window around n*f0 to search for a peak (in units of f0)."""
    tracks = []
    nyquist = spectrum.sample_rate / 2.0

    for n in range(1, max_harmonics + 1):
        expected = n * fundamental_hz
        if expected >= nyquist:
            break

        search_width = max(spectrum.bin_spacing_hz * 2, fundamental_hz * search_fraction)
        mask = (spectrum.freqs_hz >= expected - search_width) & \
               (spectrum.freqs_hz <= expected + search_width)

        if not np.any(mask):
            tracks.append(HarmonicTrack(n, expected, None, None, None, None, 0.0))
            continue

        indices = np.where(mask)[0]
        best = indices[np.argmax(spectrum.magnitude[indices])]
        measured_freq = float(spectrum.freqs_hz[best])
        amplitude = float(spectrum.magnitude[best])
        phase = float(spectrum.phase_rad[best])

        deviation_cents = float(1200 * np.log2(measured_freq / expected)) if expected > 0 else None

        neighborhood = spectrum.magnitude[max(0, best - 5): best + 6]
        prominence = amplitude / (np.median(neighborhood) + 1e-12)
        confidence = float(max(0.0, min(1.0, (prominence - 1) / 10)))

        tracks.append(HarmonicTrack(
            harmonic_number=n,
            expected_frequency_hz=expected,
            measured_frequency_hz=measured_freq,
            amplitude=amplitude,
            phase_rad=phase,
            deviation_cents=deviation_cents,
            confidence=confidence,
        ))

    return tracks


def classify_peak(frequency_hz: float, fundamental_hz: float, tolerance_cents: float = 50.0) -> str:
    """Classify a spectral peak relative to a known fundamental (Section 12)."""
    if fundamental_hz <= 0 or frequency_hz <= 0:
        return "unknown"

    ratio = frequency_hz / fundamental_hz

    if ratio >= 1.0:
        nearest_harmonic = max(1, round(ratio))
        deviation_cents = abs(1200 * np.log2(ratio / nearest_harmonic))
        if deviation_cents <= tolerance_cents:
            return "fundamental" if nearest_harmonic == 1 else "harmonic"
        return "unknown"

    inverse_ratio = 1.0 / ratio
    nearest_subharmonic = max(1, round(inverse_ratio))
    deviation_cents = abs(1200 * np.log2(inverse_ratio / nearest_subharmonic))
    if deviation_cents <= tolerance_cents:
        return "subharmonic"
    return "unknown"


def total_harmonic_distortion(tracks: list[HarmonicTrack]) -> float | None:
    if not tracks or tracks[0].amplitude is None:
        return None
    fundamental_amplitude = tracks[0].amplitude
    if fundamental_amplitude <= 1e-12:
        return None
    harmonic_energy = sum(
        (t.amplitude or 0.0) ** 2 for t in tracks[1:] if t.amplitude is not None
    )
    return float(np.sqrt(harmonic_energy) / fundamental_amplitude)


def odd_even_harmonic_ratio(tracks: list[HarmonicTrack]) -> float | None:
    odd_energy = sum((t.amplitude or 0.0) ** 2 for t in tracks if t.harmonic_number % 2 == 1)
    even_energy = sum((t.amplitude or 0.0) ** 2 for t in tracks if t.harmonic_number % 2 == 0 and t.harmonic_number > 0)
    if even_energy <= 1e-20:
        return None
    return float(odd_energy / even_energy)
