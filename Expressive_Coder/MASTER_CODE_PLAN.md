# EXPRESSIVE CODER — MASTER CODE PLAN

## COMPLETE PROJECT SCOPE

Build the actual C++ Field/Void state-machine coding engine that can autonomously build, modify, test, debug, and improve real software, applications, and programs.

This is not a generic chatbot framework and not a documentation-only project. The product is an executable coding engine whose core control logic is implemented as a deterministic Field/Void state machine first, then extended with memory, code-project context, coding actions, recovery, and CPU/GPU execution.

The complete coding plan is defined before implementation begins. Every coding step is represented by a pre-created branch. Each branch is one reserved implementation stage. The engine is coded one branch at a time. No future branch work may be implemented early.

Every branch memorandum must contain the complete current project scope, complete accumulated prior journal history, exact branch instructions, branch-specific hard start, branch-specific hard stop, progress state, what worked, what failed, architecture evidence, rollback point, and next-branch requirements.

## CANONICAL FIELD / VOID GATE FUNDAMENTALS

The C++ gate layer must encode these canonical relations directly and test them exhaustively.

### Mirrored gate pairs

- Field Gate 1 <-> Void Gate 6
- Field Gate 2 <-> Void Gate 5
- Field Gate 3 <-> Void Gate 4
- Field Gate 4 <-> Void Gate 3
- Field Gate 5 <-> Void Gate 2
- Field Gate 6 <-> Void Gate 1

The mirror relation is therefore `mirror(gate) = 7 - gate` for gate numbers 1..6.

Gate 4 is also the Gate 0 mirror/null/flip boundary in the architecture. The implementation must represent the mirror boundary explicitly rather than hiding it in ad-hoc control flow.

### Six-step cycle

1. Begin
2. Build
3. Hold
4. Build
5. Break
6. Loop

Forward cycle: `1 -> 2 -> 3 -> 4(0) -> 5 -> 6`.
Reverse cycle: `6 -> 5 -> 4(0) -> 3 -> 2 -> 1`.

### Five scale/state bands

- Micro / Floor
- Small / Low
- Medium / Mid
- Large / High
- Macro / Ceiling

The numeric scale reference may be represented as 0 / 25 / 50 / 75 / 100 while the enum remains five discrete bands.

### Four views

- Inward
- Outward
- Across
- Over

### Three moves

- Compress = -1
- Hold = 0
- Expand = +1

The movement type must be a strict ternary value. Invalid values must be rejected.

### Two choices

- Nothing
- Everything

Choice is a mirrored binary decision inside a ternary-capable state machine; HOLD remains a movement/state result rather than a third choice value.

### One shared relation

Field / Mirror / Void share one active state reference. Field expresses a candidate movement. Void measures that candidate against the current goal/reference and controls whether the next movement is allowed, corrected, overridden, held, or escalated.

## CORE EXPRESSIVE CODER LOOP

The final engine must execute this control path:

`PROJECT GOAL`
-> `CURRENT REFERENCE STATE`
-> `FIELD EXPRESSIVE PASS`
-> `CANDIDATE SOFTWARE MOVEMENT`
-> `VOID DIFFERENTIAL / OVERSIGHT`
-> `ALLOW | CORRECT | OVERRIDE | HOLD | ESCALATE`
-> `TERNARY NEXT-MOVE SELECTION (-1,0,+1)`
-> `STATE / MEMORY UPDATE`
-> `CODE / TEST / DIFF EVIDENCE`
-> `REFERENCE UPDATE`
-> `LOOP`

Field is the expressive software-building side. Void is the oversight/override side. M4/controller timing and routing coordinates the loop but does not replace either side.

## CPU / GPU RESPONSIBILITY

### CPU

The first known-good implementation is CPU-first C++.

CPU owns:

- gate enums and transition tables;
- mirror pairing;
- state packets;
- deterministic state transition logic;
- Field/Void control decisions;
- task and repository orchestration;
- journaling/state persistence;
- test/diff routing;
- branch-loop control;
- fallback execution when no GPU is present.

