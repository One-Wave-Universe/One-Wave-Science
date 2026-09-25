# Research Strategy

## Significance

The repository currently contains a large set of interrelated hypotheses spanning continuous-medium physics, state recurrence, associative memory, control logic, and low-voltage hardware. The scientific risk is high, but so is the value of a rigorous test program because the current claims are explicit enough to be falsified.

The project therefore emphasizes infrastructure for discrimination rather than advocacy for a predetermined outcome.

## Innovation

The program combines several features that are usually separated:

- circuit-level numerical validation;
- hypothesis matrices;
- AI-assisted repository maintenance;
- experimental state-machine hardware;
- direct signal acquisition;
- cross-domain model comparison;
- explicit preservation of failed hypotheses.

The innovation claim is methodological first: a unified, traceable workflow from speculative claim to executable test to durable evidence.

## Approach

### Work Package 1 — Reproducible simulation core

Inputs:
- `chapters/05_Simulation_Engine.md`
- Virtual Breadboard validated solver stack
- `docs/verification/V1_VERIFICATION_MATRIX.md`

Outputs:
- command-line or application entry points;
- test fixtures;
- control/hypothesis pairs;
- parameter receipts;
- result JSON/CSV;
- plots and hashes.

### Work Package 2 — Instrument qualification

Inputs:
- `https://github.com/One-Wave-Universe/Builds/blob/main/hardware/wave_reader_v1.md`

Outputs:
- qualified acquisition chain;
- calibration files;
- noise/bandwidth measurements;
- reproducible capture procedure;
- known limitations.

### Work Package 3 — CELL_V1 minimal physical experiment

Inputs:
- current CELL_V1 anti-drift and build packet;
- VTC-0 mapping;
- Wave Reader.

Outputs:
- one frozen test schematic;
- one control configuration;
- one experimental configuration;
- repeatability data;
- measured thresholds and drift;
- explicit no-go conditions.

### Work Package 4 — Cross-domain quantitative test

Select one claim only after the variables can be defined without metaphor.

Candidate priority:
1. continuous-medium propagation;
2. associative-memory benchmark;
3. normalized threshold/release model;
4. ATP-linked extra observable.

### Work Package 5 — External-review release

Outputs:
- methods;
- data;
- scripts;
- schematics;
- plots;
- negative-results register;
- reproducibility guide;
- proposal-facing evidence summary.

## Statistical and computational discipline

Where statistical inference is used:
- define the primary metric before inspection of final results;
- report effect size and uncertainty, not only thresholded significance;
- preserve raw data;
- distinguish exploratory from confirmatory analysis;
- avoid reusing the same data for model invention and final validation without disclosure.

## Decision logic

The project is milestone-driven. Each work package has a go/no-go gate.

A failed hypothesis does not fail the project if the experiment is valid and informative. A failed instrument, irreproducible simulator, or undefined comparator does block downstream claims.
