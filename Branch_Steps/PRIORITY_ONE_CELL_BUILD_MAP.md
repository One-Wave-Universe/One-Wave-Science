# Branch Step — Priority One Cell Build Map

Date: 2026-09-15
Branch: `codex/priority-one-cell-build-map`
Base HEAD: `3267902`

## Main goal

Turn the clarified ground-referenced recursive cell into an authoritative, test-gated build map without pretending an untested topology is finished breadboard wiring.

## Hard start

- Verified repository: `One-Wave-Universe/One-Wave-Science`.
- Read repository instructions and existing primitive/build/cell topology documents.
- Preserved existing Virtual Breadboard code and breadboard files.

## Exact change

- Added `PRIORITY_ONE_CELL_BUILD_MAP.md`.
- Made it priority one in `CURRENT_BUILD_ORDER.md`.
- Pointed the older `PRIMITIVE_BUILD_MAP.md` at the new execution authority.
- Corrected the older center description: virtual ground is ternary HOLD/zero, not another binary polarity.

## Locked requirements captured

- six hex side terminals, never corners, forming only three whole state gates;
- clockwise `A+ B+ C+ A- B- C-`, paired as `A+/A-`, `B+/B-`, and `C+/C-`;
- every gate flip resolves new Field UP together with last Void/action DOWN;
- virtual ground is the ternary HOLD/zero state;
- three-gate `DC -> AC -> RC` dependency;
- quadratic Views UP and mirrored last Actions DOWN coexist in Gate C;
- reinjection returns the measured consequence of the whole cell;
- muscle memory is rewritable path-specific impedance reinforcement;
- recall reconstructs a route from a cue;
- Build 0 through Build 7 each has a hard stop and receipts.

## Verification

- `git diff --check` — PASS.
- Repository text checks found all locked terms in the new authority and build-order pointer.
- No simulator, breadboard, application, or generated files were changed.

## Field notes

The earlier repository already contained most vocabulary but spread it across integration, timing, magnetics, and build-order files. It did not place selective memristive rewrite and whole-path reconstruction into one priority execution map. A follow-up correction removed the false six-sequential-gate reading: the six terminals form three whole mirrored gates.

## Void oversight

Decision: `ALLOW` as a documentation/build-order correction. Do not claim component-level completion. Exact switching, winding, sensing, reinforcement, rewrite, and reinjection values remain engineering selections requiring receipts.

## Look-back

- Changed: one authoritative priority build map plus two pointers/corrections.
- Worked: explicit stage order and hard stops prevent block diagrams from being called builds.
- Not done: no circuit has been electrically validated by this documentation step.
- Assumption corrected: magnetic retention alone is not muscle memory.
- Next permitted action: implement and test Build 0 simulator capability gates, one capability at a time.

## Hard stop

Reached. Stop after map, pointers, verification, and branch handoff.
