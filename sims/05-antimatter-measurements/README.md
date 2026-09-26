# Stage 05 — Antimatter Measurement Adapter

Purpose: accept measurements from CERN antimatter experiments without requiring particle identities as simulator primitives.

## Raw measurement classes

Depending on public availability:
- trap oscillation frequencies
- cyclotron / axial / magnetron frequency measurements
- spectroscopy frequency scans
- magnetic field values
- detector hit/count time series
- annihilation-position distributions
- timing coincidences
- apparatus state and uncertainty

## One-Wave representation

Each scalar or time-series measurement becomes:
- reference
- signed deviation
- amplitude
- temporal position
- detector/apparatus channel
- uncertainty
- provenance

Spatial detector measurements additionally become POINT samples.

Sequences become PATHS.

Distributed detector responses become FIELD states.

## Octave scaling

Frequency-domain data is naturally compared by octave:

f_n = f_0 * 2^n

Amplitude and geometry scaling remain separate optional derived transforms.

## Interpretation boundary

Terms supplied by experiments such as antiproton, antihydrogen, proton, positron, transition, spin state, or annihilation are retained in source metadata and reference-comparison layers.

They are not mandatory primitives of the One-Wave representation.
