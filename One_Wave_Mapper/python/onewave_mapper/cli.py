"""End-to-end demo of the hardware-independent MVP slice (Section 26, items 6-14).

Generates a synthetic guitar note (since no live input device is available
here), records it, reopens the recording, runs spectrum/pitch/harmonic/
envelope analysis, and exports WAV + JSON -- exactly the same code path a
real captured note would go through.

Usage: python -m onewave_mapper.cli [output_dir]
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

from onewave_mapper import signal_generator, metering, fft_analyzer, pitch, harmonics, envelope
from onewave_mapper.session import Session, NoteEvent
from onewave_mapper.recorder import Recorder, reopen_recording


def run(sessions_root: str = "runs") -> Path:
    sample_rate = 48000
    fundamental_hz = 220.0  # A3
    duration_seconds = 3.0

    note = signal_generator.guitar_note(fundamental_hz, duration_seconds, sample_rate)

    session = Session.create(
        sample_rate=sample_rate, bit_depth="float32", channel_count=1, buffer_size=512,
        instrument="guitar", guitar_string=5, fret=2, expected_note="A3",
    )

    recorder = Recorder(session, sessions_root)
    recorder.record_array(note.reshape(1, -1))
    audio_path = recorder.finalize()
    print(f"Recorded: {audio_path}")

    loaded_session, wav_data = reopen_recording(sessions_root, session.session_id)
    reopened_signal = wav_data.samples[:, 0]
    print(f"Reopened session {loaded_session.session_id}: "
          f"{len(reopened_signal)} samples at {wav_data.sample_rate} Hz "
          f"({'bit-exact' if np.array_equal(reopened_signal.astype(np.float32), note.astype(np.float32)) else 'lossy'} round trip)")

    scope = metering.measure(reopened_signal, sample_rate)
    print(f"Peak: {scope.peak:.4f}  RMS: {scope.rms:.4f}  Clipped: {scope.clipping_count} samples")

    spectrum = fft_analyzer.compute_spectrum(reopened_signal, sample_rate, window="hann", fft_size=8192)
    pitch_result = pitch.detect_pitch(reopened_signal, sample_rate, fmin=80, fmax=800)

    if pitch_result.frequency_hz is None:
        print("Pitch: no confident estimate")
        note_info = {"note_name": None, "cents_offset": None}
    else:
        note_info = pitch.frequency_to_note(pitch_result.frequency_hz)
        print(f"Pitch: {pitch_result.frequency_hz:.2f} Hz "
              f"({note_info['note_name']}, {note_info['cents_offset']:+.1f} cents) "
              f"confidence={pitch_result.confidence:.2f}")

    harmonic_tracks = []
    if pitch_result.frequency_hz is not None:
        harmonic_tracks = harmonics.track_harmonics(spectrum, pitch_result.frequency_hz, max_harmonics=16)
        found = [t for t in harmonic_tracks if t.measured_frequency_hz is not None]
        print(f"Harmonics found: {len(found)} / {len(harmonic_tracks)}")

    env = envelope.hilbert_envelope(reopened_signal)
    env_measurements = envelope.measure_envelope(env, sample_rate)
    print(f"Attack: {env_measurements.attack_time_seconds * 1000:.1f} ms  "
          f"Decay(-20dB): {env_measurements.decay_20db_seconds:.3f} s")

    event = NoteEvent(
        event_id=f"note_{session.session_id}",
        source_channel=1,
        start_sample=0,
        end_sample=len(reopened_signal),
        sample_rate=sample_rate,
        expected_note="A3",
        measured_frequency_hz=pitch_result.frequency_hz,
        cents_offset=note_info["cents_offset"],
        pitch_confidence=pitch_result.confidence,
        attack_time_ms=env_measurements.attack_time_seconds * 1000 if env_measurements.attack_time_seconds else None,
        decay_20db_seconds=env_measurements.decay_20db_seconds,
        rms_dbfs=20 * np.log10(max(scope.rms, 1e-12)),
        peak_dbfs=20 * np.log10(max(scope.peak, 1e-12)),
        harmonics=[t.to_dict() for t in harmonic_tracks],
    )

    root = session.root_dir(sessions_root)
    event_path = root / "exports" / f"{event.event_id}.json"
    event.save(event_path)
    print(f"Exported event JSON: {event_path}")

    return root


if __name__ == "__main__":
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "runs"
    run(output_dir)
