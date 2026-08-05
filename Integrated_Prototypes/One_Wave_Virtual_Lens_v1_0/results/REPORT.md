# One-Wave Virtual Lens v1.0 Test Report

## Result

- Unit tests: **6/6 passed**
- Continuous visual loop: **90/90 ticks confirmed**
- Reference phase flips: **90**
- Brightness-change events: **911** total
- ON events: **455**
- OFF events: **456**
- Occluded ticks: **26**
- Mean hidden-motion prediction error: **1.80 px**
- Maximum hidden-motion prediction error: **3.05 px**
- Damaged visual attractor recall: **4/4 correct**
- Physical camera used: **No**

## RAM actually allocated by tracked visual structures

- Persistent field: 262,144 bytes
- Confidence map: 262,144 bytes
- Age map: 131,072 bytes
- Prediction map: 262,144 bytes
- Local Hopfield weights: 1,048,576 bytes
- Stored visual patterns: 2,048 bytes
- Lens view: 16,384 bytes
- Event map: 16,384 bytes
- Current pattern: 512 bytes
- **Total tracked allocation: 2,001,408 bytes**

This is measured allocation, not a fixed percentage quota.

## Hopfield preservation

The complete supplied Hopfield v2.1 folder is copied under `hopfield_original/`.
The source hash is checked by the test suite against
`ORIGINAL_HOPFIELD_SHA256.txt`. The visual adapter does not edit the original
Hopfield source, musical codec, HOLD definition, or finished recall audits.

## Current boundary

The visual brain is autonomous and local. Audio, M4, and Boltzmann coupling are
not yet active. The included Boltzmann bridge contract is reference-only so the
visual packet can be integrated later without inventing a second coordinate
language.
