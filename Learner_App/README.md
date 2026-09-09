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
packet target_rules=[EQ.ADD_INVERSE]                 -> "x + 17 = 40"
packet target_rules=[EQ.MUL_INVERSE]                 -> "7x = 35"
packet target_rules=[EQ.ADD_INVERSE, EQ.MUL_INVERSE] -> "7x + 1 = 36"
packet target_rules=[EQ.SUB_INVERSE, EQ.DIV_INVERSE] -> "x/7 - 1 = 33"
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
    test_math_basic_equations.py  # math adapter acceptance tests
    test_adapter_contract.py   # second-adapter proof + protocol compliance
    fixtures/
      trivial_echo_adapter.py  # tiny non-equation adapter, tests-only
```

## Running the tests

From the repository root:

```bash
python3 -m unittest discover -s Learner_App/tests -t . -p "test_*.py" -v
```

Python standard library only — no third-party dependencies.

## Explicitly out of scope for this PR

Per the issue: no router implementation, no learner-state logic, no
flashcard system, no LLM/network calls anywhere in generation, and no UI.
