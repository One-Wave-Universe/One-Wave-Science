# Stage 00 — Universal State Container

This is the bottom of the simulation ladder.

It is not a particle and not yet a lattice. It is the smallest reusable container that can hold a physical or simulated state around a declared reference and attach real measurements to it.

## Core state

Every container may carry:

- id
- time
- reference / center
- signed value or displacement
- amplitude
- phase
- frequency / rate
- direction / orientation
- position
- velocity
- acceleration
- energy-like quantities
- uncertainty
- units
- history / previous state
- links to neighbors
- source metadata
- provenance

Fields may be null. The container does not invent values.

## Three layers

1. **STATE** — what the simulator currently says exists.
2. **MEASUREMENT** — what was observed or imported, with units and uncertainty.
3. **PROVENANCE** — where the measurement came from, including dataset, detector, event, version, DOI/record id, file, and time.

This lets one simulator use synthetic data, CERN Open Data, GWOSC data, or later astronomical data without confusing observation with model state.

## Stage-00 dynamics

The first runnable behavior remains a center-referenced oscillator:

x(t) = A cos(ωt + φ)

That oscillator is only one possible process attached to the container. The container itself is more general.

## Promotion rule

A later simulator may add:
- coupling
- neighbors
- geometry
- fields
- interaction laws
- conservation rules

but it must still be able to export its state back into this common container schema.

## Metadata grounding

GWOSC event metadata includes event/version identity, GPS time, catalog/run, detectors, parameter links, timelines, and strain-file links. Strain files expose detector, start time, sample rate, duration, and file format.

CERN Open Data records describe datasets with metadata such as event/file counts, detector conditions, production identifiers, trigger/configuration information, and record-level provenance. Event formats such as NanoAOD then carry per-event scalars and arrays of physics quantities.

The container therefore supports both:
- one value per event/state
- arrays / channels / detector-linked measurements

## Scientific rule

Metadata tells us what was measured and how it was recorded. It does not, by itself, establish a new physical law. The simulator keeps reference physics, measured data, and One-Wave hypotheses distinguishable.
