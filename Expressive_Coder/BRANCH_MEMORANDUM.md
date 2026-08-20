# BRANCH MEMORANDUM — STEP 02 MIRROR GATE SWITCH

## COMPLETE PROJECT SCOPE
Build the C++ Field/Void state-machine coding engine for autonomous software/app/program building. CPU C++ defines the reference semantics. Field expresses candidates; Void measures differential and controls the next movement. Canonical pairs are F1/V6, F2/V5, F3/V4, F4/V3, F5/V2, F6/V1. Gate 4 is also the 0 mirror/null/flip boundary. Move is ternary -1/0/+1. Six steps, five bands, four views, two choices, and one shared Field/Mirror/Void reference must remain intact. Every project is planned completely first and coded one pre-created branch at a time.

## COMPLETE ACCUMULATED JOURNAL HISTORY
Initial journal: master plan locked before implementation. Step 01 is assigned to primitive types only; deterministic CPU semantics must be proven before later behavior.

## THIS BRANCH IN THE CODING PROJECT
Step 02. Owns only the mirrored gate-pair mapping and mirror-boundary metadata.

## BEGINNING-TO-END CODING PLAN
1. Load tested Step 01 primitive types.
2. Implement `mirror_gate(Gate)` using the locked six-pair relation.
3. Implement a `GatePair` structure containing Field gate and Void gate.
4. Implement safe construction from either Field or Void side.
5. Mark Gate 4 boundary metadata explicitly as mirror/null/flip boundary information.
6. Test F1/V6 through F6/V1 individually.
7. Test `mirror_gate(mirror_gate(g)) == g` for all six gates.
8. Test pair construction from both sides.
9. Reject invalid raw gate values before mirror switching.
10. Re-run Step 01 primitive tests.

## HARD START
Step 01 primitive code and tests pass; no cycle transition logic exists yet.

## SUCCESS TEST
All six mirror pairs are exact and mirror-of-mirror always returns the original valid gate.

## HARD STOP
Stop after exhaustive mirror tests and previous tests pass.

## FORBIDDEN FUTURE WORK
Forward/reverse cycle transitions, Field candidate generation, Void decisions, memory, repo code actions, GPU.

## NEXT BRANCH
`expressive-coder/03-cycle-transition`
