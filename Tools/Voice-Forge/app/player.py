"""Thin wrapper around QMediaPlayer for previewing rendered WAV files.

Playback is optional: some headless/minimal Linux installs are missing
the system audio libraries QtMultimedia needs (PulseAudio/ALSA plugins).
When that happens we disable playback instead of crashing the app --
Voice Forge still loads, blends, and renders to disk without it.
"""
from __future__ import annotations

from PySide6.QtCore import QUrl

try:
    from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer

    _MULTIMEDIA_AVAILABLE = True
except Exception:  # pragma: no cover - depends on host audio libraries
    _MULTIMEDIA_AVAILABLE = False


class Previewer:
    def __init__(self):
        self.available = _MULTIMEDIA_AVAILABLE
        self._player = None
        self._output = None
        if self.available:
            try:
                self._player = QMediaPlayer()
                self._output = QAudioOutput()
                self._player.setAudioOutput(self._output)
            except Exception:  # pragma: no cover - depends on host audio libraries
                self.available = False
                self._player = None
                self._output = None

    def play_file(self, path: str) -> bool:
        if not self.available or self._player is None:
            return False
        self._player.setSource(QUrl.fromLocalFile(path))
        self._player.play()
        return True

    def stop(self) -> None:
        if self._player is not None:
            self._player.stop()
