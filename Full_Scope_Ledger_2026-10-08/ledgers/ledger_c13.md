# Code ledger — slice c13 (14 files)

All 14 files read in full. Repo root: /home/user/One-Wave-Science. Line numbers are file-local.

## generate_publication_figures.py
- Purpose / node IDs cited: Matplotlib/seaborn figure generator for a "Physical Review Letters manuscript Section 5" on "harmonic locking" (lines 1-7, 460). Cites no node IDs. Reads `atomic_spectroscopy_validation_results.json`, `muon_g2_validation_results.json`, `superconductor_validation_results.json`, `neural_oscillations_validation_results.json`, `mathematical_harmonic_proof_results.json` from CWD. Side effect: creates `figures/` in CWD at import time (32-33).
- Point rotation: not present.
- Path rotation: not present.
- Field: not present (only a plotted standing-wave sin(n pi x) picture, 349-352, and a "Helmholtz" label, 124).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits:
  - 59: `accuracies = [0.30, 0.0073, 99.9, 20, 100]` hard-coded rather than read from the JSONs; 100 is drawn as "Exact" (71-72).
  - 222-223: "boundary sharpness" is built from T_c itself (`T_c * 1.5` for ceramics, else `T_c`), then T_c is plotted and polyfit against it (235-238). The x axis is the output in disguise, so the trend is circular.
  - 249: BCS accuracies `[99.95, 99.95, 99.92]` hard-coded, all labelled "Exact" (262-264).
  - 283-284: EEG "measured" `[2.5, 6, 10, 20, 50]` against "predicted" `[2, 4, 8, 16, 32]`, both hard-coded.
  - 303-304: `observed_ratios = predicted_ratios = [2.0, 4.0, 1.5]`. The "prediction" is the observed value copied over, and it is shown as an Observed vs Predicted bar comparison.
  - 338: `harmonic_prediction = modes * 1.0`. Figure 6 plots the integers. It does not use data loaded from the JSON (`data` is loaded at 332 and never used).
  - 379-383: summary table with hard-coded "7/7, 2/2, 6/6, 5/5, 4/4" pass counts.
- Pass criterion: none computed. Pass counts and "Exact" labels are literal strings.
- Violations: no Point/Path/Field or magnetism rule is touched. Hard-coded observed values are presented as predictions (59, 222-238, 249, 283-284, 303-304, 379-383). This breaks the slice's "observed values used as inputs and then reported as predictions" rule.

## megacity/room.py
- Purpose / node IDs cited: a 5x5 grid world with an avatar, a switch and a goal, held as authoritative world state (1). No node IDs.
- Point rotation: not present. Grid moves only (18-23, 99-102).
- Path rotation: not present.
- Field: not present.
- Magnetism: not present. The "switch" (106-107: toggle switch_on) is a game switch, not a magnetic open/closed switch.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: none. `goal_open` = switch_on and avatar on goal (84).
- Violations: none.

## point-spin/compare.py
- Purpose / node IDs cited: prints a vocabulary table that maps quaternion terms to One-Wave terms (2-10). Cites C-308 (row "4pi trip -> C-308 closure", 9) and HEX-SPLIT (8).
- Point rotation: label only. "unit q -> site facing + spin sheet" (3), "q and -q -> two sheets, one facing" (4), "real w -> hold / ground rest" (7). No omega, no L, no I.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: label only. "multiply -> parent writes on child" (6). This is attitude composition, not rate transport. Nothing says omega_c + R_c^T omega_p.
- Hard-coded targets / refits: none.
- Pass criterion: none (it prints only).
- Violations: none. It is incomplete: point rotation appears only as attitude, and L = I omega is missing.

