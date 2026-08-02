# One-Wave Mapper

Live Guitar, Microphone, Oscilloscope, Spectrum, Resonance, and Interference Analysis Workstation

> **Scope note:** This is an audio-frequency oscilloscope, not a replacement for an electrical bench oscilloscope. It can precisely analyze what reaches the mixer or interface, but it must report dBFS until the input is properly calibrated — see Section 4.2.

---

## 1. Project Objective

Build a desktop application that captures live audio from:

- A microphone connected directly to the computer
- A USB microphone
- A guitar connected through an audio interface
- A guitar or microphone routed through a USB mixer
- Multiple mixer or interface channels simultaneously
- Imported WAV, FLAC, AIFF, and other uncompressed or lossless audio files

The application must combine the useful functions of:

- A digital audio oscilloscope
- A multichannel audio recorder
- A spectrum analyzer
- A spectrogram
- A phase and stereo analyzer
- A note and chord analyzer
- A harmonic tracker
- A resonance analyzer
- An interference and beating visualizer
- A waveform comparison laboratory
- A nested-cycle mapper

The first use case is analyzing isolated guitar notes. The second is comparing two-note intervals. The third is analyzing chords and complex resonance structures.

The application must prioritize measurement quality, synchronization, reproducibility, and preservation of the original captured signal.

---

## 2. Core Engineering Principles

### 2.1 Preserve the original signal

Every recording must save the untouched input samples before any filtering, normalization, resampling, noise reduction, or analysis.

Derived views must reference the original recording using exact sample indices.

Never overwrite the source audio.

### 2.2 Synchronize all views

The following displays must use the same time cursor and selected sample range:

- Oscilloscope waveform
- Spectrum
- Spectrogram
- Phase display
- Harmonic tracks
- Envelope
- Pitch track
- Resonance map
- Interference map
- Modulation map
- Nested-cycle view
- Event markers

Selecting a region in one display must select the same region everywhere.

### 2.3 Separate measurement from interpretation

Store objective measurements separately from experimental One-Wave classifications.

Objective measurements include:

- Frequency
- Phase
- Amplitude
- RMS
- Harmonics
- Decay time
- Correlation
- Spectral energy
- Pitch
- Beat rate

Interpretive classifications include:

- Point Rotation
- Path Rotation
- Field Rotation
- Inward
- Outward
- Across
- Over

The program must never silently present an interpretation as a physical measurement.

### 2.4 Real-time processing must not interrupt recording

Audio capture must run on a high-priority audio thread.

File writing, visual rendering, FFT processing, and advanced analysis must run on separate worker threads.

The audio callback must never perform:

- File format encoding
- UI rendering
- Large memory allocation
- Logging to disk
- Long FFT calculations
- Machine-learning inference
- Network requests

Use lock-free or low-contention ring buffers between audio capture and analysis.

---

## 3. Recommended Application Architecture

### 3.1 Recommended production stack

Use a native desktop application.

Preferred implementation:

- C++20 or newer for audio capture and real-time DSP
- JUCE for cross-platform audio devices, application UI, MIDI support, and plug-in compatibility
- CMake for builds
- FFTW, Intel IPP, Apple Accelerate, or JUCE DSP for FFT processing
- SQLite for session metadata
- JSON for portable analysis exports
- WAV or RF64 for raw multichannel audio
- OpenGL, Metal, Direct3D, or another GPU-backed rendering layer for high-density waveform and spectrogram rendering

Initial supported operating system:

- Windows 10 and Windows 11

Later support:

- macOS
- Linux

### 3.2 Windows audio backends

Support:

- WASAPI shared mode
- WASAPI exclusive mode
- ASIO
- Windows audio input devices exposed through JUCE

ASIO is important for low-latency multichannel interfaces and USB mixers.

The application must display the active backend and report:

- Device name
- Driver type
- Input channels
- Output channels
- Supported sample rates
- Supported buffer sizes
- Current latency
- Reported device clock
- Input channel format

### 3.3 Alternative prototype stack

A faster prototype may use:

- Python
- PySide6 or PyQt
- sounddevice or PortAudio
- NumPy
- SciPy
- librosa for offline experimentation
- pyqtgraph for early waveform displays

However, Python must not be treated as the final real-time architecture unless performance tests show that it can capture, analyze, and render without dropouts.

The production version should place the real-time audio engine in C++ even if scripting or experimental analysis modules use Python.

---

## 4. Audio Input and Signal Routing

### 4.1 Supported input configurations

The input manager must support:

**Mono microphone**

One channel containing a microphone signal.

**Mono direct guitar**

One instrument input from an audio interface or USB mixer.

**Stereo input**

Two-channel recording from a mixer or interface.

**Direct guitar plus microphone**

