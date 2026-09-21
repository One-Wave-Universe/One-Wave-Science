# Specific Aims

## Overall objective

Build and execute a reproducible experimental program that can verify, revise, or dismiss the highest-value One-Wave V1 claims.

## Aim 1 — Establish the simulation and control baseline

Create a single reproducible BASIS/Virtual Breadboard workflow for:
- analytic and numerical controls;
- hypothesis variants;
- fixed parameter receipts;
- deterministic or seeded reruns;
- standardized PASS / FAIL / INCONCLUSIVE / INVALID outcomes.

### Success criteria
- every V1 simulation test has an executable entry point;
- every run records parameters, version, outputs, and acceptance criteria;
- at least the initial lattice, memory, and VTC software tests can be independently rerun.

## Aim 2 — Build and qualify Wave Reader V1

Construct a measurement-first acquisition system using the proposed ADC/front-end path or a documented substitute if qualification fails.

### Success criteria
- known calibration waveforms are captured within declared amplitude/frequency tolerances;
- actual sample rate, bandwidth, noise floor, common-mode range, and reference stability are measured;
- raw data and metadata survive restart/replay;
- the instrument can measure a low-voltage CELL_V1 control build without interpretation being embedded into acquisition.

## Aim 3 — Test one physical CELL_V1 primitive against controls

Select the smallest low-voltage physical primitive that isolates:
- reference behavior;
- ternary state behavior;
- bidirectional path behavior;
- retention or hysteresis, if present;
- recovery/reinjection claims only after the control path is characterized.

### Success criteria
- schematic and BOM are frozen for the test;
- control and hypothesis configurations are measured under the same procedure;
- thresholds, drift, failure modes, and repeatability are reported;
- unsupported behavior is explicitly marked failed rather than reinterpreted.

## Aim 4 — Evaluate one cross-domain hypothesis quantitatively

Choose one cross-domain claim with measurable data, preferably either:
- continuous-medium wave propagation;
- ATP-linked state mapping;
- normalized threshold/release dynamics;
- associative-memory allocation.

### Success criteria
- variables and scaling are defined before fitting;
- a conventional/domain-specific comparator is included;
- the One-Wave formulation must outperform or add a distinct predictive observable to survive.

## Aim 5 — Produce a grant-grade evidence package

Create an externally reviewable release containing:
- methods;
- raw/processed data;
- source versions;
- negative results;
- plots with units;
- hardware photos/schematics;
- reproducibility instructions;
- a claim-by-claim evidence table.

### Success criteria
An independent technical reviewer can identify exactly what was tested, reproduce at least one core result, and distinguish established baselines from unverified interpretation.
