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
