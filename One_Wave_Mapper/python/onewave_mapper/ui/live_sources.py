"""Live signal sources feeding the RingBuffer the oscilloscope UI reads
from.

SyntheticSource and HardwareSource expose the same start()/stop()/
ring_buffer interface, so OscilloscopeWindow doesn't care which one it's
driven by. HardwareSource wraps device_manager.CaptureEngine and needs
real audio hardware, which this sandboxed environment does not have --
SyntheticSource (a QTimer standing in for the audio callback, pushing the
same kind of (channels, n) blocks into the same RingBuffer.write() a real
callback would) is what the automated GUI tests actually exercise.
"""

from __future__ import annotations

import numpy as np
from PySide6 import QtCore

from onewave_mapper.ring_buffer import RingBuffer
from onewave_mapper import signal_generator


class SyntheticSource(QtCore.QObject):
    def __init__(self, ring_buffer: RingBuffer, sample_rate: int, block_size: int = 512,
                 waveform: str = "guitar_note", parent=None):
        super().__init__(parent)
        self.ring_buffer = ring_buffer
        self.sample_rate = sample_rate
        self.block_size = block_size
        self.waveform = waveform

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._push_block)
        self._phase_sample = 0
        self._note_signal: np.ndarray | None = None
        self._note_position = 0

    def start(self) -> None:
        if self.waveform == "guitar_note":
            self._note_signal = signal_generator.guitar_note(220.0, 2.0, self.sample_rate)
            self._note_position = 0
        elif self.waveform != "sine":
            raise ValueError(f"unknown synthetic waveform: {self.waveform}")
        interval_ms = max(1, int(1000 * self.block_size / self.sample_rate))
        self._timer.start(interval_ms)

    def stop(self) -> None:
        self._timer.stop()

    def _push_block(self) -> None:
        if self.waveform == "sine":
            t = (np.arange(self.block_size) + self._phase_sample) / self.sample_rate
            block = 0.8 * np.sin(2 * np.pi * 220.0 * t)
            self._phase_sample += self.block_size
        else:
            block = self._next_note_block()

        self.ring_buffer.write(block.reshape(1, -1).astype(np.float32))

    def _next_note_block(self) -> np.ndarray:
        signal = self._note_signal
        start = self._note_position
        end = start + self.block_size
        if end >= len(signal):
            # loop the note so "live" playback continues indefinitely
            block = np.concatenate([signal[start:], signal[: end - len(signal)]])
            self._note_position = end - len(signal)
        else:
            block = signal[start:end]
            self._note_position = end
        return block


class HardwareSource(QtCore.QObject):
    """Untested in this environment -- requires sounddevice/PortAudio and a
    real input device. See device_manager.py."""

    def __init__(self, device_index: int, sample_rate: int, channels: int = 1,
                 buffer_size: int = 512, parent=None):
        super().__init__(parent)
        from onewave_mapper.device_manager import CaptureEngine  # deferred: optional dependency
        self._engine = CaptureEngine(device_index, sample_rate, channels, buffer_size)

    @property
    def ring_buffer(self) -> RingBuffer:
        return self._engine.ring_buffer

    def start(self) -> None:
        self._engine.start()

    def stop(self) -> None:
        self._engine.stop()
