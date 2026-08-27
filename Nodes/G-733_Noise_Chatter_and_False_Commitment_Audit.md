# G-733 — Noise, Chatter, and False-Commitment Audit

**Status:** YELLOW deterministic audit / physical noise model open  
**Dependencies:** B-216, G-730, G-731

## Audit model

A seeded Monte Carlo control observes a fixed latent commitment through
independent Gaussian noise. The hysteretic five-state readout is compared with
a memoryless entry-threshold readout using identical observations.

This is an instrument/control audit. Independent Gaussian samples are not yet
claimed to represent the physical One-Wave noise spectrum.

## Partial-threshold result

For true latent commitment `q=0.45`, 512 samples per trial, and 128 trials:

| noise sigma | mean hysteretic transitions | mean memoryless transitions | reduction |
|---:|---:|---:|---:|
| 0.01 | 0.000 | 0.000 | no chatter in either |
| 0.03 | 0.000 | 46.461 | 100.0% |
| 0.05 | 0.313 | 136.195 | 99.77% |
| 0.08 | 17.797 | 199.195 | 91.07% |
| 0.12 | 72.180 | 229.281 | 68.52% |

Hysteresis therefore works as intended near the partial threshold, but its
benefit degrades as noise approaches the width of the hysteresis band.

## False full-entry result

For `q=0.70`, below the default full-entry threshold `0.82`, the probability of
at least one full-entry event during a 512-sample trial was:

| noise sigma | full-entry probability |
|---:|---:|
| 0.01 | 0.0000 |
| 0.03 | 0.03125 |
| 0.05 | 1.0000 |
| 0.08 | 1.0000 |
| 0.12 | 1.0000 |

This is a multiple-opportunity effect: even a modest single-sample tail becomes
likely when hundreds of samples can trigger entry. Hysteresis controls exits
and re-entry chatter; it does not by itself validate a threshold excursion.

## Required controller correction

Full commitment must add at least one of:

- minimum dwell time beyond the full-entry threshold;
- `k-of-n` confirmation;
- filtered latent evidence with declared bandwidth;
- sequential probability/evidence-ratio test;
- phase-coherent confirmation across multiple receipts.

The selected mechanism must publish false-open probability, detection delay,
false-close probability, and correlated-noise sensitivity.

## Executable authority

- `One_Wave_Bench/logic_core/noise_hysteresis_audit.py`
- `One_Wave_Bench/logic_core/test_noise_hysteresis_audit.py`
- public deterministic readout in `commitment_map.py`

The logic suite contains forty-five passing tests. B5 remains open for delay,
correlated noise, quantization, and first-passage analysis.
