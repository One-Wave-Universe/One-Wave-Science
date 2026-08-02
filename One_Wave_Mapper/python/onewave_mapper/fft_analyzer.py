"""FFT spectrum analyzer (Section 8)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.signal import windows as sp_windows

WINDOW_FUNCTIONS = {
    "rectangular": lambda n: np.ones(n),
    "hann": sp_windows.hann,
    "hamming": sp_windows.hamming,
    "blackman": sp_windows.blackman,
    "blackman_harris": sp_windows.blackmanharris,
    "flat_top": sp_windows.flattop,
    "kaiser": lambda n: sp_windows.kaiser(n, beta=8.6),
}


def bin_spacing(sample_rate: float, fft_size: int) -> float:
    """Δf = fs / N (Section 8.1)."""
    return sample_rate / fft_size


@dataclass
class Spectrum:
    freqs_hz: np.ndarray
    magnitude: np.ndarray
    magnitude_db: np.ndarray
    phase_rad: np.ndarray
    fft_size: int
    sample_rate: float
    bin_spacing_hz: float


def compute_spectrum(signal: np.ndarray, sample_rate: float, window: str = "hann",
                      fft_size: int | None = None) -> Spectrum:
    if window not in WINDOW_FUNCTIONS:
        raise ValueError(f"unknown window function: {window}")

    n = fft_size or len(signal)
    if len(signal) < n:
        padded = np.zeros(n)
        padded[: len(signal)] = signal
        signal = padded
    else:
        signal = signal[:n]

    win = WINDOW_FUNCTIONS[window](n)
    windowed = signal * win
    coherent_gain = np.sum(win) / n

    spectrum = np.fft.rfft(windowed)
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)

    magnitude = np.abs(spectrum) / (n * coherent_gain + 1e-30)
    magnitude[1:] *= 2.0
    magnitude_db = 20 * np.log10(np.maximum(magnitude, 1e-12))
    phase = np.angle(spectrum)

    return Spectrum(
        freqs_hz=freqs,
        magnitude=magnitude,
        magnitude_db=magnitude_db,
        phase_rad=phase,
        fft_size=n,
        sample_rate=sample_rate,
        bin_spacing_hz=bin_spacing(sample_rate, n),
    )


def strongest_peak(spectrum: Spectrum, min_freq_hz: float = 0.0,
                    max_freq_hz: float | None = None) -> tuple[float, float]:
    """Returns (frequency_hz, magnitude) of the strongest bin in range, with
    parabolic interpolation across the peak's three bins for sub-bin accuracy."""
    max_freq_hz = max_freq_hz if max_freq_hz is not None else spectrum.freqs_hz[-1]
    mask = (spectrum.freqs_hz >= min_freq_hz) & (spectrum.freqs_hz <= max_freq_hz)
    if not np.any(mask):
        raise ValueError("no bins in requested frequency range")

    indices = np.where(mask)[0]
    local_peak = indices[np.argmax(spectrum.magnitude[indices])]

    if 0 < local_peak < len(spectrum.magnitude) - 1:
        alpha = spectrum.magnitude[local_peak - 1]
        beta = spectrum.magnitude[local_peak]
        gamma = spectrum.magnitude[local_peak + 1]
        denom = alpha - 2 * beta + gamma
        p = 0.5 * (alpha - gamma) / denom if abs(denom) > 1e-15 else 0.0
        freq = spectrum.freqs_hz[local_peak] + p * spectrum.bin_spacing_hz
        mag = beta - 0.25 * (alpha - gamma) * p
    else:
        freq = spectrum.freqs_hz[local_peak]
        mag = spectrum.magnitude[local_peak]

    return float(freq), float(mag)


def spectral_centroid(spectrum: Spectrum) -> float:
    weights = spectrum.magnitude
    total = np.sum(weights)
    if total <= 1e-20:
        return 0.0
    return float(np.sum(spectrum.freqs_hz * weights) / total)


def spectral_bandwidth(spectrum: Spectrum) -> float:
    centroid = spectral_centroid(spectrum)
    weights = spectrum.magnitude
    total = np.sum(weights)
    if total <= 1e-20:
        return 0.0
    variance = np.sum(weights * (spectrum.freqs_hz - centroid) ** 2) / total
    return float(np.sqrt(variance))


def spectral_rolloff(spectrum: Spectrum, rolloff_fraction: float = 0.85) -> float:
    energy = spectrum.magnitude ** 2
    cumulative = np.cumsum(energy)
    total = cumulative[-1]
    if total <= 1e-20:
        return 0.0
    threshold_index = np.searchsorted(cumulative, rolloff_fraction * total)
    threshold_index = min(threshold_index, len(spectrum.freqs_hz) - 1)
    return float(spectrum.freqs_hz[threshold_index])


def spectral_flatness(spectrum: Spectrum) -> float:
    magnitude = np.maximum(spectrum.magnitude, 1e-12)
    geometric_mean = np.exp(np.mean(np.log(magnitude)))
    arithmetic_mean = np.mean(magnitude)
    return float(geometric_mean / arithmetic_mean) if arithmetic_mean > 1e-20 else 0.0


def spectral_slope(spectrum: Spectrum) -> float:
    magnitude_db = spectrum.magnitude_db
    freqs = spectrum.freqs_hz
    mask = freqs > 0
    if np.sum(mask) < 2:
        return 0.0
    slope, _ = np.polyfit(freqs[mask], magnitude_db[mask], 1)
    return float(slope)
