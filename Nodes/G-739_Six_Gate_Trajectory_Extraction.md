---
id: G-739
title: Six-Gate Trajectory Extraction
status: yellow
tier: executable-math
claim_boundary: measured gate labels for declared trajectories; not a universal physical derivation
---

# Node G-739: Six-Gate Trajectory Extraction

## Purpose

The six recursive gates must be measured from motion rather than painted onto
an animation or imposed as a one-way script. This node defines a conservative
extractor for:

[
	ext{Begin}ightarrow	ext{Build}_{coherent}ightarrow	ext{Hold}
ightarrow	ext{Build}_{unstable}ightarrow	ext{Break}ightarrow	ext{Loop}.
]

The labels describe stability regions around a bidirectional oscillator. They
do not replace Field/Void identity, the two choices, the three moves, the five
commitment states, or the continuous Mirror phase.

## Per-sample receipt

For sample (i), the extractor receives:

- (x_i): displacement from the declared center;
- (v_i): velocity;
- (E_i): stored-state or energy ledger;
- (c_iin[0,1]): coherence;
- (h_ige0): instability/heat receipt.

The finite difference

[
dot E_i=(E_i-E_{i-1})/(t_i-t_{i-1})
]

separates building, holding, and release. Every tolerance is declared by the
caller and retains the units of its variable.

## Evidence rules

- **Begin:** inside the center band, low speed, low stored state.
- **Coherent Build:** positive energy rate with coherence above threshold and
  heat below threshold.
- **Hold:** energy rate and speed both within their tolerances while stored
  state remains above the Begin floor.
- **Unstable Build:** positive energy rate accompanied by low coherence or high
  heat.
- **Break:** negative energy rate beyond the release threshold, or a declared
  boundary excursion accompanied by outward motion.
- **Loop:** a center crossing after an observed Break. Direction and crossing
  speed are retained so Loop is not confused with exact reset.
- **Unclassified:** evidence insufficient or contradictory.

The extractor never fabricates a missing gate to make a complete sequence.

## Validation boundary

Deterministic tests cover each gate, ambiguous evidence, and the crucial rule
that Loop requires prior Break. The output includes raw energy-rate receipts and
sample indices so classification can be replayed.

This closes B3 as executable gate extraction. B4 remains responsible for the
minimum stored-state, threshold, and phase conditions that make a Break valid.

**Brick recommendation:** Yellow.
