# Boundary coupling and Phase 5 reproduction audit

Date: October 4, 2026. Starting reference: `b3e0df9f0edff500d3e8bb6b7655e14bc6120179`.

## Question and correction

Can the current solvers independently predict masses and a Mirror Gate energy? No: the reproduced code uses target mass ratios and a target-defined stopping condition. This does not show that a future four-interaction derivation is impossible.

The corrected boundary rule is reflection, deflection, tangential roll-off and scattering, with coupling and phase shift at the Mirror Gate. Geometric forced penetration is removed from C-322 and Chapters 14–15. An internal phase update alone does not exchange Field and Void.

## Reproduce

From repository root, with Python, NumPy and SciPy:

```sh
python3 solvers/audit_phase5_mass_claims.py --output /tmp/phase5-audit.json
python3 solvers/test_mirror_gate_coupling.py
```

The audit reports source SHA-256 hashes and runtime versions. The reproduced legacy solver bytes match their pinned Git blob hashes. The audit never rewrites them.

## Findings

| Flavor | Calibrated legacy output MeV | Embedded comparator MeV | Absolute relative error |
|---|---:|---:|---:|
| up | 1.956349 | 2.16 | 9.43% |
| down | 3.786755 | 4.67 | 18.91% |
| strange | 15.739982 | 95 | 83.43% |
| charm | 437.302309 | 1270 | 65.57% |
| bottom | 2591.448567 | 4180 | 38.00% |
| top | 687636.548550 | 172700 | 298.17% |

These are arithmetic comparisons to the solver's legacy targets, not a valid fit to current experimental mass definitions. [PDG's 2025 quark table](https://pdg.lbl.gov/2025/tables/rpp2025-sum-quarks.pdf) assigns different mass definitions/scales to light, heavy and top quarks. A constituent model output cannot simply be compared with all of those as pole masses.

### Dependency controls

- `QuarkTopology.mass_scale` contains target ratios. Setting it to one gives 1.980256523 MeV for up/strange/charm/bottom/top; down gives 2.630079494 MeV because of an additional coefficient. The hierarchy is not generated independently of those inputs.
- `mass_from_numerical_differentiation` does not perform the stated second velocity differentiation of the full recurrent profile.
- `find_threshold_from_energy_curve` returns the first sample with energy at least 125 GeV. Grids of 50/200/2000/20000 points return 125.08866/128.10562/125.31069/125.03695 GeV. Approaching the supplied cutoff is not predicting it.
- For the fixed outputs, placing every flavor within an illustrative 10% band would require a common positive multiplier. Strange requires 5.432–6.639; top requires 0.226–0.276. Their intervals do not overlap. This is a diagnostic band, not an experimental error bar.
- At fixed profile, the canonical work-metric scaling gives a mass factor 4 for a work-metric factor 4; implemented square-root scaling gives 2. Any different parametrization needs an explicit derivation.

## Bounded solution implemented

`mirror_gate_coupling.py` supplies a four-port conservative operator. Four tests cover 40 random Hermitian generators, unitary power conservation, reverse evolution, a diagonal phase-only null, an exact half-power transfer, and rejection of invalid/gain-producing generators.

Its coefficients are illustrative and dimensionless. It has no geometric penetration port and no target mass or 125 GeV endpoint. Port labels alone do not implement reflection or roll-off spatial geometry. Passing these tests does not validate a physical One-Wave model.

## Next calculation that can change the scientific status

Derive the boundary generator and work metric from one stable native 3D K/E/M/T profile with cross-couplings. Freeze coefficients and a measurable prediction before opening withheld data. Record convergence, null controls, uncertainty and a competing baseline. A CERN comparison needs event selections, backgrounds and detector response; a LIGO comparison needs a source-to-strain model and detector calibration.

[CERN's documented CMS four-lepton example](https://opendata.cern.ch/record/5500) provides a baseline workflow, not a replacement theory. [GWOSC](https://gwosc.org/api/) provides event, strain and quality metadata. Keep these measurement domains separate.

Scientific readiness means an independent quantitative discriminator and replication. A prize claim cannot substitute for those results.