Channel 1:

- Direct guitar or pickup signal

Channel 2:

- Microphone capturing the amplifier, acoustic body, or room

**Multichannel mixer input**

Any available input channels exposed by the interface driver.

The user must be able to:

- Enable or disable each channel
- Rename each channel
- Set channel color
- Set channel role
- Assign direct input, microphone, room microphone, pickup, amplifier microphone, or reference signal
- Monitor each channel
- Mute or solo channels
- Reverse polarity for analysis
- Apply display-only gain without changing recorded samples

### 4.2 Input calibration

The program must distinguish between:

- Digital full-scale amplitude, measured in dBFS
- Electrical voltage
- Acoustic sound pressure
- Relative amplitude

A normal audio interface does not automatically reveal the true physical voltage at its input.

Therefore:

- Display raw digital amplitude in normalized units and dBFS by default
- Only display volts when the user has performed a calibration procedure
- Only display SPL when a microphone and acoustic calibrator have been calibrated
- Store calibration profiles per device and input channel

Calibration profile fields:

```
device_id
driver_type
input_channel
sample_rate
interface_gain_setting
reference_signal
reference_voltage_or_spl
measured_digital_rms
conversion_factor
calibration_date
notes
```

Do not label the vertical oscilloscope axis as volts unless a valid calibration profile is active.

---

## 5. Audio Capture Engine

### 5.1 Required sample formats

Support:

- 16-bit PCM
- 24-bit PCM
- 32-bit integer where available
- 32-bit floating point
- 64-bit floating point internally for selected offline calculations

Preferred capture settings:

- 48 kHz at 24-bit or 32-bit float for general analysis
- 96 kHz for detailed transient and upper-harmonic inspection
- Optional 192 kHz when supported by the interface

Do not imply that higher sample rates automatically improve every measurement.

### 5.2 Channel count

Initial minimum:

- 1 to 8 simultaneous input channels

Architectural target:

- At least 32 channels

### 5.3 Buffering

Provide selectable audio buffer sizes such as:

- 32 samples
- 64 samples
- 128 samples
- 256 samples
- 512 samples
- 1024 samples
- Driver-defined values

Show:

- Input latency
- Output latency
- Total monitoring latency
- Audio callback CPU load
- Buffer underrun count
- Buffer overrun count
- Dropped sample count

### 5.4 Ring buffer

Each enabled input channel must feed a timestamped ring buffer.

The ring buffer must retain enough recent audio for:

- Live oscilloscope triggering
- Pre-trigger capture
- Spectrogram generation
- Recording startup
- Event detection

Default live history:

- 30 seconds

Configurable range:

- 5 seconds to 10 minutes, depending on memory

### 5.5 Clock and timestamps

Every audio block must be associated with:

- Session sample index
- Device sample position when available
- Host monotonic timestamp
- Wall-clock timestamp for session logging
- Channel configuration
- Active sample rate
- Buffer size
- Device state

Sample indices are the authoritative synchronization reference.

---

## 6. Digital Oscilloscope

The oscilloscope must be a serious analysis tool rather than a decorative waveform display.

### 6.1 Operating modes

**Free-run mode**

Continuously scroll or refresh without triggering.

**Auto-trigger mode**

Attempt to lock onto a trigger. Continue refreshing if no valid trigger is found.

**Normal-trigger mode**

Update only when a valid trigger event occurs.

**Single-shot mode**

Wait for one trigger, capture a defined pre-trigger and post-trigger region, and freeze.

**Recorded mode**

Inspect previously captured audio with arbitrary zoom and cursor placement.

### 6.2 Trigger types

Required:

- Rising-edge trigger
- Falling-edge trigger
- Either-edge trigger
- Level trigger
- Zero-crossing trigger
- Window trigger
- Note-onset trigger
- External-channel trigger

Later:

- Pulse-width trigger
- Dropout trigger
- Pattern trigger
- Frequency-qualified trigger
- Harmonic-phase trigger

### 6.3 Trigger controls

Provide:

- Trigger source channel
- Trigger threshold
- Trigger polarity
- Hysteresis
- Holdoff
- Pre-trigger percentage
- Post-trigger duration
- Noise rejection
- High-pass or low-pass trigger conditioning
- Auto-level button
- Trigger position
- Trigger armed indicator
- Trigger event count

Triggering must operate on either:

- Original samples
- A trigger-only filtered copy

Trigger filtering must never alter the saved source signal.

### 6.4 Timebase

Provide time-per-division or visible-window controls ranging approximately from:

- Microseconds where sample rate permits
- Individual samples
- One waveform cycle
- Milliseconds
- Seconds
- Full note duration
- Full session duration

Include:

