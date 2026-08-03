# One-Wave Mapper — Python Prototype Engine

A hardware-independent, fully tested implementation of the DSP core described
in `../PROJECT_SPECIFICATION.md`, plus a real (if headless-verified)
multi-panel measurement instrument, built against the Section 3.3 prototype
stack (NumPy/SciPy/PySide6/pyqtgraph). This is **not** the production
engine — the spec calls for that to be C++/JUCE (Section 3.1) — but every
algorithm here is real, tested code that a production port can be checked
against.

This is meant to be a measurement instrument, not a music visualizer: every
panel analyzes the same preserved, timestamped raw recording, the raw
waveform is never smoothed or replaced by a derived shape, and objective
measurement is always kept visibly separate from the experimental One-Wave
interpretive layer.

## The instrument (`onewave_mapper.gui`)

`ui/mapper_window.py` is a tabbed PySide6 + pyqtgraph window. Every tab reads
from one shared `AnalysisState` (`ui/analysis_state.py`) — one raw recording,
one cursor, one selection, one zoom/view range, one trigger point, one
Raw/One-Wave/Both mode, one highlighted-harmonic slot — so selecting a
region or moving the cursor in one tab changes what every other tab shows,
without each panel keeping its own copy of that state.

```bash
python -m onewave_mapper.gui            # full instrument
python -m onewave_mapper.gui --simple    # original single-panel oscilloscope
```

### Panels

- **Raw waveform** (`panels/waveform_panel.py`) — Audacity/oscilloscope-style
  time-domain view. Zero line through the center, positive and negative
  displacement both always visible, the plotted curve is always
  `state.raw_signal` sliced to the current view — never smoothed. Real
  mouse-wheel zoom (sample-level up to full-capture), a movable cursor with
  a live time/amplitude/frequency/phase/note readout
  (`ui/cursor_readout.py`), a draggable selection region, rising/falling/
  either-edge triggering with adjustable threshold, and free-run/triggered/
  paused/replay/loop transport modes. One-Wave tag regions (Inward/Outward/
  Across/Over) and the nested Point/Path motion overlay (individual
  waveform-period ticks when zoomed in close, note-span regions from onset
  detection) draw on top of, never in place of, the raw curve, and only in
  One-Wave/Both mode.
- **Envelope** (`panels/envelope_panel.py`) — upper *and* lower boundaries
  around the center, not one positive curve, plus real attack/peak/rollover/
  decay/resolution stage markers from `envelope.py`'s actual decay-fit
  measurements.
- **Spectrum** (`panels/spectrum_panel.py`) — FFT magnitude spectrum with
  each harmonic independently peak-labeled and clickable; clicking one sets
  `state.highlighted_harmonic`, which the Phase panel reacts to.
- **Spectrogram** (`panels/spectrogram_panel.py`) — time/frequency/intensity
  image, zoomable via pyqtgraph's native wheel/drag zoom.
- **Phase** (`panels/phase_panel.py`) — wrapped phase (-π..π) of the
  fundamental and top harmonics over time (so alignment, opposition, and
  drift are directly visible), plus a circular phase display tied to the
  shared cursor.
- **Interference** (`panels/interference_panel.py`) — two source waveforms
  shown *separately*, their real sum and difference, a time-varying
  reinforcing/cancelling boundary curve, and beat frequency/stability —
  never just the finished combined waveform. Live capture in this engine is
  single-channel, so this panel drives its own adjustable two-tone demo
  sources rather than the shared recording (see "Known limitations").
- **Resonance** (`panels/resonance_panel.py`) — a persistence trail: each
  detected resonance drawn as a time-span segment at its center frequency,
  color-coded by decay rate, width-coded by persistence.
- **Modulation** (`panels/modulation_panel.py`) — envelope movement with its
  trend removed, plus separate amplitude- and frequency-modulation spectra
  (vibrato/tremolo/beating), kept on their own modulation-rate axis instead
  of mixed with the audio-rate carrier.

### Chord geometry (`chord_geometry.py`)

Follows this repo's own canonical nodes (`Nodes/Appendix_E/E-510`-`E-512`):
the complete literal root-relative coordinate set for a chord is always
computed first (`chord_coordinates`, matches E-511's worked examples
exactly — Major `{0,+4,-5}`, Augmented `{0,+4,-4}`, etc.). A separate,
explicitly-labeled `envelope_boundary` function checks that coordinate
set's outer boundary against four named two-value geometries — this is the
canon's own *retired* "Oscillation Window" representation, kept only as a
derived overlay, never as a replacement for the literal set, and only
reported when it actually matches (a canonical Major triad's boundary is
`(-5,+4)`, which matches none of the four named shapes, and the module
does not force one).

## What the DSP core does (headless, fully tested)

