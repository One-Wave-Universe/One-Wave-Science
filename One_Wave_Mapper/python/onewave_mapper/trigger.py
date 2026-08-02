"""Oscilloscope trigger engine (Section 6.2 / 6.3).

Triggering must never alter the saved source signal (Section 6.3) -- this
module only reads the signal and returns trigger sample indices; it never
mutates its input.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np


class TriggerEdge(Enum):
    RISING = "rising"
    FALLING = "falling"
    EITHER = "either"


class TriggerType(Enum):
    LEVEL = "level"
    ZERO_CROSSING = "zero_crossing"
    WINDOW = "window"
    NOTE_ONSET = "note_onset"


@dataclass
class TriggerConfig:
    trigger_type: TriggerType = TriggerType.LEVEL
    edge: TriggerEdge = TriggerEdge.RISING
    threshold: float = 0.0
    hysteresis: float = 0.02
    holdoff_samples: int = 0
    window_low: float = -0.1
    window_high: float = 0.1
    onset_energy_ratio: float = 3.0


class TriggerEngine:
    def __init__(self, config: TriggerConfig):
        self.config = config

    def find_triggers(self, signal: np.ndarray, sample_rate: float) -> np.ndarray:
        cfg = self.config
        if cfg.trigger_type == TriggerType.ZERO_CROSSING:
            indices = self._find_level_crossings(signal, 0.0, cfg.edge, cfg.hysteresis)
        elif cfg.trigger_type == TriggerType.LEVEL:
            indices = self._find_level_crossings(signal, cfg.threshold, cfg.edge, cfg.hysteresis)
        elif cfg.trigger_type == TriggerType.WINDOW:
            indices = self._find_window_entries(signal, cfg.window_low, cfg.window_high)
        elif cfg.trigger_type == TriggerType.NOTE_ONSET:
            indices = self._find_note_onsets(signal, sample_rate, cfg.onset_energy_ratio)
        else:
            raise ValueError(f"unsupported trigger type: {cfg.trigger_type}")

        return self._apply_holdoff(indices, cfg.holdoff_samples)

    def _find_level_crossings(self, signal: np.ndarray, threshold: float,
                               edge: TriggerEdge, hysteresis: float) -> np.ndarray:
        armed_high = threshold + hysteresis
        armed_low = threshold - hysteresis

        indices = []
        state = "unarmed"
        for i in range(1, len(signal)):
            prev, curr = signal[i - 1], signal[i]

            if edge in (TriggerEdge.RISING, TriggerEdge.EITHER):
                if state != "armed_rising" and prev < armed_low:
                    state = "armed_rising"
                if state == "armed_rising" and prev < threshold <= curr:
                    frac = (threshold - prev) / (curr - prev) if curr != prev else 0.0
                    indices.append(i - 1 + frac)
                    state = "unarmed"

            if edge in (TriggerEdge.FALLING, TriggerEdge.EITHER):
                if state != "armed_falling" and prev > armed_high:
                    state = "armed_falling"
                if state == "armed_falling" and prev > threshold >= curr:
                    frac = (prev - threshold) / (prev - curr) if curr != prev else 0.0
                    indices.append(i - 1 + frac)
                    state = "unarmed"

        return np.array(sorted(indices))

    def _find_window_entries(self, signal: np.ndarray, low: float, high: float) -> np.ndarray:
        inside = (signal >= low) & (signal <= high)
        entries = np.where(np.diff(inside.astype(int)) == 1)[0] + 1
        return entries.astype(float)

    def _find_note_onsets(self, signal: np.ndarray, sample_rate: float,
                           energy_ratio: float, frame_ms: float = 5.0) -> np.ndarray:
        frame_size = max(8, int(sample_rate * frame_ms / 1000.0))
        n_frames = len(signal) // frame_size
        if n_frames < 2:
            return np.array([])
        frames = signal[: n_frames * frame_size].reshape(n_frames, frame_size)
        frame_energy = np.mean(np.square(frames), axis=1)

        onsets = []
        floor = np.median(frame_energy) + 1e-12
        for i in range(1, n_frames):
            if frame_energy[i] > energy_ratio * max(frame_energy[i - 1], floor):
                onsets.append(i * frame_size)
        return np.array(onsets, dtype=float)

    def _apply_holdoff(self, indices: np.ndarray, holdoff_samples: int) -> np.ndarray:
        if indices.size == 0 or holdoff_samples <= 0:
            return indices
        kept = [indices[0]]
        for idx in indices[1:]:
            if idx - kept[-1] >= holdoff_samples:
                kept.append(idx)
        return np.array(kept)

    def capture_frame(self, signal: np.ndarray, trigger_index: float,
                       pre_samples: int, post_samples: int) -> tuple[np.ndarray, int]:
        """Extract a pre/post-trigger frame. Returns (frame, start_index_used).

        The trigger index may be fractional (sub-sample interpolated); the
        frame is taken around the nearest integer sample.
        """
        center = int(round(trigger_index))
        start = max(0, center - pre_samples)
        end = min(len(signal), center + post_samples)
        return signal[start:end].copy(), start
