# Code ledger, slice c09

All 10 files read in full. None of them contains physics code. No file computes spin, omega, L, attitude, orbit, curl, chi, B, R, K_L, kappa_R or gravity. The physics fields below are therefore "not present" for every file. Non-physics observations are listed under Violations only when they break a repo rule (CLAUDE.md or the ledger rules). They are marked "non-physics".

## /home/user/One-Wave-Science/Integrity_Tools/close_book1_chapter_gaps.py
- Purpose / node IDs cited: a one-shot Book 1 renumbering script ("Updated 32"). REN map L6 is old to new chapter numbers (4->3 ... 19->17). FILES L7-23 maps chapter stems. It rewrites chapter references across every text file in the repo (L59-68). It patches 00_MASTER_INDEX.md (L71-83), writes 00_CHAPTER_STATUS_MAP.md (L86-96), regenerates AI_Readable_Packs/Appendix_A..G from Nodes/ and Root_Axioms/ (L99-106), and writes UPDATED_32_book1_renumber_receipt.json (L108-110). FULL_SCOPE (L25-34) names B-220, A-105, C-311 (Electric/Magnetic Duality), A-112, C-315, C-316, D-406 and E-525. These are only file paths to renumber. No physics content is read.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present. C-311 appears only as a filename in FULL_SCOPE (L27, L31).
- Parent/child: not present.
- Hard-coded targets / refits: none (physics). The receipt hard-codes `'pass':True` (L108). It is written unconditionally after the continuity check at L91.
- Pass criterion: Book 1 chapter files form the continuous range 1..17 (L90-91). After that check, pass is always True.
- Violations:
  - (non-physics) L6 and L59-68: the script is not idempotent. Running it again applies REN to already-renumbered text (for example "Chapter 5" -> "Chapter 4" again). It writes into every .md/.py/.json/... file in the repo. It must not be re-run.
  - (non-physics) L7-23: every FILES key equals its value, so the rename at L49-56 and the filename pass at L67 do nothing. The real stem migration must have happened elsewhere.
  - Rotation/magnetism canonical rules: none.

## /home/user/One-Wave-Science/Integrity_Tools/validate_repository_integrity.py
- Purpose / node IDs cited: validates node front matter (L20-31). Allowed gates are listed at L5 and lifecycles at L6. It checks node IDs in Nodes, Root_Axioms, Books, Android_Body, Musical_Universe and Governance_I_Series against the legacy alias registry (L33-47). It also checks the I-01 / reconciliation forks (L50-51), the Book 1 sequence 1..17 and the status map (L53-63), and the proof index (L65-67). It writes UPDATED_32_integrity_receipt.json (L73-74). No specific node IDs are cited.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none.
- Pass criterion: no metadata, ID, fork, chapter or proof-index errors (L69).
- Violations: none for physics. (Non-physics: the regex at L8 accepts IDs `[A-L]`, but the parser in validate_updated_32_artifacts.py at L97 accepts only `[A-G]`. This is a minor inconsistency.)

## /home/user/One-Wave-Science/Integrity_Tools/validate_updated_32_artifacts.py
- Purpose / node IDs cited: rebuilds Appendix A-G from the node files and requires a byte-for-byte match (L105-116). It also checks:
  - wiki name, gate and lifecycle against node metadata (L119-126)
  - JSON pack gate, lifecycle and claim_gate_detail (L129-139)
  - Book 1 chapter headers and sequence (L142-150)
  - stale old chapter stems anywhere in the repo (L152-160)
  - local markdown links (L163-172)
  - PDF validity and staleness, using pdfinfo and pdftotext (L175-192)

  It writes two receipts (L209-220).
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none (physics). L217 hard-codes `'book1_pdfs_regenerated':17` and L218 hard-codes `rendered_visual_samples`. These are fixed claims, not values the script computes.
- Pass criterion: the error list is empty (L195). The PDF receipt passes when there are no PDF errors, no stale pairs and 17 Book 1 PDFs (L211).
- Violations: none for physics. (Non-physics: the receipt fields at L217-218 claim regeneration and visual rendering that this script never performs.)

