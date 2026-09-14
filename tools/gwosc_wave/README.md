# GWOSC / LIGO -> Wave Analysis Pipeline

Status: **YELLOW tooling / direct wave source / One-Wave mechanism not inferred**

## CORE-RULES-PRE

Before changing this pipeline, read:

- `CORE_RULES_LOCK.md`
- `MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md`
- `MATH_BACKBONE/31_gwosc_strain_wave_analysis_v1.md`

The source is already wave data: calibrated detector strain `h(t)`. Do not relabel ordinary Fourier analysis as proof of a new field mechanism.

## Source

Gravitational Wave Open Science Center:

```text
https://gwosc.org/
https://gwosc.org/api/v2/
```

GWOSC's public API can resolve event metadata and strain-file URLs without authentication.

The first live test uses:

```text
GW150914-v2
H1 + L1
32 seconds
4 kHz
TXT.GZ strain files
```

Version 2 is used rather than the earliest release because GWOSC documents that it corrected a phase error in the earlier 4 kHz files.

## Run

From repository root:

```bash
python3 tools/gwosc_wave/gwosc_strain_wave.py \
  --event-version GW150914-v2 \
  --detectors H1,L1 \
  --sample-rate-khz 4 \
  --duration 32 \
  --window-seconds 4 \
  --band-min-hz 20 \
  --band-max-hz 512 \
  --output /tmp/gw150914-wave.json
```

To retain the exact downloaded compressed source files locally:

```bash
python3 tools/gwosc_wave/gwosc_strain_wave.py \
  --event-version GW150914-v2 \
  --detectors H1,L1 \
  --sample-rate-khz 4 \
  --duration 32 \
  --window-seconds 4 \
  --band-min-hz 20 \
  --band-max-hz 512 \
  --raw-dir /tmp/gwosc-source \
  --output /tmp/gw150914-wave.json
```

The receipt records SHA-256 checksums for downloaded source files whether or not `--raw-dir` is used.

## What is derived

For each detector separately:

- source URL and SHA-256;
- GPS start and event-centered analysis interval;
- sample count check;
- mean strain before mean subtraction;
- RMS strain;
- peak absolute strain;
- Hann-windowed one-sided raw periodogram;
- amplitude spectral density derived from that periodogram;
- declared-band integrated power;
- declared-band spectral centroid;
- strongest raw spectral bins.

These outputs are `DIRECT_STRAIN_PLUS_STANDARD_SIGNAL_DERIVED`.

## What is not done yet

This first pipeline does not perform:

- whitening;
- matched filtering;
- Bayesian parameter estimation;
- detector calibration reconstruction;
- glitch subtraction;
- antenna-pattern inversion;
- sky localization;
- source waveform fitting;
- claims of non-standard propagation.

Those require separate versioned math and validation.

## How an AI should use it

For any proposed One-Wave gravity/propagation claim, write:

```text
GWOSC SOURCE:
DETECTOR(S):
SOURCE STRAIN INTERVAL:
STANDARD GR / PUBLISHED TARGET:
ONE-WAVE EQUATION:
PREDICTED STRAIN/TIMING/PHASE QUANTITY:
FREE PARAMETERS:
NOISE / CALIBRATION CONTROL:
TEST:
RESULT: PASS / FAIL / OPEN
```

Good pressure tests include:

- H1/L1/V1 relative timing;
- chirp frequency evolution;
- propagation dispersion bounds;
- phase consistency;
- waveform residuals after comparison to a declared standard waveform;
- source-parameter scaling across many events.

Do not use a single pretty FFT peak as a theory test.

## Unit tests

```bash
PYTHONPATH=tools/gwosc_wave \
python3 -m unittest -v tools/gwosc_wave/test_gwosc_strain_wave.py
```

The synthetic sine test verifies that the FFT/periodogram path recovers a known frequency bin before live detector data are used.

## Jetson

This tool uses only the Python standard library. It is intended to run unchanged on the Jetson once the existing Hive Pipe relay credentials are restored.

No OpenClaw dependency is required. OpenClaw can later orchestrate runs, compare receipts, or launch follow-up analyses, but source analysis must remain reproducible without the agent.

## CORE-RULES-POST

After each update verify:

- direct GWOSC strain remains distinguishable from derived analysis;
- detector streams remain separate;
- source URL and checksum remain attached;
- preprocessing choices remain explicit;
- failed/noisy results remain visible;
- no raw spectral line is promoted into an astrophysical or One-Wave mechanism without controls;
- any One-Wave prediction is compared to the same accepted strain target;
- drift detected: state YES or NO.
