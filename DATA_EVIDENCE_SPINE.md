# Data Evidence Spine

## Objective

Create a reproducible route from public observational data to One Wave-compatible computational representations without allowing representation choices to masquerade as physical conclusions.

## Core contract

```text
RAW -> NORMALIZED -> ENCODED -> HYPOTHESIS_DERIVED -> VALIDATED
                           \-> QUARANTINED
```

- **RAW** preserves the source record and acquisition manifest.
- **NORMALIZED** standardizes schema, units, and coordinate description without applying a physical interpretation.
- **ENCODED** applies a declared representation transform.
- **HYPOTHESIS_DERIVED** applies stated One Wave assumptions.
- **VALIDATED** requires a predeclared baseline, held-out result, and uncertainty.
- **QUARANTINED** marks inputs or results that fail provenance, integrity, or assumption checks.

## Source adapters

### LIGO

LIGO adapter input is calibrated strain plus detector, timing, calibration/release, and quality context. Since strain is already a sampled wave observable, the initial transform preserves the series as a `WaveState`; later signal processing must be separately versioned and controlled.

### CERN

CERN adapter input is a reconstructed event record and its dataset/reconstruction provenance. The initial transform preserves source objects as a sparse field representation. It does not infer hidden phase, continuous trajectory, or a new physical mechanism.

## Evidence standard

For any hypothesis-derived transform, create an EvidencePlan before inspecting held-out results. It must name: observation, mechanism, transform/version, locked parameters, assumptions, baseline, prediction, development split, hold-out split, and a decision rule.

A successful encoding establishes only that the encoding can be computed. A scientifically stronger claim requires an externally checkable prediction that improves on—or disagrees with—a stated baseline under predefined evaluation.

## Starting points

- `External_Work/adapters/ligo/normalize_ligo.py`
- `External_Work/adapters/cern/normalize_cern.py`
- `One_Wave_Simulator/transforms/ligo_strain_to_wave.py`
- `One_Wave_Simulator/transforms/cern_event_to_wave.py`
- `One_Wave_Simulator/validation/evidence_contract.py`
- `sims/evidence_bench/`