## /home/user/One-Wave-Science/Learner_App/curriculum/rule_01_balanced_change.py
- Purpose / node IDs cited: the fixed Rule 1 "Balanced Change" lesson (RULE.BALANCED_CHANGE, L14-19). It has 3 build-up and 3 lock-down problems (L47-126), a lesson sequence guard (L129-134) and a string grader (L137-145). No node IDs are cited.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: not applicable. These are fixed arithmetic lesson items.
- Pass criterion: check_answer compares the normalized answer with `accept`. For R1-LD-3, it accepts any answer that starts with "no" (L143).
- Violations:
  - (non-physics, CLAUDE.md answer-exposure rule) The public frozen dataclass carries `teacher_close`, which contains the solved answers "x = 5" (L95) and "x = 10" (L107). The lock-down items carry `show_worked_path=False`, but nothing strips `teacher_close` from the object. Whether a fixed curriculum file counts as a "public result/API object" is for the owner to decide. This is flagged, not asserted.
  - (non-physics) L143: `startswith("no")` also accepts answers such as "not sure" or "nope, yes".
  - Rotation/magnetism canonical rules: none.

## /home/user/One-Wave-Science/Learner_App/router/recall_integration.py
- Purpose / node IDs cited: recall policy on the router side. It has:
  - RULE_INVERSES for math/basic_equations (L33-38)
  - known_rule_ids (L41-51)
  - schedule_learned_rule, which raises on unknown rules (L54-62)
  - packet_is_feasible, which uses only adapter.validate_packet (L65-92)
  - inject_due_recall, which adds a due rule to the targets without replacing them (L95-132)
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present. "Inverse" here means algebra rule inverses, not rotation.
- Hard-coded targets / refits: none.
- Pass criterion: not applicable (library).
- Violations: none. The file stays within the Router authority in CLAUDE.md.

## /home/user/One-Wave-Science/Learner_App/tests/test_rule_01_lesson.py
- Purpose / node IDs cited: unittest contract for Rule 1. It checks the 3+3 shape (L17-20), the ID and statement (L22-25), that there is no move-across wording (L27-31), that there are no coefficients (L33-35), and that lock-down hides the worked path (L37-40). It also has grading tests (L43-60).
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: not applicable.
- Pass criterion: the unittest assertions.
- Violations: none. (Note: no test checks that `teacher_close` stays out of learner-facing output.)

## /home/user/One-Wave-Science/Nexus_Integration/Truth_Computer/Reference_App/app.py
- Purpose / node IDs cited: a local HTTP answer app (serve L624-685). It answers questions over pinned One-Wave git roots with a 6-step BEGIN/BUILD/HOLD/BUILD/BREAK/LOOP Field/Void loop (STEPS L19, step L455-487, run L550-622).
  - Providers: the Claude subscription CLI with tools, MCP and hooks disabled (L349-371), or the local DeepSeek web relay (L305-347).
  - Pipeline: keyword source search (L214-257) and a read-only reference pipeline (L272-303).
  - Safeguards: provider idempotency and checkpointing (L489-520), audit-bound publication with solver='NOT_RUN' (L522-548), and a public view that strips the private candidate and audit (L115-141).

  It references og-system.json as the "node_spine" (L293). No physics node IDs are cited.
