# Physics Engine Evidence Pipelines

Status: canonical engineering/science contract. This does not assert that One-Wave is physically correct.

## Rule
The physics engine develops bottom-up from the lattice. External measurements do not tune the primitive after exposure. They are held-out evidence.

CERN/CMS collision and detector records may be transformed into wave-domain representations for One-Wave testing, but raw CERN data MUST remain identified as detector/collision measurements. A One-Wave transform is derived data, never a relabeling of the source.

GWOSC strain is already a calibrated time-series observable and enters with its detector, sample-rate, segment/data-quality, event/catalog and release metadata intact.

## Pipeline
RAW SOURCE
-> IMMUTABLE SOURCE METADATA + CONTENT HASH
-> UNITS/CALIBRATION/QUALITY MASK
-> DECLARED TRANSFORMATION
-> WAVE-DOMAIN DERIVED DATA
-> CONTROLS/NULLS
-> FROZEN ENGINE PREDICTION
-> HELD-OUT COMPARISON
-> RESIDUAL/UNCERTAINTY
-> RECEIPT
-> SUPPORTED | UNSUPPORTED | UNRESOLVED within declared scope.

No external dataset may silently alter the lattice equations, parameters, transforms, thresholds or acceptance metric after held-out exposure. Any such change creates a new version and requires a new untouched test set.

## Metadata is part of the experiment
Harvest and preserve every available relevant field exposed by the provider, not only values convenient to One-Wave.

Minimum normalized provenance:
provider, experiment/detector, dataset/record/event/catalog/version IDs, DOI/reference when present, source URL/API endpoint, release/version, retrieval timestamp, license, file identity/content hash, format, units, calibration/reconstruction level, detector/channel, run/event/GPS/time range, sample rate/binning, quality flags/segments, simulation-vs-measurement status, provider processing/pipeline labels, selections/cuts/triggers when available, uncertainty/covariance when available, source metadata snapshot hash.

Unknown/missing fields remain explicit null/unknown values. Never infer them.

## CERN/CMS wave-data transform
Keep two layers:
1. RAW/RECONSTRUCTED CERN layer: provider-native events, tracks/hits/clusters/energies/momenta/timestamps/IDs and metadata as available.
2. ONE-WAVE DERIVED layer: an explicit versioned transform into quantities such as frequency/scale/phase/path/field coordinates only where mathematically defined.

Each transform records assumption IDs, equations, units, normalization, parameters, transform version/commit, input hashes, output hash, controls, uncertainty and inverse/reconstruction check where possible.

Particle names in CERN metadata remain provider labels. They are not One-Wave primitives.

Required controls include shuffled/event-mixed data, phase/randomized controls where applicable, acceptance/detector controls, simulated/provider controls where available, and conventional reconstruction baseline.

## GWOSC
Ingest API v2 catalogs, event versions/parameters, observing runs, datasets, timelines/data-quality segments and strain-file metadata before strain analysis.
Preserve detector, GPS interval, sample rate, event/catalog/version, data-quality segments and strain statistics/metadata.
One-Wave transforms of h(t) are separate derived artifacts with frozen transform IDs.

## Engine integration
External-data adapters are read-only evidence adapters. They do not live inside the numerical update law.

Engine core:
lattice state -> update law -> energy/accounting ledger -> propagation/dispersion -> stable dynamics -> interactions.

Evidence adapters:
engine prediction -> declared observable transform -> CERN/GWOSC comparable representation -> residual/null/held-out validator.

The renderer is downstream and cannot alter either solver or evidence.

## Required first sequence
E0 provider metadata snapshots + hashes
E1 D-415 zero-input/perturbation engine kernel and energy ledger
E2 G-766 analytic/numerical dispersion + refinement/anisotropy
E3 stable dynamic structure tests
E4 interaction tests
E5 freeze engine + observable transform
E6 blind/held-out CERN and/or GWOSC comparison
E7 residuals, controls, uncertainty and receipt

Failure at a lower rung blocks interpretation of a higher rung as evidence for One-Wave.
