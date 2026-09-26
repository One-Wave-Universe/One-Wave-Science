# Stage 04 — GWOSC Strain → One-Wave Temporal Field

Input is calibrated detector strain h(t), not compact-object labels.

## Raw state

For each detector sample:

- detector: H1 / L1 / V1 / K1 when available
- GPS time
- h(t)
- sample rate
- data-quality flags
- source file/version

## One-Wave transform

Reference:
h_ref = 0 unless the source product defines another baseline.

Signed excitation:
q(t) = h(t) - h_ref

At each sample:
- amplitude = |q(t)|
- sign = sign(q(t))
- temporal direction = dq/dt
- local phase may be derived only from an explicitly documented analytic-signal or Fourier transform

Do not invent phase from sign alone.

## Path

One detector's ordered strain samples form a temporal path.

## Field

Multiple detectors form a distributed measurement field when aligned in time.

Cross-detector relations:
- lag
- correlation
- coherence
- amplitude ratio
- phase difference where transform-defined

## Octave analysis

Frequency octaves are physical analysis bands:

f_n = f_0 * 2^n

Keep this separate from arbitrary amplitude scaling.

Compare:
- band-limited energy
- coherence
- lag
- waveform morphology
- scale-normalized persistence

## Reference interpretation

GWOSC catalog labels and published source-parameter estimates remain comparison metadata.

The One-Wave simulator consumes strain first.
