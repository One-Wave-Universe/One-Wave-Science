# FIELD CODER — LOOP DYNAMICS

## AUTHORITY

This file is mandatory project memory for every Field branch.

The complete current project goal in `Field_Coder/BUILD_SCOPE.md` must be copied forward intact and read before coding. It must not be replaced by a shorthand description, abbreviated role label, or branch-local summary.

Every branch must also carry the complete prior branch journal/history required to reconstruct how the project reached the current state.

## BEFORE EVERY BRANCH — REQUIRED PROJECT ANALYSIS NOTES

Before the branch hard start may pass, write a visible project-analysis / notes-to-self entry covering:

- full project goal and current plan version;
- exact branch purpose and why this stage exists in the complete engine;
- previous known-good behavior that must survive;
- prior journal entries and failed approaches that matter here;
- assumptions being carried into this branch;
- architecture tensions or contradictions already visible;
- what files, tests, state, interfaces, and behaviors could be affected;
- what must not be touched yet;
- what evidence would prove this branch is actually correct;
- likely failure modes;
- rollback point;
- current workspace cleanliness and any stale/conflicting files that could mislead the next worker;
- explicit cleanup actions required before implementation;
- exact first change and exact first test;
- effects this branch could have on later CPU/GPU, Field/Void, M4, persistence, and real-program integration work.

These notes must be concrete project reasoning suitable for another AI or human to inspect. Do not fabricate hidden chain-of-thought. Record observable evidence, decisions, risks, consequences, hypotheses, and reasons.

## WORKSPACE CLEANUP — REQUIRED THROUGHOUT

At branch entry, after every meaningful change, and before branch close:

1. inspect the Field workspace for stale, duplicate, contradictory, superseded, or false project information;
2. remove or correct information that conflicts with the current authoritative project goal and plan;
3. preserve useful historical evidence only when clearly labeled as historical and non-authoritative;
4. remove dead implementation artifacts that are not part of the approved branch result when safe to do so;
5. verify no future-branch implementation leaked in;
6. verify tests, docs, progress, journal, and branch memorandum all describe the same actual state;
7. record every cleanup action in the branch journal;
8. never silently erase evidence of a failed approach—move it into clearly labeled failure/history notes when it remains useful.

If old information could misdirect a future worker, leaving it unlabeled is a branch failure.

## DURING THE BRANCH — REQUIRED SELF-CHECK LOOP

For every controlled change:

- reread the full project goal and current branch contract;
- state the exact intended change;
- state expected effects and possible side effects;
- make one change only;
- inspect the actual diff/result;
- run the declared test immediately;
- compare expected behavior to observed behavior;
- record what worked;
- record what failed;
- record what changed in the project model because of the evidence;
- record whether the change creates pressure on future architecture;
- clean stale/conflicting workspace information created or exposed by the change;
- update progress and journal before the next change;
- apply the three-attempt rule to one failing approach;
- stop rather than invent an unplanned fourth attempt.

## AFTER EVERY BRANCH — REQUIRED PROJECT ANALYSIS NOTES

Before hard stop may pass, write a second visible project-analysis / notes-to-self entry covering:

- what the branch actually changed;
- what behavior is now proven;
- what remained unchanged and why that matters;
- what worked technically;
- what did not work technically;
- failed assumptions;
- surprises or mismatches between plan and implementation;
- new architecture evidence;
- performance, CPU/GPU, state, persistence, interface, testing, and integration consequences;
- effects on the separate Void side and M4 routing contract without implementing those future parts early;
- technical debt created or removed;
- stale or false information removed during cleanup;
- files or ideas future branches must distrust or revisit;
- exact known-good state and rollback point;
- unresolved risks;
- what the next branch must know before touching code;
- whether the current master plan still fits the evidence;
- if it does not, create an explicit architecture-change record rather than silently changing the plan.

## JOURNAL LAW

Every branch memorandum and diary must contain:

- the full current project scope;
- complete relevant prior journal history;
- pre-branch project-analysis notes;
- hard-start evidence;
- change-by-change work/test evidence;
- progress state;
- what worked;
- what failed;
- cleanup actions;
- architecture observations;
- post-branch project-analysis notes;
- hard-stop evidence;
- next-branch entry conditions.

Historical branches must not be given invented contemporaneous thoughts. If old evidence is reconstructed later, label it `RECONSTRUCTED FROM REPOSITORY EVIDENCE` and distinguish it from notes written at the time.

## EFFECT-OF-ACTION RULE

Before and after each branch, explicitly consider how the worker's actions affect the project as a whole: correctness, drift risk, maintainability, future branch assumptions, testing confidence, state compatibility, CPU/GPU behavior, Field/Void separation, M4 control, and real coding/app/program workloads.

A branch is not successful merely because new code runs. Its effect on the complete project must be understood and recorded.

## HARD START ADDITION

Hard start cannot pass unless the full project goal, prior history, pre-branch analysis notes, workspace-cleanliness check, allowed scope, forbidden scope, rollback point, first change, and first test are present and consistent.

## HARD STOP ADDITION

Hard stop cannot pass unless post-branch analysis notes, cleanup evidence, what-worked/what-failed evidence, architecture consequences, regressions, journal/progress, known-good state, and next-branch conditions are present and consistent.
