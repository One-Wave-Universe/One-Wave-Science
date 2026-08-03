"""Single shared source of truth for the whole mapper window (Section 20:
"one transport control, one timeline, one selection, one zoom location,
one playhead, one trigger point, one set of timestamped markers").

Every panel reads from an AnalysisState instance and reacts to its Qt
signals instead of keeping its own copy of cursor/selection/zoom/trigger/
mode -- that's what keeps every view locked together. The raw recording
held here is the untouched, timestamped signal (Section 2.1); panels may
derive views from it but must never write back into `raw_signal`.
"""

from __future__ import annotations

from enum import Enum

import numpy as np
from PySide6 import QtCore


class ViewMode(Enum):
    RAW = "raw"
    ONE_WAVE = "one_wave"
    BOTH = "both"


class TransportMode(Enum):
    FREE_RUN = "free_run"
    TRIGGERED = "triggered"
    PAUSED = "paused"
    REPLAY = "replay"
    LOOP = "loop"


class AnalysisState(QtCore.QObject):
    recording_changed = QtCore.Signal()
    cursor_changed = QtCore.Signal(int)
    selection_changed = QtCore.Signal(object)          # (start_sample, end_sample) or None
    view_range_changed = QtCore.Signal(int, int)
    playhead_changed = QtCore.Signal(int)
    trigger_point_changed = QtCore.Signal(object)       # sample index or None
    mode_changed = QtCore.Signal(str)
    transport_mode_changed = QtCore.Signal(str)
    highlighted_harmonic_changed = QtCore.Signal(object)  # harmonic number or None
    markers_changed = QtCore.Signal()
    cycle_visibility_changed = QtCore.Signal(str, bool)  # "point" | "path" | "field", visible

    def __init__(self, sample_rate: int, parent=None):
        super().__init__(parent)
        self.sample_rate = sample_rate

        self._raw_signal = np.zeros(0, dtype=np.float32)
        self.cursor_sample = 0
        self.selection: tuple[int, int] | None = None
        self.view_start_sample = 0
        self.view_end_sample = 0
        self.playhead_sample = 0
        self.trigger_sample: int | None = None
        self.mode = ViewMode.BOTH
        self.transport_mode = TransportMode.FREE_RUN
        self.highlighted_harmonic: int | None = None
        self.markers: list[dict] = []

        # nested Point/Path/Field motion visibility (Section 16.3) -- each
        # level independently toggleable, so a fast oscillation nested
        # inside a repeating path nested inside a slower field envelope
        # can each be shown or hidden on their own.
        self.show_point_rotation = True
        self.show_path_rotation = True
        self.show_field_rotation = True

    # -- raw recording (Section 2.1) --------------------------------------

    @property
    def raw_signal(self) -> np.ndarray:
        """The preserved, untouched recording. Callers must not mutate this
        in place -- copy it first if you need a derived/filtered version."""
        return self._raw_signal

    def set_recording(self, signal: np.ndarray, sample_rate: int | None = None) -> None:
        self._raw_signal = signal
        if sample_rate is not None:
            self.sample_rate = sample_rate
        self.view_start_sample = 0
        self.view_end_sample = max(1, len(signal))
        self.recording_changed.emit()

    def append_to_recording(self, block: np.ndarray) -> None:
        self._raw_signal = np.concatenate([self._raw_signal, block]) if self._raw_signal.size else block.copy()
        self.recording_changed.emit()

    # -- cursor / selection / zoom -----------------------------------------

    def set_cursor(self, sample_index: int) -> None:
        n = len(self._raw_signal)
        self.cursor_sample = int(np.clip(sample_index, 0, max(0, n - 1)))
        self.cursor_changed.emit(self.cursor_sample)

    def set_selection(self, start_sample: int | None, end_sample: int | None) -> None:
        if start_sample is None or end_sample is None:
            self.selection = None
        else:
            self.selection = (int(min(start_sample, end_sample)), int(max(start_sample, end_sample)))
        self.selection_changed.emit(self.selection)

    def set_view_range(self, start_sample: int, end_sample: int) -> None:
        n = len(self._raw_signal)
        start_sample = int(np.clip(start_sample, 0, max(n, 1)))
        end_sample = int(np.clip(end_sample, start_sample + 1, max(n, start_sample + 1)))
        self.view_start_sample, self.view_end_sample = start_sample, end_sample
        self.view_range_changed.emit(start_sample, end_sample)

    def zoom_to_full_capture(self) -> None:
        self.set_view_range(0, max(1, len(self._raw_signal)))

    def zoom_to_samples(self, center_sample: int, n_samples: int) -> None:
        half = max(1, n_samples // 2)
        self.set_view_range(center_sample - half, center_sample + half)

    def zoom_to_note(self, center_sample: int, note_duration_seconds: float = 1.0) -> None:
        self.zoom_to_samples(center_sample, int(note_duration_seconds * self.sample_rate))

    def pan(self, delta_samples: int) -> None:
        width = self.view_end_sample - self.view_start_sample
        self.set_view_range(self.view_start_sample + delta_samples, self.view_start_sample + delta_samples + width)

    # -- playback / trigger --------------------------------------------------

    def set_playhead(self, sample_index: int) -> None:
        self.playhead_sample = int(sample_index)
        self.playhead_changed.emit(self.playhead_sample)

    def set_trigger_point(self, sample_index: int | None) -> None:
        self.trigger_sample = sample_index
        self.trigger_point_changed.emit(sample_index)

    def set_mode(self, mode: ViewMode) -> None:
        self.mode = mode
        self.mode_changed.emit(mode.value)

    def set_transport_mode(self, mode: TransportMode) -> None:
        self.transport_mode = mode
        self.transport_mode_changed.emit(mode.value)

    # -- cross-panel linking ------------------------------------------------

    def set_highlighted_harmonic(self, harmonic_number: int | None) -> None:
        self.highlighted_harmonic = harmonic_number
        self.highlighted_harmonic_changed.emit(harmonic_number)

    def add_marker(self, sample_index: int, label: str) -> dict:
        marker = {"sample": sample_index, "label": label, "time_seconds": sample_index / self.sample_rate}
        self.markers.append(marker)
        self.markers_changed.emit()
        return marker

    def clear_markers(self) -> None:
        self.markers = []
        self.markers_changed.emit()

    # -- nested Point/Path/Field visibility (Section 16.3) ------------------

    def set_point_rotation_visible(self, visible: bool) -> None:
        self.show_point_rotation = visible
        self.cycle_visibility_changed.emit("point", visible)

    def set_path_rotation_visible(self, visible: bool) -> None:
        self.show_path_rotation = visible
        self.cycle_visibility_changed.emit("path", visible)

    def set_field_rotation_visible(self, visible: bool) -> None:
        self.show_field_rotation = visible
        self.cycle_visibility_changed.emit("field", visible)
