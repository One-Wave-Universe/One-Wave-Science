# Learner App — Worker 1: reusable problem parser/builder

Implements the issue-#40 contract: a small, reusable, deterministic
rule-driven problem-structure engine, with `math/basic_equations` as the
first domain adapter used to prove the contract. This is **not** an
algebra-specific generator with a thin wrapper — the core has no algebra
knowledge in it at all (see `tests/test_core.py::CorePurityTests`, which
scans the core source files for algebra vocabulary and fails if any is
found).

## Architecture: router → generic core → adapter

```text
ROUTER (not built here)
  owns: target rules, allowed/forbidden rules, prerequisites,
        sequencing, difficulty, review scheduling, learner state,
        progression, domain/adapter selection
  |
  v  RulePacket(packet_id, seed, domain, target_rules, ...)
  |
GENERIC PARSER / PROBLEM-BUILDER CORE   (parser/core.py, parser/adapter.py, parser/verifier.py)
  owns: resolving the adapter, driving generation with a seeded RNG,
        independently reparsing the generated artifact, verifying
        requested/forbidden rule presence, rejecting bad packets
  knows nothing about: equations, coefficients, variables, or any
        other domain vocabulary
  |
  v  dispatches by packet.domain through an explicit registry
  |
DOMAIN ADAPTER (parser/adapters/math_basic_equations.py is the first one)
  owns: domain syntax/semantics, candidate generation, its own
        independent tokenizer/parser, domain-specific structural
        validation and metadata (e.g. "single_target_unknown")
  |
  v  GeneratedProblem(artifact_text, structure, rules_used,
                       verification, metadata, ...)  -- no answer field
  |
  v (back to the router)
```

The core/adapter boundary is enforced two ways:

1. **Source-level**: `tests/test_core.py::CorePurityTests` greps
   `parser/core.py`, `parser/adapter.py`, and `parser/verifier.py` for
   algebra vocabulary (`EQ.`, `coefficient`, `variable_name`, `equation`,
   `divisor`, `lhs`, `rhs`) and fails the build if any of it leaks in.
2. **Behavioral**: `tests/test_adapter_contract.py` registers a second,
   unrelated adapter (`tests/fixtures/trivial_echo_adapter.py`, which
   generates plain words, not equations) and runs it through the exact
   same `build_problem()` pipeline with zero changes to the core files.
   That is the proof a second adapter can be added without touching
   generation/verification core logic.

## Generate → reparse → verify

`build_problem()` in `parser/core.py` never trusts the object the
generator used internally to build the artifact text. The pipeline is:

```text
RulePacket
  -> generic contradiction check (a rule cannot be both target and forbidden)
  -> resolve adapter (from the registry by packet.domain, or an explicit
     override -- either way resolved_adapter.domain must equal packet.domain)
  -> adapter.validate_packet(packet)         # domain-specific rejection
  -> adapter.generate_candidate(packet, rng)  # returns TEXT only
  -> adapter.parse_artifact(artifact_text)    # independent reparse of that text
  -> adapter.inspect_rules(structure)
  -> adapter.validate_structure(structure, packet)
  -> verifier.build_verification(...)
  -> return GeneratedProblem only if verification.passed, else raise
```

`generate_candidate` and `parse_artifact` are separate code paths with no
shared internal object — the math adapter's generator builds a string from
random integers directly; its parser is a from-scratch tokenizer + small
recursive-descent parser that only ever looks at that string, and rejects
any character the grammar doesn't recognize instead of silently skipping it
(`_tokenize()` checks every gap between matched tokens, not just the
matches themselves — see `TokenizerCoverageTests`). A deliberately broken
generator (see
`test_math_basic_equations.py::test_malformed_candidate_fails_reparse_and_verification`)
demonstrates the reparse step actually catches bad output instead of
rubber-stamping it.

`verifier.build_verification()` enforces three things generically, none of
them domain-specific: every target rule is demonstrated
(`requested_rules_present`), no forbidden rule is demonstrated
(`forbidden_rules_absent`), and — just as important — nothing else showed
up either: `rules_used` must be a subset of
`target_rules | allowed_support_rules`. That last check is what stops the
worker from silently adding a rule the router never approved; "merely not
forbidden" is not the same as "permitted," since the router may simply not
have thought to forbid it. See `test_verifier.py`'s
`test_build_verification_fails_on_unapproved_extra_rule`.

`build_problem()`'s `adapter=` parameter (mainly used by tests to exercise
a deliberately broken adapter without touching the registry) still can't
be used to build a packet under an adapter for the wrong domain —
`resolved_adapter.domain` is checked against `packet.domain` regardless of
where the adapter came from, so domain selection stays the router's call.

