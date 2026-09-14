# CERN -> Wave Data Converter

Status: YELLOW tooling / standard transform implemented / One-Wave mechanism not inferred.

## CORE-RULES-PRE

Before changing this tool, read:

- `CORE_RULES_LOCK.md`
- `MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md`
- `MATH_BACKBONE/30_cern_fourvector_to_wave_transform_v1.md`

This converter must preserve the source measurement/reconstruction and must not present derived or scaled values as CERN measurements.

## First live source

CMS Open Data record 545 publishes educational CSV datasets derived from 2011 collision data. `Dimuon_DoubleMu.csv` contains two reconstructed muons per event with fields including:

- `Run`, `Event`
- `E1`, `px1`, `py1`, `pz1`, `pt1`, `eta1`, `phi1`, `Q1`
- `E2`, `px2`, `py2`, `pz2`, `pt2`, `eta2`, `phi2`, `Q2`
- event-level dimuon invariant mass `M`

Direct source used by the live test:

```text
https://opendata.cern.ch/record/545/files/Dimuon_DoubleMu.csv
```

The portal describes these as derived/educational datasets. They are excellent for validating the transform and exploring structure, but they are not a substitute for a full CMS physics analysis chain.

## Output layers

### `STANDARD_DERIVED`

Calculated directly from the source four-vector with fixed physical constants:

- momentum magnitude
- transverse momentum
- mass reconstructed from the individual four-vector
- Planck frequency `E/h`
- angular frequency `E/hbar`
- de Broglie wavelength `hc/p`
- spatial wave number `p/(hbar*c)`
- transverse wavelength
- Compton and reduced-Compton wavelengths where mass is nonzero
- beta, gamma, group velocity, conventional phase velocity
- direction cosines
- rapidity
- reconstructed event pair mass and delta from source `M`

These are not additional CERN detector channels. They are a mathematically equivalent derived view of the CERN kinematic record.

### `SCALED_ANALOG`

Optional hardware/simulation mapping:

```text
energy_ratio = E / E_reference
analog_frequency = energy_ratio * bench_frequency_reference
```

This preserves ratios while bringing numbers into a realizable numerical/electronic range. It is explicitly not a claim that a GeV collision object physically oscillates at the bench frequency.

## Example

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

A 10 GeV object maps to 1 kHz only in the `SCALED_ANALOG` layer. A 5 GeV object maps to 500 Hz, a 20 GeV object to 2 kHz, preserving the energy ratio.

## Next datasets

After record 545 works end-to-end, extend the same converter rather than writing dataset-specific physics:

- W -> electron + missing transverse energy educational records
- Higgs -> four-lepton candidate records
- particle-level / simulated-track records with energy and momentum fields
- modern NanoAOD / PF candidate records, adding a ROOT reader without changing the transform equations

## Jetson path

The intended execution path is the repo's canonical Hive Pipe terminal route. At the time this branch was created, GitHub Actions could run normally but the configured `JETSON_GATEWAY_URL` and `JETSON_GATEWAY_TOKEN` secrets were absent, so the relay could not reach the Jetson. The converter is therefore tested on GitHub-hosted Linux first and is ready to run unchanged on the Jetson once the existing relay credentials are restored.

Do not commit Hive Pipe tokens or tunnel credentials to this repository.

## CORE-RULES-POST

- Source fields are preserved.
- Standard-derived values and scaled analog values are visibly separated.
- No free fit parameter is used in the physical transform.
- Hardware scaling requires explicit reference values.
- Pair invariant mass is independently reconstructed as a consistency test.
- One-Wave interpretation remains YELLOW until it predicts something beyond the standard transform and survives comparison.
