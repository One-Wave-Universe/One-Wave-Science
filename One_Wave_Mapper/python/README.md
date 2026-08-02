# One-Wave Mapper — Python Prototype Engine

A hardware-independent, fully tested implementation of the DSP core described
in `../PROJECT_SPECIFICATION.md`, built against the Section 3.3 prototype
stack (NumPy/SciPy). This is **not** the production engine — the spec calls
for that to be C++/JUCE (Section 3.1) — but every algorithm here is real,
tested code that a production port can be checked against.

## Why Python, and why not the live oscilloscope yet

This was written in a Linux container with no audio hardware and no
display. Everything that can be verified without a microphone or a screen
is implemented and tested here:

- Ring buffer, trigger engine, FFT/pitch/harmonic/envelope/phase analysis
- Spectrogram (STFT tiling, linear/log/note axes, fundamental/harmonic
  track overlays), resonance detection with ring-down analysis and a
  caller-supplied classification hook, and chord/interval analysis
  (N-note harmonic-sieve detection, shared harmonics, beat/
  intermodulation candidates, roughness)
- Interference analysis (Section 14): sum/difference, frequency-dependent
  cancellation/reinforcement, beat detection, constructive/destructive
  scoring, and the isolated-vs-combined residual comparison workflow
- Cycle objects with Point/Path/Field tagging and modulation-spectrum
  detection (Section 16), and the four One-Wave interpretive views —
  Inward/Outward/Across/Over — as a configurable, evidence-linked rule
  engine kept strictly separate from objective measurement (Section 17)
- Calibration profiles (Section 4.2) — dBFS is always available; volts/SPL
  conversion refuses to run without an active `CalibrationProfile`
