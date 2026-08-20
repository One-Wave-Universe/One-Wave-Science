# BRANCH MEMORANDUM — STEP 03 CYCLE TRANSITION

## COMPLETE PROJECT SCOPE
Build the C++ Field/Void state-machine coding engine for autonomous software/app/program building. CPU C++ is the semantic reference. Field expresses a candidate; Void compares against the shared reference and controls the next movement. Gate pairs remain F1/V6, F2/V5, F3/V4, F4/V3, F5/V2, F6/V1. Gate 4 carries mirror/null/flip boundary meaning. Move is strict ternary Compress=-1, Hold=0, Expand=+1. The six-step path is Begin -> Build -> Hold -> Build -> Break -> Loop and reverse in the opposite direction. Every project is fully planned before coding and implemented one pre-created branch at a time.

## COMPLETE ACCUMULATED JOURNAL HISTORY
Initial journal: plan and gate semantics locked. Step 01 owns primitives. Step 02 owns mirror pairing. CPU correctness precedes later neural/GPU behavior.

## THIS BRANCH IN THE CODING PROJECT
Step 03. Owns only deterministic six-position forward/reverse/hold transitions and explicit loop-boundary behavior.

## BEGINNING-TO-END CODING PLAN
1. Load tested primitive and mirror code.
2. Define cycle cursor containing the active Field/Void pair position.
3. Implement Expand(+1) as one forward position.
4. Implement Compress(-1) as one reverse position.
5. Implement Hold(0) as no position change.
6. Implement explicit position-6 Loop behavior.
7. Implement explicit reverse boundary behavior at position 1.
8. Keep mirror pair synchronized after every transition.
9. Test all 18 gate-position/move combinations.
10. Test one complete forward loop and one complete reverse loop.
11. Test Hold at every position.
12. Re-run Steps 01-02 tests.

## HARD START
Primitive and mirror tests pass; no shared state packet or Field/Void policy exists yet.

## SUCCESS TEST
Every legal state/move combination yields one deterministic synchronized next pair and all full-cycle tests pass.

## HARD STOP
Stop after transition-table coverage and previous tests pass.

## FORBIDDEN FUTURE WORK
State packet fields beyond transition cursor, Field candidate generation, Void differential/policy, persistence, repo actions, GPU.

## NEXT BRANCH
`expressive-coder/04-state-packet`
