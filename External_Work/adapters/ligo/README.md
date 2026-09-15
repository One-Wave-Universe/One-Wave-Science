# LIGO Adapter

This adapter normalizes calibrated gravitational-wave detector observations and their metadata. It does not infer a new physical mechanism.

## Inputs

- Calibrated strain series, typically represented as \(h(t)\).
- Detector identifier and time basis.
- Sample rate, calibration/release identifier, data-quality information, and segment bounds.
- Optional provenance for conditioning products such as PSD estimates or gating.

## Required controls

Every proposed feature must be evaluated with the same procedure on: event/on-source data, off-source segments, and time-shifted or otherwise defined background controls. Parameter fitting must occur before held-out evaluation.

## Output

`normalize_ligo_observation()` emits a `NormalizedObservation` suitable for a declared transform such as whitening, time-frequency decomposition, or a One Wave hypothesis-derived mapping.
