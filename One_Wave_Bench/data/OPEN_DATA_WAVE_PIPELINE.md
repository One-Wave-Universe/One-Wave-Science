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
