# One-Wave Mapper — Python Prototype Engine

A hardware-independent, fully tested implementation of the DSP core described
in `../PROJECT_SPECIFICATION.md`, plus a real (if headless-verified) live
oscilloscope UI, built against the Section 3.3 prototype stack
(NumPy/SciPy/PySide6/pyqtgraph). This is **not** the production engine — the
spec calls for that to be C++/JUCE (Section 3.1) — but every algorithm here
is real, tested code that a production port can be checked against.

## What this actually does

Point it at a captured (or synthetic) sound and it maps out everything
measurable about that wave in one place: oscillation speed (frequency),
physical wavelength, octave/note, harmonics, resonance, envelope life-cycle
(growth/sustain/decay, with the Point/Path/Field "nested cycles of motion"
structure), and how it interferes or beats against other waves — see
`wave_map.py` and `prediction.py` below. Objective measurement always stays
separate from the experimental One-Wave interpretive tags (Section 2.3).

## Why Python, and the hardware/display gap

This was written in a Linux container with no audio hardware and, for most
of development, no display. Xvfb/Qt's offscreen platform turned out to be
available, so the oscilloscope UI is now real and screenshot-verified — see
"The GUI" below — but it has still never touched a real microphone or a real
screen. Everything else is implemented and tested here:

- Ring buffer, trigger engine, FFT/pitch/harmonic/envelope/phase analysis
- Wavelength (Section 1's implied physical wave, not just its digitized
  frequency): `lambda = speed_of_sound / f`, with a temperature-adjustable
  speed of sound
- Spectrogram (STFT tiling, linear/log/note axes, fundamental/harmonic
  track overlays), resonance detection with ring-down analysis and a
  caller-supplied classification hook, and chord/interval analysis
  (N-note harmonic-sieve detection, shared harmonics, beat/
  intermodulation candidates, roughness)
- Interference analysis (Section 14): sum/difference, frequency-dependent
  cancellation/reinforcement, beat detection, constructive/destructive
  scoring, and the N-note isolated-vs-combined residual comparison
  workflow (record every note, then the real chord, then see how they
  differ from a plain linear sum)
- `prediction.py`: the forward-looking counterpart to that comparison —
  predicts beat frequencies, harmonic collisions, roughness, and
  interference scores for N isolated notes *before* any combined
  recording exists, purely from linear superposition
- `fretboard.py`: a registry for "record every note on the neck," so a
  chord shape can be turned into the isolated-signal list either of the
  above needs by (string, fret) lookup
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

## The GUI

`onewave_mapper/ui/oscilloscope_window.py` is a real PySide6 + pyqtgraph
window, not a mockup:

- A triggered oscilloscope trace (rising/falling/either edge, adjustable
  threshold, pre/post-trigger window), wired straight to `RingBuffer` and
  `TriggerEngine`
- A **life-cycle envelope panel** underneath it, showing the Hilbert
  envelope over ~2 seconds of history — growth, sustain, decay — instead
  of just the one triggered slice, plus a live "Life-cycle state" readout
  from the One-Wave Inward/Outward/Over tags
- Live Pitch/Note/Wavelength readouts computed from the same `pitch.py`
  and `wavelength.py` used everywhere else
- A synthetic source (`ui/live_sources.py`) standing in for a real audio
  callback via a `QTimer` pushing blocks into the same `RingBuffer.write()`
  a real one would call — this is what the automated tests exercise
- A `HardwareSource` wrapping `device_manager.CaptureEngine` for a real
  device, untested here for lack of hardware

Verified against Qt's offscreen platform in `tests/test_gui_smoke.py`: the
window constructs, both the scope trace and the envelope panel actually
redraw across timer ticks with real (if synthetic) audio flowing, Freeze
stops both, changing trigger settings doesn't crash, and a grabbed
screenshot is a real non-blank image. That is meaningfully short of "looked
at on a real screen with a real guitar plugged in" — there is neither a
display nor audio hardware in the container this was built in.

Run it:

```bash
python -m onewave_mapper.gui
```

## Build / run instructions

```bash
cd One_Wave_Mapper/python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the automated tests (includes offscreen GUI smoke tests)
pytest -q

# Run the end-to-end DSP demo (synthetic guitar note -> record -> reopen ->
# spectrum/pitch/harmonics/envelope -> WAV + JSON export)
python -m onewave_mapper.cli runs

# Run the live oscilloscope UI
python -m onewave_mapper.gui
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
├── wavelength.py          physical wavelength (lambda = v/f), speed of sound
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
│                          scores, N-note isolated-vs-combined comparison
├── prediction.py           forward prediction of N-note interactions
│                          (beats/collisions/roughness) before any combined
│                          recording exists
├── fretboard.py            Section 10.2/10.3 — (string, fret) note registry
├── cycles.py               Section 16 — Cycle objects, Point/Path/Field,
│                          modulation spectrum
├── one_wave_views.py       Section 17 — Inward/Outward/Across/Over rule engine
├── chord.py               Section 18 — intervals, N-note pitch detection, ChordEvent
├── wave_map.py             unified per-signal report: frequency, wavelength,
│                          octave/note, harmonics, resonance, rotational
│                          envelope (Cycle tree), One-Wave tags, optional
│                          interference vs. a second signal
├── wav_io.py             Section 2.1/21.1 — RIFF/WAV read/write (PCM16/24/32, float32/64)
├── session.py            Section 7.2/7.3, 21.3 — session + note-event schema
├── recorder.py           Section 7 — ties the above together, hardware-independent
├── device_manager.py     Section 3.2/5 — sounddevice capture (needs real hardware)
├── cli.py                End-to-end DSP demo (MVP items 6-14, Section 26)
├── gui.py                 Oscilloscope UI entry point (python -m onewave_mapper.gui)
└── ui/
    ├── oscilloscope_window.py   Section 6/20 — the live scope + life-cycle panel
    └── live_sources.py          synthetic (tested) and hardware (untested) sources
```

