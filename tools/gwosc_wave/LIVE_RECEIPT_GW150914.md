# LIVE RECEIPT — GW150914-v2 H1 + L1 SOURCE-FIRST STRAIN ANALYSIS

Status: **PIPELINE PASS / DIRECT STRAIN PRESERVED / ONE-WAVE MECHANISM OPEN**

Date: 2026-09-14

## CORE-RULES-PRE

- Direct GWOSC strain is the reference.
- H1 and L1 streams stay separate.
- Source checksums and exact processing choices stay attached.
- Raw FFT/periodogram peaks are not automatically astrophysical source modes.
- One-Wave interpretation remains separate from standard signal-derived quantities.

## Live execution

GitHub Actions workflow:

```text
GWOSC Wave Pipeline Tests
```

Successful run ID:

```text
34909583870
```

Job ID:

```text
104193860664
```

Result:

```text
6 / 6 unit/synthetic tests PASS
GWOSC_TRANSFORM_PASS
```

Earlier failures remain meaningful engineering receipts:

1. the first API attempt requested a browsable representation instead of machine JSON;
2. the next attempt exposed that GWOSC's `4 kHz` file label means an exact sample rate of 4096 Hz, not 4000 Hz;
3. one later attempt timed out at the public service before metadata returned;
4. the successful run used the corrected JSON API request and exact 4096 Hz mapping.

No analysis equation was changed to rescue the result.

## Source event

```text
event = GW150914-v2
name = GW150914
catalog = O1_O2-Preliminary
run = O1
GPS event time = 1126259462.4
DOI = https://doi.org/10.7935/K5MW2F23
```

Source files are 32-second 4-kHz-label GWOSC TXT.GZ releases with actual sample rate:

```text
4096 Hz
131072 samples per detector
```

Both source sample counts matched the metadata.

## Analysis contract

```text
center = event GPS time
analysis window = 4.0 s
samples = 16384
sample rate = 4096 Hz
dt = 0.000244140625 s
df = 0.25 Hz
analysis band = 20..512 Hz
mean subtraction = yes
window = Hann
spectrum = one-sided raw periodogram
whitening = no
matched filtering = no
parameter estimation = no
```

This is deliberately a transparent raw-strain analysis, not a reproduction of the full LIGO/Virgo discovery/parameter-estimation pipeline.

## H1 receipt

Source SHA-256:

```text
f8357860261bb39859e8c92308e065ff984ccb23cc3a81f73e4b2671f1737df2
```

4-second event-centered segment:

```text
RMS strain = 2.3628526895642907e-19
peak absolute strain = 6.467412454665105e-19
20..512 Hz raw periodogram band power = 2.71737086555393e-42 strain^2
raw spectral centroid = 108.23234368130025 Hz
```

Strongest raw periodogram bin in the declared band:

```text
36.75 Hz
ASD = 1.5842761538962648e-21 / sqrt(Hz)
PSD = 2.509930931804341e-42 strain^2 / Hz
```

Other strong raw bins include approximately 35.75, 36.0, 36.5, 37.0, 60.0, 331.75/332.0, and 501.5..502.0 Hz.

These are **raw detector-spectrum features**, not automatically GW150914 source frequencies. Noise lines and instrumental features must be controlled before physical interpretation.

## L1 receipt

Source SHA-256:

```text
3da578c84a05393c2bd1d130c0e680b4c0f86dc9777588ac7c898ed317f8ec9b
```

4-second event-centered segment:

```text
RMS strain = 2.5454276076185333e-19
peak absolute strain = 7.193576388434842e-19
20..512 Hz raw periodogram band power = 2.598065198086397e-40 strain^2
raw spectral centroid = 503.11740575211263 Hz
```

Strongest raw periodogram bin in the declared band:

```text
509.5 Hz
ASD = 1.2941949574537729e-20 / sqrt(Hz)
PSD = 1.674940587898773e-40 strain^2 / Hz
```

The strongest raw L1 bins cluster near roughly 499.5..511 Hz in this unwhitened segment. That concentration is a warning that the raw spectrum is dominated by detector/instrument structure and must not be mislabeled as the astrophysical chirp.

## What this establishes

PASS:

- GWOSC event metadata resolves programmatically;
- exact H1/L1 public strain files download;
- source checksums are preserved;
- the 4-kHz label is correctly interpreted as 4096 Hz;
- 4-second event-centered windows contain 16384 samples;
- pure-stdlib FFT/periodogram calculations run reproducibly;
- H1/L1 direct strain and derived descriptors remain separate.

OPEN / YELLOW:

- whitening/noise-model pipeline;
- matched-filter comparison to standard GR waveform templates;
- H1/L1 timing/phase reconstruction;
- chirp-track extraction;
- propagation/dispersion residuals;
- any One-Wave gravity/field mechanism.

## Next hard test

The useful next LIGO test is **not** searching raw peaks for a One-Wave pattern.

It is:

```text
source H1 + L1 strain
-> established noise/whitening control
-> published/standard GW150914 waveform target
-> One-Wave predicted waveform or propagation correction
-> residual comparison
-> PASS / FAIL / OPEN
```

If One-Wave has no independent predicted waveform/phase/timing rule yet, status remains OPEN.

## CORE-RULES-POST

- Direct GWOSC strain remained the reference.
- Source checksums and exact sample rates were preserved.
- H1/L1 were not merged into one invented waveform.
- Preprocessing choices are explicit.
- Raw spectral peaks were not promoted as source modes.
- Earlier implementation failures were preserved rather than hidden.
- No One-Wave claim was promoted by the successful pipeline.
- Math remains explicit in `MATH_BACKBONE/31_gwosc_strain_wave_analysis_v1.md`.
- Drift detected: no.
