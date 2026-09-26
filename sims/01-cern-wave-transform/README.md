# Stage 01 — CERN Event → One-Wave State Transform

Purpose: use CERN Open Data as measured input while expressing each event in One-Wave coordinates.

## Scientific boundary

CERN detector data are not assumed to be literal waves. CMS NanoAOD stores reconstructed event observables such as momentum, azimuth, pseudorapidity, object counts and missing transverse momentum. This stage defines a reversible analysis transform from those observables into One-Wave state coordinates.

The raw observables are always retained beside the transformed state.

## First transform

For each reconstructed object i:

- amplitude / expressed strength: A_i = pT_i
- phase-like coordinate: phi_i = detector azimuth φ_i
- path inclination coordinate: eta_i = pseudorapidity η_i
- signed transverse vector:
  - X_i = pT_i cos(phi_i)
  - Y_i = pT_i sin(phi_i)

For an event:

- total expressed scalar strength: S = sum_i pT_i
- net transverse vector:
  - X = sum_i X_i
  - Y = sum_i Y_i
- net amplitude: R = sqrt(X^2 + Y^2)
- net phase: Phi = atan2(Y, X)
- coherence ratio: C = R / S, for S > 0

C ranges from near 0 for strongly cancelling transverse directions toward 1 for strongly aligned transverse directions.

## One-Wave 0–100 lean

The first non-arbitrary signed lean must come from a declared comparison, not from particle labels.

For a chosen opposed partition P+ and P-:

D = (S_plus - S_minus) / (S_plus + S_minus)

Normalize:

W = 50 + 50 D

Then classify using the locked One-Wave bands:

- 90–100: extreme expression / danger
- 85–75: strong expression
- 70–60: moderate expression
- 55–45: active middle / stable oscillating region
- 40–30: moderate compression
- 25–15: strong compression
- 10–0: extreme compression / danger

The unnamed 5-point gaps remain transition/hysteresis regions.

The partition must be explicit. Examples to test rather than assume:
- detector hemisphere +η versus -η
- clockwise versus counterclockwise transverse contribution
- selected detector/object channel versus its declared complement
- measured visible transverse vector versus missing transverse vector

## Point → Path → Field

POINT:
one detector/reconstructed-object contribution represented by {pT, phi, eta, time/event id}.

PATH:
ordered or associated contributions linked by detector geometry, reconstructed track/jet structure, or event relation.

FIELD:
event-wide or region-wide vector/scalar aggregation over all selected points and paths.

## Required controls

Every plot must permit comparison with:
1. raw CERN observable distribution;
2. shuffled-phase control;
3. sign-reflected control;
4. standard HEP summary quantities;
5. One-Wave transformed quantities.

Any apparent structure that also appears after shuffling is not evidence for a physical One-Wave relation.

## First dataset

Start with CMS 2016 RunH NanoAOD JetHT or SingleMuon because NanoAOD is directly readable with ROOT-compatible Python tools and contains event branches without requiring CMSSW for basic analysis.

Do not ingest the whole dataset first. Validate the transform on a small reproducible sample, then scale.
