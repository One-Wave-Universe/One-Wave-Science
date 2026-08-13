
## G-721 Corrected — Primitive Is the Triple (n,k,s), Not the Derived (p,r) Pair

The prior pass's generator (`p=n+k, r=2p+s`) reproduced every packet form correctly but was mis-described as "minimal." Challenged directly: `p` is a derived anchor, and dropping `n` after forming it loses information the generator's own decoder still silently needed. Attacked computationally before touching the node text, per instruction not to assume minimality just because the tables came out right, and not to touch the wiki page until the attack was finished.

- **Degeneracy confirmed**: `(n=4,k=1)` and `(n=5,k=0)` both give `p=5`, and at equal `s` produce the identical derived `(m,r)` pair — yet they are different states ("identity 4 looking one ahead" vs. "identity 5 at its own anchor"). `(p,r)` alone cannot recover `n`. Brute-force verified, zero exceptions.
- **Corrected primitive**: the minimal distinguishable state is the triple `(n,k,s)` — identity, reference displacement, local polarity. `p=n+k`, `m=2p`, `r=m+s` are kept as derived coordinates only; `(n,p,s)` is an equally valid re-expression of the same triple, but `(p,s)`/`(p,r)` alone is not.
- **No privileged k**: tested `k` over `[-5,+5]`, not just the inherited `{-1,0,1}` — zero decoder failures, zero collisions anywhere in range. `k=0,±1` were simply the values the original packet and the two-family proposal happened to use, not structurally special values.
- **Operator algebra formalized and verified**: reference-shift `T_a:(n,k,s)->(n,k+a,s)` and polarity-flip `P:(n,k,s)->(n,k,-s)`. Verified `T_aT_b=T_(a+b)` (composition), `PT_a=T_aP` (commutation — reference-shift and polarity-flip are independent, not just independent table columns), and `P(P(x))=x` (involution). The group generated is `Z x Z/2` acting on `(k,s)` with `n` fixed. Domain-specific rules (alphabet boundary, tonal modulus, the two reversal operators) declared explicitly separate from this algebra, not folded into it.
- Extended `alphabet_tonal_generator_validator.py` with permanent regression tests for the degeneracy counterexample, the extended-k sweep, and the T_a/P composition/commutation/involution checks; receipts regenerated, all checks pass.
- Updated `Nodes/G-721_Mirrored_Alphabet_Rabbit_Hop_Coordinate_Algorithm.md` and `AI_Readable_Packs/G-721_Mirrored_Alphabet_Rabbit_Hop.json` to reflect the corrected primitive; "New Predictions" gains the proven algebraic-independence finding.
- `Wiki_Pages/G-721_Wiki_Page.html` not touched, per explicit instruction — it was already stale after the prior pass and remains so.
- Repository integrity validator passes with zero errors: 176 nodes, gate/lifecycle counts unchanged (no new node created — this corrects G-721 in place).

## G-721 Generalized — Minimal Generator Replaces Four-Rail Proposal

A proposed extension to G-721 (Mirrored Alphabet Rabbit-Hop) offered two "independent" arithmetic families plus a tonal correspondence. Brute-force testing found the second family was not independent - it was the first family's formula evaluated one letter ahead and re-anchored - and surfaced three real problems (a branch-decode collision, a reversal-rule contradiction between traversal classes, and a false 13-to-13 cardinality claim). Rather than patch those into the four-rail picture, went looking for the minimal generator that explains all of it and actively tried to falsify it.

