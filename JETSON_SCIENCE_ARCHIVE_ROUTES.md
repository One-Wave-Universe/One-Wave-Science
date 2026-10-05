# Jetson scientific archive routes — AI operating authority

Read GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md, AI_BRIDGE_START_HERE.md and ENGINE_EVIDENCE_PIPELINES.md first. Resolve the actual device, canonical repository root, branch, HEAD and working-tree status at each action boundary. Use the matching receipt, not a green workflow or remembered result. Source registry: One_Wave_Bench/data/open_data_sources.json. Conversion chart: Engine/PARTICLE_TO_WAVE_CONVERSION_CHART.md.

## Verified 2026-10-05 on the Jetson

| Route | Matching live result | Scope |
|---|---|---|
| CERN Open Data | CMS search and record 5501; ALICE, ATLAS, LHCb searches returned matching experiment labels | Public record metadata; search results also include documentation |
| GWOSC | Run list, GW150914 event and strain-file metadata returned | LIGO/Virgo/KAGRA archive route; not separate detector strain analyses |
| MAST Hubble/HST | 714 observations near Crab | Native query table |
| MAST JWST / TESS | 18 / 6 observations near Crab | Native query tables |
| HEASARC NuSTAR | 108 rows in 0.1-degree Crab region | numaster table; 0.01-degree query legitimately returned zero |
| Gaia | 3 source IDs and coordinates via synchronous TAP | Removed expensive global ORDER BY and asynchronous polling |
| ESO / ALMA | 3 observation IDs and sky coordinates each | Public ObsCore TAP metadata |
| DESI | DR1 directory links returned | Release inventory only; no spectral download or database search |
| OpenNeuro | ds000224 Midnight Scan Club record returned | Brain MRI/fMRI dataset metadata; no subject images fetched |
| DANDI | 3 brain-search records returned | Public neuroscience dataset versions/asset counts; no recording assets fetched |
| PhysioNet | S001 EEG recording identifiers returned | EEG Motor Movement/Imagery RECORDS index; no EDF samples fetched |
| HEPData | HTTP 403 on search and two public record routes | BLOCKED on this route; do not claim a successful bridge |

The registry covers additional missions through their archives. Kepler/K2, GALEX and individual HEASARC missions other than NuSTAR were not separately queried in this pass. This is not every telescope, collider or brain archive worldwide. A new source/instrument needs its own matching query receipt. See One_Wave_Bench/data/receipts/science-routes-20261005/receipt.json for exact hashes, cache paths and failures.

## Runnable worker

The Jetson native-query dependency environment was installed at ~/.local/share/one-wave/science-data-venv. Reproduce it using:

```bash
python3 -m venv ~/.local/share/one-wave/science-data-venv
~/.local/share/one-wave/science-data-venv/bin/python -m pip install -r scripts/science-data-requirements.txt
```

Run from the verified Science checkout containing these scripts. Keep outputs in the metadata cache, not a second maintained repository copy.

```bash
python3 scripts/science_archive_search.py cern-open-data --query CMS --output .one-wave-metadata/current/cern
python3 scripts/science_metadata_bundle.py --output .one-wave-metadata/current/cern-gwosc
~/.local/share/one-wave/science-data-venv/bin/python scripts/archive_metadata_query.py mast --mission HST --output .one-wave-metadata/current/hst
~/.local/share/one-wave/science-data-venv/bin/python scripts/archive_metadata_query.py mast --mission JWST --output .one-wave-metadata/current/jwst
~/.local/share/one-wave/science-data-venv/bin/python scripts/archive_metadata_query.py heasarc --radius-deg 0.1 --output .one-wave-metadata/current/nustar
python3 scripts/science_archive_search.py gaia-archive --output .one-wave-metadata/current/gaia
python3 scripts/science_archive_search.py eso --output .one-wave-metadata/current/eso
python3 scripts/science_archive_search.py alma --output .one-wave-metadata/current/alma
python3 scripts/science_archive_search.py openneuro --record ds000224 --output .one-wave-metadata/current/openneuro
python3 scripts/science_archive_search.py dandi --query brain --output .one-wave-metadata/current/dandi
python3 scripts/science_archive_search.py physionet-eeg --query S001 --output .one-wave-metadata/current/eeg
python3 scripts/science_archive_search.py desi --output .one-wave-metadata/current/desi
```

A source already registered but requiring a different record/product uses its documented native archive query and equivalent provenance. OpenNeuro record query and bounded listing are implemented; global free-text search is not. GWOSC route lists runs; use science_metadata_bundle.py for event/strain metadata. ESO/ALMA/Gaia relay queries are bounded metadata samples, not arbitrary ADQL searches. Search limits are 1–10 rows where the service supports them, body cap 2 MiB, timeout at most 60 seconds. Native MAST cone searches can return more rows; record that count. Pagination links are preserved; no page is called the whole catalog.

## Bridge and relay use

Remote Desktop Commander is the proven direct Jetson route for this receipt. The existing Bridge-Comand Hive Pipe terminal_run route can carry the same argument vectors. Discover the current device/gateway; never copy a stale tunnel URL. Send argv, the verified cwd, a bounded timeout, intention and consequence. Example argv:

```json
["python3","scripts/science_archive_search.py","openneuro","--record","ds000224","--output",".one-wave-metadata/current/openneuro"]
```

Use intention: retrieve public metadata for the named repository question. Use consequence: write hashed source/receipt artifacts only, without changing solver equations or relabeling metadata as measurements. Require a matching request/device ID, actual exit code, source IDs, acquisition timestamp, raw-body or native-table hash, and receipt path. This pass verifies direct-device execution and an authenticated local Hive Pipe MCP call to terminal_run: matching JSON-RPC request ID and exit 0 fetched GWOSC metadata with the same hash. The external HTTPS/tunnel route was not separately tested. Bridge-Comand owns transport; this Science document owns source/transform directions. No new competing daemon or copied canon is needed.

## Reference and interpretation gate

Before each fetch, inspect this registry and current metadata status. Before each transform, verify raw hashes and classify the source. Before each scientific conclusion, read units, calibration, quality, masks, selection and held-out controls. Metadata never supplies missing phase, waveform, detector units or a physical coupling law. Acquisition failures remain failures. Do not bypass HEPData's denial or invent replacement measurements; another permitted acquisition route requires a separate receipt.

Official source documentation: https://docs.openneuro.org/api.html ; https://docs.dandiarchive.org/api/rest-api/ ; https://physionet.org/content/eegmmidb/1.0.0/ ; https://archive.eso.org/programmatic/ ; https://almascience.eso.org/alma-data/archive/archive-documentation ; https://data.desi.lbl.gov/doc/access/ ; https://astroquery.readthedocs.io/en/stable/mast/mast_obsquery.html .
