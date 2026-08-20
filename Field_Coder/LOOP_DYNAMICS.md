# FIELD CODER — LOOP DYNAMICS

Mandatory on this branch.

## PROJECT MEMORY LAW
Read and carry forward the complete `BUILD_SCOPE.md` verbatim. Do not replace it with a shorthand project description. Carry forward prior journal/history needed to reconstruct the project.

## BEFORE BRANCH
Before hard start, write visible notes-to-self/project-analysis covering: full goal; plan version; exact branch purpose; previous known-good behavior; prior failures; assumptions; architecture tensions; affected files/interfaces/state/tests; forbidden future work; proof criteria; likely failure modes; rollback point; workspace cleanliness; stale/false/conflicting information to remove; exact first change/test; likely effects on CPU/GPU, Field/Void separation, M4 control, persistence, and real coding/app/program workloads.

Record evidence, decisions, risks, consequences, hypotheses and reasons. Do not fabricate hidden chain-of-thought.

## DURING BRANCH
For each change: reread full goal/branch contract; declare one change and expected effects; change one thing; inspect diff/result; test immediately; compare expected/actual; record what worked and failed; record architecture evidence; clean stale/duplicate/contradictory information; update journal/progress; enforce three-attempt limit.

## WORKSPACE CLEANUP
At entry, after meaningful changes, and before close, inspect for stale, false, superseded, duplicate or contradictory project information. Correct/remove misleading material. Preserve useful historical failure evidence only when clearly labeled historical/non-authoritative. Remove dead artifacts when safe. Verify no future-branch work leaked in. Record cleanup actions.

## AFTER BRANCH
Before hard stop, write visible notes-to-self/project-analysis covering: actual changes; proven behavior; preserved behavior; what worked; what failed; failed assumptions; surprises; architecture evidence; CPU/GPU/state/persistence/interface/testing/integration consequences; effects on Void/M4 contracts; technical debt; stale information removed; files/ideas future branches should distrust or revisit; known-good state; rollback point; unresolved risks; what next branch must know; whether the master plan still fits the evidence.

If architecture must change, record an explicit architecture-change decision. Do not silently rewrite the plan.

## JOURNAL/MEMORANDUM REQUIREMENT
Every branch memorandum/diary must contain the full current project scope, relevant prior journal history, pre-branch analysis, hard-start evidence, change/test evidence, progress, what worked, what failed, cleanup actions, architecture observations, post-branch analysis, hard-stop evidence, and next-branch entry conditions.

Do not invent retroactive historical thoughts. Reconstructed old analysis must be labeled `RECONSTRUCTED FROM REPOSITORY EVIDENCE`.

## HARD START
Cannot pass without full goal, prior history, pre-branch analysis, cleanup check, allowed/forbidden scope, rollback point, first change and first test.

## HARD STOP
Cannot pass without post-branch analysis, cleanup evidence, worked/failed evidence, architecture consequences, regression evidence, journal/progress, known-good state and next-branch conditions.