### GPU

GPU work is forbidden until the deterministic CPU implementation passes.

GPU later owns parallelizable work such as:

- evaluating many candidate state vectors;
- scoring candidate code actions;
- batched differential calculations;
- lattice/vector state updates;
- optional model/tensor adapter execution.

The GPU must not redefine gate semantics. CPU and GPU must produce equivalent gate/differential results for the same deterministic fixture inputs.

## REQUIRED C++ STANDARD

Use portable C++17 or newer unless a later branch records a justified architecture change.

Prefer:

- scoped `enum class` types;
- immutable/simple state structs;
- explicit transition functions;
- deterministic tests;
- no undefined implicit integer-to-enum switching;
- no provider-specific AI dependency in the core gate library;
- CPU-first reference implementations before GPU kernels.

## PRE-CREATED PROGRAMMING BRANCHES

### 00 — `expressive-coder/00-master-plan`

Purpose: lock complete project scope, canonical gate semantics, full branch roadmap, memory/journal laws, and branch loop rules.

Hard start: repository is readable and `main` is available.

Internal coding plan:
1. write complete project scope;
2. define canonical primitives;
3. define CPU/GPU boundary;
4. define all implementation branches;
5. create all planned branches;
6. create branch memorandum requirements;
7. record initial project journal/progress.

Hard stop: all planned branches exist and the plan is explicit enough that each branch can be implemented without inventing its purpose while coding. No engine implementation beyond tiny compile/test scaffolding is allowed here.

### 01 — `expressive-coder/01-gate-primitives`

Purpose: code the C++ fundamental enums/types and validation rules.

Hard start: Step 00 complete; master plan and memorandum loaded.

Internal coding plan:
1. create C++ library directory;
2. define Side, Gate, Step, Scale, View, Move, Choice, VoidDecision;
3. encode ternary move values exactly -1/0/+1;
4. add value validation/conversion helpers;
5. add static/runtime tests for all legal values and rejection of illegal raw inputs;
6. verify no transition logic from Step 02 is implemented early.

Hard stop: all primitive types compile and tests prove exact enum/value semantics.

### 02 — `expressive-coder/02-mirror-gate-switch`

Purpose: code and prove mirrored gate switching.

Hard start: Step 01 primitive types pass.

Internal coding plan:
1. implement `mirror_gate(Gate)`;
2. implement Field/Void pair object;
3. prove F1/V6 through F6/V1 exhaustively;
4. represent mirror boundary metadata for Gate 4/0;
5. reject invalid gate input before switching;
6. test mirror-of-mirror returns original gate.

Hard stop: exhaustive tests prove all six mirror pairs and involution behavior.

### 03 — `expressive-coder/03-cycle-transition`

Purpose: code deterministic six-step forward/reverse/hold switching.

Hard start: Step 02 mirror switching passes.

Internal coding plan:
1. define cycle cursor/state;
2. implement Expand(+1) transition;
3. implement Compress(-1) transition;
4. implement Hold(0) transition;
5. implement Gate 6 Loop boundary behavior explicitly;
6. implement reverse boundary behavior explicitly;
7. test full forward cycle, reverse cycle, hold-at-every-gate, and loop behavior.

Hard stop: every legal gate/move combination has a deterministic tested next state.

### 04 — `expressive-coder/04-state-packet`

Purpose: build the complete shared state packet carried through Field/Void.

Hard start: Step 03 transitions pass.

Internal coding plan:
1. define current gate pair;
2. add Step, Scale, View, Move, Choice;
3. add active project/task/reference identifiers;
4. add attempt/approach state;
5. add known-good/candidate state IDs;
6. add validation/invariants;
7. test copy/equality/serialization-ready representation.

Hard stop: valid packets round-trip through deterministic construction and invalid combinations are rejected.

### 05 — `expressive-coder/05-field-expression`

Purpose: code Field's expressive candidate-generation interface without Void approval logic.

