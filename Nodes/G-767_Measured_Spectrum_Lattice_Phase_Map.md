---
node_id: "G-767"
canonical_name: "Measured Spectrum Lattice Phase Map"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Spectral Field Mapping / Open Data / Cross-Scale Lattice Test"
claim_gate_detail: "YELLOW — defines falsifiable scale-phase tests; no superfluid crystal lattice is established until recurrence survives nulls and held-out data"
metadata_standard: "I-06"
---

# G-767 — Measured Spectrum Lattice Phase Map

## Question

Can independent measured excitation spectra be compressed by a common recursive scale coordinate more strongly than matched null data?

Experiment-provided particle/object names are retained only as source metadata. The analysis operates on measured energy/mass-like scales, widths, lifetimes, counts, momenta, angles, strain, frequency, uncertainties and provenance.

## Scale coordinate

For a positive measured scale x and declared reference x0:

```
u = log2(x/x0)
n = floor(u)
phi = u - n
```

n is octave depth. phi in [0,1) is scale phase. x0 must be fixed a priori or fit on training data and frozen before held-out evaluation.

For resonance-like measurements also retain width Gamma and define Q=x/Gamma when dimensionally appropriate. Test whether scale phase, width/Q and family-independent spectral density covary.

## Continuous spectrum map

For measured spectral density N(x), construct density in logarithmic scale:

rho(u) = dN / dlog2(x)

and compare octave slices rho_n(phi). Candidate recurrence is a shared component F(phi):

rho_n(phi) = A_n F(phi) + epsilon_n(phi)

A recurring visual pattern is not enough. Quantify recurrence/coherence and compare it with null ensembles preserving selection function, bandwidth and density.

## Required nulls

1. log-scale shuffle preserving sample count/range;
2. circular phase shift;
3. event mixing where event data exist;
4. detector acceptance/background control;
5. smooth-density draws matched to the observed marginal distribution;
6. conventional/reference reconstruction;
7. synthetic exact-octave positive control;
8. synthetic non-octave negative control.

## Cross-domain sequence

A. PDG/reference tables: measured scales, widths, lifetimes and uncertainties.
B. CERN: event-level energy/invariant-scale and detector excitation spectra.
C. GWOSC: calibrated strain h(t), Fourier/time-frequency spectra.
D. spectroscopy/antimatter/astronomy only after A-C freeze the statistic.

The statistic and scale-reference rule are frozen before moving to the next domain. Independent domains are validation, not extra tuning data.

## Candidate lattice signatures

A lattice interpretation becomes worth further work only if several signatures co-occur:
- octave recurrence beyond matched nulls;
- preferred sub-octave phase positions stable to bin/window changes;
- systematic width/Q relation to phase position;
- recurrence across independent runs/instruments;
- held-out prediction using one frozen parameterization;
- compatibility with G-766 numerical lattice dispersion rather than merely a numerological ratio.

## Superfluid/crystal boundary

"Superfluid crystal lattice" is a One-Wave hypothesis, not an ingest assumption. Spectral recurrence alone cannot establish superfluidity or crystallinity. A stronger case would additionally require quantitative dispersion, collective-mode, symmetry/anisotropy, defect/transport or coherence predictions that distinguish the proposed lattice from smooth-field and conventional controls.

## Pass gate

Advance only when the predeclared statistic beats all matched nulls with uncertainty propagated, remains stable under resolution/selection sweeps, and predicts held-out data. Report negative results.

## Dependencies

- `sims/00_CANONICAL_INGEST_RULE.md`
- `sims/01-cern-wave-transform/README.md`
- `sims/04-gwosc-strain/README.md`
- `Nodes/G-766_Discrete_Lattice_Dispersion_and_Octave_Emergence_Proof.md`
