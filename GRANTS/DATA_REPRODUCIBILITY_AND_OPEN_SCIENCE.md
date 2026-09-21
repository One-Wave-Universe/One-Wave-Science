# Data, Reproducibility, and Open Science Plan

## Guiding rule

A result that cannot be traced to its code, configuration, raw data, and analysis should not support a grant claim.

## Required artifacts per experiment

- unique test ID;
- git commit SHA;
- hardware revision;
- schematic/BOM revision;
- software environment;
- raw data;
- calibration file;
- processed data;
- analysis code;
- plot source;
- acceptance criterion;
- final status;
- known deviations.

## Data classes

1. **Raw measurement data** — immutable after capture.
2. **Calibration data** — versioned and linked to instruments.
3. **Processed data** — regenerated from raw sources.
4. **Simulation output** — generated from committed code/config.
5. **Interpretation metadata** — separate from raw observables.

## Reproducibility target

At least one representative result from each major work package should be reproducible from a documented command or application workflow.

## Negative results

Negative and null results are retained. They should include:
- what failed;
- whether the test itself was valid;
- whether the claim is dismissed or merely inconclusive;
- what parameter region was actually tested.

## Data release

Default preference:
- open code;
- open schemas;
- open processed data;
- open raw data where size/privacy/IP constraints permit;
- persistent version tags/releases for grant milestones.

## Human/biological data boundary

Any future work involving identifiable human data, medical data, or formal human-subject experiments requires appropriate ethics/IRB review and must not be initiated merely because a repository hypothesis mentions affect or physiology.
