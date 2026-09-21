# Milestones and Go/No-Go Gates

## Phase 0 — Proposal readiness

**Deliverables**
- proposal-facing repository map;
- verified status labels;
- test matrix;
- budget framework;
- facilities/team gap list.

**Go condition:** all major proposal claims trace to a file, test, or clearly labeled hypothesis.

## Phase 1 — Reproducibility baseline

**Deliverables**
- BASIS runner;
- stable control/hypothesis receipt format;
- at least three rerunnable tests.

**Go condition:** independent rerun reproduces declared outputs within tolerance.

**No-go:** results depend on undocumented manual steps or shifting parameters.

## Phase 2 — Wave Reader qualification

**Deliverables**
- calibrated acquisition path;
- known-signal capture;
- measured noise and bandwidth;
- restart/replay proof.

**Go condition:** measurement error and noise are below the effect size required by the first hardware test.

**No-go:** front-end uncertainty is comparable to or larger than the claimed effect.

## Phase 3 — CELL_V1 control characterization

**Deliverables**
- frozen BOM/schematic;
- baseline reference behavior;
- ternary threshold map;
- drift and failure-mode log.

**Go condition:** control behavior is stable enough to distinguish the experimental condition.

**No-go:** threshold drift or uncontrolled parasitics prevent discrimination.

## Phase 4 — Experimental mechanism test

**Deliverables**
- predeclared hypothesis;
- control comparison;
- repeated measurements;
- analysis notebook/script.

**Go condition:** repeatable effect exceeds declared measurement and control uncertainty.

**No-go:** effect disappears under control, reverses unpredictably, or falls within noise.

## Phase 5 — Cross-domain model test

**Deliverables**
- dimensionless variables;
- comparator model;
- held-out or independent dataset;
- residual comparison.

**Go condition:** the One-Wave formulation adds predictive value beyond the comparator.

**No-go:** model is only a relabeling, requires post-hoc tuning, or does not generalize.

## Phase 6 — External review package

**Deliverables**
- public/reviewer release;
- methods;
- data;
- code;
- negative results;
- claim-evidence map.

**Success condition:** a technically competent outsider can reproduce at least one core result and audit the rest.
