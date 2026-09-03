# Branch Step — Rabbit-Hop Reconstruction

## MAIN GOAL
Build a reliable Field/Void software-construction engine for real programs.

## WHY THIS STEP EXISTS
G-721 coordinates existed, but the requested constellation traversal and
memory-rebuild behavior did not. Documentation was being mistaken for code.

## CURRENT STEP GOAL
Add one executable, receipt-producing rabbit-hop reconstruction slice.

## HARD START
- Repository root verified: `/workspace/scratch/8c97bfddfea7/One-Wave-Science`
- Branch: `state-machines/rabbit-hop-reconstruction`
- Starting HEAD: `edd31cc7e5c198fd023a9314e67c9cf96c6e3132`
- Worktree was clean.

## REFERENCE FILES
- `AGENTS.md`
- `JETSON_OPENCLAW_RUNTIME.md`
- `ARCHITECTURE_MEMORY_REBUILD_CONSTELLATION.md`
- `ARCHITECTURE_RABBIT_HOPPING_SCALE_TRANSLATOR.md`
- `One_Wave_Bench/brain/rabbit_hop_alphabet.py`
- `One_Wave_Bench/brain/command_memory.py`

## ALLOWED FILES
- `One_Wave_Bench/brain/constellation_memory.py`
- `One_Wave_Bench/brain/test_constellation_memory.py`
- `One_Wave_Bench/brain/README.md`
- This branch-step receipt

## PROTECTED WORKING FEATURES
Existing brain, logic-core, dynamics, engine, simulator, and micro tests.

## ONE CHANGE
Connect constellation neighborhood entry, reversible G-721 traversal,
Hopfield-style completion, bounded seeded Boltzmann ambiguity, validation, and
a matched flat baseline in one CPU-reference module.

## SUCCESS CRITERIA
- Partial cue plus rabbit handle reconstructs the intended distinct memory.
- Flat baseline remains ambiguous on the same cue.
- At least one `2N +/- 1` connector is recorded and exactly reversible.
- Probabilistic fill is seeded and marked uncertain.
- Context validation can accept, hold, or reject without rewriting storage.
- Protected tests remain passing.

## PROGRESS REPORT
- Completed: executable reconstruction module and deterministic acceptance tests
- Working: route-aware rebuild, baseline comparison, inverse receipts, uncertainty,
  and validation
- Not working: no failures observed in this bounded step
- Blocked: none
- Attempt: Approach A, attempt 1/3 passed
- Tests: `python -m unittest discover -s One_Wave_Bench -p 'test_*.py'`
  passed 41/41; `git diff --check` passed
- Field position: implementation matches the canonical subsystem separation.
- Void pre-decision: `ALLOW`; bounded new module, no actuator authority
- Void post-decision: `ALLOW`; tests prove the requested path and preserve all
  previously covered behavior
- Hard stop: stop after tests, diff review, receipt update, and review-ready commit.

## LOOK-BACK REFLECTION
- What changed: rabbit hopping now participates in executable memory rebuild,
  rather than ending at coordinate generation.
- What worked: a partial `flower` cue is ambiguous in the matched flat baseline;
  route handle `A` traverses shared connector `3` to reconstruct distinct memory
  `B`, and the stored receipt reverses exactly.
- What failed: nothing in Approach A.
- Evidence: 41/41 repository Python tests pass and the diff whitespace check passes.
- Learned: prior audits checked named-file presence, not end-to-end behavior.
- Protected software: all previously discovered One_Wave_Bench tests still pass.
- Main-goal advance: yes; the runtime gains a testable memory-routing primitive.
- Carry forward: integrate this proposal receipt into the live M4 cycle in a
  separate branch-step; do not fold that extra scope into this one.

## HANDOFF
- Known-good state: this branch after the review-ready commit
- Verified features: constellation entry, G-721 traversal, Hopfield completion,
  bounded seeded Boltzmann ambiguity, context validation, matched baseline,
  inverse route receipt
- Open problems: live M4/dual-state runtime consumption is not part of this step
- Failed approaches not to repeat: none
- Tests that must continue passing: full `One_Wave_Bench` unittest discovery
- Next branch-step: consume `RebuildReceipt` in the live M4 active-world loop
- Admin/escalation required: NO
