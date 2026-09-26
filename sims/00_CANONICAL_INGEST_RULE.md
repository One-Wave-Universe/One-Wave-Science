# External Measurement Ingest — Canonical No-Particle-Assumption Rule

This file locks the ingest rule for One-Wave Science simulators.

## Core rule

External scientific data enters as **measurement / excitation / detector-response data first**.

Do not promote a reconstructed object label into a fundamental ontology.

Names such as electron, muon, proton, antiproton, jet, hadron, neutron star, black hole, or gravitational wave may be retained as:
- source metadata
- experiment-provided reconstruction labels
- comparison categories
- reference-model interpretations

They are not required primitives of the One-Wave simulator.

## Canonical ingest layers

1. RAW MEASUREMENT
   - detector channel / sensor
   - coordinates
   - timestamp
   - amplitude / energy / strain / signal
   - sample rate / bandwidth
   - uncertainty / quality flags
   - run / event / file provenance

2. EXCITATION STATE
   - signed deviation from declared reference
   - amplitude-like magnitude
   - direction / orientation where measured
   - phase-like coordinate only when defined from measurement or geometry
   - time history

3. POINT
   - one localized measurement/excitation sample

4. PATH
   - ordered relation through time, geometry, or detector layers

5. FIELD
   - aggregate spatial/temporal excitation state

6. SCALE STACK
   - reversible 2^n octave transforms
   - raw values preserved
   - amplitude and geometry scaling controlled independently

7. REFERENCE INTERPRETATION
   - experiment-provided particle/object/event labels
   - standard-model / GR / detector reconstruction outputs
   - kept for comparison, never silently substituted for raw measurement

## Octave scaling

For integer octave n:

scale(n) = 2^n

Raw source measurements remain immutable.

Derived amplitude:
A_n = A_0 * 2^n

Derived geometry, when explicitly enabled:
r_n = r_0 * 2^n

All normalized descriptors must be tested for persistence across selected octaves and against controls.

## Controls

At minimum:
- shuffled phase/angle
- coordinate reflection
- event mixing
- detector/sensor acceptance
- noise/background where supplied
- conventional reconstruction/reference model

A One-Wave pattern is not evidence of a new physical relation unless it survives these controls.
