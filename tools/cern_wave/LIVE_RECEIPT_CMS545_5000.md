# LIVE RECEIPT — CMS-545 CERN -> WAVE TRANSFORM — 5,000 EVENTS

Status: **TRANSFORM PASS / SOURCE-MASS LINEAGE YELLOW / JETSON RELAY BLOCKED BY MISSING SECRETS**

Date: 2026-09-14

CORE-RULES-PRE:
- Reference CERN source first.
- Preserve all failed checks and unresolved discrepancies.
- Separate source data, standard-derived wave quantities, scaled analog quantities, and One-Wave interpretation.
- Do not call a GitHub-hosted run a Jetson run.
- Do not claim OpenClaw was used when it was not reached.

## Source

CERN CMS Open Data record: `CMS-545`

Live input:

```text
https://opendata.cern.ch/record/545/files/Dimuon_DoubleMu.csv
```

The CERN record describes this as an educational derived dataset containing a subset of full event information.

## Execution

GitHub Actions workflow:

```text
CERN Wave Transform Tests
```

Run ID:

```text
34908363455
```

Job ID:

```text
104190114503
```

Final result:

```text
SUCCESS
TRANSFORM_PASS
```

Unit tests: 4 / 4 passed.

Live events consumed: 5,000.

Objects transformed: 10,000 reconstructed muons.

## Standard-derived wave range

From the published CERN four-vectors using fixed Planck/de Broglie relations:

```text
frequency min = 6.691543430040613e+23 Hz
frequency max = 1.0168055823409656e+26 Hz

de Broglie wavelength min = 2.9483780411025317e-18 m
de Broglie wavelength max = 4.48347527835979e-16 m
```

These are `STANDARD_DERIVED` values. They are not extra detector channels.

## Bench-scaled analog range

Declared mapping:

```text
10 GeV -> 1000 Hz
```

Using

```text
f_analog = (E / 10 GeV) * 1000 Hz
```

observed analog range across the 10,000 objects:

```text
276.74 Hz -> 42051.7 Hz
```

This is `SCALED_ANALOG`, not a claim that the collision physically occurred at audio/electronic frequencies.

This range is useful for future hardware/simulation experiments because relative energy structure is preserved while the numerical scale is moved into a realizable band.

## First transformed real CERN object

Source identity:

```text
Run   = 165617
Event = 74601703
object_index = 1
charge = -1
```

Published four-vector:

```text
E  =  9.6987 GeV
px = -9.5104 GeV
py =  0.3662 GeV
pz =  1.8633 GeV
```

Derived kinematics / wave view:

```text
p = 9.698128556066887 GeV
m_from_printed_fourvector = 0.1052815273444724 GeV
beta = 0.9999410803578713

group velocity = 299774794.33566177 m/s
conventional phase velocity = 299810122.70513636 m/s

frequency = 2.3451352267447746e+24 Hz
angular frequency = 1.4734919197880042e+25 rad/s

de Broglie wavelength = 1.2784342637161563e-16 m
wave number = 4.914750398758389e+16 rad/m

unit direction x = -0.9806428059824543
unit direction y =  0.03775986241911747
unit direction z =  0.19212985157165913

rapidity = 0.19453596559400244
```

Bench analog under the declared 10 GeV -> 1 kHz mapping:

```text
energy ratio = 0.96987
analog frequency = 969.87 Hz
```

Pair check for this event:

```text
source M       = 17.4922 GeV
recomputed M   = 17.49208969534515 GeV
rounding gap   = 0 GeV
```

## Preserved failed checks / source-lineage result

The first live validation incorrectly demanded a fixed 10 MeV agreement between the published `M` column and a mass recomputed from the rounded public four-vector columns.

That check failed:

```text
maximum center-value difference = 0.017016449838837655 GeV
```

A second check derived a conservative interval from the displayed decimal precision instead of loosening the tolerance after seeing the result.

That still left:

```text
source-mass-lineage consistent events   = 4948
source-mass-lineage unresolved events   = 52
maximum remaining rounding gap          = 0.006236910768313564 GeV
```

This is preserved as a source-lineage issue, not converted into evidence for One-Wave.

Worst event in this run:

```text
Run = 165617
Event = 76225718
source M = 3.1505 GeV
recomputed M = 3.1675164498388377 GeV
center delta = 0.017016449838837655 GeV
remaining displayed-rounding gap = 0.006236910768313564 GeV
```

CERN describes record 545 as an educational subset, so the current result means only that its published `M` field is not exactly reproducible from the rounded subset columns for 52 / 5000 tested events. The extraction lineage remains OPEN until the generating code or higher-precision inputs establish why.

## Individual four-vector precision diagnostics

```text
E^2 - p^2 negative after published-value rounding: 52 objects
beta > 1 beyond declared tolerance: 0 objects
```

Negative mass-squared values from rounded educational columns remain visible as warnings and are not silently treated as physical negative masses.

## Jetson / OpenClaw status

The canonical repo path is:

```text
GitHub Actions -> authenticated HTTPS -> Hive Pipe MCP /mcp -> terminal_run -> Jetson
```

A non-destructive Jetson probe was attempted through this exact path.

It did **not** reach the Jetson because GitHub Actions currently has empty / unavailable:

```text
JETSON_GATEWAY_URL
JETSON_GATEWAY_TOKEN
```

The branch's ordinary GitHub Actions runner was independently tested and passed, so this is specifically the missing relay-credential configuration, not a generic Actions failure.

OpenClaw was therefore **not executed or inspected on the Jetson** in this run. No claim is made that it is installed.

No relay token or tunnel URL was committed to the repository.

## What is ready once the relay is restored

The converter is stdlib-only Python and needs no CERN-specific package for the CSV pass.

It can run unchanged on the Jetson and produce:

- source-preserving JSONL;
- standard-derived frequency/wavelength/velocity/direction values;
- source-lineage diagnostics;
- optional explicit bench-scaled analog values;
- event-level audit receipts.

The next useful extensions are additional CERN datasets with missing transverse energy, four-lepton/Higgs candidates, and lower-level track/PF candidate data, while keeping the same transform definitions fixed.

CORE-RULES-POST:
- CERN source data remained the reference.
- Original columns were preserved.
- Standard-derived values and scaled analog values are separately labeled.
- Failed validations were preserved and narrowed rather than erased.
- No arbitrary fit tolerance was introduced.
- No source-lineage discrepancy was promoted as One-Wave evidence.
- Jetson execution was not falsely claimed.
- OpenClaw execution was not falsely claimed.
- Math backbone remained explicit and append-only.
- Drift detected: no.
