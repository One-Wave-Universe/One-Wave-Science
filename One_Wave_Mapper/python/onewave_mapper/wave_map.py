"""Unified wave map: wavelength, oscillation speed (frequency/octave),
harmonics, resonance, interference, and the full Point/Path/Field
"rotational envelope" of a captured sound, in one report.

Every other module in this package answers one question (what's the
pitch, what's the spectrum, is there a resonance, are two signals
interfering). This ties them together so a single call answers "what
came through, and how is it moving" for one signal -- objective
measurement (frequency, wavelength, harmonics, resonance) kept separate
from the One-Wave interpretive tags per Section 2.3, but reported
side by side.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from onewave_mapper import fft_analyzer, pitch as pitch_module, harmonics as harmonics_module
from onewave_mapper import resonance as resonance_module, cycles as cycles_module
from onewave_mapper import one_wave_views, wavelength as wavelength_module
from onewave_mapper import interference as interference_module


@dataclass
class WaveMap:
    sample_rate: float
    duration_seconds: float
    speed_of_sound_mps: float

    # oscillation speed / octave (objective measurement)
    frequency_hz: float | None
    wavelength_m: float | None
    note_name: str | None
    octave: int | None
    cents_offset: float | None
    pitch_confidence: float

    harmonics: list
    resonances: list

    # the "rotational envelope": Point cycles (fast waveform periods),
    # the Path cycle (whole attack-sustain-decay span), and any detected
    # modulation (vibrato/tremolo/beat), each level named per Section 16.3
    point_cycle_count: int
    path_cycle: dict | None
    modulation_cycle: dict | None

    # One-Wave interpretive tags over the same window (Section 17) --
    # experimental, evidence-linked, never a substitute for the above
    one_wave_tags: list

    # only populated when a second signal is passed for comparison (Section 14)
    interference: dict | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def map_wave(signal: np.ndarray, sample_rate: float, source_channel: int = 1,
             speed_of_sound_mps: float = wavelength_module.SPEED_OF_SOUND_DRY_AIR_20C_MPS,
             fmin: float = 60.0, fmax: float = 1500.0, max_harmonics: int = 16,
             max_point_cycles: int = 32, compare_signal: np.ndarray | None = None) -> WaveMap:
    duration_seconds = len(signal) / sample_rate

    pitch_result = pitch_module.detect_pitch(signal, sample_rate, fmin=fmin, fmax=fmax)

    frequency_hz = pitch_result.frequency_hz
    wavelength_m = None
    note_name = None
    octave = None
    cents_offset = None
    harmonic_tracks: list = []

    if frequency_hz is not None:
        wavelength_m = wavelength_module.wavelength_meters(frequency_hz, speed_of_sound_mps)
        note_info = pitch_module.frequency_to_note(frequency_hz)
        note_name = note_info["note_name"]
        cents_offset = note_info["cents_offset"]
        octave = int(np.floor(round(note_info["midi_note_float"]) / 12)) - 1

        fft_size = min(16384, max(256, 1 << int(np.floor(np.log2(max(len(signal), 8))))))
        spectrum = fft_analyzer.compute_spectrum(signal, sample_rate, window="hann", fft_size=fft_size)
        harmonic_tracks = harmonics_module.track_harmonics(spectrum, frequency_hz, max_harmonics)

    resonance_fft_size = min(4096, max(256, 1 << int(np.floor(np.log2(max(len(signal), 8))))))
    resonance_hop_size = max(64, resonance_fft_size // 4)
    resonances = resonance_module.detect_resonances(
        signal, sample_rate, fft_size=resonance_fft_size, hop_size=resonance_hop_size,
    ) if len(signal) >= resonance_fft_size else []

    cycle_tree = cycles_module.build_note_cycle_tree(
        signal, sample_rate, source_channel, max_point_cycles=max_point_cycles,
    )

    one_wave_tags = one_wave_views.classify_window(signal, sample_rate)

    interference_result = None
    if compare_signal is not None:
        n = min(len(signal), len(compare_signal))
        scores = interference_module.interference_scores(signal[:n], compare_signal[:n], sample_rate)
        beats = interference_module.detect_beats(signal[:n] + compare_signal[:n], sample_rate)
        interference_result = {"scores": scores.to_dict(), "beats": beats.to_dict()}

    return WaveMap(
        sample_rate=sample_rate,
        duration_seconds=duration_seconds,
        speed_of_sound_mps=speed_of_sound_mps,
        frequency_hz=frequency_hz,
        wavelength_m=wavelength_m,
        note_name=note_name,
        octave=octave,
        cents_offset=cents_offset,
        pitch_confidence=pitch_result.confidence,
        harmonics=[h.to_dict() for h in harmonic_tracks],
        resonances=[r.to_dict() for r in resonances],
        point_cycle_count=len(cycle_tree["point_cycles"]),
        path_cycle=cycle_tree["path_cycle"].to_dict(),
        modulation_cycle=cycle_tree["modulation_cycle"].to_dict() if cycle_tree["modulation_cycle"] else None,
        one_wave_tags=[t.to_dict() for t in one_wave_tags],
        interference=interference_result,
    )
