# One-Page Experimental Spine

## Problem

The repository contains a broad family of unverified continuous-medium and state-recurrence hypotheses, but broad theory is not fundable by itself. The fundable unit is a narrow, falsifiable experiment with a calibrated measurement chain.

## Proposed first funded experiment

**Question:** Does the smallest CELL_V1 physical primitive exhibit a reproducible state-dependent behavior that cannot be explained by the matched conventional control configuration?

## Step 1 — Qualify the instrument

Use Wave Reader V1 or an equivalent validated acquisition chain to establish:
- amplitude accuracy;
- frequency accuracy;
- bandwidth;
- noise floor;
- reference stability;
- repeatability after restart.

## Step 2 — Freeze the control

Build the simplest reference circuit using the same supply, layout discipline, instrumentation, and nominal component class.

Measure:
- thresholds;
- hysteresis;
- drift;
- transient response;
- current;
- reference behavior.

## Step 3 — Freeze the experimental configuration

Add only the proposed CELL_V1 feature being tested.

Do not change multiple mechanisms at once.

## Step 4 — Predeclare the decision rule

Example structure:

```text
If the experimental configuration produces a repeatable state-dependent
response exceeding instrument + control uncertainty by the predefined margin,
advance to replication.

If not, mark the tested mechanism FAIL / DISMISSED-SCOPE.
```

## Step 5 — Replicate

Repeat across:
- multiple runs;
- multiple builds/components where practical;
- restart/reconnect;
- blinded or scripted analysis where possible.

## Step 6 — Release the evidence

Publish:
- schematic;
- BOM;
- calibration;
- raw traces;
- processing code;
- uncertainty;
- failed runs;
- result classification.

## Why this is fundable

The experiment is:
- bounded;
- measurable;
- low-voltage;
- falsifiable;
- useful even if negative;
- directly enabled by existing repository infrastructure;
- expandable only after passing explicit gates.
