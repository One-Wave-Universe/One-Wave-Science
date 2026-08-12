# Updated 39 — Relational-Mechanics Node Backlog and First Developed Nodes

A user review of the July 28+ development gap identified roughly 100
missing node addresses for a "relational mechanics" layer: differential/
relational motion, moving reference states, point-path-field tracking,
orbital wake/resonance dynamics, and the simulation-methodology rules
needed to test any of it honestly. Per explicit instruction, this update
registers the full scope as a coverage map and writes real, substantive
nodes only for the subset that already had enough worked reasoning
behind it — it does not fabricate derivations for the rest.

## What was added

### 1. Coverage manifest
`RELATIONAL_MECHANICS_NODE_BACKLOG.md` — all ~100 proposed nodes (A, B,
C, D, E, F, G series) with proposed dependencies and a three-tier
status legend (MAPPED / DEVELOPED / CANONICAL) mapped onto I-06's
existing gate/lifecycle vocabulary rather than inventing new fields.
Most entries remain MAPPED: title and one-line intended claim only, no
invented reasoning.

**Numbering correction:** the user's draft reused C-323–C-337 for this
block, colliding with the intrinsic-cell hardware nodes committed
immediately prior (C-323–C-326, Updated 38). Per explicit instruction,
those hardware IDs are permanent; the new block was shifted instead to
**C-327–C-341**. A/B/D/E/F/G needed no shift.

### 2. Eighteen developed nodes
Full I-06 nodes with real derivations, wiki pages, and honest gates —
the subset the user identified as already having substantive reasoning
behind it:

- **A-118** Relational Differential Primitive, **A-119** Moving
  Reference State, **A-120** Point-Path-Field Rotation, **A-125**
  Scale-Locality.
- **C-327** Relational Acceleration Equation, **C-328** Common-Mode
  Field Cancellation, **C-329** Actual State = Reference + Differential,
  **C-330** Moving Local Potential Perturbation, **C-331** Relative
  Encounter Frame Transformation, **C-332** Relational Energy Transfer
  — the full gravity-assist derivation chain, restated relationally and
  checked against standard patched-conic mechanics (Gray-equivalent by
  design; C-332's energy formula matches the standard slingshot result).
- **D-420** Resonant Phase Correlation, **D-421** Coherent Differential
  Accumulation, **D-422** Incoherent Differential Cancellation — the
  coherent-vs-random-walk accumulation pair needed before any
  resonance-clearing or libration claim can be tested.
- **G-734** Standard-Mechanics Control Run, **G-735**
  Prediction-Difference Gate, **G-736** No Hidden Controller Rule,
  **G-737** No Victory Without Observable Match, **G-743**
  Claim/Metaphor/Test Separation — simulation-methodology rules that
  make no physics claim of their own; they gate every future claim in
  this backlog (and, for G-743, repository-wide).

### 3. Governance updates
- `00_MASTER_INDEX.md`: 18 new rows across Appendix A, C, D, and G, plus
  a pointer to the backlog manifest.
- `DUPLICATE_NAME_DISAMBIGUATION.md`: A-103 (state-level differential)
  vs A-118 (slope-level differential) — distinct, do not merge.

## Honesty constraints actually enforced

- All 18 developed nodes reference the backlog manifest by name, not by
  bare node-ID code, for any of the ~82 still-MAPPED items they touch —
  the repository's own integrity validator (`idpat` unresolved-ID scan)
  enforced this mechanically, catching 34 premature ID citations that
  had to be rewritten before this update could pass.
- C-327/C-330/C-331/C-332 are explicitly labeled Gray-equivalent
  restatements of standard mechanics, not new physics — G-735
  (Prediction-Difference Gate) exists specifically so that equivalence
  is never later mistaken for a discovery.
- No MAPPED backlog row had its "Definition" column filled in with
  invented reasoning to look more finished.

## Integrity

`Integrity_Tools/validate_repository_integrity.py` passes with zero
errors after this change: 172 node files, 172 unique IDs, gate counts
YELLOW 106 / GREEN 64 / BRONZE 2, lifecycle counts ACTIVE 143 /
ACTIVE_HYPOTHESIS 21 / PROPOSED_BUILD 4 / HELD 3 / BLOCKED 1.

## Suggested next builds

- Promote MAPPED rows to DEVELOPED only in the dependency order the
  backlog manifest lays out, starting from whatever a given row's
  proposed dependencies actually require.
- Run C-327's suggested Kepler-orbit sanity check and C-332's
  documented-flyby numerical check as the first real (not merely
  algebraic) validations of the gravity-assist chain.
- Do not number a second "balanced-electronics" series until the
  backlog manifest's placeholder note for it is resolved, to avoid a
  third numbering collision.
