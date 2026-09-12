# One-Wave Books — Canonical Publication Root

This directory is the canonical home for book manuscripts.

## Source-of-truth rule

- **Editable manuscript source:** Markdown where available; HTML only for book families currently authored directly as HTML.
- **Generated presentation output:** PDF. A PDF beside its source is not a second manuscript and must never be edited as authority.
- **Figures:** reusable source art/graphs live in `Books/figures/` or a book-local `figures/` directory.
- **Evidence:** raw data, simulation code, and receipts remain in their canonical experiment/simulation locations and are linked from the chapter.
- **Nodes outrank books:** books explain and apply the A–G node system; they do not silently invent new canonical mechanics.

## Duplicate-control rule

There must be one canonical editable manuscript for each public chapter. Before deleting an apparent duplicate, classify it as one of:

1. **exact duplicate** — same substantive content; keep canonical copy, delete redundant copy;
2. **generated output** — PDF/render of source; keep as output, never treat as duplicate authority;
3. **legacy/superseded** — preserve only when history/provenance is required, under `History/` rather than beside active manuscripts;
4. **parallel active draft** — merge unique material into the canonical manuscript, then remove the parallel draft;
5. **same name, different concept** — do not merge merely because terminology overlaps; respect `DUPLICATE_NAME_DISAMBIGUATION.md`.

No new top-level book manuscript tree should be created outside `Books/`. Existing parallel trees must be consolidated only after unique material is migrated.

## Publication standard

Technical chapters use the shared spine where applicable:

`Gray → 2D → 3D → Mathematics → Predictions/Tests → Yellow Audit → Future Work → Closing Thoughts`

Every quantitative chapter must define its variables, include equations appropriate to its subject, and show at least one meaningful figure or graph when geometry/dynamics/comparison is part of the argument. Evidence graphs require data or defined simulations; decorative art must be marked as illustration.

## Current book families

| Family | Current state | Immediate job |
|---|---|---|
| Book 1 — Micro | 17 active chapters | equation/figure audit across chapters |
| Book 2 — Small | 5 active source chapters in this recovery branch | data-backed graphs for Ch2–Ch5 |
| Book 3 — Medium | scope-only on main | build grounded physiology nodes/reference chapters before One-Wave claims |
| Book 4 — Large | scope-only on main | build grounded planetary/solar mechanics before One-Wave claims |
| Book 5 — Macro | 5 active chapters | reconcile cosmology only after stacked E-533/E-534/E-535 decisions |
| Android | proposed technical build manual | consolidate with proposed-brain book where content truly overlaps |
| Engineer the Future | 5 rendered Vol1 chapters | recover/retain editable source authority and equation/figure audit |
| Musical Universe | active parallel material | merge unique root material into `Books/Musical_Universe/`, then retire root duplicate tree |
| Proposed Android Brain | 4 active hypothesis/build chapters | finish after canonical architecture audit |
| Proposed One-Wave Consciousness | 5 active hypothesis chapters | retain explicit hypothesis status and grounding gaps |

## Recovery sequence

1. Establish canonical manuscript paths and chapter maps.
2. Correct false or dimensionally broken equations before visual polish.
3. Add equations, graphs, diagrams, and labeled illustration source assets.
4. Merge unique material from parallel drafts.
5. Delete only confirmed redundant/superseded copies.
6. Regenerate PDFs from canonical source.
7. Run a final link, equation, figure, and claim-status audit.
