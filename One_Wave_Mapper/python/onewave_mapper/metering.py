"""Objective scope measurements over a signal region (Section 6.6).

These are pure measurements only -- no One-Wave interpretation is attached
here, per Section 2.3.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np


@dataclass
class ScopeMeasurements:
    minimum: float
    maximum: float
    peak: float
    peak_to_peak: float
    rms: float
    mean: float
    dc_offset: float
    crest_factor: float
    zero_crossing_rate_hz: float
    positive_peak: float
    negative_peak: float
    asymmetry: float
    clipping_count: int
    clipped_percentage: float
    estimated_snr_db: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def measure(signal: np.ndarray, sample_rate: float, clip_ceiling: float = 0.999) -> ScopeMeasurements:
    if signal.size == 0:
        raise ValueError("cannot measure an empty signal")

    minimum = float(np.min(signal))
    maximum = float(np.max(signal))
    positive_peak = maximum
    negative_peak = minimum
    peak = float(np.max(np.abs(signal)))
    peak_to_peak = maximum - minimum
    rms = float(np.sqrt(np.mean(np.square(signal))))
    mean = float(np.mean(signal))
    dc_offset = mean
    crest_factor = float(peak / rms) if rms > 1e-12 else float("inf")

    zero_crossings = np.sum(np.diff(np.signbit(signal)))
    duration_seconds = len(signal) / sample_rate
    zero_crossing_rate_hz = float(zero_crossings / (2 * duration_seconds)) if duration_seconds > 0 else 0.0

    asymmetry = float((positive_peak + negative_peak) / (peak_to_peak + 1e-12))

    clipped_mask = np.abs(signal) >= clip_ceiling
    clipping_count = int(np.sum(clipped_mask))
    clipped_percentage = float(100.0 * clipping_count / len(signal))

    estimated_snr_db = estimate_snr_db(signal)

    return ScopeMeasurements(
        minimum=minimum,
        maximum=maximum,
        peak=peak,
        peak_to_peak=peak_to_peak,
        rms=rms,
        mean=mean,
        dc_offset=dc_offset,
        crest_factor=crest_factor,
        zero_crossing_rate_hz=zero_crossing_rate_hz,
        positive_peak=positive_peak,
        negative_peak=negative_peak,
        asymmetry=asymmetry,
        clipping_count=clipping_count,
        clipped_percentage=clipped_percentage,
        estimated_snr_db=estimated_snr_db,
    )


def estimate_snr_db(signal: np.ndarray, noise_floor_percentile: float = 5.0) -> float | None:
    """Rough SNR estimate: total power vs. power of the quietest frames.

    This is a coarse estimator suitable for a live meter readout, not a
    substitute for a calibrated noise-floor measurement.
    """
    frame_size = max(64, len(signal) // 100)
    if frame_size >= len(signal):
        return None
    n_frames = len(signal) // frame_size
    if n_frames < 2:
        return None
    frames = signal[: n_frames * frame_size].reshape(n_frames, frame_size)
    frame_power = np.mean(np.square(frames), axis=1)
    noise_power = np.percentile(frame_power, noise_floor_percentile)
    total_power = np.mean(frame_power)
    if noise_power <= 1e-20:
        return None
    return float(10 * np.log10(total_power / noise_power))


def rise_fall_time(signal: np.ndarray, sample_rate: float, low_fraction: float = 0.1,
                    high_fraction: float = 0.9) -> dict:
    """Rise time from low_fraction to high_fraction of the transition, and matching fall time."""
    peak = np.max(np.abs(signal))
    low = low_fraction * peak
    high = high_fraction * peak

    above_low = np.where(signal >= low)[0]
    above_high = np.where(signal >= high)[0]
    rise_time_seconds = None
    if above_low.size and above_high.size:
        first_low = above_low[0]
        first_high = above_high[above_high >= first_low]
        if first_high.size:
            rise_time_seconds = float((first_high[0] - first_low) / sample_rate)

    below_low_after_peak = np.where(signal <= low)[0]
    below_high_after_peak = np.where(signal <= high)[0]
    fall_time_seconds = None
    if below_low_after_peak.size and below_high_after_peak.size:
        peak_index = int(np.argmax(signal))
        after_peak_high = below_high_after_peak[below_high_after_peak >= peak_index]
        after_peak_low = below_low_after_peak[below_low_after_peak >= peak_index]
        if after_peak_high.size and after_peak_low.size:
            first_high = after_peak_high[0]
            first_low = after_peak_low[after_peak_low >= first_high]
            if first_low.size:
                fall_time_seconds = float((first_low[0] - first_high) / sample_rate)

    return {"rise_time_seconds": rise_time_seconds, "fall_time_seconds": fall_time_seconds}