## point-spin/quat.py
- Purpose / node IDs cited: a minimal unit quaternion `Q` plus a "4pi trip" receipt (37-44). No node IDs (the companion compare.py ties it to C-308).
- Point rotation: attitude only, held as a unit quaternion (7-12). It is normalised on every construction and product (15-19, 22-29). It is STARTED by a fixed prescribed step, `axis_angle(z, pi/3)` (40), from the identity (39). The only thing that CHANGES it is the fixed left-multiply `q = step * q` (44), 13 times, which covers 0 to 720 degrees and shows the w sign flip at 360 degrees (43). There is no omega, no inertia tensor, no L = I omega, and no torque. Gravity and compression gradient: not present. Open/closed magnetic switch: not present. Parent organization target rate: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: `__mul__` (22-29) is a Hamilton product, so the composition R_parent R_child is available. There is no rate transport.
- Hard-coded targets / refits: none (60-degree step, 13 steps).
- Pass criterion: none. It prints a table and asserts nothing.
- Violations: none against the rules. It is a kinematic demo only: attitude is driven by a prescribed increment, not by L = I omega. It must not be cited as a G-749 point-rotation solver.

## scripts/brain_buddy_council.py
- Purpose / node IDs cited: orchestrates Gemini, DeepSeek and local-Ollama "council" calls, with reference snapshots and a six-step FIELD/VOID public-artifact loop (2-14, 477-479, 537-773). Requires I-06 metadata (38). No physics node IDs.
- Point rotation: not present.
- Path rotation: not present.
- Field: "FIELD"/"VOID" are software phase labels for proposer and checker roles (477-478: "never model thought traces or physical gates"). They have no physical field.
- Magnetism: not present.
- Parent/child: parent/child loops are nested sub-questions (716-728). They have nothing to do with physics rates.
- Hard-coded targets / refits: none. Endpoints are hard-coded: 127.0.0.1:11434 (275), 127.0.0.1:3000 (294), 192.168.55.100:3001 (296). Default local model is qwen3:0.6b (262).
- Pass criterion: AGREED_RESOLUTION or AGREED_NEXT_ACTION from VOID ALLOW with no objections (732-743), or RETURNED when transports answer non-empty (897). It states outright that this is "not scientific validation" (773, 900).
- Violations: none. Writes into the repo (`External_Work/brain_buddy/outbox`) only with --save (432-455).

## scripts/g721_word_grammar_proofs.py
- Purpose / node IDs cited: G-721a/G-721b Fibonacci/Sturmian word-grammar checks (2-7). States "Does not prove lattice physics" (6).
- Point rotation, path rotation, field, magnetism, parent/child: not present.
- Hard-coded targets / refits: `CANONICAL_PREFIX_26` (14) is checked against the generator (92). This is a self-consistency check, not a physical target.
- Pass criterion: 9 assert-based tests (180-201). Phi is a consequence check within 1% (123-132).
- Violations: none.

## scripts/node_graph_integrity.py
- Purpose / node IDs cited: audits I-06 metadata, the master-index listing and dependency resolution. It also locks reciprocal edges (57-73): C-311->C-319, D-408->C-319, D-409->C-319, C-319->C-320, A-115->C-320, C-306->C-320, C-307->C-320, D-409->C-320, C-319->D-413, C-320->D-413, A-115->D-416, C-307->D-416, D-409->D-416, C-320->D-416, D-413->D-416. The D-413 README must cite A-115, C-311, C-319, C-320, D-413 and D-416 (75, 229-235). AI start must cite C-319, C-320 and D-416 (239-241).
- Point rotation: not present as code. No locked edge involves G-749, G-750 or G-769, so the graph lock enforces the magnetism-to-gravity chain but not the point-rotation chain.
- Path rotation: not present.
- Field: not present.
- Magnetism: graph topology only (C-311 -> C-319 -> C-320 <- A-115).
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: zero metadata, index or locked-edge errors (245-255).
- Violations: no rule violation. Gap: the canonical rules list C-306/C-307/C-311/C-319/C-320/G-749/G-750/G-769 as one set, but LOCKED_EDGES (57-73) omits G-749, G-750 and G-769, so the point-rotation chain is not graph-locked.

## scripts/normalize_legacy_node_metadata.py
- Purpose / node IDs cited: rewrites legacy `Nodes/*.md` front matter to I-06 (NODE or NODE_ARTIFACT) and defaults the gate to BROWN (2-14). It writes into the repo unless run with --check (213-214). No physics.
- Point rotation, path rotation, field, magnetism, parent/child, hard-coded targets: not present.
- Pass criterion: with --check, exit 1 if any file would change (216-220).
- Violations: none. Its keyword-based lifecycle inference (86-96) could mark a node HELD just because the word "parked" appears in the first 500 characters. That is a metadata risk, not a physics one.

