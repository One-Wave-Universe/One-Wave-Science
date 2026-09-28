# Hex lattice lock + ω_s — first run

Brick: **YELLOW**. This run is a fail that is allowed to be a fail.

## Drives (D-414 official folds, not reinterpreted)

| Channel | Envelope |
|---|---|
| Z_K | CODATA-2022 proton fold. Anchor 938.27208816 MeV. Not derived. |
| Z_M | GW150914 bidirectional 48-pt envelope. Higgs boundary 125.11 GeV is the scale stamp. LIGO stays LIGO. |
| Z_T | Keepin U-235 thermal β=0.0067 fold. |
| Z_E | PhysioNet S001R01 present in the local drive pack; unused on this first hex pass. |

Fold grammar: BEGIN→MOVE→HOLD→BUILD→BREAK→LOOP, doubled, mirrored through the center (B-221 / B-224).

## What was asked

1. Same lock inequality on a **hex lattice**, not three free masses.
2. Measure ω_s(τ) against ω_s² = 3τ/2.
3. Kill H mid-run and require dissolve.
4. Source χ, not a painted Gaussian.

## What happened (2026-09-28)

- Hex sites: axial R=5.
- χ from declared MACRO + three local Yukawa sources.
- Three labeled centroids ran to the rim. Spread ≈ 4.72 on every τ. **0 locked / 5 failed.**
- Measured ω_s stayed ~0.002–0.016. Theory √(1.5τ) is 0.27–1.64. Relative error on ω_s² ≈ 1. The shear law is **not** recovered on this field.
- H-kill at step 140: **dissolved** (spread/identity of the three labels broke). That part of the inequality held.

## Why this is the cause behaving

A hex that always locked would have been a lie. The triad bust locked 28/32 because it was three point masses. The lattice has not earned that bust. Do not promote D-413/D-414.

## Next cut (do not skip)

Hold three blobs on the hex with source χ only — no rim-running. Then measure ω_s from the **field**, not from an overlay spring. Then compare ω_s² to 3τ/2. Then kill H.

Local runner: `OneWaveEngine/busts/hex_lattice_lock.py`
Envelopes: official `waves_bundle.json` → `drive_envelopes.json`
