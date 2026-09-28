# Stage 06 — Spectral Lattice Phase Map

Runnable first test for G-767. It maps positive measured scales into fractional log2 phase and compares circular phase coherence with a matched-range log-uniform null.

This is a scaffold, not evidence of a lattice. The next data adapters should preserve immutable source values, units, uncertainty, selection/acceptance and provenance. Particle/object labels may be carried as metadata but do not enter the statistic.

## Input

CSV:

```
scale,width,uncertainty,label
3.0969,0.0000926,,source-label
...
```

Run:

```bash
python3 spectral_lattice_phase.py measurements.csv --x0 1.0 --trials 10000
```

Do not optimize x0 on the evaluation data. Freeze x0/statistic on training data before held-out tests.

## Expansion order

1. synthetic exact-octave/non-octave fixtures;
2. machine-readable measured resonance table with uncertainty;
3. CERN continuous invariant-scale/event spectrum with acceptance controls;
4. octave-slice density correlation rho_n(phi);
5. width/Q versus phase analysis;
6. frozen-statistic GWOSC frequency-domain validation;
7. compare any surviving mode with G-766 lattice dispersion.


## Real-data ingest: CMS record 700

The first real continuous spectrum is the official CERN Open Data CMS Run2010B dimuon-derived dataset, record 700. It contains 100,000 selected events and publishes invariant mass M together with event/four-vector metadata. CERN explicitly classifies this as an education-derived dataset and says it is not suitable for a full physics analysis; G-767 therefore uses it as a reproducible spectral-method benchmark, not as a precision new-physics dataset.

```bash
cd sims/06-spectral-lattice-phase
python3 fetch_cms_dimuon.py --out data
python3 spectral_lattice_phase.py data/cms_record700_g767_scales.csv --x0 1.0 --trials 10000
```

The fetcher queries the official record API, selects the largest official CSV, preserves the raw bytes, records SHA-256/provenance, and emits a minimal scale CSV. Do not commit large downloaded source data unless the repository data policy explicitly calls for it.

### Interpretation warning

The current circular-coherence statistic is only a first diagnostic. A continuous selected mass spectrum can generate apparent phase concentration from its marginal density and acceptance. The next control must therefore estimate the smooth observed log-density and draw matched null samples from it; the simple log-uniform null is insufficient for a lattice claim.

## PDG machine-readable expansion

PDG's 2026 edition exposes Summary Table and Particle Listing data through its machine-readable API. Add a PDG adapter only against the documented API/schema and preserve edition, quantity, units, uncertainty, status and source identifiers. Do not hand-copy a preferred list of resonances. The PDG table is a second dataset; it must not be used to tune the CMS statistic and then counted as independent validation.
