# Science data acquisition and Mirror coupling work

## Run from the verified checkout

First use Algorithm Zero to identify the actual checkout/HEAD. These are ordinary Python terminal commands on either laptop or Jetson; they require no AI subscription API key. Use the repository's verified terminal route. Do not use an old command receipt as proof of a new run.

The lightweight CERN/GWOSC metadata bundle uses Python's standard library:

```sh
python3 scripts/science_metadata_bundle.py --cern-record 5501 --gwosc-event GW150914 --output /tmp/one-wave-science-data
python3 scripts/science_metadata_bundle.py --verify --output /tmp/one-wave-science-data
python3 scripts/test_science_metadata_bundle.py
```

The first command fetches a CERN record, a GWOSC event record and its strain-file metadata, following bounded pagination. A failed request or capped/inconsistent page count yields a failed/incomplete receipt and nonzero exit. It never substitutes numbers. Three complete requests do not mean the entire CERN or GWOSC archive was ingested.

Raw HTTP bodies are saved by SHA-256 name alongside unchanged decoded provider records. The verifier recomputes hashes and compares decoded records. Summaries leave unknown units/license/calibration explicit. Provider metadata, even when numerically encoded, is not measured strain or collision events.

A checked-in acquisition receipt and exact source bodies are in [receipts/science-metadata-20261004](receipts/science-metadata-20261004/receipt.json). This is a historical snapshot, not a live service-health claim.

## Readers and native archive tools

Use an isolated environment so host system packages remain intact:

```sh
python3 -m venv /tmp/one-wave-science-tools
/tmp/one-wave-science-tools/bin/pip install -r One_Wave_Bench/data/science-tools-requirements.txt
```

| Tool | Job |
|---|---|
| gwosc | Official public GWOSC metadata/data-location client |
| h5py | Read provider HDF5 strain products with attributes |
| uproot | Read CERN ROOT trees/histograms without installing ROOT |
| astroquery + astropy | Query MAST, HEASARC and Gaia; preserve table columns, units and masks |

The metadata bundle needs none of these optional packages. Install ROOT or XRootD only when the selected CERN workflow actually requires them. Retain provider checksums and license/attribution when downloading products.

Native client queries:

```sh
/tmp/one-wave-science-tools/bin/python scripts/archive_metadata_query.py mast --mission HST --coordinates "83.6331 22.0145" --radius-deg 0.01 --output /tmp/one-wave-mast
/tmp/one-wave-science-tools/bin/python scripts/archive_metadata_query.py heasarc --catalog numaster --coordinates "83.6331 22.0145" --radius-deg 0.01 --output /tmp/one-wave-heasarc
/tmp/one-wave-science-tools/bin/python scripts/archive_metadata_query.py gaia-archive --adql "SELECT TOP 10 source_id,ra,dec FROM gaiadr3.gaia_source ORDER BY source_id" --output /tmp/one-wave-gaia
```

These produce provider-client ECSV tables and receipts with query, row count, units, client versions and content hash. ECSV is a client serialization, not an exact wire-response snapshot. Empty results remain empty. Failures remain failed; acquisition alone is not model validation.

For HEPData use a selected publication/table record through the existing registry and acquisition CLI, or its provider download. The tested record endpoint returned HTTP 403 in this session. No table was acquired; do not claim it was. For non-JSON products use the provider-native reader and preserve equivalent provenance, not `open_data_fetch.py` which expects JSON.

PDG is the reference for comparison definitions and scales, not an invented uniform pole-mass target. [2025 quark table](https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf).

## All registered domains

The existing [source registry](open_data_sources.json) includes CERN ALICE/ATLAS/CMS/LHCb, HEPData, GWOSC LIGO/Virgo/KAGRA, MAST telescope missions, HEASARC high-energy missions and Gaia. A registry entry is a route definition, not proof that every record or mission is downloaded. Select a bounded observation/record relevant to the predicted observable. Keep source-native identities and all available metadata.

Native documentation: [GWOSC API](https://gwosc.org/api/), [CMS four-lepton workflow](https://opendata.cern.ch/record/5500), [MAST queries](https://astroquery.readthedocs.io/en/stable/mast/mast_obsquery.html), [HEASARC API](https://heasarc.gsfc.nasa.gov/docs/archive/apis.html), [Gaia TAP](https://astroquery.readthedocs.io/en/stable/gaia/gaia.html).

## Connect measurements to a falsifiable prediction

1. Reference the actual update and stable native 3D K/E/M/T profile.
2. Derive boundary coupling and phase response without a penetration port.
3. Freeze generator, work metric, normalization, observable transform and uncertainty.
4. Retrieve selected measurement products plus reconstruction/calibration, quality masks, selections and uncertainties.
5. Reproduce the provider baseline before comparing One-Wave predictions.
6. Evaluate an untouched comparison set with null controls, convergence and competing-baseline residuals.

CERN invariant mass and LIGO strain are different observables with different units and detectors. A source-to-detector forward model is required for each. Do not treat normalized metadata coordinates as measured physical phase.

Current proof commands:

```sh
python3 solvers/test_mirror_gate_coupling.py
python3 solvers/audit_phase5_mass_claims.py --output /tmp/phase5-audit.json
```

The former tests a conservative algebraic witness; the latter reproduces target dependencies in legacy solvers. Neither is a first-principles 3D solution or an experimental discovery.

## Verified October 4 run

- CERN record 5501 metadata: 24 provider file entries; complete endpoint snapshot.
- GW150914 event and strain-file metadata: complete endpoint snapshots, four strain-file entries; source hashes verify.
- Optional packages installed and imported: astroquery 0.4.11, astropy 8.0.1, gwosc 0.8.3, h5py 3.16.0, uproot 5.7.6.
- MAST/HST query: 714 records; client ECSV output SHA-256 recorded in the native receipt. This table remains an external acquisition output, not a detector-model validation.
- HEASARC/numaster narrow query: succeeded with zero rows. Empty output was retained.
- Gaia: failed with a DNS-resolution error; no fabricated substitute table.
- HEPData selected endpoint: HTTP 403; no table acquired.

Ten tests pass: four conservative-operator tests and six metadata preservation/completeness tests. The legacy mass dependency audit also exits zero, confirming the reported code findings. Native archive results and installation are from this execution environment, not proof that packages or services were activated on the laptop or Jetson.

A second HEASARC query at radius 0.1 degree returned 108 NuSTAR observation records. Both the empty narrow result and successful wider result are retained separately; the query radius is part of the provenance.

The three successful native-client ECSV outputs are archived as gzip files beside their receipts. Each receipt's SHA-256 refers to the decompressed ECSV bytes. Preserve the receipt and its query with every table.
