# Updated 38 — One-Wave Intrinsic Cell Hardware

This update adds the first **proposed physical hardware** track for a One-Wave
"cell": an analog, no-processor-in-the-loop organelle intended to sense its own
boundary, resolve ternary state, time its own oscillation, remember its
orientation, and repay its own losses. Everything below is Proposed Build under
I-05 — no physical unit has been built or tested yet.

## What was added

### 1. Four new canonical nodes (Appendix C, Applied Mechanics & Engineering)
- **C-323** Primitive Continuous Mirrored Chain — working-notes vocabulary
  (six-pair mirrored chain, five-level scale) that underlies the hardware
  nodes below. GREEN, Active Hypothesis.
- **C-324** One-Wave V0 Hex Cell — Multicellular Host Architecture — the
  six-organelle-plus-coordinator hex-ring scaling target and its seven-item
  V0 proof checklist. YELLOW, Proposed Build.
- **C-325** One-Wave V0-A Intrinsic Cell — Engineering Architecture and
  Simulation — the full intrinsic-cell organ architecture, operating loop,
  ternary language mapping, SPICE skeleton, and a behavioral (control-level)
  simulation comparing decay, continuous drive, phase-timed refresh, and
  restart. YELLOW, Proposed Build. Carries forward `manifest.json`, BOM, SPICE
  circuit, and simulation receipts (CSV + PNG) from the source engineering
  package, plus an explicit note on a stale Raspberry Pi Pico reference left
  in the imported source docs.
- **C-326** One-Wave V0 Intrinsic Cell — First Organelle Build Wiring — the
  refined, breadboard-buildable single-organelle schematic (Sections A-F),
  block-diagram SVG, and BOM. Supersedes C-325's own schematic section for
  the first physical build. YELLOW, Proposed Build.

### 2. Wiki pages
`Wiki_Pages/C-323_Wiki_Page.html` through `C-326_Wiki_Page.html`, matching the
existing canonical-metadata banner and status-plate template used across the
A-G wiki set.

### 3. New book chapter
`Books/Engineer_The_Future/Vol1/Ch06_The_Intrinsic_Cell.html` (+ generated
`.pdf`) — the sixth Volume I chapter, in the existing steampunk-field-manual
template, grounded in C-323 through C-326 and carrying its own Yellow Audit
plate.

### 4. Master index and book plan
- `00_MASTER_INDEX.md` Appendix C table extended to C-326 (24 active files).
- `BOOK_SYSTEM_MASTER_PLAN.md` Engineer the Future section now lists all six
  current Volume I chapters.

## Explicitly not proven

Per the imported `manifest.json`: superconducting operation, MTJ memory, full
six-node field rotation, and energy savings on physical hardware. No physical
organelle has passed the C-325/C-326 test plan; the behavioral simulation is a
control-level model, not a transistor-level or magnetic SPICE proof.

## Integrity

`Integrity_Tools/validate_repository_integrity.py` passes with zero errors
after this change: 154 node files, 154 unique IDs, gate counts YELLOW 95 /
GREEN 57 / BRONZE 2, lifecycle counts including PROPOSED_BUILD 4 (up from 1,
i.e. C-324, C-325, C-326, plus the prior G-722) and ACTIVE_HYPOTHESIS 8.

## Suggested next builds

- Build and test the single organelle in C-326 against the C-325 test plan
  before attempting any multi-cell coupling.
- Resolve the stale Raspberry Pi Pico selection-logic note in C-325's imported
  `docs/06_SOURCES_AND_PART_NOTES.md` once a physical build is underway.
- Formalize C-323's chain into an explicit update rule and internal
  consistency check before any promotion past GREEN.