Point a signal at it and it maps out everything measurable about that wave:
oscillation speed (frequency), physical wavelength, octave/note, harmonics,
resonance, envelope life-cycle, and how it interferes or beats against other
waves — see `wave_map.py` and `prediction.py`.

- Ring buffer, trigger engine, FFT/pitch/harmonic/envelope/phase analysis
- Wavelength: `lambda = speed_of_sound / f`, temperature-adjustable speed
  of sound (`wavelength.py`)
- Spectrogram, resonance detection with ring-down analysis and a
  caller-supplied classification hook, chord/interval analysis (N-note
  harmonic-sieve detection, shared harmonics, beat/intermodulation
  candidates, roughness)
- Interference analysis: sum/difference, frequency-dependent cancellation/
  reinforcement, beat detection, constructive/destructive scoring, and the
  N-note isolated-vs-combined residual comparison workflow (record every
  note, then the real chord, then see how they differ from a plain linear
  sum)
- `prediction.py`: forecasts beat frequencies, harmonic collisions,
  roughness, and interference scores for N isolated notes *before* any
  combined recording exists, purely from linear superposition
- `fretboard.py`: a (string, fret) registry for "record every note on the
  neck," turning a chord shape into the isolated-signal list either of the
  above needs
- Cycle objects with Point/Path/Field tagging and modulation-spectrum
  detection, and the four One-Wave interpretive views (Inward/Outward/
  Across/Over) as a configurable, evidence-linked rule engine kept
  strictly separate from objective measurement
- Calibration profiles — dBFS is always available; volts/SPL conversion
  refuses to run without an active `CalibrationProfile`