A `RulePacket` is meant to be a fixed instruction, not something a caller
can quietly edit after handing it to the worker: `constraints` and
`metadata` are snapshotted at construction (`models._freeze_mapping()`
/ `_deep_freeze()`) into read-only mappings, recursively -- a mapping
becomes a `MappingProxyType`, a list/tuple becomes a tuple, and a set
becomes a `frozenset`, at every nesting depth, not just the top level. So
mutating the caller's original dict afterward (including a dict or list
nested *inside* a constraint value), or assigning into `packet.constraints`
directly, cannot change what a later `build_problem()` call sees. An
arbitrary custom object nested inside a constraint value is left as-is --
the core freezes the standard container shapes it can recognize
generically, not arbitrary domain-specific object graphs. See
`test_models.py`.

The worker never repairs an infeasible router constraint by widening it.
If `EQ.MUL_INVERSE`/`EQ.DIV_INVERSE` is targeted and no coefficient/divisor
`>= 2` fits inside the router's exact `coefficient_range`,
`validate_packet()` rejects the packet outright rather than drawing a
value outside that range (`CoefficientRangeExactnessTests`). Likewise, for
`EQ.SUB_INVERSE` the term value is now constructed *around* whatever
constant was drawn (`term_value = constant + <extra>`) instead of being
picked independently and then clamped — so a wide `constant_range` always
produces a valid equation instead of occasionally raising
`ProblemVerificationError` from a packet `validate_packet()` had already
accepted (`ConstantRangeFeasibilityTests`). A `constant_range` that could
produce a negative constant (v1's grammar has no unary minus anywhere) is
rejected the same way, at `validate_packet()` time rather than
intermittently by seed once generation runs (`ConstantRangeSignTests`) --
`0` is still an allowed constant, since whether a trivial instance like
`"x + 0 = 5"` is worth practicing is a router/curriculum call, not
something this worker should silently veto.

## Determinism

`core.build_problem()` seeds a fresh `random.Random(packet.seed)` per call
and hands that single RNG to the adapter — adapters must not create their
own uncontrolled randomness. Same `RulePacket` (same seed) always produces
byte-identical `artifact_text` and structure.

## No-answer rule

`GeneratedProblem` (see `parser/models.py`) has no `answer`/`solution`
field, and the math adapter's `generate_candidate()` never returns or
stores the value that satisfies the equation — it derives the right-hand
side directly from randomly chosen term/constant values, so there is no
"solved x" anywhere in the code to accidentally leak.
`tests/test_core.py::NoAnswerFieldTests` and
`tests/test_math_basic_equations.py::test_no_public_output_reveals_the_solved_unknown`
assert this at the dataclass level.

## `math/basic_equations` adapter (v1)

Supported rule recipes (adapter fixtures, not curriculum):

```text
EQ.IDENTITY      x = c
EQ.ADD_INVERSE   x + b = c
EQ.SUB_INVERSE   x - b = c
EQ.MUL_INVERSE   a*x = c
EQ.DIV_INVERSE   x/a = c
```

Supported target-rule combinations for v1 (`SUPPORTED_COMBOS` in
`parser/adapters/math_basic_equations.py`): each rule alone, plus
`{ADD_INVERSE, MUL_INVERSE}`, `{SUB_INVERSE, MUL_INVERSE}`,
`{ADD_INVERSE, DIV_INVERSE}`, `{SUB_INVERSE, DIV_INVERSE}`. A coefficient
and a divisor together on the same term is not supported in v1, so
`{MUL_INVERSE, DIV_INVERSE}` is rejected by `validate_packet()` before
generation.

**Explicitly unsupported in v1** (raises a rejection or a parse failure,
by design):

- variables on both sides of `=`
- parentheses
- exponents
- non-integer / fractional coefficients
- negative numbers anywhere (grammar has no unary minus)
- more than one constant term
- more than one occurrence of the variable
- multi-letter variable names
- any `constraints.number_domain` other than `"integer"` (the default)
- any character the tokenizer doesn't recognize, even mid-artifact (e.g.
  `"x + 4 @ = 9"` is rejected, not silently read as `"x + 4 = 9"`)