- Horizontal zoom
- Horizontal pan
- Zoom around cursor
- Fit selection
- Fit event
- Fit recording
- Samples-per-pixel indicator

### 6.5 Vertical controls

Provide:

- Auto scale
- Manual scale
- Channel offset
- Display gain
- Normalize display only
- Overlay channels
- Stack channels
- Difference signal
- Sum signal
- Mid-side conversion
- Polarity inversion for comparison

### 6.6 Scope measurements

For the visible or selected region, calculate:

- Minimum sample
- Maximum sample
- Peak amplitude
- Peak-to-peak amplitude
- RMS
- Mean
- DC offset
- Crest factor
- Zero-crossing rate
- Positive peak
- Negative peak
- Waveform asymmetry
- Period
- Fundamental frequency
- Frequency from cursor spacing
- Rise time
- Fall time
- Attack time
- Decay time
- Clipping count
- Clipped-sample percentage
- Estimated signal-to-noise ratio

### 6.7 Measurement cursors

Provide:

- Two vertical time cursors
- Two horizontal amplitude cursors
- Delta time
- Inverse delta time
- Delta amplitude
- Sample index
- Timestamp
- Nearest zero crossing
- Nearest detected peak
- Nearest event marker

---

## 7. Recorder and Session System

### 7.1 Recording modes

Support:

- Manual record
- Triggered record
- Note-onset record
- Threshold record
- Continuous session record
- Loop record
- Punch-in region
- Pre-roll and post-roll

### 7.2 Session structure

Each session must contain:

```
Session
├── session.json
├── session.sqlite
├── audio
│   ├── raw_multichannel.wav
│   ├── optional_channel_01.wav
│   └── optional_channel_02.wav
├── analysis
│   ├── pitch_tracks
│   ├── harmonic_tracks
│   ├── envelopes
│   ├── resonance_events
│   └── interference_events
├── thumbnails
├── exports
└── logs
```

### 7.3 Session metadata

Store:

- Session ID
- Creation date
- Application version
- Operating system
- Audio device
- Driver
- Sample rate
- Bit depth
- Channel count
- Buffer size
- Latency
- Calibration profile
- Instrument
- Guitar string
- Fret
- Expected note
- Pick type
- Pick position
- Pickup selection
- Amplifier
- Microphone
- Microphone position
- Room notes
- User annotations

### 7.4 Non-destructive editing

Allow:

- Region selection
- Markers
- Labels
- Trimming views
- Loop regions
- Analysis regions
- Exclusion regions
- Event grouping

Never modify raw source samples during ordinary editing.

---

## 8. Frequency-Domain Analysis

### 8.1 FFT spectrum analyzer

Provide:

- Linear-frequency scale
- Log-frequency scale
- Musical-note scale
- Linear-amplitude scale
- dBFS scale
- Power spectral density
- Magnitude spectrum
- Phase spectrum

FFT controls:

- FFT size
- Window function
- Overlap
- Averaging
- Peak hold
- Exponential smoothing
- Linear averaging
- Frequency range
- Minimum displayed level
- Maximum displayed level

Recommended window options:

- Rectangular
- Hann
- Hamming
- Blackman
- Blackman-Harris
- Flat-top
- Kaiser

Display the tradeoff between frequency resolution and time resolution.

Calculate:

```
Δf = fs / N
```

where:

- `fs` is the sample rate
- `N` is FFT size
- `Δf` is FFT-bin spacing

### 8.2 Spectrum measurements

Provide:

- Strongest peak
- Estimated fundamental
- Harmonic frequencies
- Harmonic amplitudes
- Harmonic phase
- Spectral centroid
- Spectral bandwidth
- Spectral rolloff
- Spectral flatness
- Spectral slope
- Noise floor
- Total harmonic distortion
- Harmonic-to-noise ratio
- Inharmonicity
- Odd-versus-even harmonic energy

### 8.3 Fundamental detection

Use more than one method.

Candidate methods:

- Autocorrelation
- YIN or probabilistic YIN
- Cepstrum
- Harmonic product spectrum
- Spectral peak fitting
- Phase-vocoder frequency estimation
- Zero-crossing estimate as a secondary reference

The application should calculate confidence and disagreement between methods.

Do not force a pitch result when confidence is poor.

Pitch result fields:

```
time
frequency_hz
midi_note_float
note_name
cents_offset
confidence
method
voiced_probability
```

---

## 9. Spectrogram

### 9.1 Required controls

Provide:

- Adjustable FFT size
- Adjustable hop size
- Window selection
- Frequency range
- Dynamic range
- Linear, log, and note-oriented frequency axes
- Magnitude or power display
- Optional reassigned spectrogram
- Optional constant-Q transform
- Optional mel display for comparison
- Cursor readout
- Peak tracking overlays
- Fundamental track overlay
- Harmonic track overlay

