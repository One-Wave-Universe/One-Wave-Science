# HOW TO USE CERN DATA WITHOUT DRIFT — AI OPERATOR GUIDE

Status: **OPERATIONAL GUIDE / SOURCE-FIRST / NO ONTOLOGY PROMOTION**

## CORE-RULES-PRE

Before doing any CERN/One-Wave work, read in this order:

1. `CORE_RULES_LOCK.md`
2. `MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md`
3. `MATH_BACKBONE/30_cern_fourvector_to_wave_transform_v1.md`
4. `MATH_BACKBONE/30A_cern_csv_rounding_interval_v1.md`
5. `MATH_BACKBONE/30B_cern_source_mass_lineage_audit_v1.md`
6. `tools/cern_wave/LIVE_RECEIPT_CMS545_5000.md`

Do not begin by asking what One-Wave wants the data to say. Begin with what the source actually contains.

## 1. First supported source

CERN CMS Open Data record 545:

```text
https://opendata.cern.ch/record/545
```

First live CSV:

```text
https://opendata.cern.ch/record/545/files/Dimuon_DoubleMu.csv
```

The table contains two reconstructed muons per event plus an event-level dimuon invariant mass.

Keep the original source fields. Do not replace them with derived fields.

## 2. Run the converter

From the repository root:

```bash
python3 tools/cern_wave/cern_wave_convert.py \
  --input https://opendata.cern.ch/record/545/files/Dimuon_DoubleMu.csv \
  --output /tmp/dimuon-wave.jsonl \
  --summary /tmp/dimuon-wave-summary.json \
  --source-record CMS-545 \
  --reference-energy-gev 10 \
  --bench-frequency-hz 1000 \
  --max-events 5000
```

Build the event-level receipt:

```bash
python3 tools/cern_wave/cern_wave_receipt.py \
  /tmp/dimuon-wave.jsonl \
  --output /tmp/dimuon-wave-receipt.json
```

Run unit tests:

```bash
PYTHONPATH=tools/cern_wave \
python3 -m unittest -v tools/cern_wave/test_cern_wave_convert.py
```

## 3. Know the three layers

### A. SOURCE

Examples:

```text
E1 px1 py1 pz1 pt1 eta1 phi1 Q1
E2 px2 py2 pz2 pt2 eta2 phi2 Q2
M
Run Event
```

These are the published CERN/CMS values. Preserve them.

### B. STANDARD_DERIVED

The converter calculates standard equivalent quantities from the published four-vector:

```text
p
pT
E/h
E/hbar
hc/p
p/(hbar*c)
beta
gamma
group velocity
conventional phase velocity
direction cosines
rapidity
reconstructed pair invariant mass
```

These are derived from established equations. CERN did not directly measure a separate frequency channel merely because `E/h` is calculated.

### C. SCALED_ANALOG

Optional declared mapping for simulation/hardware:

```text
energy_ratio = E / E_reference
analog_frequency = energy_ratio * bench_reference_frequency
```

Example:

```text
10 GeV -> 1000 Hz
```

This mapping preserves a ratio for bench work. It is not a claim that the collision happened at 1 kHz.

## 4. How to use the transformed data to pressure-test One-Wave

Do not scan for a pretty pattern and call it proof.

For each One-Wave node, write:

```text
SOURCE VARIABLES:
ONE-WAVE CLAIM:
REQUIRED EQUATION:
PREDICTED OBSERVABLE:
STANDARD TARGET:
FREE PARAMETERS:
TEST:
RESULT: PASS / FAIL / OPEN
```

Good targets include:

- mass/excitation relationships;
- resonance structure;
- decay widths and lifetimes when the source contains them;
- angular/path relationships using `px,py,pz,eta,phi`;
- charge/opposed-channel hypotheses;
- jet/confinement hypotheses using lower-level data;
- detector-coupling claims when event-level detector information is available.

## 5. What an AI must not do

Do not:

- alter CERN source values to improve a One-Wave fit;
- choose a coefficient after seeing the answer and call it derived;
- promote `E/h` into proof that the event is ontologically One-Wave;
- call a scaled analog frequency a measured frequency;
- erase failed events;
- silently discard source columns whose lineage is inconvenient;
- use rounded educational values as if they were the complete CMS reconstruction chain;
- interpret a source-lineage discrepancy as new physics without independent evidence.

## 6. Important live receipt already discovered

The 5,000-event CMS-545 run transformed 10,000 reconstructed muons successfully.

It also found that 52 / 5,000 published event masses were not reproducible from the displayed rounded subset columns alone, even after a displayed-precision interval check. Preserve this as source-lineage YELLOW. See:

```text
tools/cern_wave/LIVE_RECEIPT_CMS545_5000.md
MATH_BACKBONE/30B_cern_source_mass_lineage_audit_v1.md
```

Do not fit the discrepancy away.

## 7. Adding a new CERN dataset

Before adding a dataset:

1. record the exact CERN URL / DOI / record number;
2. record whether fields are measured, reconstructed, simulated, derived, or educational;
3. map source columns to existing transform variables without changing the equations;
4. if new physics variables are needed, add a new versioned math-backbone file rather than rewriting an adopted one;
5. run source-preservation tests;
6. run numerical sanity tests;
7. generate a receipt;
8. only then test a One-Wave hypothesis.

Suggested progression:

```text
CMS dimuon -> four-lepton/Higgs -> W + missing transverse energy -> jets/tracks/PF -> decay/lifetime datasets
```

## 8. Jetson

The converter is standard-library Python and can run directly on the Jetson.

Launcher:

```bash
bash scripts/run_cern_wave_on_jetson.sh
```

The current remote GitHub -> Hive Pipe path is blocked until the repository's Jetson gateway URL/token are restored. Do not commit those credentials.

## CORE-RULES-POST

After every CERN-data update, verify:

- exact source remains attached;
- source fields remain unchanged;
- equations were not summarized away;
- standard-derived and scaled-analog values remain labeled separately;
- failed rows/events remain visible;
- free parameters are declared;
- One-Wave interpretation is not promoted without a new prediction and comparison;
- a PASS / FAIL / OPEN result is recorded;
- drift detected: state YES or NO explicitly.