- a zero divisor or a zero coefficient (`"x/0 = 5"`, `"0x = 5"` are both
  rejected at parse time, an input-boundary check, not just a generator
  round-trip check -- a zero coefficient in particular would otherwise
  divide by zero inside `validate_structure()`'s integer-domain check)
- a malformed `coefficient_range`/`constant_range` (wrong shape, non-int,
  or reversed `lo > hi`) or a non-positive `difficulty` -- these fail
  cleanly in `validate_packet()` rather than crashing later inside
  `generate_candidate()`
- a `coefficient_range` with no value `>= 2` when `EQ.MUL_INVERSE` or
  `EQ.DIV_INVERSE` is targeted (e.g. `(1, 1)`) -- rejected as infeasible
  rather than silently drawing a coefficient outside that range

### Number domain: solutions stay integers

`constraints.number_domain` defaults to `"integer"`, v1's only supported
value (`validate_packet()` rejects anything else). When `EQ.MUL_INVERSE` is
targeted, `generate_candidate()` builds the coefficient's term from a
hidden integer multiplier (never returned or stored) instead of picking
the term's value independently, so the unknown always solves to a whole
number — `7x = 34` (unknown `34/7`) can't be generated.
`validate_structure()` then independently re-derives the term's value from
the public `rhs`/constant and checks it's an exact multiple of the
coefficient, catching any adapter that violated this without trusting the
generator's intent. See `IntegerSolutionTests`.

Example generated artifacts (structural metadata only, no answers):

```text
packet target_rules=[EQ.ADD_INVERSE]                 -> "x + 12 = 46"
packet target_rules=[EQ.MUL_INVERSE]                 -> "7x = 42"
packet target_rules=[EQ.ADD_INVERSE, EQ.MUL_INVERSE] -> "7x + 17 = 24"
packet target_rules=[EQ.SUB_INVERSE, EQ.DIV_INVERSE] -> "x/7 - 17 = 2"
```

## Layout

```text
Learner_App/
  README.md
  parser/
    __init__.py
    models.py      # RulePacket, GeneratedProblem, VerificationResult
    core.py         # build_problem(): the generate -> reparse -> verify pipeline
    adapter.py      # ProblemAdapter protocol + explicit registry
    verifier.py      # pure rule-presence/absence checks
    adapters/
      __init__.py                 # register_default_adapters()
      math_basic_equations.py     # first real domain adapter
  tests/
    test_core.py               # core purity + reusability acceptance tests
    test_verifier.py           # verifier unit tests
    test_models.py             # RulePacket immutability tests
    test_math_basic_equations.py  # math adapter acceptance tests
    test_adapter_contract.py   # second-adapter proof + protocol compliance
    fixtures/
      trivial_echo_adapter.py  # tiny non-equation adapter, tests-only
```

## Phase 2: Router Loop + Two State Machines (issue #42)

Phase 2 proves one complete deterministic learning cycle on top of the
Phase 1 worker above, without changing it.

```text
STATE MACHINE A (LearnerTaskState) <-> ROUTER LOOP <-> STATE MACHINE B (EvaluatorState)
                                            |
                                    Phase 1 worker (parser.core.build_problem)
```

**The router loop is the orchestrator, not a third state machine.** There
are exactly two state machines in this phase:

- **State Machine A** (`router/state_machine_a.py`) — the live
  learner/task interaction state. Five states, one allowed cycle:
  `IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING -> IDLE`. Each
  edge is its own function (`assign_problem`, `present_to_learner`,
  `receive_attempt`, `apply_route_decision`, `resolve_cycle`); calling one
  out of order raises `IllegalTaskTransitionError` rather than silently
  coercing the state.
- **State Machine B** (`router/state_machine_b.py`) — evaluation of a
  learner attempt into structured evidence. Three states, one allowed
  cycle: `IDLE -> EVALUATING -> EMITTED -> IDLE`. Its pure evaluation
  logic (`evaluate_attempt`) only ever compares rule-ID *strings* — the
  problem's target rules against the attempt's self-reported
  `reported_rules_used` — to compute `missing_rules` and `error_kind`
  (set whenever a target rule is missing, regardless of `outcome`, so a
  "correct" attempt that skipped a target rule is still visibly
  incomplete). `outcome` (`"correct" | "incorrect" | "incomplete"`) is
  supplied by the `LearnerAttempt` itself, from whatever graded it
  upstream of this phase (a human, a test harness, or — per CLAUDE.md —
  a later explicitly authorized answer-checking component); State
  Machine B never re-derives or leaks a solved answer. **B stays at
  `EMITTED` after `submit_attempt()` returns** — it does not reset to
  `IDLE` until the router explicitly consumes its evidence in
  `route_next()`.
- **Router Loop** (`router/router_loop.py`, class `RouterLoop`) — owns
  routing/sequencing: it reads the current task state, applies the
  deterministic policy in `router/policy.py` to build a `RouteDecision`,
  turns that into a `RulePacket`, calls Phase 1's `build_problem()`
  through its public contract only, and drives both state machines
  through one cycle. All of this loop's bookkeeping (curriculum
  position, current route, repeated-error tracking) is **instance
  state** on one `RouterLoop` object, never module-level/global state —
  two independently constructed instances with the same config and seed
  always produce the same sequence of decisions.

