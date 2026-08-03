"""Cursor readout: time/amplitude/frequency/phase/note at one sample
index, computed from a local window around it. Pure functions (no Qt),
so panels can share identical readout logic and it's directly testable.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np
from scipy.signal import hilbert

from onewave_mapper import pitch as pitch_module


@dataclass
class CursorReadout:
    sample_index: int
    time_seconds: float
    amplitude: float
    frequency_hz: float | None
    note_name: str | None
    cents_offset: float | None
    phase_rad: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def measure_at_cursor(raw_signal: np.ndarray, sample_rate: float, cursor_sample: int,
                       window_samples: int = 2048, fmin: float = 60.0, fmax: float = 1500.0) -> CursorReadout:
    n = len(raw_signal)
    if n == 0:
        return CursorReadout(sample_index=0, time_seconds=0.0, amplitude=0.0, frequency_hz=None,
                              note_name=None, cents_offset=None, phase_rad=None)

    cursor_sample = int(np.clip(cursor_sample, 0, n - 1))
    amplitude = float(raw_signal[cursor_sample])
    time_seconds = cursor_sample / sample_rate

    half = window_samples // 2
    start = max(0, cursor_sample - half)
    end = min(n, cursor_sample + half)
    window = raw_signal[start:end]

    frequency_hz = None
    note_name = None
    cents_offset = None
    phase_rad = None

    if len(window) >= 64:
        pitch_result = pitch_module.detect_pitch(window, sample_rate, fmin=fmin, fmax=fmax)
        if pitch_result.frequency_hz is not None:
            frequency_hz = pitch_result.frequency_hz
            note_info = pitch_module.frequency_to_note(frequency_hz)
            note_name = note_info["note_name"]
            cents_offset = note_info["cents_offset"]

        analytic = hilbert(window)
        local_index = cursor_sample - start
        local_index = int(np.clip(local_index, 0, len(analytic) - 1))
        phase_rad = float(np.angle(analytic[local_index]))

    return CursorReadout(
        sample_index=cursor_sample,
        time_seconds=time_seconds,
        amplitude=amplitude,
        frequency_hz=frequency_hz,
        note_name=note_name,
        cents_offset=cents_offset,
        phase_rad=phase_rad,
    )
