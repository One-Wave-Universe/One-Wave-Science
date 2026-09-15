# External Work

## Purpose

`External_Work` is the provenance boundary between third-party data and One Wave analysis. It holds source manifests, source-specific adapters, retrieved payloads, and exported analysis products. Nothing placed here becomes a One Wave physical claim merely by being imported or encoded.

## Evidence flow

```text
public source record
  -> raw payload
  -> normalized observation
  -> declared transform
  -> WaveState
  -> validation report
```

Each transition must retain source identifiers, units, coordinate frames, software version, assumptions, and failure status.

## Layout

- `inbox/` — raw or externally retrieved payloads. Do not silently edit source data.
- `outbox/` — reproducible exports: WaveState payloads, reports, and visualization inputs.
- `manifests/` — source acquisition and dataset provenance.
- `adapters/ligo/` — LIGO strain and metadata normalization.
- `adapters/cern/` — CERN event and metadata normalization.

## Status vocabulary

- `RAW`: source record received; no interpretation.
- `NORMALIZED`: schema, units, and source coordinates standardized.
- `ENCODED`: represented as a field or wave by an explicit transform.
- `HYPOTHESIS_DERIVED`: incorporates One Wave assumptions.
- `VALIDATED`: meets a predeclared held-out or external test.
- `QUARANTINED`: provenance, integrity, or assumption failure.

## Scientific rule

A reversible or useful encoding is not evidence that the encoded ontology is physically true. New physical claims require a fixed transform, a competing baseline, and a quantitative prediction assessed on data not used to set the transform.