- Point rotation: not present. The "Field"/"Void" names here are workflow phases, not physical fields.
- Path rotation: not present.
- Field: not present (phase labels only).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. The prompt states "No solver ran; do not invent measurements" (L572). Published answers are marked solver='NOT_RUN' and evidence_class='candidate' (L540).
- Pass criterion: a structured candidate with balanced citations [S#] that are a subset of the sources (L582-596), a same-model audit decision of ALLOW (L598-602), and an unchanged reference hash at every step (fresh L439-449).
- Violations:
  - (non-physics, CLAUDE.md "Preserve the existing Nexus database") health() reports `nexus='no existing database assumed'` (L262). The app keeps its own SQLite state (L46-56) and does not attach to the existing Nexus database. This is not a write conflict, but it does not integrate with Nexus either.
  - (non-physics) The audit is the same provider model (L598). The code labels this honestly as "not independent corroboration".
  - Rotation/magnetism canonical rules: none.

## /home/user/One-Wave-Science/Nexus_Integration/Truth_Computer/Reference_App/knowledge_loop.py
- Purpose / node IDs cited: a deterministic "source qualification" knowledge store with no model calls (docstring L1-6). It runs a FIELD/VOID transition machine (TRANSITIONS L28-31) over cursors 0-5. It stores an append-only archive protected by triggers (L94-132). It checks an exact source-span match against git (observe L252-280, void_audit L330-355) and commits a record version with proposition_status='NOT_VALIDATED' (L446-461). It also has a hash-chained transitions integrity check (load L196-227). AUTHORITIES lists the reference spec files (L21-26). No physics node IDs are cited.
- Point rotation: not present.
- Path rotation: not present.
- Field: not present (workflow phase labels).
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: none. A record proves fidelity to its source, not the truth of the proposition (L3-4, L278).
- Pass criterion: every cursor's Void audit returns ALLOW on an exact payload match against the freshly observed source (L342-355). The job completes at cursor 5 with a committed consequence (L431-433).
- Violations: none.

## /home/user/One-Wave-Science/Nexus_Integration/Truth_Computer/Reference_App/test_app.py
- Purpose / node IDs cited: tests app.py. The fixture node is "OG-13" (L15). Test areas:
  - the Field/Void loop with 12 events (L29-37)
  - citation and drift holds (L38-54)
  - journal isolation and denied paths (L55-61)
  - crash recovery at every checkpoint without a repeated provider call (L88-113)
  - in-flight calls are never reissued (L115-128)
  - privacy of the candidate, audit and extra fields (L130-140, L271-316)
  - CAS concurrency (L193-198, L230-239)
  - real process-crash lock release (L251-269)
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: not applicable (a stub provider in fixtures).
- Pass criterion: the unittest assertions.
- Violations: none.

## /home/user/One-Wave-Science/Nexus_Integration/Truth_Computer/Reference_App/test_knowledge_loop.py
- Purpose / node IDs cited: tests knowledge_loop.py. The fixture node is "X-1" (L24). Test areas:
  - first record and reuse (L35-49)
  - correction then escalation (L51-73)
  - restart at every boundary (L75-85)
  - commit crash (L87-98)
  - append-only archive (L146-150)
  - schema check constraints (L152-156)
  - identity and binding (L158-161, L192-200)
  - the unrelated database is left untouched (L184-190)
  - CRLF bytes are preserved (L202-205)
  - audits cannot be fabricated and cursors cannot jump (L217-224, L285-300)
  - HTTP build (L249-282)
  - snapshot trace (L302-322)
- Point rotation: not present.
- Path rotation: not present.
- Field: not present.
- Magnetism: not present.
- Parent/child: not present.
- Hard-coded targets / refits: not applicable.
- Pass criterion: the unittest assertions.
- Violations: none.

## Slice summary
- **Canonical point-rotation implementations:** none. No file in this slice implements Point, Path or Field rotation, magnetism (B, R, K_L, kappa_R), gravity, or parent/child transport.
- **Violations of the rotation/magnetism canonical rules:** none. The slice has no physics code, so it cannot violate the L bookkeeping, open/closed magnetic switch, K_L, or transport rules.
- **Non-physics findings:**
  - close_book1_chapter_gaps.py (L6, L59-68) applies the REN renumber to repo text in a way that is not idempotent and covers the whole repo. Its FILES map (L7-23) is an identity map that does nothing. Its receipt hard-codes pass True (L108).
  - validate_updated_32_artifacts.py (L217-218) writes receipt claims (17 PDFs regenerated, visual samples rendered) that it does not perform.
  - rule_01_balanced_change.py (L95, L107) carries solved answers in `teacher_close` on public lesson objects. This is a possible conflict with the CLAUDE.md answer-exposure rule. L143 has a loose "no" grader.
  - app.py (L262) works without the existing Nexus database ("no existing database assumed"). It neither preserves nor integrates with it.
- **Live vs dead:**
  - Live: Reference_App/app.py and knowledge_loop.py are the running answer app and knowledge-store builder, with full tests. Learner_App recall_integration.py is live router code. rule_01_balanced_change.py is live curriculum, with tests.
  - Repeatable checkers: validate_repository_integrity.py and validate_updated_32_artifacts.py.
  - One-shot legacy: close_book1_chapter_gaps.py, a historic Updated 32 migration that must not be re-run.
