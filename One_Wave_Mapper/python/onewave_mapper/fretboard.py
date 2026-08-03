"""Fretboard note registry (Section 10.2/10.3).

A place for "record every note on the neck" to live: register one
isolated recording per (string, fret), look positions up by chord shape,
and hand that list of signals to interference.compare_isolated_vs_combined_n
or wave_map.predict_interaction. This module only stores/organizes
recordings and their measured pitch -- it doesn't invent fret positions
for an ambiguous pitch (Section 10.3: "The user must be able to choose
the actual string and fret when several positions produce the same
pitch"), since that requires the player's own knowledge of what they
played.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np

from onewave_mapper import pitch as pitch_module
from onewave_mapper.wav_io import read_wav

# Standard tuning, open-string frequency in Hz. String 1 = high E, string 6 = low E.
STANDARD_TUNING_HZ = {
    1: 329.63,  # E4
    2: 246.94,  # B3
    3: 196.00,  # G3
    4: 146.83,  # D3
    5: 110.00,  # A2
    6: 82.41,   # E2
}


def expected_frequency_hz(string_number: int, fret_number: int,
                           tuning: dict[int, float] = STANDARD_TUNING_HZ) -> float:
    if string_number not in tuning:
        raise ValueError(f"no open-string frequency for string {string_number}")
    return tuning[string_number] * (2 ** (fret_number / 12.0))


@dataclass
class FretboardEntry:
    string_number: int
    fret_number: int
    expected_note: str
    expected_frequency_hz: float
    measured_frequency_hz: float | None
    cents_error: float | None
    sample_rate: float | None
    audio_path: str | None

    def to_dict(self) -> dict:
        return asdict(self)


class FretboardMap:
    def __init__(self, tuning: dict[int, float] = STANDARD_TUNING_HZ):
        self.tuning = tuning
        self._entries: dict[tuple[int, int], FretboardEntry] = {}
        self._signals: dict[tuple[int, int], np.ndarray] = {}

    def register(self, string_number: int, fret_number: int, signal: np.ndarray | None = None,
                 sample_rate: float | None = None, audio_path: str | Path | None = None,
                 fmin: float = 60.0, fmax: float = 1500.0) -> FretboardEntry:
        """Register a recording for one fret position. Either pass signal +
        sample_rate directly, or audio_path to a WAV file (loaded lazily via
        get_signal() but pitch-measured now if provided)."""
        if signal is None and audio_path is not None:
            wav_data = read_wav(str(audio_path))
            signal = wav_data.samples[:, 0]
            sample_rate = wav_data.sample_rate

        expected_hz = expected_frequency_hz(string_number, fret_number, self.tuning)
        expected_note = pitch_module.frequency_to_note(expected_hz)["note_name"]

        measured_frequency_hz = None
        cents_error = None
        if signal is not None:
            if sample_rate is None:
                raise ValueError("sample_rate is required when signal is given")
            pitch_result = pitch_module.detect_pitch(signal, sample_rate, fmin=fmin, fmax=fmax)
            if pitch_result.frequency_hz is not None:
                measured_frequency_hz = pitch_result.frequency_hz
                cents_error = float(1200 * np.log2(measured_frequency_hz / expected_hz))
            self._signals[(string_number, fret_number)] = signal

        entry = FretboardEntry(
            string_number=string_number,
            fret_number=fret_number,
            expected_note=expected_note,
            expected_frequency_hz=expected_hz,
            measured_frequency_hz=measured_frequency_hz,
            cents_error=cents_error,
            sample_rate=sample_rate,
            audio_path=str(audio_path) if audio_path is not None else None,
        )
        self._entries[(string_number, fret_number)] = entry
        return entry

    def get(self, string_number: int, fret_number: int) -> FretboardEntry | None:
        return self._entries.get((string_number, fret_number))

    def get_signal(self, string_number: int, fret_number: int) -> np.ndarray:
        key = (string_number, fret_number)
        if key in self._signals:
            return self._signals[key]
        entry = self._entries.get(key)
        if entry is None:
            raise KeyError(f"no fretboard entry registered for string {string_number} fret {fret_number}")
        if entry.audio_path is None:
            raise KeyError(f"entry for string {string_number} fret {fret_number} has no stored signal or audio_path")
        wav_data = read_wav(entry.audio_path)
        signal = wav_data.samples[:, 0]
        self._signals[key] = signal
        return signal

    def signals_for_chord(self, positions: list[tuple[int, int]]) -> list[np.ndarray]:
        """Assemble the isolated-signal list for a chord shape, e.g.
        [(6, 0), (5, 2), (4, 2), (3, 1), (2, 0), (1, 0)] for open E major.
        Raises KeyError naming the first missing position, rather than
        silently skipping a string the player hasn't recorded yet."""
        signals = []
        for string_number, fret_number in positions:
            try:
                signals.append(self.get_signal(string_number, fret_number))
            except KeyError as exc:
                raise KeyError(
                    f"chord shape needs string {string_number} fret {fret_number}, "
                    f"which hasn't been recorded yet"
                ) from exc
        return signals

    def coverage_report(self, string_numbers: list[int] | None = None,
                         fret_range: tuple[int, int] = (0, 12)) -> dict:
        """Which (string, fret) positions are registered vs. still missing,
        over the given range -- for tracking progress through 'record every
        note on the neck.'"""
        string_numbers = string_numbers or sorted(self.tuning.keys())
        registered = []
        missing = []
        for string_number in string_numbers:
            for fret_number in range(fret_range[0], fret_range[1] + 1):
                key = (string_number, fret_number)
                (registered if key in self._entries else missing).append(key)
        return {
            "registered_count": len(registered),
            "missing_count": len(missing),
            "registered": registered,
            "missing": missing,
        }
