# Rabbit Hopping × Circle of Fifths × Algorithm Zero — integration v1

**Status:** Mathematical translations and finite-state checks proposed; physical envelope mechanism **UNVERIFIED**. Additive integration to `Math_Verification` branch. Do not replace existing canonical source rules.

## Authoritative references
- `RABBIT_HOPPING_TRANSLATOR_HYPOTHESIS_QUESTIONS.md`: preserve source identity, selected center and wrapper as separate packet fields; mirrored packets, orientation and shared wrapper transitions. The 3-tuple is **not** automatically a 3D point.
- `UPDATED_43_TWO_CHOICE_THREE_MOVE_SIX_ROUTE_LOGIC.md`: two committed choices × three ternary moves = six routes; Ground excluded; five commitment states downstream and separate.
- `Nodes/DUAL_BUTTERFLY_HARMONIC_COORDINATES_A_E_20261010.md`: signed semitone offsets around each note center and separate per-string butterflies.
- `MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md`: append-only protected math; status and evidence boundaries.

## Three distinct coordinates, connected by explicit translators
1. **Pitch packet**: `(note_identity, absolute_semitone_index, low_offset, high_offset, octave, phase)`. Note identity is not an amplitude or spatial coordinate. Pitch-class wrap `n mod 12` does not erase octave.
2. **Rabbit packet**: `(source_identity, orientation_dependent_rank, selected_center, wrapper, polarity, route)`. For center T, wrappers are T-1 and T+1; mirror negates whole numerical packet. An offset or wrapper is **not** a musical interval unless an explicit map is selected.
3. **Algorithm Zero route**: `(choice, move)`, choice in YES/NO and move in DOWN/HOLD/UP. Exactly six valid committed routes. Do not treat HOLD as Ground. Do not infer a unique route from note or pitch alone.

## Explicit provisional integration
- Circle of Fifths supplies note selection and absolute frequencies under a declared tuning; for A major, `-5 (A4) +4` maps to E4/A4/C#5; for E5 the same local offsets map B4/E5/G#5.
- Rabbit Hopping can assign each selected note an identity-preserving packet and a center/wrapper transition. The choice of alphabet vs tone source rank, and the mapping from pitch to Rabbit center T, are **configuration inputs**, not an established physical derivation.
- Algorithm Zero supplies a six-route label for **observed** directional center crossing, Hold, and choice; crossing direction may be measured from sign of velocity, but binary YES/NO cannot be guessed from the sign alone. The five downstream commitment states require calibrated thresholds/history.
- Coupling/interference: compute superposition from actual frequency/phase/amplitude measurements; use coupled oscillator equations only with independently justified coupling coefficients and an energy ledger. Do not claim physical transfer from matching wrappers or musical intervals.
- Damping decreases amplitude in the standard linear model; a time-decreasing frequency requires separately justified dynamics.

## Tests
- Rabbit: A normal rank 1, reverse rank 26; (1,4,3)/(1,4,5), mirrors (-1,-4,-3)/(-1,-4,-5); T+1=(T+2)-1.
- Circle: +7 and -5 same pitch class but different absolute frequency; octave doubles frequency; +4 and +3 differ by one semitone.
- Algorithm Zero: six routes; reject Ground and conflicting dual assertion as committed binary choices; HOLD remains a valid movement.
- Cross-system: never convert Rabbit 3-tuples into spatial XYZ, pitch semitones into amplitude, or six routes into five commitment states.

## Falsification and next experiment
Record actual strings (isolated A4, E5 and together), estimate spectra, phase, decay and bridge response; compare measured superposition with independent isolated recordings. Determine whether any additional coupling model predicts held-out measurements. Record FAIL/INCONCLUSIVE explicitly. The integration is a **routing and analysis specification**, not proof of One-Wave field physics.
