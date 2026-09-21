# One-Wave Field Theory V1 — Verification Matrix

**Status:** active verification ledger

This file is the shared test index for the V1 hypothesis/specification layer. Inclusion means **test this**, not **accept this**.

## Status vocabulary

- **UNVERIFIED** — claim exists; no adequate test completed.
- **TEST DEFINED** — variables, controls, outputs, and failure condition are explicit.
- **PASS** — predefined acceptance criterion passed.
- **FAIL** — predefined acceptance criterion failed.
- **INCONCLUSIVE** — valid run did not discriminate.
- **INVALID** — setup/data/solver made the run unusable.
- **VERIFIED-SCOPE** — repeated evidence supports only the exact stated scope.
- **DISMISSED-SCOPE** — repeated valid evidence contradicts the exact stated scope.
- **REVISE** — formulation changed; old version remains historically traceable.

## Core matrix

| ID | Source | Claim / proposition | Control or comparator | Required observable | Current status |
|---|---|---|---|---|---|
| V1-LAT-01 | chapters/01 | Continuous-medium propagation can reproduce target wave behavior without numerical-grid artifacts dominating | analytic/standard wave control | phase velocity, dispersion, convergence vs grid | UNVERIFIED |
| V1-LAT-02 | chapters/01 | Stable localized structures emerge from the proposed dynamics | null/known nonlinear-wave control | lifetime, energy/state conservation, perturbation response | UNVERIFIED |
| V1-LAT-03 | chapters/01 | Model yields a discriminating physical prediction | accepted model | predefined residual/prediction metric | UNVERIFIED |
| V1-ATP-01 | chapters/02 | ATP-linked events map to measurable local lattice/phase variables beyond biochemical controls | biochemical/thermodynamic control | preregistered extra observable | UNVERIFIED |
| V1-AFF-01 | chapters/03 | Proposed expansion/compression variables correlate with measured physiological state | standard physiological predictors | blinded predictive accuracy / effect size | UNVERIFIED |
| V1-QUA-01 | chapters/04 | One dimensionless release model survives biological and quasar-scale normalization | separate domain models | normalized residuals and invariant parameters | UNVERIFIED |
| V1-BAS-01 | chapters/05 | BASIS runtime produces reproducible control-vs-hypothesis receipts | repeated identical run | deterministic/seeded outputs, hashes, telemetry | UNVERIFIED |
| V1-MEM-01 | Hopfield module | Stored melody/sign patterns can be recalled from controlled corruption | nearest-pattern/simple lookup baseline | exact/noisy recall accuracy, spurious attractors | UNVERIFIED |
| V1-MEM-02 | Boltzmann config | Equal 0.20 multimodal allocation is useful relative to alternatives | unequal/adaptive allocation | recall quality, interference, capacity | UNVERIFIED |
| V1-VTC-01 | vtc_zero_logic | Yellow CLEAR/BREAK and Red DOWN/Compress map coherently onto current state semantics | current CELL_V1 semantics | state-transition table with no contradictions | UNVERIFIED |
| V1-VTC-02 | vtc_zero_logic | Proposed split-rail/pot threshold setup is stable and compatible | current reference implementation | drift, noise, threshold margin | UNVERIFIED |
| V1-WR-01 | wave_reader_v1 | Proposed ADC path captures known signals at declared performance | calibrated generator/scope | amplitude/frequency error, noise, actual sample rate | UNVERIFIED |
| V1-WR-02 | wave_reader_v1 | Jetson acquisition path saves reproducible raw data + metadata across restart | repeated calibration capture | byte/data equivalence within declared tolerance | UNVERIFIED |

## Receipt rule

Each test should create or link a receipt containing:

```text
test_id
git_sha
date/time
operator/agent
hardware/software version
input/source dataset
control configuration
hypothesis configuration
units
parameters
seed
raw output location
processed output location
acceptance criterion
observed result
status
notes / failure mode
```

## Promotion / dismissal rule

A chapter or node must not be globally labeled verified because one subtest passes. Update only the exact matrix row and claim scope supported by evidence.

Likewise, a failed formulation should remain discoverable with a DISMISSED-SCOPE marker so future work does not unknowingly recreate the same failed claim.