- WAV read/write (including 32-bit float, which the stdlib `wave` module
  can't write), session/note-event JSON schema, a `Recorder` that never
  overwrites an existing recording

`device_manager.py` wraps `sounddevice`/PortAudio for real device listing
and live capture, matching the `RingBuffer` interface above — but it
**requires real audio hardware to test** and has not been run against one.

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

# Run the full instrument
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
├── chord_geometry.py       Nodes/Appendix_E E-510/511/512 — literal chord
│                          coordinates + derived envelope-boundary overlay
├── wave_map.py             unified per-signal report: frequency, wavelength,
│                          octave/note, harmonics, resonance, rotational
│                          envelope (Cycle tree), One-Wave tags, optional
│                          interference vs. a second signal
├── wav_io.py             Section 2.1/21.1 — RIFF/WAV read/write (PCM16/24/32, float32/64)
├── session.py            Section 7.2/7.3, 21.3 — session + note-event schema
├── recorder.py           Section 7 — ties the above together, hardware-independent
├── device_manager.py     Section 3.2/5 — sounddevice capture (needs real hardware)
├── cli.py                End-to-end DSP demo (MVP items 6-14, Section 26)
├── gui.py                 Entry point (python -m onewave_mapper.gui [--simple])
└── ui/
    ├── analysis_state.py         shared timeline/cursor/selection/mode --
    │                             the single source of truth every panel reads
    ├── cursor_readout.py         time/amplitude/frequency/phase/note at a
    │                             sample index (pure function, no Qt)
    ├── mapper_window.py          assembles all panels into one tabbed window
    ├── oscilloscope_window.py    Section 6/20 — original single-panel scope
    ├── live_sources.py           synthetic (tested) and hardware (untested) sources
    └── panels/
        ├── waveform_panel.py      raw waveform, zoom/pan/cursor/selection/
        │                         trigger/transport, One-Wave + Point/Path overlays
        ├── envelope_panel.py      upper/lower boundary, life-cycle stage markers
        ├── spectrum_panel.py      FFT + independently clickable harmonic peaks
        ├── spectrogram_panel.py   time/frequency/intensity image
        ├── phase_panel.py         per-harmonic phase vs. time + circular display
        ├── interference_panel.py  two sources, sum, difference, beat, boundary
        ├── resonance_panel.py     persistence trail
        └── modulation_panel.py    AM/FM spectra, envelope movement
```

`recorder.py` never overwrites an existing recording (Section 2.1).
Objective measurement (metering, FFT, pitch, harmonics, phase, envelope,
wavelength) lives entirely separately from any One-Wave interpretive
tagging (Section 2.3) — `NoteEvent.one_wave_tags` and `WaveMap`'s tags are
deliberately plain, user-editable lists, not something baked into the
measurement itself.

## Testing

269 tests in `tests/`, including direct implementations of every Section
24.3 acceptance test (`test_acceptance_*`) and offscreen-Qt smoke tests for
every panel plus the assembled `MapperWindow`
(`test_analysis_state.py`, `test_waveform_panel.py`, `test_envelope_panel.py`,
`test_spectrum_panel.py`, `test_spectrogram_panel.py`, `test_phase_panel.py`,
`test_interference_panel.py`, `test_resonance_panel.py`,
`test_modulation_panel.py`, `test_mapper_window.py`, `test_gui_smoke.py`).
Run `pytest -q` from this directory.

## Known limitations

- **No real hardware, and no real screen.** `device_manager.py` and
  `ui/live_sources.py`'s `HardwareSource` are written but unverified.
  Everything GUI-related has only ever been proven against Qt's offscreen
  platform in this container.
- **The engine is single-channel end to end** (`RingBuffer`,
  `AnalysisState`, `SyntheticSource` all carry one channel). There is no
  stereo/spatial panel, and no multi-mic capture path — Section "Stereo and
  spatial view" is not implemented. Real stereo would need multichannel
  capture threaded through `RingBuffer` and `AnalysisState` first.
- **The Interference panel doesn't share the main recording.** It drives
  its own two adjustable synthetic tones rather than two channels of the
  shared `AnalysisState`, because that state only holds one channel. A real
  two-mic (guitar DI + amp mic, say) workflow needs the stereo work above.
- **Cross-panel harmonic highlighting is Spectrum ↔ Phase only.**
  `state.highlighted_harmonic_changed` exists and both panels honor it;
  Spectrogram, Interference, and Resonance don't yet react to it. Adding a
  reaction to each is mechanical (they already redraw from the same state)
  but not done.
- **Only Point and Path rotation actually render.** Field Rotation has a
  toggle and a state flag (`show_field_rotation`) but nothing draws yet —
  Field-level structure (a chord's whole interference field, a multi-mic
  room response) needs multiple simultaneously-analyzed sources, which the
  single-channel `AnalysisState` doesn't carry today.
- **No continuous live streaming across the heavy panels.** `MapperWindow`
  loads a captured recording (synthetic here) and analyzes it — it doesn't
  yet re-run the spectrogram/resonance/phase analysis on a timer the way
  the simpler `--simple` oscilloscope's envelope panel does; recomputing
  those every frame needs a performance pass that should happen against
  real hardware, not guessed at here.
- **Ring buffer uses a coarse lock, not lock-free SPSC.** Fine for
  prototyping; the production C++ audio callback (Section 2.4) must use a
  real lock-free structure.
- **No SQLite session store, only JSON.**
- **Resonance classification is `"unknown"` by default**, with a
  caller-supplied `classifier` hook but no built-in one — frequency range
  alone isn't a reliable basis for "body" vs. "room" vs. "pickup" without a
  characterized setup. `coherence_score` is `None` until a second channel
  exists.
- **Blind delay estimation struggles on dense, harmonically-overlapping
  chords** (e.g. a full open-E six-string chord); see
  `test_compare_isolated_vs_combined_n_dense_chord_is_a_documented_hard_case`.
  A triad's delays recover precisely (tested).
- **`chord.detect_pitches` degrades on closely-spaced/overlapping notes**
  for the same underlying reason. Recovers a clean triad (tested).
- **`prediction.py` is a purely linear forecast** — no amplifier/pickup
  nonlinearity, string coupling, or room effects. That gap is exactly what
  `compare_isolated_vs_combined_n`'s residual measures once a real
  recording exists.
- **`chord_geometry.envelope_boundary`'s four named shapes are checked for
  an exact match, not assumed** — most real chords/roots/voicings won't
  match any of them, by design (see "Chord geometry" above).
- **`pink_noise()` is a Voss-McCartney approximation**, not a calibrated
  1/f reference.
- **Wavelength assumes a fixed, overridable speed of sound** — this engine
  has no way to measure the actual propagation medium.

## Next five implementation tasks

1. Run it for real: install on a machine with a microphone/interface and a
   display, confirm `device_manager.py`/`HardwareSource` actually capture
   live audio, and get a first real (non-offscreen) screenshot.
2. Multichannel `AnalysisState`/`RingBuffer` so the Interference panel can
   show two real captured channels (DI + mic, or two mics) instead of its
   synthetic demo, and so a Stereo/spatial panel becomes possible at all.
3. Wire `state.highlighted_harmonic_changed` into the Spectrogram,
   Interference, and Resonance panels (mechanical, given they already
   redraw from shared state), and add a Field Rotation renderer once
   multichannel state (task 2) gives it something real to group.
4. A fretboard-driven session workflow: use `fretboard.py` plus
   `Recorder`/`Session` to actually walk the neck, save each note, then
   feed a chord shape's `signals_for_chord()` into both
   `prediction.predict_interaction` (before playing the chord) and
   `interference.compare_isolated_vs_combined_n` (after recording the real
   strum) — load the results straight into `MapperWindow` via
   `load_recording()`.
5. Tighter harmonic peeling in `chord.detect_pitches` (partial removal
   weighted by expected amplitude rolloff instead of full zeroing) and a
   documented failure mode when `min_separation_hz` can't be met, aimed at
   the same dense-chord limitation `compare_isolated_vs_combined_n` has.