`router/policy.py`'s `decide_next_route()` is a pure function (same
arguments always produce the same `(RouteDecision, next curriculum
index)`), driven only by `outcome`, `rules_satisfied` (the router's own
read of `not evidence.missing_rules`), and the router's own repeated-error
count. Router authority means the router *decides using* State Machine
B's evidence, not that it ignores it: a `"correct"` outcome that didn't
demonstrate every target rule does **not** advance — it routes as
`REPEAT`/`REDUCE_DIFFICULTY`/`EXPLAIN` with its own distinct reason codes
(`correct_missing_rules_repeat`, etc.), same as an outright wrong answer.
`decide_next_route()`'s signature has no `confidence`/`metadata`/`evidence`
parameter at all, so an evidence object's advisory fields structurally
cannot influence the decision beyond `outcome` and `rules_satisfied`.
`DEFAULT_CURRICULUM` is demo *configuration* (a fixed sequence of
rule-target steps for `math/basic_equations`) kept separate from the
algorithm, exactly as Phase 1 kept domain constraints out of its core.

### The evidence handshake

`route_next()` takes **no evidence argument** — there is no parameter
through which a caller could substitute forged or stale evidence for what
State Machine B actually emitted. It reads
`self.evaluator_state.last_evidence` directly, requires
`evaluator_state.lifecycle_state == EMITTED` (raising
`IllegalEvaluationTransitionError` otherwise), and defensively checks the
evidence's `problem_id` against the active `task_state.current_problem_id`
(raising `StaleAttemptError` on mismatch, though this cannot happen via
the public API since `submit_attempt()` already checked the same match
before evaluating). Only after computing and applying its decision does
`route_next()` acknowledge B back to `IDLE` and resolve A back to `IDLE` —
so both state machines reach their clean boundary state together, and
only once the router has actually consumed the evidence that put them
there.

### Failure behavior

- A `RulePacket` Phase 1 rejects (`PacketRejectedError`) or fails to
  verify (`ProblemVerificationError`) propagates unchanged out of
  `RouterLoop.generate_problem()`, and `task_state` stays `IDLE` — an
  unverified problem is never assigned or presented.
- `submit_attempt()` validates the `LearnerAttempt` (`validate_attempt()`
  in `state_machine_b.py`) *before* any state mutation: a malformed
  outcome/`problem_id` raises `MalformedAttemptError`, and a
  `problem_id` that doesn't match the active cycle raises
  `StaleAttemptError` — in both cases `task_state`/`evaluator_state` are
  left exactly as they were, so the rejected attempt cannot mutate the
  active cycle.
- Calling a `RouterLoop` method out of turn (e.g. `generate_problem()`
  twice without completing the cycle) raises `IllegalTaskTransitionError`
  from State Machine A rather than silently continuing.

### Running the Phase 2 demo

```bash
python3 -m Learner_App.demo_phase2
```

Headless, no UI, no LLM/network calls. Drives a `RouterLoop` through a
correct attempt (`ADVANCE`), an incorrect attempt
(`REPEAT`/`REDUCE_DIFFICULTY`), and a repeated same-category incorrect
attempt (`EXPLAIN`) — printing the generated problem, evidence, and next
`RouteDecision` at each step. Running it twice produces byte-identical
output (same `base_seed`).

## Running the tests

From the repository root, Phase 1 and Phase 2 tests together:

```bash
python3 -m unittest discover -s Learner_App/tests -t . -p "test_*.py" -v
```

Python standard library only — no third-party dependencies. CI runs this
same command on every push/PR touching `Learner_App/**`
(`.github/workflows/learner-app-tests.yml`).

## Explicitly out of scope

Per issue #40 (Phase 1): no router implementation, no learner-state
logic, no flashcard system, no LLM/network calls anywhere in generation,
no UI.

Per issue #42 (Phase 2): no six-step flashcard/recursive recall system
(Phase 3), no UI, no LLM/network calls in the core loop. The router does
not build a generic workflow framework — `RouterLoop`/`policy.py` are
concrete and specific to proving this one loop, not a reusable
state-machine core with its own adapter contract.
