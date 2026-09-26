# Stage 03 — Field

Stage 03 turns many Stage-01 excitation points and Stage-02 paths into an event-wide field description.

## No particle requirement

The field is computed directly from measured detector excitations and geometry.

## Field quantities

For a chosen spatial binning:

- scalar excitation density
- weighted vector resultant
- radial profile
- angular profile
- gradient estimate
- symmetry / imbalance
- directional coherence
- detector-subsystem contribution
- path density
- octave-persistence score

## Octave stack

For n in a selected range, for example -4..+4:

- preserve raw data
- compute scale factor 2^n
- optionally scale amplitude
- optionally scale geometry
- recompute normalized field descriptors
- compare descriptors across octaves

The octave stack is a family of views of the same event, not duplicated measurements.

## Persistence test

For normalized descriptor F_n at octave n:

compare F_n against F_0.

Features that persist under reversible scale changes are marked scale-stable.

Features that disappear or are created only by the transform are marked transform-dependent.

## Controls

Always compare against:

- randomized azimuth
- coordinate reflection
- event mixing
- detector acceptance map
- conventional reconstruction summaries

## Goal

Stage 03 should answer:

Can the same detector event be represented as a coherent point -> path -> field structure, and which parts of that structure survive scale transformation and controls?
