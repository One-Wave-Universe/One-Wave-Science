"""Spectrogram engine (Section 9).

Renders an STFT magnitude surface with adjustable FFT size, hop size, and
window (Section 9.1), plus linear/log/note-oriented frequency axis
mappings and fundamental/harmonic track overlays (Section 9.3) built on
top of the same pitch/harmonic modules used for single-frame analysis, so
the spectrogram and the spectrum/pitch panels stay numerically consistent
(Section 2.2 -- synchronized views).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from onewave_mapper.fft_analyzer import WINDOW_FUNCTIONS, bin_spacing, Spectrum
from onewave_mapper import pitch as pitch_module
from onewave_mapper import harmonics as harmonics_module


@dataclass
class Spectrogram:
    times_seconds: np.ndarray       # shape (n_frames,) -- center time of each frame
    freqs_hz: np.ndarray             # shape (n_freq_bins,)
    magnitude: np.ndarray            # shape (n_freq_bins, n_frames), linear
    magnitude_db: np.ndarray         # shape (n_freq_bins, n_frames)
    phase_rad: np.ndarray            # shape (n_freq_bins, n_frames)
    fft_size: int
    hop_size: int
    sample_rate: float

    def frame_spectrum(self, frame_index: int) -> Spectrum:
        """Reconstruct a single-frame Spectrum, so pitch.py/harmonics.py can
        run on one spectrogram column exactly as they would on a live FFT."""
        return Spectrum(
            freqs_hz=self.freqs_hz,
            magnitude=self.magnitude[:, frame_index],
            magnitude_db=self.magnitude_db[:, frame_index],
            phase_rad=self.phase_rad[:, frame_index],
            fft_size=self.fft_size,
            sample_rate=self.sample_rate,
            bin_spacing_hz=bin_spacing(self.sample_rate, self.fft_size),
        )


def compute_spectrogram(signal: np.ndarray, sample_rate: float, fft_size: int = 2048,
                         hop_size: int = 512, window: str = "hann") -> Spectrogram:
    if window not in WINDOW_FUNCTIONS:
        raise ValueError(f"unknown window function: {window}")
    if hop_size <= 0 or fft_size <= 0:
        raise ValueError("fft_size and hop_size must be positive")

    win = WINDOW_FUNCTIONS[window](fft_size)
    coherent_gain = np.sum(win) / fft_size

    n = len(signal)
    n_frames = max(0, 1 + (n - fft_size) // hop_size) if n >= fft_size else 0
    n_freq_bins = fft_size // 2 + 1
    freqs = np.fft.rfftfreq(fft_size, d=1.0 / sample_rate)

    magnitude = np.zeros((n_freq_bins, max(n_frames, 0)))
    phase = np.zeros((n_freq_bins, max(n_frames, 0)))
    times = np.zeros(max(n_frames, 0))

    for frame_index in range(n_frames):
        start = frame_index * hop_size
        frame = signal[start: start + fft_size] * win
        spectrum = np.fft.rfft(frame)

        frame_magnitude = np.abs(spectrum) / (fft_size * coherent_gain + 1e-30)
        frame_magnitude[1:] *= 2.0

        magnitude[:, frame_index] = frame_magnitude
        phase[:, frame_index] = np.angle(spectrum)
        times[frame_index] = (start + fft_size / 2) / sample_rate

    magnitude_db = 20 * np.log10(np.maximum(magnitude, 1e-12))

    return Spectrogram(
        times_seconds=times,
        freqs_hz=freqs,
        magnitude=magnitude,
        magnitude_db=magnitude_db,
        phase_rad=phase,
        fft_size=fft_size,
        hop_size=hop_size,
        sample_rate=sample_rate,
    )


def frequency_axis(freqs_hz: np.ndarray, scale: str = "linear",
                    reference_a4_hz: float = 440.0) -> np.ndarray:
    """Transform a frequency axis for display (Section 9.1: linear/log/note)."""
    if scale == "linear":
        return freqs_hz
    if scale == "log":
        safe = np.maximum(freqs_hz, 1e-6)
        return np.log10(safe)
    if scale == "note":
        safe = np.maximum(freqs_hz, 1e-6)
        return 69 + 12 * np.log2(safe / reference_a4_hz)
    raise ValueError(f"unknown frequency axis scale: {scale}")


def fundamental_track(signal: np.ndarray, sample_rate: float, frame_size: int = 2048,
                       hop_size: int = 512, fmin: float = 60.0, fmax: float = 1500.0,
                       min_confidence: float = 0.5) -> dict:
    """Per-frame fundamental estimate over time, for spectrogram overlay (Section 9.3)."""
    n = len(signal)
    n_frames = max(0, 1 + (n - frame_size) // hop_size) if n >= frame_size else 0

    times = np.zeros(n_frames)
    freqs = np.full(n_frames, np.nan)
    confidences = np.zeros(n_frames)

    for frame_index in range(n_frames):
        start = frame_index * hop_size
        frame = signal[start: start + frame_size]
        result = pitch_module.detect_pitch(frame, sample_rate, fmin=fmin, fmax=fmax,
                                            min_confidence=min_confidence)
        times[frame_index] = (start + frame_size / 2) / sample_rate
        confidences[frame_index] = result.confidence
        if result.frequency_hz is not None:
            freqs[frame_index] = result.frequency_hz

    return {"times_seconds": times, "frequency_hz": freqs, "confidence": confidences}


def harmonic_track_overlay(spectrogram: Spectrogram, fundamental_freqs_hz: np.ndarray,
                            max_harmonics: int = 8) -> list[list]:
    """Per-frame harmonic tracks (Section 9.3), one HarmonicTrack list per frame
    with a valid (non-NaN) fundamental estimate; frames without one are []."""
    n_frames = spectrogram.magnitude.shape[1]
    if len(fundamental_freqs_hz) != n_frames:
        raise ValueError("fundamental_freqs_hz must have one entry per spectrogram frame")

    tracks_by_frame = []
    for frame_index in range(n_frames):
        f0 = fundamental_freqs_hz[frame_index]
        if np.isnan(f0) or f0 <= 0:
            tracks_by_frame.append([])
            continue
        frame_spectrum = spectrogram.frame_spectrum(frame_index)
        tracks_by_frame.append(harmonics_module.track_harmonics(frame_spectrum, f0, max_harmonics))

    return tracks_by_frame