Hard start: Step 04 state packet passes.

Internal coding plan:
1. define FieldInput;
2. define CandidateMovement;
3. map goal/reference/state into one bounded candidate;
4. attach expected changed scope and expected test;
5. attach requested ternary movement;
6. forbid Field from marking itself approved;
7. test deterministic fake candidate generator.

Hard stop: Field produces exactly one structurally valid candidate and cannot self-approve.

### 06 — `expressive-coder/06-void-differential`

Purpose: code the Void differential calculation against the reference.

Hard start: Step 05 candidate contract passes.

Internal coding plan:
1. define reference evidence input;
2. compare intended vs actual state dimensions;
3. compute bounded differential flags/scores;
4. detect scope expansion, missing evidence, regression and conflict;
5. preserve separate raw evidence from decision policy;
6. test known matching and mismatching fixtures.

Hard stop: Void produces deterministic differential evidence without yet changing code.

### 07 — `expressive-coder/07-oversight-override`

Purpose: code Void's next-state authority.

Hard start: Step 06 differential passes.

Internal coding plan:
1. define decision policy for ALLOW/CORRECT/OVERRIDE/HOLD/ESCALATE;
2. map differential evidence to decision;
3. map decision to bounded next movement;
4. enforce OVERRIDE as replacement of next action, not unrestricted implementation;
5. prove HOLD leaves state unchanged;
6. prove ESCALATE terminates autonomous movement.

Hard stop: all five Void outcomes are reachable, deterministic, and tested.

### 08 — `expressive-coder/08-field-void-loop`

Purpose: integrate Field candidate generation, Void differential, decision, and ternary transition into one CPU loop.

Hard start: Steps 01-07 pass.

Internal coding plan:
1. instantiate shared state;
2. run Field once;
3. run Void differential;
4. run oversight decision;
5. apply permitted/overridden ternary movement;
6. update state once;
7. emit loop evidence record;
8. test ALLOW/CORRECT/OVERRIDE/HOLD/ESCALATE fixtures end-to-end.

Hard stop: one complete deterministic Field/Void cycle works without repository-editing behavior.

### 09 — `expressive-coder/09-memory-reference`

Purpose: persist state, references, journal events, attempts, and known-good state.

Hard start: Step 08 loop passes.

Internal coding plan:
1. define persistent engine state format;
2. save/load exact state;
3. append immutable journal event records;
4. persist known-good and candidate references;
5. persist branch/attempt/approach state;
6. reject corrupt/incomplete state;
7. test restart continuity.

Hard stop: process restart restores exact loop state and journal history.

### 10 — `expressive-coder/10-code-project-context`

Purpose: connect the engine read-only to a real local code project.

Hard start: Step 09 persistence passes.

Internal coding plan:
1. locate `$HOME/One-Wave-Science` or configured project root;
2. read branch/HEAD/status;
3. discover relevant source/test/build files;
4. build read-only code context packet;
5. record project goal and branch contract with context;
6. prove working tree remains unchanged.

Hard stop: engine reconstructs a fixture/project context without modifying files.

### 11 — `expressive-coder/11-code-action`

Purpose: allow one controlled code edit from an approved Field candidate.

Hard start: Step 10 read-only context passes.

Internal coding plan:
1. define approved edit action;
2. restrict paths to declared scope;
3. create rollback snapshot/reference;
4. apply exactly one change;
5. block undeclared path edits;
6. capture actual diff;
7. test success and blocked-scope fixtures.

Hard stop: one bounded edit can be applied and safely rolled back.

### 12 — `expressive-coder/12-test-diff-feedback`

Purpose: feed actual code/test evidence back through Field/Void.

Hard start: Step 11 controlled edit passes.

Internal coding plan:
1. run declared build/test command;
2. capture stdout/stderr/exit/timeout;
3. capture actual diff/file inventory;
4. compare expected vs actual behavior;
5. feed evidence into Void differential;
6. produce next decision;
7. verify failed tests do not crash controller.

