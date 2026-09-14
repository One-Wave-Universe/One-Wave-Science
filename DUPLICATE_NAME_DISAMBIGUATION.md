# Duplicate-Name Disambiguation Registry

| Shared term | Node | Canonical display name | Distinction | Merge rule |
|---|---|---|---|---|
| Balance | B-201 | Equilibrium Balance | Scalar equilibrium/imbalance measure | Do not merge with G-709 |
| Balance | G-709 | Regulated-Response Balance | Feedback-scaled response rule | Do not merge with B-201 |
| Pressure | B-202 | Pressure | State generated from scalar imbalance | Do not merge with E-503 |
| Pressure | E-503 | Pressure (Gradient Form) | Spatial-gradient energy/pressure specialization | Do not merge with B-202 |
| Mirror | B-205 | Mirror | Flip operation | Do not merge with C-301 |
| Mirror Gate | C-301 | Mirror Gate | Boundary/location where the flip operates | Do not merge with B-205 |

## ID collisions (distinct from shared terminology above)

The rows above disambiguate one *term* shared by two different IDs. The
two entries below are a different, more serious problem found while
backfilling `00_MASTER_INDEX.md`'s Appendix G (2026-09): the *same ID*
assigned to two substantively unrelated node concepts, not a shared
term and not a topic + its own supporting receipt (compare `G-728`'s
laundry-list node plus its `G-728_E1_STAMP.md`/`G-728_PROGRESS_OVERLAY.md`
tracking files, or `G-757`'s seven-cell node plus its
`G-757_HESSIAN_RECEIPT.md` -- those are one topic with auxiliary
artifacts sharing its ID on purpose, not collisions).

| ID | File A | File B | Status |
|---|---|---|---|
| G-743 | `G-743_PPF_Schema_and_2D_Hex_Graph.md` — PPF schema / 2D hex graph math trail (YELLOW-MATH-TRAIL) | `G-743_Proven_Quadrature_Rotating_Field_Views_Up_Actions_Down.md` — demonstrated quadrature rotating-field hardware (GREEN) | UNRESOLVED — not renamed; renumbering either file risks breaking cross-references not exhaustively traced in this pass |
| G-744 | `G-744_Field_Void_Occupancy_and_Loop_Pickup.md` — Field/Void occupancy, five lifecycle verbs, loop pickup (YELLOW-DOMAIN-WRAPPER) | `G-744_Literal_One_Cell_Breadboard_Build_Real_Parts_and_Math.md` — literal one-cell breadboard hardware build (YELLOW) | UNRESOLVED — not renamed; renumbering either file risks breaking cross-references not exhaustively traced in this pass |

Resolution requires: grep every node/chapter for references to each
`G-743`/`G-744` mention, determine which file each reference actually
means from context, assign one of the two files a fresh ID, and update
every referencing file to match before this can be closed. Do not
resolve by silently picking one file to keep.