- **Found the generator**: `p=n+k, r=2p+s, s in {-1,0,+1}` (anchor + ternary differential - the repo's own `-1(0)+1` foundational choice, applied to the doubled anchor). Verified to reproduce every packet either the original or the proposed extension ever used, as special cases, across all 26 letters.
- **Resolved the branch-decode collision**: `(n,m,r) -> (k,s)` decoder, verified collision-free across the full ternary range where the original single-rail formula `b=|r|-2|n|` could not distinguish `k=0` from `k=1` states.
- **Resolved the reversal contradiction**: half-mirror traversals reverse by ordinary sequence-reversal; round-trip traversals are palindromes under sequence-reversal (a no-op) and instead reverse by orientation-exchange (arm swap around the gate). Verified both operators exactly; these must not be cross-applied.
- **Resolved the tonal cardinality claim**: 12 unique tonal states + 1 closure-return visit gives a 13-position *traversal* count, not a 13-state *cardinality* match with the alphabet's 13-symbol half. Both numbers reported honestly rather than forced to align.
- **New predictions surfaced by the generator, not put in by hand**: `s=0` at `k!=0` (never used by either prior framing), symmetric look-behind (`k<0`, verified for all n), the alphabet's Z-boundary having no tonal counterpart (linear vs. cyclic domain), and a candidate (unconfirmed) structural match between `s in {-1,0,+1}` and G-744's Field/Mirror/Void ternary / B-223's Three Moves.
- Added an explicit boundary note against E-510 Music Clock before writing the tonal extension - E-510 already owns 12-tone harmonic/chord content and its own text says "must not be collapsed" with G-721; the new tonal section is coordinate/mirror grammar only, reciprocal note added in E-510.
- Preserved the original packet, the original `k=0` branch-decode formula (still correct where `k=0` is fixed by context), and G-721a-e's existing single-rail traces unmodified - extended, not replaced.
- Added `Nodes/G-721_Sequence_Validation/alphabet_tonal_generator_validator.py` plus its JSON/CSV receipts as reproducible evidence.
- `Wiki_Pages/G-721_Wiki_Page.html` is pandoc-generated MathML and was not hand-edited to match; it is now stale relative to the node source (same handling as the Book 5 Ch1 PDF earlier in this session).
- Repository integrity validator passes with zero errors.

## G-744/G-745/G-746 Added — Truth Computer Evaluation Architecture (reconciled, not filed verbatim)

- Added three companion G-series nodes for the Truth Computer's claim-evaluation architecture, preserving the user's three-way content separation (ternary evaluator / provenance trace / commit workbench) as instructed. IDs G-744-746 confirmed free (highest prior real G-series ID was G-743).
- Reconciled against existing canon before filing, per instruction not to trust the drafted IDs/dependencies blindly:
  - G-702 Evaluation already flags "whether Evaluation is binary or graded" as its own open question - G-744 is filed as answering that question for claims specifically, not as an independent new concept; G-702 promoted to primary upstream.
  - G-712 Evaluation Mathematics' open significance-threshold math is explicitly NOT resolved by G-744 - different question (signal significance vs. claim truth-value), cross-referenced both directions, not conflated.
  - G-711 Gate 7's existing "Void->Evaluate, Field->Modulate" split uses the same words as G-744's Field/Void ternary outcome for a different referent - explicit non-merge note added in both nodes.
  - G-704 Kabeuchi identified as the real structural precedent for G-745's lens chain and G-746's commit cycle (both single-cycle generalizations) - added as upstream, reciprocal cross-references added in G-704.
  - Dropped the drafted G-718 Connection Gates citation from G-744 - no operational overlap found on inspection (different domain: inter-system relational connection, not claim evaluation).
- Found a significant pre-existing, unreconciled system: `Nexus_Integration/Truth_Computer/` (a working, already-built "Updated 41" implementation with a fixed 22-stage OG-00-OG-21 spine and a 5-way source-status classifier) is prior art in the same "Truth Computer" project, but a materially different mechanism from G-744/745/746 (different classification axis, fixed spine vs. declared lenses). Flagged in both new nodes and in `00_MASTER_INDEX.md` as a known unreconciled item - not resolved in this pass, since it also overlaps substantially with the canonical A-series and B-221/C-301 and would need its own separate reconciliation pass.
- G-746 (the commit workbench) found to be the most genuinely novel of the three - no normalization/change-ledger/commit-versioning mechanism exists anywhere else in the repository, including in the existing Truth Computer code.
- Updated `00_MASTER_INDEX.md` Appendix G (38 nodes) and added three wiki pages.
- Repository integrity validator passes with zero errors: 176 nodes.

## D-435 Promoted — Twelvefold-Shell Rotation-Group Closure

- Promoted the verified twelve-neighbor rotational-closure result to a full node: `Nodes/D-435_Twelvefold_Shell_Rotation_Group_Closure.md`, gate BRONZE, lifecycle ACTIVE. Core claim stated first and treated as first-class content per instruction: D-409's shell has rotation-group order 24, element orders 1/2/3/4 only, no 6-fold or 12-fold closure.
- Scoped narrowly per instruction: explicit Non-Claims section (idealized geometry only, no single privileged operator, shared order-4 with C-301 is a noted coincidence only) and an explicit Non-Equivalence Warning toward C-301 rather than any implied link.
- Linked to D-409 as geometric source (reciprocal cross-reference added in both directions), to G-716/D-411 as the corrective boundary on numeral interpretation (already cross-referenced from the prior pass), and to C-301 only through the non-equivalence warning.
- Updated `00_MASTER_INDEX.md` Appendix D (17 nodes) and added `Wiki_Pages/D-435_Wiki_Page.html`.
- Left B-221's additive-vs-rotational LOOP tension unresolved, as instructed.
- Repository integrity validator passes with zero errors: 173 nodes, gate counts include BRONZE 3 (up from 2).

## D-417 Retired; Twelve-Neighbor Rotational Closure Verified Numerically

- Retired D-417's original "6:1 / 1:12 Rotational Closure Relation" backlog claim as already covered by D-409/D-411. Added the missing cross-references directly: G-716 now cites D-409/D-411 in its Dependencies and Dimensional Boundary section (with an explicit not-merged note); D-409 and D-411 now cite G-716 reciprocally. No node was built for the retired meaning.
- Investigated the surviving question separately, per instruction: does D-409's twelve-neighbor shell have its own discrete rotational symmetry, derived from the geometry itself rather than borrowed from C-301's `M^4=I` or assumed from the 6/12 counts. Added `Integrity_Tools/verify_d409_rotational_closure.py`, which numerically constructs D-409's exact 12-point shell and searches directly for its rotation symmetries.
- Result: the shell's full rotation group has order 24 (chiral octahedral, isomorphic to S4); individual element orders are only 1, 2, 3, or 4. No order-6 or order-12 rotation exists - the naive "12 neighbors implies 12-fold closure" reading is numerically false for this geometry. Documented the operator, state space, order, invariants, and failure cases in the backlog per instruction. Node assignment for this candidate is left open, not decided unilaterally.
- Flagged B-221's existing additive-vs-rotational LOOP tension (naming A-111 and C-301) explicitly for later reconciliation; not resolved in this pass.
- Repository integrity validator passes with zero errors.

## D-417 Evidence Dossier (no new node created)

- Exhausted existing canon against D-417's blank "6:1 / 1:12 Rotational Closure Relation" title before writing anything new. Found the counting relationship it names is already stated in D-409 and D-411 (both canonical). Found G-716 (BRONZE, the highest-proven gate in this area) already uses near-identical `N > 1(0)1 < M` notation across its full 24-12-6-3-1-24 conversion path, with its own explicit warning that these layer labels are not automatically spatial/neighbor counts - the same warning D-417 would need to honor. Found C-301/C-308 already define a real "closure" (4pi, M^4=I) at a different number (4, not 6/12) and different domain - a duplicate-name risk to flag, not a duplicate mechanism. Found B-221 already carries an unresolved additive-vs-rotational LOOP-candidate tension naming C-301 directly.
- Applied I-04 disposition to each overlap rather than asserting one. Offered one candidate reading (rotational symmetry closure of D-409's twelve-neighbor shell) explicitly flagged as inference, not confirmed content.
- No Nodes/ file created for D-417. No other MAPPED backlog rows touched. Recommendation (whether D-417 becomes a real node or is retired in favor of cross-references) left open, not decided unilaterally.
- Repository integrity validator passes with zero errors; only file changed is the backlog manifest.

## Newer-Concepts Reconciliation (DC/AC/RFC, wake continuation, 3>1(0)1<6, measurement-as-capture)

- Corrected `Nodes/C-324_V0_Hex_Cell_Multicellular_Host_Architecture.md`: its Motion section previously read "RC (Rotational Current)"; RFC (Rotating Field Current) is confirmed intentional, not a typo. Correction stated in the node itself. Added a candidate I-04 Scale-Specific Instance cross-reference to the backlog's Nested Point-Path-Field Recursion item, explicitly not merged.
- Split wake continuation through resonance into two distinct sub-claims with separate falsifiers: decay-rate suppression vs. coherent-reinjection growth. Connected provisionally to A-126/F-609 and D-420/D-421; noted A-115's `g_wake` has no decay term yet, so neither sub-case can be written down until that's added.
- Reconciled `3>1(0)1<6` against D-411 (already canonical) and the D-415-D-418 backlog items. Found a real convergence: the ladder's `6:1-(0)-1:12` line matches the backlog's independently-filed D-417 "6:1 / 1:12 Rotational Closure Relation" almost verbatim. Flagged an unresolved ambiguity: D-411 pairs 3:1 with 6:1 (doubling), the new notation pairs 3:1 with 1:6 (reciprocal) - not yet shown to be the same mapping. Also flagged D-410's existing 24:1 vs. the notation's 1:24 as not yet shown identical, and B-226's six-gate `(0)` (a step index) vs. this ladder's `(0)` (a ratio reference point) as not yet shown to be the same role.
- Separated measurement-as-capture into G-743's four components explicitly; flagged the required check against G-706 Validation ("confirmation through successful participation in a cycle") as unresolved rather than assuming novelty from vocabulary alone.
- No new node IDs assigned. Repository integrity validator passes with zero errors.

## Chapter-Pass Audit (I-04 disposition check against existing Books/ canon)

- Found A-115 (already canonical, GREEN) defines a general static `g_wake` term, applied at galactic scale in Book 5 Ch1's Extended Compression Effect — the backlog's A-126 and F-609–F-614 wake family are not a blank slate. Per I-04, the base wake concept is already covered; the genuine Unproven Delta is finite propagation (D-429/D-430 backlog items) and orbital/planetary-scale instantiation, not the wake mechanism itself. Annotated the affected backlog rows accordingly; no new node files created.
- Found `Books/Book4_Large/00_Scope_and_Status.html`'s "Orbital Dynamics" row was stale ("no supporting nodes exist at all") now that C-327–C-332 exist. Corrected in place (+ regenerated PDF): bridge nodes now exist but remain unvalidated (no D-427 simulation, no G-734/G-737 result) — the gap moved, it did not close, and no chapter was written.
- Added one cross-reference line to Book 5 Ch1's Future Work section pointing to the backlog's finite-propagation test items, without regenerating that chapter's PDF (no known reproduction of its original generation pipeline; PDF is now slightly stale relative to source, consistent with how this repo already treats PDFs as periodically-resynced presentation copies).
- Checked the remaining Books/ keyword hits (resonance/orbital in Book 1 Micro chapters) — confirmed false positives (electron orbitals, D-413's lattice "orbital-restoring" simulation, harmonic-shell resonance), no action needed.
- Repository integrity validator passes with zero errors after this pass.

## Updated 39 — Relational-Mechanics Node Backlog and First Developed Nodes

- Registered the ~100-node relational-mechanics coverage gap (differential/relational motion, moving reference states, point-path-field tracking, orbital wake/resonance dynamics, simulation methodology) as `RELATIONAL_MECHANICS_NODE_BACKLOG.md`, using a MAPPED/DEVELOPED/CANONICAL legend mapped onto existing I-06 gate/lifecycle fields rather than new vocabulary. Most entries remain MAPPED (title + one-line claim only, no invented reasoning).
- Renumbered the backlog's C-series block from a colliding C-323–C-337 to C-327–C-341 to avoid overwriting the just-committed intrinsic-cell hardware nodes; those hardware IDs (C-323–C-326) are treated as permanent.
- Added 18 fully developed I-06 nodes with wiki pages for the subset already backed by real reasoning: A-118, A-119, A-120, A-125; C-327 through C-332 (the full relational gravity-assist derivation chain, Gray-equivalent to standard patched-conic mechanics by design); D-420, D-421, D-422 (coherent vs. incoherent resonance accumulation); G-734, G-735, G-736, G-737, G-743 (simulation-methodology governance rules, no physics claim of their own).
- Added an A-103/A-118 entry to `DUPLICATE_NAME_DISAMBIGUATION.md`.
- Fixed 34 premature bare-ID citations to still-MAPPED backlog items across the 18 new node files, caught by the repository's own unresolved-ID integrity check.
- Repository integrity validator passes with zero errors: 172 node files, 172 unique IDs.

---

## Updated 38 — One-Wave Intrinsic Cell Hardware

- Added C-323 (Primitive Continuous Mirrored Chain, working-notes vocabulary), C-324 (V0 Hex Cell multicellular host architecture), C-325 (V0-A intrinsic cell engineering architecture, SPICE skeleton, and behavioral simulation), and C-326 (V0 first-organelle buildable wiring, schematic, and BOM). All Proposed Build under I-05; no physical hardware has been built or tested yet.
- Added matching Wiki_Pages entries for C-323 through C-326.
- Added Books/Engineer_The_Future/Vol1/Ch06 "The Intrinsic Cell", grounded in the four new nodes, with generated PDF.
- Updated 00_MASTER_INDEX.md Appendix C table and BOOK_SYSTEM_MASTER_PLAN.md's Engineer the Future chapter list.
- Flagged a stale Raspberry Pi Pico selection-logic note preserved from the imported source material in C-325; the no-processor-in-the-loop core rule remains binding.
- Repository integrity validator passes with zero errors: 154 node files, 154 unique IDs.

---

## Updated 32 — Repository Integrity Repair

- Established I-06 canonical YAML metadata for every active node and root axiom.
- Split gate, lifecycle, classification, and claim-detail fields.
- Conservatively normalized mixed statuses to one node gate without deleting subclaim detail.
- Disambiguated B-201 Equilibrium Balance and G-709 Regulated-Response Balance.
- Resolved the I-01 and duplex reconciliation governance forks; historical variants moved under History.
- Added a title-verified legacy ID alias registry and removed nonexistent F-609/F-610 forward dependencies.
- Repaired D-02b to E-508 and removed the anonymous E-501 embedded persistence duplicate.
- Rebuilt Internal_Proofs with a canonical index and moved raw conversational sources to History.
- Closed the Book 1 numbering gaps by renaming the existing chapters into one continuous Ch1-Ch17 sequence; no chapter prose was invented, deleted, or merged.
- Moved the unnumbered Neutrino ALT draft out of active Nodes.
- Regenerated Appendix A-G AI packs and normalized wiki gate/lifecycle banners.

# Updated 31 - Visible Curvature Surface Synchronization (July 23, 2026)

- Rebuilt the D-413 renderer so the imposed well appears as an actual depression in the triangular lattice from the first frame.
- Added shaded triangular faces, curved sampled depth contours, a Ground-to-bottom depth marker, top-down and curved-surface projections, and view-only vertical exaggeration.
- Locked the displacement display height and restoring-gradient calculation to the same interpolated lattice surface.
- Synchronized D-413 source, AI pack, Appendix D, wiki, standalone browser artifact, and simulation package.
- Kept all Updated 30 Yellow limitations: the well is imposed and the bounded shell is not a quark, proton, particle, or derived gravity mechanism.

---

# Updated 30 - Ground Lattice Orbital-Restoring Simulation (July 23, 2026)

- Added D-413, the first runnable triangular Ground-lattice background for later quark and proton simulations.
- Added Ground-fixed, displacement-fixed scrolling, and well-fixed camera modes over one physical state.
- Added an imposed curvature depression, bounded displacement shell, off-axis restoring orbit, and torque-generated axial spin.
- Added symmetric-shell, no-well, frozen-lattice, and zero-input controls.
- Added browser CSV export plus Python CSV/JSON/graph receipts.
- Synchronized D-408, D-412, Appendix D, Book 1 Chapters 1-2, wiki pages, and affected PDFs.
- Retained Yellow limitations: no derived gravity, quark, proton, charge, Mirror Gate, or Mass Effect.

---

# Updated 29 - Route Grammar, Android Motor Memory, Lattice Simulation Standard, and Fake Mustache Desk (July 23, 2026)

- Added D-411 to separate mirrored axis-pair counts, directed-route counts, and centered state counts; locked ratio-domain declarations.
- Added D-412 as the mandatory real-simulation and state-driven visualization standard for lattice, quark-phase, proton-knot, shell, Mirror-Gate, and Mass-Effect work.
- Added G-721b through G-721e for Sturmian, episturmian, Arnoux-Rauzy, and plastic/Padovan route or rail candidates.
- Added G-722 for hybrid Hopfield/Boltzmann subconscious procedural movement with local `-1(0)+1` choice and binary top-down safety only.
- Added G-723 for Pisot/Salem/Mahler spectral audits and G-723a as a HELD advanced regulator-computation shelf.
- Updated Android Brain Chapters 1-4 and Book 1 Chapters 1-2 with the correct movement and physical-simulation dependency order.
- Added the Fake Mustache Math Desk to The One-Wave Times with three clearly labeled satirical issues.
- Added finite sequence-family and spectral regression suites with CSV, JSON, and graph receipts; these validate reference mathematics only, not android movement or physical lattice claims.
- Regenerated the affected wiki pages with self-contained MathML and synchronized the changed presentation PDFs, including single-page newspaper layouts.

---

# Updated 28 — Alphabet Rabbit-Hop / Fibonacci Word Validation (July 23, 2026)

- Added G-721 as the canonical mirrored alphabet coordinate and rabbit-hop route grammar.
- Locked signed packets `±(n,2n,2n+1)`, separate direction/location and recursive/state axes, and exact forward/reverse mirror rules.
- Added G-721a to validate the ordered `2n` versus `2n+1` branch trace with the Fibonacci word sequence.
- Restricted golden-ratio metrics to Fibonacci-word generation lengths and symbol counts; removed the temptation to spray `1.618` across unrelated lattice and physical quantities.
- Added a reproducible A-to-Z reference validator with positive, negative-mirror, reverse, balance, factor-complexity, CSV, JSON, and graph receipts.
- Kept live `-1(0)+1` choice foundational; Fibonacci/binary validation remains top-down and cannot drive movement.

---

# Updated 27 — Dimensional Coordination Architecture (July 23, 2026)

- Added A-117, the mandatory dimensional integrity and projection declaration.
- Added D-408, the native 2D sixfold triangular/hexagonal lattice and seven-cell cluster.
- Added D-409, the native 3D twelvefold close-packed coordination candidate.
- Added D-410, the 4D twenty-fourfold Field/Void recurrence shell.
- Locked 6:1, 12:1, and 24:1 as distinct relationships rather than interchangeable geometry labels.
- Clarified Flower-of-Life, Seed-of-Life, Fruit-of-Life, and Metatron-style diagrams as declared 2D overlap/index/connection views, not the full 3D object.
- Added dimensional cross-references to projection, spherical default, hex-lattice, Kuramoto, conversion-grammar, and reduced-tension-network nodes.

---

# One-Wave Repository Change Log

## Updated 26 - Permanent Mass-Assumption Erasure and Synchronization

**Date:** July 23, 2026

- Identified the old transport-to-mass claim as a misunderstanding of C-309, not a One-Wave derivation. It is permanently removed from canonical sources.
- Rebuilt E-509 as `Local-Transport Partition`; deleted the invalid conversion from transport bookkeeping into Mass Effect.
- Synchronized C-309, C-318, A-112, the Master Index, books, wiki pages, AI-readable packs, and affected PDFs.
- Removed pre-audit mass snapshots from the distributed master so AI readers cannot silently promote obsolete text.
- Locked the Mass Effect to all four interactions together and retained approximately 125 GeV as the distinct Mirror-Gate boundary-response measurement.

- Added `UPDATED_24_MASS_MIRROR_GATE_RESOLUTION.md` as the concise canonical handoff for the repaired derivation.

- Updated 24 mass/Mirror-Gate correction: removed the scalar-potential and harmonic-oscillator imports from canonical One-Wave mass math.
- Rebuilt C-318 around the four-interaction carried-pattern response: internal knot, electrical shell, Mirror Gate, Boundary-Tension Weave, and cross-couplings.
- Rebuilt C-322 around signed finite pressure-work to the first actual mirrored-basin crossing; retained the approximately 125 GeV measurement as the empirical Mirror-Gate anchor.
- Separated local Mass Effect from the 125 GeV gate barrier as two derivatives of the same four-interaction architecture.
- Proved the current quantitative blocker: the normalized update has a global energy-scale freedom. Added the scale-free gate-to-mass ratio and separated prediction versus calibration routes.
- Removed nonexistent C-319/C-320 as active dependencies while retaining the formation-versus-stability distinction directly in C-318 and Chapter 15.
- Narrowed C-321 to a conditional slender-neck reduction of C-317; preserved the N=3 Fermat junction and withdrew unsupported direct extension to nuclear/carbon binding.


This is a concise change record, not a store of full pre-edit copies.

## 2026-07-22

- Separated Active Hypothesis, Proposed Build, disputed formulation, and quarantine status through I-05.
- Dissolved the accidental H-series; active hypotheses remain in their proper A–G locations and use Green/Yellow/Bronze proof status.
- Resolved the C-316 electron sign/direction contradiction and the B-225 five-stage cycle naming conflict.
- Reanalyzed D-407 neutron-shell calibration and exposed the missing shell-geometry-to-energy map.
- Replaced E-527's failed product-only oscillator with a tested hysteretic recharge/depletion model; reduced model reached Bronze.
- Resolved G-720's internal `Move` collision by using Receive → Hold → Commit.
- Repointed the missing physics friction-limit alias to C-309 and removed the obsolete physics use of I-05 from Book 1 Chapter 10.
- Corrected Chapter 11's time math: elapsed lattice time is `t=NΔt`; damping time is `τ_d=Δt/γ=1/μ`.
- Updated C-313 with the finite-damping continuum scaling and weak-damping dispersion test.
- Created A-115 Unified Compression Field as the load-bearing A-series home for the One-Wave identity `gravity = dark-matter behavior = Higgs-like compression/resistance field`; dissolved the dead physics I-09 address.
- [SUPERSEDED BY UPDATED 24] Created the first C-322 harmonic-resonance target. Updated 24 retains only the measured 125 GeV / joule anchor and replaces the oscillator mechanism with pressure-work.
- Rewrote Book 1 Ch15 so the 125 GeV value is a derivation target, not a borrowed proof; added explicit Fake-Mustache, failure, and Bronze requirements.
- [SUPERSEDED IN UPDATED 22] Linked Book 1 Ch12 and Book 5 Ch1 to A-115; the temporary expansion-based `w_eff < -1/3` test was later identified as framework contamination and removed.



## Presentation Reconciliation - Updated 21

- Rebased the Updated_20 presentation work onto Updated_13 canonical physics and governance.
- Regenerated Micro, Small, and Macro textbook PDFs from current Markdown sources.
- Preserved the Android manga-style build manual and Engineer the Future steampunk manuals.
- Added Appendix A AI-readable and wiki views.
- Restored C-318 as a canonical source node from its surviving wiki record.
- Added `PRESENTATION_ARCHITECTURE.md`, a corrected book-system plan, and two One-Wave Times issues.
- Kept Musical Universe format explicitly unresolved.
- Added no pre-edit snapshot trail.


## Static-Cosmos and Terminology Update - Updated 22

- Removed expansion-cosmology contamination from A-115, Book 5 Ch4, wiki/AI mirrors, and public presentation text.
- Renamed the One-Wave outward-return process **White Energy** and defined it as quasar/white-hole-scale ejection and reinjection, never expansion of space.
- Added E-528 Static Redshift Transport, E-529 Low-Coupling Return Mode, and E-530 White Energy Recirculation Loop.
- Resolved dead physics aliases I-08 -> E-528 and I-10 -> C-311.
- Added A-116 Three-Dimensional Spherical Default with the minimum-surface derivation.
- Recast C-317 as Boundary-Tension Weave: gluon -> Tension-Link excitation, quark -> Vortex Phase, confinement -> Knot Lock, proton -> Three-Vortex Knot.
- Added `ONE_WAVE_TERMINOLOGY_LEGEND.md`; Standard names remain in Gray reference sections and One-Wave names control the interpretation layer.
- Added no pre-edit snapshot trail.

- Dimensional correction: C-317 now derives neck energy from lateral surface area, `E_neck = 2*pi*a*sigma_T*L = tau_T*L`, rather than the dimensionally invalid `sigma_T*A_perp*L`.
- Conservation correction: A-115 and E-530 now include explicit White Energy density/flux in the closed energy sum.
- Added I-01 Rules 16-17 enforcing the static-cosmos boundary, canonical terminology legend, and 3D geometry default.
