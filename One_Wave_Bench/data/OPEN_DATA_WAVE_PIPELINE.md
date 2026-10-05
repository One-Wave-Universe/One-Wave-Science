# Open Data -> Wave Data Pipeline

This restores the missing executable conversion layer behind the repository's
"real data as wave data" work.

The source record is always preserved as provenance. The converter implements
the A-111 requirement that a wave representation declare:

- state identity;
- coupling rule;
- timing relationship;
- propagation behavior.

## Two representations

### 1. measurement_series

Use this when the source already provides an ordered measured series such as
strain, light-curve flux, spectrum bins, detector counts, or another sampled
observable.

The raw source values remain in every output state. The normalized amplitude is
only an analysis coordinate.

Output is labeled:

`source_measurement_wave`

### 2. metadata_sequence

Use this only when the source is metadata rather than a sampled physical series.

Numeric metadata fields are deterministically ordered and normalized into a
derived analysis sequence. This output is always labeled:

`derived_metadata_wave`

and carries an explicit warning that the source metadata is **not** thereby
claimed to be a physical waveform.

## Frequency and timing contract (v2)

The output schema is `one-wave-wave-data-v2`. For both representations, each
state has `f: null` and `frequency_known: false`: this adapter does not estimate
physical signal frequency. Unknown is distinct from an observed zero-Hz/DC
component. Never replace null with zero for physical inference.

For a measurement series with complete, finite, strictly increasing source `t`
values and an explicit top-level `time_unit` of `s`, `ms`, `us` or `ns`:

- `sample_interval_s` is the elapsed source time before the state; the first
  state has null because there is no preceding sample.
- `inverse_sample_interval_Hz` is the inverse of that interval, not signal
  frequency. Nonuniform time steps retain their individual interval rates.
- `timing.sample_rate_Hz` is populated only when all converted intervals agree
  within relative tolerance `1e-9` (zero absolute tolerance); otherwise null.
- `timing.uniform_sampling` is true/false when intervals can be assessed and
  null when unavailable. A single sample cannot establish cadence.

Absent, mixed source/index, undeclared-unit or unsupported-unit timing produces
no cadence in Hz. Existing fallback index coordinates are retained but explicitly
classified in `timing.time_coordinates`; output `t` stays in the source unit,
not silently converted to seconds. For complete source timestamp series, duplicate
or reversed timestamps are rejected. Mixed source/index timing is unassessed and
never produces cadence. Nonfinite supplied timestamps, sample values and positions
are rejected. Metadata
sequence coordinates are `metadata_index`, never physical time or Hertz.

The existing `A` normalization is a dimensionless display coordinate. Existing
`phi` is zero for measurements and algebraic for metadata, not a measured phase.
Raw sample records, provenance, mapping fields, ordering and representation labels
are preserved. This adapter does not assert that every source series is periodic.

### Migration from v1

v1 filled measurement `f` with inverse absolute time spacing (including inferred
row spacing) and metadata `f` with zero. Neither was a signal-frequency estimate.
Consumers must branch on the schema and require `frequency_known` before using
`f` physically; they must not coerce missing frequency to numeric zero. Read
cadence from the explicit timing fields only. External numeric-only v1 consumers
need adaptation; v2 intentionally does not preserve misleading numeric frequency.
No executable consumer of the adapter's output was found in the inspected producer,
tests and pipeline documentation; the separate universal state-container schema
already permits null frequency. This is not proof about external integrations.

Tests: `python3 scripts/test_open_data_to_wave.py`. The 10-Hz synthetic test series
sampled at 100 Hz verifies that cadence is reported as 100 Hz while the unestimated
signal frequency stays null. It is a software fixture, not acquired physical data.

## Source registry

`One_Wave_Bench/data/open_data_sources.json` currently covers:

- CERN Open Data for ALICE, ATLAS, CMS, LHCb, and other public CERN records;
- HEPData for published collider/scattering tables and distributions;
- GWOSC for LIGO/Virgo/KAGRA;
- MAST for JWST, Hubble, Kepler/K2, TESS, and related missions;
- HEASARC for Chandra, Fermi, Swift, NuSTAR, NICER, IXPE, XRISM, XMM-Newton, and other missions;
- Gaia Archive for Gaia catalogs.

This is a registry, not an assertion that every archive record has already been
downloaded.

## Input contract

Example measurement-series input:

```json
{
  "mode": "measurement_series",
  "time_unit": "s",
  "provenance": {
    "source": "gwosc",
    "record_id": "GW150914-L1"
  },
  "mapping": {
    "state_identity": "L1 strain sample",
    "coupling_rule": "adjacent samples",
    "timing_relationship": "source GPS/sample time",
    "propagation_behavior": "ordered detector strain series"
  },
  "samples": [
    {"t": 0.0, "value": 1.2e-21},
    {"t": 0.000244140625, "value": 1.4e-21}
  ]
}
```

Run:

```bash
python3 scripts/open_data_to_wave.py input.json -o wave.json
```

## Required provenance

Every transformed record must keep at least:

- archive/source;
- stable record ID, DOI, observation ID, event ID, or equivalent;
- original units where known;
- source URL or record location where available;
- retrieval date for downloaded records;
- source experiment/mission/instrument where applicable.

Do not replace archive identifiers with One-Wave labels.

## Boundary

The transform is a numerical representation layer. It does not reinterpret the
source experiment, establish a One-Wave physical claim, or convert metadata
labels into measured physics by declaration.

## Live acquisition layer

AI and Jetson work must acquire real public source records before numerical
transformation. Do not invent substitute values when a source is unavailable.

Example:

    python3 scripts/open_data_fetch.py gwosc --url https://gwosc.org/api/v2/runs -o data/raw/gwosc-runs.json

The fetch envelope preserves source ID, requested/final URL, UTC retrieval time,
SHA-256 of the exact HTTP body, HTTP metadata, and the unchanged source record.

For CERN Open Data, HEPData, MAST, HEASARC, and Gaia records that require native
clients, TAP/ADQL, product URLs, FITS, ROOT, HDF5, CSV, VOTable, or other archive
formats, use the registry-declared native method and preserve equivalent provenance.

Required sequence:

    reference repository
      -> select registered archive
      -> fetch/query a real source record
      -> preserve raw record + provenance + hash
      -> classify measurement data versus metadata
      -> only then transform/analyze
      -> retain original values and units
      -> report archive record IDs with results

If live retrieval fails, report the failure. Never substitute generated numbers.
Metadata-derived coordinates remain derived_metadata_wave and are not detector measurements.

## Reproducible science metadata bundle

Use [SCIENCE_DATA_RUNBOOK.md](SCIENCE_DATA_RUNBOOK.md) for live CERN/GWOSC snapshots, exact raw-body hash verification, pagination/failure handling, and native MAST/HEASARC/Gaia query tools. The existing single-record fetcher now also saves its exact HTTP body as `<output>.raw` so its hash can be independently verified.

The corrected Mirror boundary permits coupling and phase shift with reflection, deflection, roll-off and scattering, without forced geometric penetration. A measured comparison requires the derived four-interaction response and a frozen detector-observable transform; metadata acquisition alone does not supply that derivation.