## scripts/ppf_scale_hop_receipts.py
- Purpose / node IDs cited: "Point / Path / Field nested scale hops with reconstructable receipts" (2). Uses the Rabbit-Hopping N-grammar "only as an addressing translator" and "does not claim CELL_V1 hardware, gravity, or consciousness proof" (4-5).
- Point rotation: label only. Layer "point" = (after, m=0, wrapper=+1) (59). No spin, omega or L.
- Path rotation: label only. Layer "path" = (before, m=1, wrapper=-1) (60). No ride rate.
- Field: label only. Layer "field" = (after, m=2, +1) (61). "closure" uses identical parameters (62), so field and closure receipts differ only by their label.
- Magnetism: not present.
- Parent/child: integer parent pointers only. The next scale's center has parent_N = N-1 (56-57, 63-78). No rate transport.
- Hard-coded targets / refits: none.
- Pass criterion: 6 integer round-trip tests (95-145). `test_path_and_point_keep_distinct_receipts` (134-138) checks only point vs path. Field vs closure is not distinguished.
- Violations: none. Point, Path and Field are kept as three separate integer receipts, which matches the canonical separation in addressing only and carries no physical rates. Minor: field == closure parameter collision (61-62).

## scripts/rabbit_hop_proofs.py
- Purpose / node IDs cited: Rabbit Hopping N-based translator arithmetic, with 10 exact-integer tests (2-10). Cites ARCHITECTURE_RABBIT_HOPPING_SCALE_TRANSLATOR.md. Claims GREEN for the arithmetic only.
- Point rotation, path rotation, field, magnetism, parent/child: not present.
- Hard-coded targets / refits: `invert_N = 27 - N` (35-36), which is alphabet inversion. Not a physical target.
- Pass criterion: 10 assert-based tests (91-212).
- Violations: none.

## scripts/science_archive_search.py
- Purpose / node IDs cited: a bounded HTTPS relay to public archives (CERN Open Data, HEPData/DataCite, PDS, SDSS, GWOSC, DANDI, OpenNeuro, PhysioNet, Gaia, ESO, ALMA, DESI) that writes response receipts (17-114). Labels results "provider_metadata_not_measurements" (59). No node IDs.
- Point rotation, path rotation, field, magnetism, parent/child: not present.
- Hard-coded targets / refits: default queries "CMS"/"Higgs" (19-21). These are search terms, not fitted values.
- Pass criterion: `status == "acquired"` (111, 119).
- Violations: none. It writes only to the user-supplied `--output` directory.

## scripts/six_gate_canon_lock.py
- Purpose / node IDs cited: a read-only text checker for the CELL_V1 "three physical bidirectional mirrors / six directed interfaces / logical M-A positions" canon (2-12, 23-68). Cites G-711, B-206b, B-206c, B-221a, G-729, G-739, G-740 and C-301 (53-80).
- Point rotation, path rotation, field, magnetism, parent/child, hard-coded targets: not present.
- Pass criterion: required phrases present and forbidden phrases absent (83-129, 147).
- Violations: none.