### 9.2 Rendering

The spectrogram must:

- Scroll smoothly in real time
- Support frozen inspection
- Render large recordings without loading the entire image into memory
- Use tiled or level-of-detail rendering
- Support GPU acceleration
- Preserve exact mapping from pixels to sample ranges and frequency bins

### 9.3 Event overlays

Overlay:

- Pick attack
- Fundamental estimate
- Harmonic tracks
- Pitch drift
- Vibrato
- Noise bursts
- Resonance bands
- Beat envelopes
- Clipping
- Analysis markers

---

## 10. Note Detection and Guitar Mapping

### 10.1 Note event segmentation

Detect:

- Note onset
- Attack peak
- Attack end
- Sustain region
- Decay start
- Note offset
- Secondary attacks
- Muting event
- String noise
- Pick noise

Use a combination of:

- Spectral flux
- Energy rise
- High-frequency transient content
- Envelope derivative
- Pitch stability
- User-adjustable thresholds

### 10.2 Guitar metadata

For each note capture, support:

- String number
- Fret number
- Tuning
- Expected note
- Measured note
- Cents error
- Pickup selection
- Picking position
- Picking direction
- Fingered or open string
- Muted or natural decay
- Harmonic technique
- Capo position

### 10.3 Fretboard view

Show:

- Standard and custom tunings
- Detected note
- Possible string-and-fret positions
- Recorded samples associated with each fret
- Average pitch error
- Average decay time
- Harmonic fingerprint
- Resonance fingerprint

The user must be able to choose the actual string and fret when several positions produce the same pitch.

---

## 11. Envelope and Transient Analysis

Calculate several envelopes rather than relying on one representation.

Include:

- Absolute-amplitude envelope
- Peak envelope
- RMS envelope
- Hilbert envelope
- Band-limited envelopes
- Fundamental-only envelope
- Harmonic-specific envelopes

Measure:

- Attack time
- Attack slope
- Attack overshoot
- Peak time
- Sustain mean
- Sustain variation
- Decay rate
- Decay time to minus 20 dB
- Decay time to minus 40 dB
- Estimated RT60 when appropriate
- Multi-stage decay
- Modulation depth
- Tremolo rate
- Envelope asymmetry

Permit logarithmic and linear decay fitting.

A guitar note may not follow one simple exponential decay. Support piecewise decay models.

---

## 12. Harmonic Tracking

For a detected fundamental `f0`, examine expected harmonic locations:

```
fn ≈ n * f0
```

where `n` is the harmonic number.

Track:

- Frequency
- Amplitude
- Phase
- Decay rate
- Frequency drift
- Deviation from exact integer multiple
- Harmonic confidence
- Birth and disappearance time

Support at least:

- First 32 harmonics initially
- Up to 128 where sample rate and signal quality permit

Do not confuse spectral peaks with harmonics automatically. Classify peaks as:

- Fundamental
- Harmonic
- Subharmonic
- Intermodulation product
- Noise component
- Room or body resonance
- Unknown peak

---

## 13. Phase Analysis

### 13.1 Single-channel phase

Provide:

- FFT phase
- Unwrapped phase
- Instantaneous phase for selected bands
- Phase rotation over time
- Phase reset events
- Fundamental phase
- Harmonic phase relative to the fundamental

### 13.2 Multichannel phase

For two selected channels, calculate:

- Cross-correlation
- Delay estimate
- Phase difference by frequency
- Magnitude-squared coherence
- Polarity relationship
- Interchannel level difference
- Interchannel time difference
- Correlation coefficient
- Mid-side energy

### 13.3 Displays

Include:

- Phase-versus-frequency
- Phase-versus-time
- Lissajous display
- Goniometer
- Correlation meter
- Delay-compensated comparison
- Difference waveform
- Sum waveform

Allow the user to align channels manually or automatically.

Store the original channel timing before alignment.

---

## 14. Interference Analysis

### 14.1 Two-signal comparison

For signals `x1(t)` and `x2(t)`:

```
x_sum(t) = x1(t) + x2(t)
x_difference(t) = x1(t) - x2(t)
```

Display:

- Source A
- Source B
- Sum
- Difference
- Phase difference
- Correlation
- Frequency-dependent cancellation
- Frequency-dependent reinforcement

### 14.2 Beat analysis

For two sinusoidal components:

```
f_beat = |f2 - f1|
```

Detect and display:

- Expected beat frequency
- Measured amplitude-modulation rate
- Beat-envelope phase
- Beat stability
- Drift over time
- Harmonic-specific beat rates

### 14.3 Constructive and destructive interference

Estimate interference behavior by time and frequency.

Provide:

