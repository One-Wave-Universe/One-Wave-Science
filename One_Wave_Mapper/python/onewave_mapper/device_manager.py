"""Live audio device listing and capture (Section 3.2, 5).

This module requires the optional `sounddevice` dependency (PortAudio) and
a real audio device, neither of which exist in a headless CI/sandbox
container -- it cannot be exercised or verified there. It is written
against the same RingBuffer/Recorder interfaces used by the tested,
hardware-independent code, so once `pip install sounddevice` succeeds on a
machine with an actual microphone/interface, capture should work without
touching the rest of the engine.

The real-time audio callback below intentionally does none of the things
Section 2.4 forbids: no file I/O, no large allocation, no logging, only a
copy into a pre-allocated ring buffer.
"""

from __future__ import annotations

from dataclasses import dataclass

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except OSError:
    sd = None
    SOUNDDEVICE_AVAILABLE = False
except ImportError:
    sd = None
    SOUNDDEVICE_AVAILABLE = False

from onewave_mapper.ring_buffer import RingBuffer


@dataclass
class DeviceInfo:
    index: int
    name: str
    driver_type: str
    max_input_channels: int
    max_output_channels: int
    default_sample_rate: float


def require_sounddevice() -> None:
    if not SOUNDDEVICE_AVAILABLE:
        raise RuntimeError(
            "sounddevice/PortAudio is not available in this environment. "
            "Install it on a machine with real audio hardware: pip install sounddevice"
        )


def list_devices() -> list[DeviceInfo]:
    require_sounddevice()
    devices = sd.query_devices()
    result = []
    for index, device in enumerate(devices):
        result.append(DeviceInfo(
            index=index,
            name=device["name"],
            driver_type=sd.query_hostapis(device["hostapi"])["name"],
            max_input_channels=device["max_input_channels"],
            max_output_channels=device["max_output_channels"],
            default_sample_rate=device["default_samplerate"],
        ))
    return result


class CaptureEngine:
    """Owns the live audio stream and feeds a RingBuffer from the audio callback."""

    def __init__(self, device_index: int, sample_rate: int, channels: int,
                 buffer_size: int, ring_buffer_seconds: float = 30.0):
        require_sounddevice()
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.channels = channels
        self.buffer_size = buffer_size
        self.ring_buffer = RingBuffer(channels, int(ring_buffer_seconds * sample_rate), sample_rate)
        self.dropped_block_count = 0
        self._stream = None

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            self.dropped_block_count += 1
        self.ring_buffer.write(indata.T)

    def start(self) -> None:
        self._stream = sd.InputStream(
            device=self.device_index,
            channels=self.channels,
            samplerate=self.sample_rate,
            blocksize=self.buffer_size,
            dtype="float32",
            callback=self._audio_callback,
        )
        self._stream.start()

    def stop(self) -> None:
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None