`recorder.py` never overwrites an existing recording (Section 2.1) and
keeps the ring buffer's recent-history mirror separate from the full
captured array, so live triggering/inspection and the archival WAV write
are backed by the same untouched samples.

Objective measurement (metering, FFT, pitch, harmonics, phase, envelope,
wavelength) lives entirely separately from any One-Wave interpretive
tagging (Section 2.3) — `NoteEvent.one_wave_tags` and `WaveMap`'s tags are
deliberately plain, user-editable lists, not something baked into the
measurement itself.

## Testing

157 tests in `tests/`, including direct implementations of every Section
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

Plus `tests/test_gui_smoke.py` (offscreen Qt) for the oscilloscope window
itself. Run `pytest -q` from this directory.

## Known limitations

- **No real hardware, and no real screen.** `device_manager.py` and
  `ui/live_sources.py`'s `HardwareSource` are written but unverified.
  Everything GUI-related has only ever been proven against Qt's offscreen
  platform in this container.
- **Ring buffer uses a coarse lock, not lock-free SPSC.** Fine for
  prototyping and for feeding the DSP modules under test; the production
  C++ audio callback (Section 2.4) must use a real lock-free structure.
- **No SQLite session store, only JSON.** Section 7.2's `session.sqlite`
  is not implemented; `session.json` covers the same metadata for now.
- **Resonance classification is `"unknown"` by default.** `resonance.py`
  scores candidates (prominence, persistence, decay, Q, phase stability)
  and accepts a `classifier` callback (Section 15.1) — but ships no
  built-in guitar/room classifier, since frequency range alone isn't a
  reliable basis for "body" vs. "room" vs. "pickup" without a
  characterized setup. `coherence_score` is likewise `None` until a
  second channel is wired in.
- **Blind delay estimation struggles on dense, harmonically-overlapping
  chords.** `compare_isolated_vs_combined_n` recovers a triad's true
  per-note delays precisely (tested), but a full six-string open-E chord
  — whose strings are almost entirely octave/fifth-related — is close to
  a worst case for broadband cross-correlation; see
  `test_compare_isolated_vs_combined_n_dense_chord_is_a_documented_hard_case`.
  `alignment_window_samples` (restricting correlation to the attack
  transient) helps but doesn't fully solve it for the densest chords.
- **`chord.detect_pitches` degrades on closely-spaced or highly
  harmonically-overlapping notes**, for the same underlying reason:
  peeled harmonics from one note can eat a real peak belonging to
  another. Recovers a clean triad (tested); not stress-tested past that.
- **`prediction.py` is a purely linear forecast.** It will not predict
  amplifier/pickup nonlinearity, string coupling, or room effects —
  that's exactly the gap `compare_isolated_vs_combined_n`'s residual is
  for measuring once a real combined recording exists.
- **One-Wave rule engine implements one indicator per view, not every
  one Section 17 lists.** `inward_rule`/`outward_rule` use envelope
  slope only; `across_rule` is zero-crossing only; `over_rule` is
  modulation-spectrum only. All four are ordinary Python callables
  matching the `OneWaveRule` signature, so adding more indicators as
  additional or replacement rules doesn't require touching the engine.
- **`pink_noise()` is a Voss-McCartney approximation**, adequate as a test
  signal but not a calibrated 1/f reference.
- **Wavelength assumes a fixed speed of sound** (dry air, 20°C by
  default, overridable) — this engine has no way to measure the actual
  propagation medium.

## Next five implementation tasks

1. Run it for real: install on a machine with a microphone/interface and
   a display, confirm `device_manager.py`/`HardwareSource` actually
   capture live audio, and get a first real screenshot (not an offscreen
   one) of the oscilloscope + life-cycle panel.
2. Spectrogram/resonance/interference panels alongside the oscilloscope
   in the GUI, wired to `spectrogram.py`, `resonance.py`, and
   `interference.py` — turning the remaining tested-but-headless analysis
   modules into Section 20's actual dockable-panel workspace.
3. A fretboard-driven session workflow: use `fretboard.py` plus
   `Recorder`/`Session` to actually walk the neck, save each note to
   disk, then feed a chord shape's `signals_for_chord()` into both
   `prediction.predict_interaction` (before playing the chord) and
   `interference.compare_isolated_vs_combined_n` (after recording the
   real strum) — the full round-trip the user's workflow calls for.
4. Multichannel `coherence_score` wiring in `resonance.py`, using
   `phase_analysis.magnitude_squared_coherence`, and a first real
   (non-illustrative) frequency-band-plus-coherence resonance classifier
   for a characterized guitar/room setup.
5. Tighter harmonic peeling in `chord.detect_pitches` (partial removal
   weighted by expected amplitude rolloff instead of full zeroing) and a
   documented failure mode when `min_separation_hz` can't be met, aimed
   at closing the gap `compare_isolated_vs_combined_n`'s dense-chord
   limitation shares.
