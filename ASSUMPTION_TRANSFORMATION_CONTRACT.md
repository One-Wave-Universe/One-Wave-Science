# One-Wave Assumption & Transformation Contract

**Status: CANONICAL PROCESS CONTRACT**

One-Wave metadata is used to lock the exact assumptions and transformations under test. It does **not** turn an assumption into a fact merely because it is registered.

## Immutable chain

`RAW SOURCE → SOURCE/UNITS → ASSUMPTION → TRANSFORMATION → CONTROLS/NULLS → RESULT → RESIDUAL → VALIDATION STATUS → VERSIONED REFERENCE`

Every scientific simulator, public-data ingest, digital CELL comparison, and physical bench comparison must be able to name the IDs used at each applicable step.

## Assumption record

Every assumption receives a stable ID and version and records:
- exact statement;
- scope/domain;
- motivation;
- required source classes;
- units/dimensions;
- parameters and allowed calibration;
- falsification/disconfirmation conditions;
- competing/null interpretation;
- dependencies;
- status;
- provenance.

Changing the statement, equations, units, parameter freedom, or falsification conditions creates a new version. Never silently edit a tested assumption.

## Transformation record

Every transformation receives a stable ID/version and records:
- input schema and units;
- exact equation/algorithm;
- parameter values/ranges;
- normalization/reference choices;
- output schema and units;
- implementation commit/hash;
- deterministic seed where relevant;
- controls/nulls;
- known numerical limitations;
- source assumption IDs.

A transformation is not allowed to acquire extra free parameters after held-out data is inspected without a new version and explicit recalibration status.

## Validation states

Allowed scientific states:

`PROPOSED → CALIBRATED → TESTING → SUPPORTED | UNSUPPORTED | UNRESOLVED → SUPERSEDED`

SUPPORTED means supported within the declared dataset, controls, uncertainty and scope. It is not universal proof.

## Raw data law

Raw provider records are immutable inputs. Preserve provider, record ID/DOI when available, source URL, retrieval time, content hash, units, license/usage metadata, and raw path.

One-Wave transformed data must be stored separately and point backward to raw hashes/IDs.

## Control law

A result cannot be promoted to SUPPORTED without declared applicable controls/nulls and an inspectable receipt. Negative results remain in the ledger.

## Cross-system law

Science owns the semantic definition of assumptions and transformations.

Bridge-Comand transports their IDs, versions, provenance and receipts without redefining them.

Builds/digital CELL/Jetson/analog bench may consume the same definitions and return comparison receipts. They do not silently fork the scientific definition.

## Comparison target

Where applicable, the same transformation definition should be runnable against:
- public/experimental source data;
- One-Wave scientific simulation;
- digital CELL/reference runtime;
- analog CELL bench traces.

Differences are first-class residuals, not errors to hide.

## Supersession

Never overwrite history. New evidence creates a new validation receipt or a superseding version. Every superseded record names its successor and every successor names what it replaces.
