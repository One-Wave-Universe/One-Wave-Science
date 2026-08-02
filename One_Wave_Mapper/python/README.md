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
├── trigger.py            Section 6.2/6.3 — trigger engine
├── fft_analyzer.py       Section 8 — windowed FFT spectrum
├── pitch.py              Section 8.3 — multi-method fundamental detection
├── harmonics.py          Section 12 — harmonic tracking / peak classification
├── phase_analysis.py     Section 13 — delay, phase difference, coherence
├── envelope.py           Section 11 — envelopes, attack/decay, decay fitting
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

54 tests in `tests/`, including direct implementations of every Section
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
- **Spectrogram, resonance analyzer, interference/beat visualizer UI,
  chord/polyphonic pitch, and One-Wave interpretive rule engine (Sections
  9, 14-19) are not implemented.** The measurement primitives they'd be
  built on (FFT, envelope, phase, harmonics) are done and tested.
- **`pink_noise()` is a Voss-McCartney approximation**, adequate as a test
  signal but not a calibrated 1/f reference.
- **Calibration profiles (Section 4.2) are not implemented** — there is no
  dBFS-to-volts/SPL conversion yet; everything is dBFS/normalized, which
  is the spec's required default in the absence of calibration.

## Next five implementation tasks

1. Calibration profile storage (Section 4.2) and dBFS-only display
   enforcement in whatever UI comes next.
2. A minimal PySide6 + pyqtgraph oscilloscope UI wired to `TriggerEngine`
   and `RingBuffer`, run and screenshotted on a machine with a display —
   the first real test of `device_manager.py` against live hardware.
3. Spectrogram engine (Section 9): STFT tiling with linear/log/note
   frequency axes, backed by `fft_analyzer.compute_spectrum`.
4. Resonance analyzer (Section 15): prominence/persistence/decay-based
   candidate detection and Q-factor estimation, reusing `envelope.py`'s
   exponential-decay fit.
5. Chord/interval analysis (Section 18): two-fundamental polyphonic
   detection on top of the existing single-pitch `pitch.py`, plus the
   isolated-vs-combined residual comparison from Section 14.4.
