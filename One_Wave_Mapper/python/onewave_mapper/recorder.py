"""Recorder tying the ring buffer, WAV writer, and session together
(Section 7).

Deliberately hardware-independent: `record_from_blocks` accepts any
iterable of (channels, n) numpy blocks, so it is fully testable with
synthetic signals here and can be fed real blocks from
`device_manager.CaptureEngine` on a machine with real audio hardware.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from onewave_mapper.ring_buffer import RingBuffer
from onewave_mapper.session import Session
from onewave_mapper.wav_io import write_wav, read_wav


class Recorder:
    def __init__(self, session: Session, sessions_root: str | Path):
        self.session = session
        self.sessions_root = Path(sessions_root)
        self._blocks: list[np.ndarray] = []
        self._ring_buffer: RingBuffer | None = None

    def record_from_blocks(self, blocks, ring_buffer_seconds: float = 30.0) -> None:
        """Consume an iterable of (channels, n) blocks, keeping the untouched
        original samples and mirroring recent history into a ring buffer for
        live triggering/inspection, per Section 5.4."""
        capacity = max(1, int(ring_buffer_seconds * self.session.sample_rate))
        self._ring_buffer = RingBuffer(self.session.channel_count, capacity, self.session.sample_rate)

        for block in blocks:
            block = np.atleast_2d(block)
            self._blocks.append(block.copy())
            self._ring_buffer.write(block)

    def record_array(self, signal: np.ndarray, block_size: int = 512) -> None:
        signal = np.atleast_2d(signal)
        n = signal.shape[1]

        def block_iter():
            for start in range(0, n, block_size):
                yield signal[:, start:start + block_size]

        self.record_from_blocks(block_iter())

    @property
    def ring_buffer(self) -> RingBuffer:
        if self._ring_buffer is None:
            raise RuntimeError("no recording in progress or completed")
        return self._ring_buffer

    def full_recording(self) -> np.ndarray:
        if not self._blocks:
            return np.zeros((self.session.channel_count, 0), dtype=np.float32)
        return np.concatenate(self._blocks, axis=1)

    def finalize(self, filename: str = "raw_multichannel.wav", bit_depth: str = "float32") -> Path:
        """Write the untouched captured samples to disk and save session metadata.
        Never overwrites an existing recording for this session (Section 2.1)."""
        root = self.session.make_directory_structure(self.sessions_root)
        audio_path = root / "audio" / filename
        if audio_path.exists():
            raise FileExistsError(f"refusing to overwrite existing recording: {audio_path}")

        recording = self.full_recording()
        write_wav(str(audio_path), recording.T, self.session.sample_rate, bit_depth=bit_depth)
        self.session.save(self.sessions_root)
        return audio_path


def reopen_recording(sessions_root: str | Path, session_id: str,
                      filename: str = "raw_multichannel.wav"):
    """Load a previously recorded session's session.json and original audio, unmodified."""
    root = Path(sessions_root) / session_id
    session = Session.load(root / "session.json")
    wav_data = read_wav(str(root / "audio" / filename))
    return session, wav_data