Hard stop: real edit evidence can drive the next Field/Void decision.

### 13 — `expressive-coder/13-recovery-loop`

Purpose: implement bounded correction and three-attempt recovery.

Hard start: Step 12 feedback loop passes.

Internal coding plan:
1. track approach ID and attempt 1/3;
2. allow targeted Attempt 2 from evidence;
3. require materially different Attempt 3;
4. forbid hidden Attempt 4;
5. search project coding references when stuck;
6. rollback failed candidate when required;
7. produce escalation packet when unresolved.

Hard stop: automated fixture proves correct retry, rollback, and escalation behavior.

### 14 — `expressive-coder/14-cpu-gpu-adapter`

Purpose: preserve CPU semantics while adding an optional GPU compute seat.

Hard start: Step 13 CPU recovery loop passes.

Internal coding plan:
1. define provider-neutral compute interface;
2. retain CPU reference implementation;
3. add optional GPU backend boundary;
4. batch candidate/differential vectors only;
5. compare CPU and GPU fixture outputs;
6. fall back automatically to CPU;
7. forbid GPU backend from redefining gate semantics.

Hard stop: compute backend is replaceable and deterministic fixtures agree with CPU reference.

### 15 — `expressive-coder/15-autonomous-coder-trial`

Purpose: prove the complete engine can perform one tiny software repair from goal to verified candidate.

Hard start: Steps 01-14 pass.

Internal coding plan:
1. create/use sacrificial fixture repo;
2. ingest explicit coding goal;
3. reconstruct context;
4. Field produces one candidate;
5. Void oversees/overrides;
6. apply controlled edit;
7. build/test/diff;
8. retry if required;
9. preserve known-good state;
10. emit complete journal/progress/evidence packet.

Hard stop: one successful task and one deliberate failure/recovery path pass end-to-end.

### 16 — `expressive-coder/16-real-app-program-trial`

Purpose: apply the engine to one tiny real app/program-building task under the same controls.

Hard start: Step 15 sacrificial trial passes.

Internal coding plan:
1. choose one bounded real software task;
2. load full project scope and branch memorandum;
3. operate through the complete Field/Void loop;
4. make only declared edits;
5. run actual project tests/build;
6. preserve rollback point;
7. record complete evidence;
8. stop after one review-ready candidate.

Hard stop: one real code/app/program task is completed or safely escalated without uncontrolled scope expansion.

## GLOBAL HARD START FOR EVERY IMPLEMENTATION BRANCH

Before coding any branch:

1. include the complete project scope in the branch memorandum;
2. include the complete accumulated journal history in the branch memorandum;
3. identify plan version;
4. identify branch number/name and exact purpose;
5. identify exact beginning-to-end internal coding sequence;
6. verify previous required branch evidence;
7. verify local project/branch/HEAD/known-good state;
8. identify allowed files/subsystem;
9. identify forbidden files/future work;
10. identify first permitted code change and its exact test;
11. write pre-branch journal entry;
12. do not code if any required item is missing.

## GLOBAL HARD STOP FOR EVERY IMPLEMENTATION BRANCH

Before leaving any branch:

1. complete only the branch's assigned subsystem;
2. run all branch-required tests;
3. rerun previous known-good tests;
4. verify no future branch work leaked in;
5. record every meaningful code change;
6. record exact tests/results;
7. record what worked;
8. record what did not work;
9. record architecture evidence for future plan revisions;
10. record attempts and failed approaches;
11. preserve known-good/rollback reference;
12. update progress;
13. append complete post-branch journal;
14. identify next branch and its hard start;
15. stop coding this branch immediately.

## PROJECT JOURNAL — INITIAL ENTRY

Project created as a preplanned branch-by-branch C++ build. No implementation branch may invent its own purpose. Gate semantics are locked before neural/model/GPU behavior. CPU deterministic correctness is the reference. Every later AI worker must reconstruct intent from repository memory, not conversation memory.