- WAV read/write (including the 32-bit float format the stdlib `wave`
  module can't write)
- Session and note-event JSON schema, directory layout
- A `Recorder` that accepts any block source (synthetic or live) and never
  overwrites an existing recording

`device_manager.py` wraps `sounddevice`/PortAudio for real device listing
and live capture, matching the interfaces above — but it **requires real
audio hardware to test** and has not been run against one. See "Known
limitations" below.

## Build / run instructions

```bash
cd One_Wave_Mapper/python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the automated tests
pytest -q

# Run the end-to-end demo (synthetic guitar note -> record -> reopen ->
# spectrum/pitch/harmonics/envelope -> WAV + JSON export)
python -m onewave_mapper.cli runs
```

To use live hardware (on a machine that has a microphone/interface and a
working PortAudio install):

```bash
pip install sounddevice
python3 -c "from onewave_mapper.device_manager import list_devices; \
            [print(d) for d in list_devices()]"
```

## Architecture

```
onewave_mapper/
├── ring_buffer.py       Section 5.4/5.5 — timestamped multichannel ring buffer
├── signal_generator.py  Section 24.2 — synthetic test signals
├── metering.py           Section 6.6 — objective scope measurements
├── calibration.py        Section 4.2 — calibration profiles, dBFS/volts/SPL
├── trigger.py            Section 6.2/6.3 — trigger engine
├── fft_analyzer.py       Section 8 — windowed FFT spectrum
├── spectrogram.py         Section 9 — STFT tiling, axis scales, track overlays
├── pitch.py              Section 8.3 — multi-method fundamental detection
├── harmonics.py          Section 12 — harmonic tracking / peak classification
├── resonance.py           Section 15 — resonance detection, ring-down analysis,
│                          classification hook
├── phase_analysis.py     Section 13 — delay, phase difference, coherence
├── envelope.py           Section 11 — envelopes, attack/decay, decay fitting
├── interference.py        Section 14 — sum/difference, beats, interference
│                          scores, isolated-vs-combined residual comparison
├── cycles.py               Section 16 — Cycle objects, Point/Path/Field,
│                          modulation spectrum
├── one_wave_views.py       Section 17 — Inward/Outward/Across/Over rule engine
├── chord.py               Section 18 — intervals, N-note pitch detection, ChordEvent
├── wav_io.py             Section 2.1/21.1 — RIFF/WAV read/write (PCM16/24/32, float32/64)
├── session.py            Section 7.2/7.3, 21.3 — session + note-event schema
├── recorder.py           Section 7 — ties the above together, hardware-independent
├── device_manager.py     Section 3.2/5 — sounddevice capture (needs real hardware)
└── cli.py                End-to-end demo (MVP items 6-14, Section 26)
```

`recorder.py` never overwrites an existing recording (Section 2.1) and
keeps the ring buffer's recent-history mirror separate from the full
captured array, so live triggering/inspection and the archival WAV write
are backed by the same untouched samples.

Objective measurement (metering, FFT, pitch, harmonics, phase, envelope)
lives entirely separately from any One-Wave interpretive tagging (Section
2.3) — `NoteEvent.one_wave_tags` is deliberately an empty, user-editable
list here, not something this engine fills in automatically.

## Testing

109 tests in `tests/`, including direct implementations of every Section
24.3 acceptance test:

- `test_acceptance_frequency_accuracy_440hz_within_0p1hz` — autocorrelation
  pitch detection on a 440 Hz sine, tolerance ±0.1 Hz
- `test_acceptance_beat_detection_440_and_442hz_gives_2hz_beat` — envelope
  modulation spectrum of a two-tone signal
- `test_acceptance_phase_difference_90_degrees` — Hilbert-transform
  instantaneous phase difference between a signal and a 90°-shifted copy
- `test_acceptance_delay_detection_48_samples_at_48khz` — cross-correlation
  delay estimate on broadband noise with a known 48-sample delay
- `test_acceptance_trigger_stability_no_horizontal_jumping` — trigger
  interval jitter on a stable periodic tone

Run `pytest -q` from this directory.

## Known limitations

- **No real hardware or GUI testing.** `device_manager.py` is written but
  unverified; there is no oscilloscope/spectrogram UI yet (Section 20) —
  building one needs PySide6/pyqtgraph or, for production, JUCE, on a
  machine with a display.
- **Ring buffer uses a coarse lock, not lock-free SPSC.** Fine for
  prototyping and for feeding the DSP modules under test; the production
  C++ audio callback (Section 2.4) must use a real lock-free structure.
- **No SQLite session store, only JSON.** Section 7.2's `session.sqlite`
  is not implemented; `session.json` covers the same metadata for now.
- **Resonance classification is `"unknown"` by default.** `resonance.py`
  scores candidates (prominence, persistence, decay, Q, phase stability)
  and now accepts a `classifier` callback (Section 15.1) — but ships no
  built-in guitar/room classifier, since frequency range alone isn't a
  reliable basis for "body" vs. "room" vs. "pickup" without a
  characterized setup. `coherence_score` is likewise `None` until a
  second channel is wired in.
- **`chord.detect_pitches` degrades on closely-spaced or highly
  harmonically-overlapping notes.** The iterative-peeling approach
  recovers a clean triad (tested), but hasn't been stress-tested against
  dense six-string voicings or notes a semitone apart, where peeled
  harmonics from one note can eat a real peak belonging to another.
- **One-Wave rule engine implements one indicator per view, not every
  one Section 17 lists.** `inward_rule`/`outward_rule` use envelope
  slope only (not e.g. explicit phase-convergence or harmonic-generation
  indicators); `across_rule` is zero-crossing only (not phase/frequency-
  track intersection); `over_rule` is modulation-spectrum only (not
  explicit phase-wrap detection). All four are ordinary Python callables
  matching the `OneWaveRule` signature, so adding more indicators as
  additional or replacement rules doesn't require touching the engine.
- **`pink_noise()` is a Voss-McCartney approximation**, adequate as a test
  signal but not a calibrated 1/f reference.

## Next five implementation tasks

1. A minimal PySide6 + pyqtgraph oscilloscope UI wired to `TriggerEngine`
   and `RingBuffer`, run and screenshotted on a machine with a display —
   the first real test of `device_manager.py` against live hardware, and
   the first place `calibration.py`'s dBFS-only-by-default rule needs to
   actually be enforced on an axis label.
2. A spectrogram/interference/resonance/cycle panel layer on top of the
   oscilloscope UI from task 1, wired to `spectrogram.py`,
   `interference.py`, `resonance.py`, and `cycles.py` — turning the
   tested-but-headless analysis modules into Section 20's actual
   dockable-panel workspace.
3. Multichannel `coherence_score` wiring in `resonance.py`, using
   `phase_analysis.magnitude_squared_coherence` across two channels of
   the same resonance candidate, and a first real (non-illustrative)
   frequency-band-plus-coherence resonance classifier for a
   characterized guitar/room setup.
4. Stress-test and harden `chord.detect_pitches` against dense/close
   voicings (Section 18.3's four-note and six-string cases): tighter
   peeling (partial harmonic removal instead of full zeroing, weighted
   by expected amplitude rolloff) and a documented failure mode when
   `min_separation_hz` can't be met.
5. SQLite session store (Section 7.2's `session.sqlite`) alongside the
   existing `session.json`, plus persisting `Cycle`/`OneWaveTag`/
   `ResonanceEvent`/`ChordEvent` objects into a session's `analysis/`
   subdirectories so a full session round-trips everything computed
   about it, not just the note-event JSON `cli.py` currently exports.
