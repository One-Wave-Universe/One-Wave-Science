# Jetson Science Metadata Worker Contract

The Jetson is the external scientific metadata worker for One-Wave-Science.

## Worker loop

1. **REFERENCE** — query the local metadata lens before inventing dataset names, event IDs, run IDs, detector releases, or source URLs.
2. **FETCH** — refresh only the bounded public metadata needed for the task.
3. **COMPARE** — separate measured/public metadata from One-Wave interpretation.
4. **WORK** — use the evidence to build or revise simulations, solvers, mappings, tests, and documentation.
5. **RECEIPT** — every evidence-dependent repo change records source, record/event ID, fetch time, and the exact claim the metadata supports.
6. **HOLD** — missing metadata, source failure, or ambiguous identifiers do not become guessed facts. Route the unresolved item back through the bridge.

## Local interface

```bash
python3 tools/jetson_science_metadata.py sync cern --limit 25
python3 tools/jetson_science_metadata.py sync gwosc --limit 25
python3 tools/jetson_science_metadata.py search "Higgs"
python3 tools/jetson_science_metadata.py search "GW"
```

Cache:
`~/.local/share/one-wave-science-metadata/metadata.sqlite3`

The cache is external evidence storage, not repository canon. Do not commit the SQLite database or downloaded raw datasets.

## AI rule

AI workers may use metadata to locate and characterize real scientific observations. They must not describe a One-Wave mapping as validated merely because a CERN/GWOSC record exists. A validation claim requires an explicit conventional baseline, One-Wave calculation, residual/comparison, and an independently checkable result.

## Expansion

New adapters belong behind the same interface. Candidate public sources include PDG and additional astronomy/cosmology catalogs. Each adapter must preserve original source identifiers and URLs.