- Constructive-interference score
- Destructive-interference score
- Phase-alignment score
- Cancellation depth
- Reinforcement gain
- Recurrence period
- Frequency-region heatmap

Avoid claiming perfect physical separation when sources are already mixed into one microphone signal.

### 14.4 Isolated-versus-combined comparison

For chord experiments:

1. Record note A individually.
2. Record note B individually.
3. Record A and B together.
4. Time-align and level-align the individual recordings.
5. Generate the predicted linear sum.
6. Compare the predicted sum with the real combined recording.

Calculate:

```
r(t) = x_real_chord(t) - [x_A(t) + x_B(t)]
```

Analyze the residual for:

- Nonlinear amplifier behavior
- Pickup interaction
- String coupling
- Body resonance
- Intermodulation distortion
- Timing differences
- Picking differences
- Room effects

The application must label this comparison as an experiment, because exact repeatability of human picking is limited.

---

## 15. Resonance Analysis

A resonance must not be defined only as a large FFT peak.

A resonance candidate should be evaluated using:

- Frequency prominence
- Persistence
- Decay rate
- Energy concentration
- Phase stability
- Reappearance
- Cross-channel coherence
- Response after the excitation has weakened
- Comparison against neighboring frequencies

### 15.1 Resonance types

Allow classification as:

- String resonance
- Body resonance
- Pickup resonance
- Amplifier resonance
- Speaker or cabinet resonance
- Room resonance
- Sympathetic-string resonance
- Electrical hum
- Feedback resonance
- Unknown resonance

### 15.2 Resonance measurements

For each resonance event, store:

```
center_frequency_hz
bandwidth_hz
quality_factor
start_sample
end_sample
peak_level_dbfs
decay_rate_db_per_second
phase_stability
persistence_score
coherence_score
classification
confidence
notes
```

Estimate quality factor:

```
Q = fc / Δf
```

where:

- `fc` is center frequency
- `Δf` is measured bandwidth

### 15.3 Ring-down analysis

Allow the user to select an excitation and analyze the following decay.

Provide:

- Bandpass-isolated ring-down
- Envelope
- Exponential fit
- Multi-exponential fit
- Decay constants
- Frequency drift
- Phase progression

---

## 16. Modulation and Nested-Cycle Analysis

Detect slower cycles acting on faster cycles.

Analyze:

- Amplitude modulation
- Frequency modulation
- Phase modulation
- Vibrato
- Tremolo
- Beating
- Periodic pickup or picking variation
- Repeated decay fluctuations
- Low-frequency body movement
- Compressor pumping

### 16.1 Modulation spectrum

Calculate the spectrum of:

- Amplitude envelope
- Instantaneous frequency
- Instantaneous phase difference
- Harmonic amplitudes

Display modulation frequencies separately from audio-carrier frequencies.

### 16.2 Cycle object

Every detected cycle should use a common structure:

```
cycle_id
parent_cycle_id
child_cycle_ids
source_channel
start_sample
end_sample
period_samples
frequency_hz
amplitude
phase
confidence
detection_method
cycle_level
one_wave_tags
```

### 16.3 Cycle levels

**Point Rotation**

A local oscillation or repeating component.

Examples:

- Individual waveform cycle
- Harmonic phase cycle
- Speaker-cone oscillation
- Local string-motion cycle

**Path Rotation**

A cycle or recurrence traveling through a route or process.

Examples:

- Attack into sustain and decay
- Wave propagation along a string
- Signal movement through pickup, amplifier, speaker, and air
- Beat envelope developing through time

**Field Rotation**

A containing organization made of multiple cycles or paths.

Examples:

- Full string-body-room system
- Chord interference field
- Repeating harmonic organization
- Multichannel resonance field

These classifications must initially be user-editable tags rather than unquestionable automatic truths.

---

## 17. One-Wave Interpretive Views

The program must provide four experimental interpretive views over the measured data.

### 17.1 Inward

Potential indicators:

- Falling envelope
- Convergence toward equilibrium
- Destructive interference
- Compression
- Decay
- Phase convergence
- Returning or reflected energy

### 17.2 Outward

Potential indicators:

- Attack
- Increasing amplitude
- Energy emission
- Harmonic generation
- Divergence
- Pressure or electrical excursion away from equilibrium

### 17.3 Across

Potential indicators:

- Zero crossing
- Transient crossing
- Phase intersection
- Frequency-track intersection
- Direct transfer between regions or channels

### 17.4 Over

Potential indicators:

- Recurrence
- Oscillation
- Beat-envelope rollover
- Phase wrapping
- Vibrato
- Repeating decay structure

These views must be configurable rule sets.

Every One-Wave tag must link back to the measurements that produced it.

Example:

```
Tag: Over
Reason:
- 5.8 Hz repeating modulation
- confidence 0.91
- detected in fundamental amplitude envelope
- active from sample 144000 to 288000
```