## scripts/sync_node_graph_indexes.py
- Purpose / node IDs cited: rewrites `00_MASTER_INDEX.md` rows and inserts the "Magnetism / Gravity canonical bridge" into `AI_CANONICAL_START_HERE.md` (4-11, 133-168). It writes into the repo unless run with --check (171-177). Cites C-311, D-408, D-409, C-319, A-115, C-320, D-413, D-416, C-318, D-415, B-206b and G-711 (25-40).
- Point rotation: not present. The bridge text (40) mentions "tidal/spin locking" and "torque" but never names G-749, G-750 or G-769, and has no open/closed switch (dL/dt = 0 vs -gamma L).
- Path rotation: C-319 row (25) says the "rotational magnetic state reorganizes directional lattice path accessibility".
- Field: A-115 compression-gradient/restoring field (40, item 5).
- Magnetism: text only (40). `g_OW = -alpha_g K_L grad(chi)` with mandatory `K_L -> I` recovery. "Do not collapse this to magnetism = gravity". No lunar dipole. Mercury is 3:2, not 1:1. The text does not say whether K_L is a tensor or a scalar, how R is built, or what kappa_R is.
- Parent/child: not present.
- Hard-coded targets / refits: none numeric. D-416 row (27): "locking required to emerge rather than be initialized", which agrees with canon. Hard-coded appendix counts "22 active files" and "16 nodes" (150-157).
- Pass criterion: with --check, fail if sync would change files (191-195).
- Violations: no hard violation, since the bridge matches the "magnetism does not become gravity", "K_L -> I recovery", "no lunar dipole" and "Mercury 3:2" rules. Soft conflicts:
  - 40: the bridge's "locked interpretation" routes spin locking through magnetic -> lattice -> restoring response -> "can alter ... torque". It skips the G-749 point-rotation node and the open/closed (dL/dt = 0 / -gamma L) switch, and it does not state that turning the magnetic channel off must still leave the face.
  - 27: D-416 is framed as a C-319/C-320 magnetic falsification set for Moon/Mercury locking. Canon says the bound-lattice lock (resistance = mass / organization) must hold with the magnetic channel off.
  - Torque alteration via magnetism (40) is not tied back to C-306/C-307 L bookkeeping.

## scripts/test_six_gate_canon_lock.py
- Purpose / node IDs cited: 4 unittest cases for six_gate_canon_lock (9-45). They use temp fixtures and do not touch the repo.
- Point rotation, path rotation, field, magnetism, parent/child, hard-coded targets: not present.
- Pass criterion: `check()` returns [] for the current contract and flags the superseded, missing-separation and Gate 7 cases.
- Violations: none.

## Slice summary
- **Canonical point rotation:** no file in this slice implements it. No file carries L = I omega, an inertia tensor, a magnetic open/closed switch, or rate transport omega_c + R_c^T omega_p.
- **Point-spin files:** `point-spin/quat.py` is the only rotation code. It holds attitude as a unit quaternion, starts it with a prescribed fixed 60-degree step about z, and changes it only by repeated left-multiplication (40-44). It is a kinematic 4pi demo, not a solver. `point-spin/compare.py` is a vocabulary table for the same idea (C-308 closure, "parent writes on child" = quaternion multiply, which composes attitude and does not transport rates).
- **Point / Path / Field as labels only:** `scripts/ppf_scale_hop_receipts.py` keeps Point, Path and Field as three distinct integer address receipts with no physical rates. Field and closure share parameters (61-62).
- **Magnetism text:** `scripts/sync_node_graph_indexes.py` (AI_BRIDGE, line 40) carries the magnetism/gravity bridge text, which agrees with canon on g = -alpha K_L grad chi, K_L -> I, magnetism != gravity, no lunar dipole and Mercury 3:2. It omits G-749/G-769, the open/closed switch, and "magnetic channel off must still leave the face". The D-416 row (27) frames locking as a magnetic-coupling test.
- **Graph lock:** `scripts/node_graph_integrity.py` locks the C-311/C-319/C-320/A-115/C-306/C-307/D-413/D-416 graph but has no locked edge for G-749, G-750 or G-769.
- **Hard-coded targets reported as predictions:** `generate_publication_figures.py` at 59, 222-238 (circular boundary-sharpness fit), 249, 283-284, 303-304 (observed == predicted copied) and 379-383. These are not rotation-related.
- **No physics content:** `megacity/room.py`, `brain_buddy_council.py`, `g721_word_grammar_proofs.py`, `normalize_legacy_node_metadata.py`, `rabbit_hop_proofs.py`, `science_archive_search.py`, `six_gate_canon_lock.py`, `test_six_gate_canon_lock.py`.
- **Live solvers vs tools:** there are no live physics solvers in this slice. The live tooling is the integrity, sync and canon-lock checkers, the council orchestrator and the archive relay. `generate_publication_figures.py` is a legacy figure script: it depends on validation-result JSONs in the CWD and creates `figures/` on import. `point-spin/*` and `megacity/room.py` are small demos.
- **Scripts that write into the repo when run:** `normalize_legacy_node_metadata.py` and `sync_node_graph_indexes.py` without --check, and `brain_buddy_council.py` with --save. None was run.
