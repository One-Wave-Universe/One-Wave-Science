# Stage 01 — CERN Detector Excitation → One-Wave Transform

Purpose: use CERN Open Data at the lowest practical detector level and express measured collision excitations in One-Wave coordinates without replacing the raw measurements.

## Canonical starting point

Do **not** start from jets, electrons, muons, or other reconstructed object labels.

Start from detector-space measurements when available:

- tracker reconstructed-hit positions
- ECAL crystal energy deposits
- HCAL tile energy deposits
- muon-chamber hits
- event provenance: run, event, luminosity section, timestamp

CMS event-display data explicitly exposes tracker rec-hits, ECAL rec-hits, HCAL rec-hits, and muon rec-hits. A separate CMS open dataset also exposes tracker-hit positions in ROOT ntuples that can be read without CMS-specific software.

## Scientific boundary

The detector recorded interactions/excitations in detector material. One-Wave may analyze those measurements as a spatial excitation pattern.

That is a hypothesis/representation layer, not a claim that CERN already measured a literal fundamental wave field.

Every transformed value must retain its raw source measurement.

## Lowest-level point

A detector excitation point is:

```
{
  event_id,
  detector,
  channel,
  x, y, z,
  energy_or_signal,
  time_if_available,
  raw_source
}
```

No particle identity is required.

## One-Wave point transform

For a hit/deposit at position (x,y,z):

```
r = sqrt(x^2 + y^2 + z^2)
phi = atan2(y,x)
rho = sqrt(x^2 + y^2)
```

Candidate state coordinates:

- POINT position = (x,y,z)
- amplitude-like measured strength = detector energy/signal
- phase-like geometric coordinate = phi
- path coordinate = r or ordered detector-layer traversal
- signed opposed coordinates come only from declared detector partitions
- provenance remains attached

## Event resultant

For weights w_i equal to the measured detector signal or energy where physically meaningful:

```
X = Σ w_i cos(phi_i)
Y = Σ w_i sin(phi_i)
S = Σ |w_i|
R = sqrt(X^2 + Y^2)
Phi = atan2(Y,X)
C = R/S
```

C is a directional coherence statistic, not proof of quantum phase coherence.

## One-Wave opposed lean

For a declared opposed detector partition:

```
D = (S_plus - S_minus)/(S_plus + S_minus)
W = 50 + 50D
```

Use the locked bands:

- 90–100 extreme expression / danger
- 75–85 strong expression
- 60–70 moderate expression
- 45–55 active middle / stable oscillating region
- 30–40 moderate compression
- 15–25 strong compression
- 0–10 extreme compression / danger

The six unnamed 5-point gaps remain transition/hysteresis regions.

Possible partitions must be tested, never assumed:
- +x / -x
- +y / -y
- +z / -z
- +eta / -eta
- clockwise / counterclockwise projected contribution
- detector subsystem A / declared opposed subsystem B

## Point → Path → Field

POINT:
one measured detector excitation.

PATH:
a geometry-ordered sequence of measured points. A path can be compared with a CMS reconstructed track but does not inherit that track as ground truth.

FIELD:
the complete spatial excitation pattern of an event or detector region, including scalar strength, vector resultants, density, gradients, and symmetry/imbalance measures.

## Required controls

Each claimed pattern must be compared with:
1. raw detector coordinates and deposited signal;
2. randomized azimuth control;
3. reflected-coordinate control;
4. event-mixed control;
5. conventional CMS reconstruction when available;
6. detector geometry/acceptance effects.

If the One-Wave statistic survives only because of detector geometry or selection, it is not new physics.

## First real-data targets

1. CMS event-display sample derived from `/JetHT/Run2012B-22Jan2013-v1/AOD`
   - 25 events
   - tracker rec-hits
   - ECAL/HCAL rec-hits
   - muon rec-hits
   - browser-readable event representation

2. CMS record 12220 tracker-hit enriched samples
   - explicit tracker-hit positions
   - ROOT ntuple format
   - no CMS-specific software required for basic reading
   - useful for larger statistical tests

Start with one event. Preserve every raw coordinate. Reproduce it visually. Then apply the One-Wave transform. Only after that scale to many events.