---

## 18. Chord and Interval Analysis

### 18.1 Interval measurements

For two detected fundamentals `f1` and `f2`, calculate:

```
R = f2 / f1
```

Also calculate:

- Ratio approximation
- Cents interval
- Beat frequencies
- Common harmonic locations
- Harmonic collisions
- Harmonic reinforcement
- Roughness estimate
- Consonance-related descriptive metrics
- Phase recurrence period

Do not reduce the analysis to standard musical labels only.

Display both:

- Conventional note and interval names
- Raw frequency relationships

### 18.2 Chord representation

A chord event should include:

```
detected_fundamentals
candidate_notes
confidence_per_note
frequency_ratios
pairwise_intervals
shared_harmonics
beat_components
intermodulation_candidates
resonance_candidates
phase_relationships
envelope_relationships
one_wave_tags
```

### 18.3 Polyphonic pitch detection

Start with two simultaneous notes.

Later add:

- Three-note detection
- Four-note detection
- Six-string guitar chord estimation

Use:

- Spectral peak grouping
- Harmonic-sieve models
- Multi-pitch salience
- Non-negative matrix factorization where useful
- Candidate fundamental scoring

Always show confidence and permit manual correction.

---

## 19. Optional Nonlinear Analysis

For signals passing through amplifiers, pedals, or clipping stages, calculate:

- Total harmonic distortion
- Intermodulation distortion
- Added harmonics
- Compression
- Saturation curve
- Dynamic range reduction
- Odd/even harmonic balance
- Residual from predicted linear sum

For two tones `f1` and `f2`, search for products such as:

```
m*f1 ± n*f2
```

where `m` and `n` are small integers.

Mark these as possible intermodulation products, not guaranteed identifications.

---

## 20. User Interface

### 20.1 Main workspace

Recommended layout:

```
┌──────────────────────────────────────────────────────────────┐
│ Device | Sample Rate | Buffer | Record | Trigger | CPU        │
├──────────────┬───────────────────────────────────────────────┤
│ Sessions     │ Oscilloscope                                  │
│ Recordings   ├───────────────────────────────────────────────┤
│ Notes        │ Spectrogram                                   │
│ Chords       ├───────────────────────────────────────────────┤
│ Events       │ Spectrum / Phase / Harmonics                  │
│ Cycles       ├───────────────────────────────────────────────┤
│ Resonances   │ Envelope / Pitch / Modulation                 │
│ Markers      ├───────────────────────────────────────────────┤
│              │ Interference / Nested Cycles                  │
├──────────────┴───────────────────────────────────────────────┤
│ Fretboard | Point | Path | Field | Inward | Outward | etc.   │
└──────────────────────────────────────────────────────────────┘
```

### 20.2 Dockable panels

Panels must be:

- Dockable
- Resizable
- Hideable
- Saveable as workspace layouts
- Undockable to another monitor

### 20.3 Required panels

- Device setup
- Channel mixer
- Oscilloscope
- Spectrum
- Spectrogram
- Pitch
- Harmonics
- Phase
- Correlation
- Envelope
- Resonance
- Interference
- Nested cycles
- One-Wave tags
- Fretboard
- Session browser
- Event list
- Measurement table
- Logs and performance monitor

### 20.4 Navigation

Support:

- Mouse wheel zoom
- Click-and-drag pan
- Zoom selection
- Keyboard transport
- Marker shortcuts
- Snap to zero crossing
- Snap to onset
- Snap to waveform peak
- Snap to pitch period
- Linked cursors
- Undo and redo for annotations and settings

---

## 21. Data Export

### 21.1 Audio export

Support:

- WAV
- RF64 for large files
- FLAC
- Selected channels
- Selected ranges
- Original or processed copies

Never describe a processed export as the raw original.

### 21.2 Analysis export

Support:

- JSON
- CSV
- SQLite
- PNG
- SVG for suitable charts
- PDF report later

### 21.3 JSON event example

```json
{
  "event_id": "note_00017",
  "source_channel": 1,
  "start_sample": 482100,
  "end_sample": 721440,
  "sample_rate": 48000,
  "expected_note": "A3",
  "measured_frequency_hz": 219.83,
  "cents_offset": -1.34,
  "pitch_confidence": 0.97,
  "attack_time_ms": 12.4,
  "decay_20db_seconds": 2.83,
  "rms_dbfs": -18.7,
  "peak_dbfs": -5.1,
  "harmonics": [],
  "resonances": [],
  "cycles": [],
  "one_wave_tags": []
}
```

---

## 22. Performance Requirements

### 22.1 Audio reliability

Target:

- Zero dropped samples during ordinary recording
- No UI operation may stop audio capture
- Recovery from device disconnect without application crash
- Clear warning if sample loss occurs
- Sample-loss location recorded in session metadata

### 22.2 UI rendering

Target:

- At least 60 frames per second for oscilloscope movement where hardware permits
- At least 30 frames per second for complex multiview workspaces
- Smooth zooming over recordings lasting at least several hours
- Level-of-detail waveform rendering
- Background spectrogram tile generation

### 22.3 Analysis latency

Initial target at 48 kHz:

- Oscilloscope: under one audio buffer plus rendering delay
- Peak and RMS meters: under 50 ms
- Pitch estimate: under 100 ms when stable
- Live spectrum: under 100 ms
- Live spectrogram: under 200 ms
- Advanced resonance analysis may run asynchronously

---

## 23. Safety and Signal Warnings

Display warnings that:

- A guitar speaker output must never be connected directly to a computer or ordinary line input.
- Speaker-level signals require an appropriate load box, attenuator, or interface designed for them.
- Phantom power should only be enabled when the connected microphone or device supports it.
- Instrument input, line input, microphone input, and speaker output are different signal levels.
- Headphone monitoring levels can damage hearing.
- The application measures the digitized signal; it is not a high-voltage laboratory oscilloscope.
- The application must never be connected to mains electrical circuits.

---

## 24. Testing Requirements

### 24.1 Unit tests

Test:

- Ring buffer correctness
- FFT frequency accuracy
- Window functions
- RMS and peak calculations
- Trigger detection
- Pitch detection
- Harmonic assignment
- Beat-frequency calculation
- Cross-correlation
- Delay estimation
- Phase calculation
- Resampling
- File writing
- Session serialization

### 24.2 Synthetic-signal tests

Generate known test signals:

- Pure sine
- Square wave
- Triangle wave
- Sawtooth
- White noise
- Pink noise
- Two-tone beating
- Harmonic series
- Frequency sweep
- Exponential decay
- Amplitude modulation
- Frequency modulation
- Phase offset between channels
- Known delay between channels
- Clipped signals
- Signals with DC offset

Validate measured values against known values.

### 24.3 Example acceptance tests

**Frequency accuracy**

Input:

- 440 Hz sine wave

Requirement:

- Measured stable frequency within a configurable tolerance, initially ±0.1 Hz offline

**Beat detection**

Input:

- 440 Hz plus 442 Hz

Requirement:

- Detect approximately 2 Hz amplitude beating

**Phase difference**

Input:

- Identical 1 kHz signals with a 90-degree phase difference

Requirement:

- Report phase difference near 90 degrees

**Delay detection**

Input:

- Identical broadband signals with one channel delayed by 48 samples at 48 kHz

Requirement:

- Estimate approximately 1 millisecond delay

**Trigger stability**

Input:

- Stable periodic sine wave

Requirement:

- Triggered waveform remains visually locked without unnecessary horizontal jumping

### 24.4 Real-device tests

Test with:

- Built-in computer microphone
- USB microphone
- Two-channel USB interface
- USB mixer
- ASIO driver
- WASAPI shared mode
- WASAPI exclusive mode
- 44.1, 48, 88.2, and 96 kHz
- Multiple buffer sizes
- Device disconnect and reconnect
- Driver failure
- Sample-rate mismatch

---

## 25. Development Phases

**Phase 1: Reliable live oscilloscope**

Implement:

- Audio-device selection
- WASAPI input
- ASIO input
- Mono and stereo capture
- Ring buffer
- Live waveform
- Channel selection
- Timebase
- Vertical scaling
- Rising and falling edge trigger
- Trigger threshold and holdoff
- Freeze
- Single capture
- RMS, peak, frequency, and clipping
- WAV recording
- Basic session saving

This phase is complete only when the waveform remains stable and recording does not drop samples.

**Phase 2: Spectrum and spectrogram**

Implement:

- FFT spectrum
- Window selection
- FFT-size controls
- Peak detection
- Spectrogram
- Linked cursors
- Fundamental estimate
- Basic harmonic markers

**Phase 3: Guitar note analyzer**

Implement:

- Note onset detection
- Attack, sustain, and decay segmentation
- Note-name detection
- Cents deviation
- Harmonic tracking
- Envelope analysis
- Guitar string and fret metadata
- Fretboard view
- Repeat-recording comparison

**Phase 4: Multichannel phase and comparison**

Implement:

- Two-channel overlay
- Cross-correlation
- Time-delay estimate
- Phase difference
- Coherence
- Lissajous display
- Mid-side display
- Direct-guitar-versus-microphone comparison

**Phase 5: Interference and resonance laboratory**

Implement:

- Two-tone comparison
- Beat detection
- Sum and difference views
- Linear-prediction comparison
- Residual analysis
- Resonance candidates
- Ring-down analysis
- Persistence and decay metrics

**Phase 6: Nested-cycle mapper**

Implement:

- Common cycle object
- Parent-child cycle relationships
- Point, Path, and Field tags
- Modulation spectrum
- Cycle browser
- User editing
- Confidence and evidence display

**Phase 7: One-Wave views**

Implement:

- Inward
- Outward
- Across
- Over
- Configurable classification rules
- Evidence-linked tags
- Comparison across notes and chords

**Phase 8: Chord analysis**

Implement:

- Two-note polyphonic estimation
- Three-note estimation
- Frequency ratios
- Pairwise beat analysis
- Shared harmonics
- Chord-event objects
- Isolated-versus-combined experiments
- Nonlinear residual analysis

---

## 26. Minimum Viable Product Definition

The MVP must allow a user to:

1. Connect a USB mixer, audio interface, or microphone.
2. Select an input device and channel.
3. See a live, triggered oscilloscope waveform.
4. Adjust timebase, amplitude scale, trigger level, edge, and holdoff.
5. View peak, RMS, frequency, period, and clipping.
6. Record an isolated guitar note.
7. Reopen the recording.
8. Inspect the waveform sample by sample.
9. View a synchronized spectrum and spectrogram.
10. Detect the fundamental note and tuning error.
11. Display at least the first 16 harmonics.
12. Measure attack and decay.
13. Save the session.
14. Export raw WAV and JSON measurements.
15. Compare two recordings of the same guitar note.

Do not begin chord recognition until these functions are stable and tested.

---

## 27. Suggested Internal Module Structure

```
src/
├── app/
│   ├── Application
│   ├── CommandManager
│   └── WorkspaceManager
├── audio/
│   ├── AudioDeviceManager
│   ├── AudioCaptureEngine
│   ├── AudioRingBuffer
│   ├── ChannelRouter
│   ├── MonitorEngine
│   └── DeviceDiagnostics
├── recording/
│   ├── Recorder
│   ├── WavWriter
│   ├── SessionManager
│   └── RecoveryJournal
├── dsp/
│   ├── Metering
│   ├── TriggerEngine
│   ├── FFTAnalyzer
│   ├── SpectrogramEngine
│   ├── PitchDetector
│   ├── HarmonicTracker
│   ├── EnvelopeAnalyzer
│   ├── PhaseAnalyzer
│   ├── CorrelationAnalyzer
│   ├── InterferenceAnalyzer
│   ├── ResonanceAnalyzer
│   ├── ModulationAnalyzer
│   └── CycleDetector
├── models/
│   ├── Session
│   ├── AudioChannel
│   ├── NoteEvent
│   ├── ChordEvent
│   ├── HarmonicTrack
│   ├── ResonanceEvent
│   ├── Cycle
│   └── OneWaveTag
├── ui/
│   ├── MainWindow
│   ├── ScopePanel
│   ├── SpectrumPanel
│   ├── SpectrogramPanel
│   ├── PhasePanel
│   ├── EnvelopePanel
│   ├── InterferencePanel
│   ├── CycleMapPanel
│   ├── FretboardPanel
│   └── MeasurementPanel
├── rendering/
│   ├── WaveformRenderer
│   ├── SpectrogramRenderer
│   ├── PlotRenderer
│   └── LevelOfDetailCache
├── storage/
│   ├── SQLiteStore
│   ├── JsonExporter
│   └── CsvExporter
└── tests/
```

---

## 28. First Coding Assignment

Begin with a small but production-minded vertical slice.

Create a Windows desktop application that:

1. Lists available audio input devices.
2. Supports WASAPI and ASIO when available.
3. Lets the user select one device, sample rate, buffer size, and up to two channels.
4. Captures floating-point samples without blocking the audio callback.
5. Stores samples in a lock-free ring buffer.
6. Draws a live waveform using GPU-assisted rendering where practical.
7. Implements rising-edge and falling-edge triggering.
8. Provides trigger threshold, hysteresis, holdoff, and pre-trigger position.
9. Shows:
   - Peak
   - Peak-to-peak
   - RMS
   - DC offset
   - Estimated period
   - Estimated frequency
   - Clipping indicator
10. Records the original samples to a WAV file.
11. Logs dropped buffers or device errors.
12. Includes automated tests using generated sine waves.
13. Uses clean interfaces so spectrum and spectrogram modules can be added next.

Before writing large amounts of UI code, define the audio-thread ownership model, ring-buffer behavior, timestamp strategy, session format, and testing approach.

The first deliverable should include:

- Build instructions
- Architecture explanation
- Source tree
- Working code
- Automated tests
- Known limitations
- A list of the next five implementation tasks
