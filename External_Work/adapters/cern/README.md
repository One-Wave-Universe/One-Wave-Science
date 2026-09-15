# CERN Adapter

This adapter normalizes collision-event metadata and reconstructed observables without equating an event record to a physical wave. A later transform may encode the event as a field, but that representation remains an explicit modeling choice.

## Inputs

- Dataset and reconstruction release.
- Run, luminosity block, and event identifiers where available.
- Object collections and declared units/frame.
- Selection criteria, uncertainties, and detector/reconstruction context.

## Output

`normalize_cern_event()` emits `NormalizedObservation`. It preserves an event's supplied observables and records the collection semantics. It does not fabricate unmeasured continuous trajectories or phase.

## Validation principle

A field encoding must be judged against conventional representations—histograms, graph encodings, images, or established reconstruction outputs—on a predeclared task and held-out event set.
