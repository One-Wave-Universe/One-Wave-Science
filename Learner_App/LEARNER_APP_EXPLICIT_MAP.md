# Learner App — Explicit System Map

This file is the detailed operating map for the Learner App. It describes what each part owns, how information moves, how lessons are structured, how rules are stored, how problems are generated, how attempts are evaluated, how recall is kept separate from concept teaching, and how the system must respond when the learner is confused.

The central requirement is simple:

> The learner must understand why a move is legal before the app compresses that move into shorthand.

The app is not allowed to substitute repetition, vocabulary, or symbolic manipulation for understanding.

---

## 1. Primary teaching contract

The learner is taught in this order:

```text
concrete situation
    -> what is actually true
    -> what is being asked
    -> what parts match
    -> what part differs
    -> one legal move
    -> why that move is legal
    -> visible result
    -> verify the relationship still holds
    -> only then compress into mathematical shorthand
```

A technically correct explanation is still considered a bad lesson if it skips the causal structure and jumps directly to a rule name or symbolic shortcut.

### Required learner-facing questions

Every new rule should make it possible for the learner to answer:

1. What is happening?
2. What am I trying to find?
3. Which parts match?
4. Which part is extra or different?
5. What single move can I make?
6. Why is that move allowed?
7. What changed?
8. What stayed true?
9. How can I check that I did not break the relationship?
10. When would this rule *not* apply?

---

## 2. Hard separation: understanding vs recall

The Learner App contains two different learning mechanisms. They must not be mixed together.

### A. Math logic learner

Purpose:

```text
build understanding
explain structure
teach legal moves
connect cause to procedure
diagnose conceptual gaps
```

This is where algebra rules, examples, explanations, and reasoning live.

### B. Recall / flash-card worker

Purpose:

```text
recall
repetition
speed
automatic retrieval of facts already understood
```

The recall worker must never be used to force memorization of a concept the learner does not understand.

A concept lesson must work correctly even if the recall worker is completely disabled.

Do not place flash-card cadence, six-step recall scheduling, multiplication-table recursion, or recall timing inside curriculum rule definitions.

---

## 3. Top-level architecture

The current architecture is:

```text
                    +---------------------+
                    |   CURRICULUM MAP    |
                    | rules + prerequisites|
                    +----------+----------+
                               |
                               v
+----------------+     +-------+--------+      +----------------+
| Learner State  |<--->|   ROUTER LOOP  |<---->| Recall Worker  |
| State Machine A|     |  sole sequencer |      | spaced recall  |
+----------------+     +-------+--------+      +----------------+
                               |
                  +------------+-------------+
                  |                          |
                  v                          v
        +-------------------+      +-------------------+
        | Problem Builder   |      | Explanation /    |
        | generic core      |      | Teaching Content |
        +---------+---------+      +-------------------+
                  |
                  v
        +-------------------+
        | Domain Adapter    |
        | math/basic_eqs    |
        +---------+---------+
                  |
                  v
        +-------------------+
        | Generated Problem |
        | no answer field   |
        +---------+---------+
                  |
                  v
        +-------------------+
        | Learner Attempt   |
        +---------+---------+
                  |
                  v
        +-------------------+
        | Evaluator         |
        | State Machine B   |
        +---------+---------+
                  |
                  v
        +-------------------+
        | Evidence          |
        +---------+---------+
                  |
                  +-----------> Router decides next action
```

There are exactly two lifecycle state machines in the current design.

The Router Loop is the orchestrator. It is not a third state machine.

---

## 4. State Machine A — learner/task lifecycle

Canonical lifecycle:

```text
IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING -> IDLE
```

### IDLE

No active problem.

Allowed next action:

```text
assign verified problem
```

### PRIMED

A verified problem has been assigned but not yet presented.

Allowed next action:

```text
present problem to learner
```

### EXECUTING

The learner is actively working the problem.

Allowed next action:

```text
receive learner attempt
```

### VECTORING

The learner attempt has been received and evaluation/routing information is available.

Allowed next action:

```text
apply router decision
```

### RESOLVING

The cycle is being closed cleanly.

Allowed next action:

```text
resolve -> IDLE
```

Illegal transitions must fail loudly rather than silently skipping lifecycle stages.

---

## 5. State Machine B — evaluation lifecycle

Evaluation lifecycle:

```text
IDLE -> EVALUATING -> EMITTED -> IDLE
```

Its job is to produce structured evidence about the learner attempt.

It does not own curriculum progression.

It does not own lesson selection.

It does not override the router.

It must preserve the difference between:

- final answer correctness
- whether the target rule was actually demonstrated
- missing rule usage
- incomplete reasoning
- repeated conceptual error category

A correct answer that bypasses the target reasoning is not automatically mastery of that rule.

---

## 6. Router Loop — sole sequencing authority

The router owns:

- current curriculum position
- active target rule(s)
- prerequisites
- allowed support rules
- forbidden rules
- difficulty
- repeated error tracking
- whether to repeat, simplify, explain, advance, or inject due recall
- domain selection
- problem seed

The router must not invent explanations itself.

The router decides *what kind of teaching action happens next*.

### Core routing outcomes

```text
ADVANCE
REPEAT
REDUCE_DIFFICULTY
EXPLAIN
REVIEW / RECALL when due and compatible
```

### Required behavior

If the learner is correct and demonstrates all target rules:

```text
advance
```

If the learner is incorrect once:

```text
repeat or reduce difficulty
```

If the learner repeats the same conceptual error:

```text
explain the missing logic from another angle
```

After repeated failure of the same explanation style, switch angle rather than repeating the same wording.

---

## 7. Canonical rule definition

Every rule must live as a canonical object or canonical content definition referenced by:

- curriculum
- generator
- explanation layer
- answer/evidence checker
- problem rule links
- recall worker

The same rule must not be redefined independently in several places.

### Required rule fields

Each rule should eventually expose at least:

```text
rule_id
name
plain_language_rule
trigger
purpose
legal_move
why_valid
what_changes
what_stays_true
verification_method
when_not_to_use
prerequisites
allowed_support_rules
forbidden_shortcuts
worked_examples
non_examples
error_patterns
explanation_variants
```

### Required learner-facing form

Every rule must be explainable as:

```text
IF this situation is present
THEN make this move
BECAUSE this relationship makes the move valid
DO NOT use it when these conditions are absent
```

No rule may be only a label such as "subtract both sides" or "cancel terms."

---

## 8. Rule-book identity

Rule-book heading:

> **Rules are rules… cause we’re fucking tools!**

The rule book is not ordered only from easiest to hardest.

Rules must also be grouped by rules that are commonly used together.

The learner should repeatedly encounter earlier rules inside later problems so old logic remains active while new logic is added.

---

## 9. First rule sequence

### Rule 001 — equality / same-value truth

The learner must first understand that:

```text
left side = right side
```

means both expressions currently claim the same value.

The equal sign is not an instruction to calculate. It is a relationship claim.

The learner should be encouraged to check whether that claim is true.

### Rule 002 / first taught move — Balanced Change

Plain form:

> If two sides are equal, doing the same valid operation to the whole left side and the whole right side keeps them equal.

Trigger:

```text
two sides are equal
AND an attached amount is hiding the target
```

Move:

```text
apply the matching inverse operation to both complete sides
```

Reason:

```text
the relationship is preserved because both equal values changed in the same way
```

Forbidden shortcut during first learning:

```text
"move it across"
"flip the sign"
"just cancel it"
```

Those phrases may only appear after the learner can explain the underlying transformation.

---

## 10. Lesson object

A lesson is not just a problem list.

Each lesson should contain:

```text
lesson_id
primary_rule_id
prerequisite_rule_ids
teaching_goal
concrete_setup
truth_statement
goal_statement
structure_identification
one legal move
reason for move
visible result
verification step
compressed shorthand
boundary / non-example
build-up problems
lock-down problems
error-specific explanation routes
completion criteria
```

### Required teaching shape

```text
1. Situation
2. Truth
3. Goal
4. Structure
5. Legal move
6. Reason
7. Visible result
8. Verification
9. Compression
10. Boundary
```

---

## 11. Build-up problems vs lock-down problems

These are lesson practice, not flash cards.

### Build-up problems

Purpose:

```text
construct understanding
```

The app may show more of the reasoning path.

For a new rule, begin with approximately three build-up problems.

Each build-up problem should remove one layer of support as understanding increases.

Example progression:

```text
Problem 1: identify matching structure + choose move with guidance
Problem 2: learner chooses move, explanation still available
Problem 3: learner performs move and verifies relationship
```

### Lock-down problems

Purpose:

```text
prove the learner can independently recognize and use the rule
```

Approximately three initial lock-down problems.

The app should not reveal the current answer.

It may link to the relevant canonical rule and unrelated worked examples.

If the learner is not moving smoothly through the lock-down set, the app should not simply mark the lesson complete.

---

## 12. Problem generator

The problem generator receives a `RulePacket` from the router.

It does not choose curriculum.

It does not decide what the learner should study.

It only generates a problem satisfying the router's exact constraints.

Current generic pipeline:

```text
RulePacket
 -> reject contradictory target/forbidden rule request
 -> resolve domain adapter
 -> validate packet
 -> generate text candidate using seeded RNG
 -> independently parse generated text
 -> inspect rules actually present
 -> validate structure
 -> generic verification
 -> return GeneratedProblem only if verified
```

### Generator hard rules

- same packet + same seed = same generated artifact
- generated problem must demonstrate every requested target rule
- generated problem must contain no forbidden rule
- generated problem must contain no undeclared extra rule
- generator must not leak the answer
- the generated text must be independently reparsed rather than trusted
- if constraints are impossible, reject the packet instead of silently widening them

---

## 13. Domain adapters

The generic problem-building core must remain domain-agnostic.

Math knowledge belongs in math adapters.

Future adapters may include:

```text
math/basic_equations
math/fractions
math/decimals
math/ratios
math/geometry
coding/basic_logic
coding/control_flow
physics/basic_measurement
```

Adding a new domain must not require rewriting the generic core.

The existing second test adapter that generates plain words remains the proof that the core is not secretly algebra-specific.

---

## 14. Current math/basic_equations scope

Current rule families supported by the v1 adapter include:

```text
EQ.IDENTITY
EQ.ADD_INVERSE
EQ.SUB_INVERSE
EQ.MUL_INVERSE
EQ.DIV_INVERSE
```

Initial forms include:

```text
x = c
x + b = c
x - b = c
a*x = c
x/a = c
```

Some two-rule combinations are supported.

The adapter intentionally does not yet handle everything.

Unsupported forms should fail clearly rather than being approximated.

Examples currently out of scope include:

- variables on both sides
- parentheses
- exponents
- negative-number grammar
- non-integer coefficients
- multiple variables
- multiple occurrences of the unknown

These should be added only when the teaching rules for them are explicit.

---

## 15. Problem presentation

A generated problem shown to the learner should include:

```text
problem statement
rule reference link(s)
optional request for one next move
optional request for explanation
space for learner work
check / submit control
```

It must not include:

```text
hidden solved x exposed in metadata
answer-shaped hint
shortcut that bypasses the target rule
unrequested advanced vocabulary
```

The learner should normally make one transformation at a time.

---

## 16. Attempt format

A learner attempt should eventually be able to record separately:

```text
problem_id
written next line / transformation
reported rule used
learner explanation
final answer if the lesson stage asks for it
confidence / "I guessed" flag if useful
request for rule help
```

Do not collapse all of this into only `correct/incorrect`.

The app needs to know whether the learner understood the move or merely landed on the right number.

---

## 17. Error diagnosis

Errors should be classified by missing logic whenever possible.

Examples:

```text
misread equality
changed only one side
changed only one term instead of the whole side
used wrong inverse
invented an unexplained number
combined unlike terms
failed to recognize a matched pair
did not understand coefficient meaning
performed a memorized shortcut but cannot explain why
arithmetic slip after correct structural move
```

An arithmetic slip and a conceptual mistake are not the same event and should not route to the same remediation.

### Three-repeat rule

If the same explanation style fails approximately three times:

```text
stop repeating it
switch the framing
```

Possible alternate framings:

- concrete objects
- matching baggage
- side-by-side comparison
- split a larger group into shared + extra
- diagram
- number-only example
- verbal description before symbols

---

## 18. Language policy

Prefer language such as:

```text
same value
matching part
extra part
attached to
remove the matched pair
split this so we can see what is shared
expose the unknown
this number came from...
this changed
this stayed true
check that both sides still match
```

Avoid introducing unexplained phrases such as:

```text
move it across
flip the sign
just cancel
obviously
simply
coefficient
factor it
normalize it
```

Technical vocabulary should be introduced only after the learner already understands the structure the word names.

---

## 19. Matched-pair / comparison logic

A major future rule family is comparison by shared structure.

Example conceptual decomposition:

```text
6c = 4c + 2c
```

The learner should first see:

```text
both expressions contain the same 4c part
one side has 2c extra
```

Only after that should notation compress the operation into subtraction/cancellation.

Learner-facing phrase that should remain available:

> They had the same thing in them -> compare and remove matched pairs.

---

## 20. "When in trouble, double the double"

This mnemonic belongs to the rule system only when the underlying condition is explicit.

It is not permission to multiply an equation randomly.

The lesson must explain:

```text
what matching group is being created
why doubling the whole equation preserves its truth
why that particular multiplier was chosen
what becomes comparable afterward
```

The number used in an operation may never appear as magic.

Every number introduced by a transformation must have an origin.

---

## 21. Recall worker

The recall worker maintains previously learned rule availability over time.

It is a worker under router authority.

It is not a curriculum planner and not a third state machine.

Its records include concepts such as:

```text
times_seen
times_correct
times_missed
current_recall_step
next_due_cycle
success_streak
error_streak
direction
```

Recall may be injected only when compatible with the active curriculum problem.

A due recall rule must not replace the curriculum's current target.

If the combination cannot be generated cleanly, skip that recall opportunity rather than corrupting the lesson.

---

## 22. Six-step recall system

The six-step recursive recall system belongs here, not in the concept curriculum files.

General behavior:

```text
new mastered item -> recall step 1
successful recall -> move farther out
miss -> move closer
continue through six steps
when appropriate, schedule a real inverse/reverse relationship
```

For arithmetic-fact practice, the separate flash-card subsystem may later use the user's intended six-up / six-down multiplication-and-division structure.

That repetition system must only operate on facts or rules already understood.

---

## 23. Curriculum progression

Curriculum should behave more like progressive skill practice than a chapter dump.

Principle:

> Keep the active challenge just above demonstrated skill, while continuing to reuse earlier skills.

This is similar to practicing a guitar riff that is slightly beyond current ability rather than repeatedly playing only mastered material.

Progression should therefore:

```text
introduce one new structural idea
reuse older rules inside it
vary surface form
increase independence
mix old + new only when both are valid together
back up when prerequisite logic is missing
```

Do not advance merely because a fixed number of questions was completed.

---

## 24. Difficulty is multidimensional

Do not represent difficulty only as bigger numbers.

Difficulty can increase through:

```text
less scaffolding
more irrelevant surface information
more than one known rule
rules used in a different order
larger arithmetic values
new representation
word problem translation
shared terms
unknown placement
need to choose among multiple legal rules
```

The router should eventually distinguish these dimensions.

---

## 25. Word problems

Word problems should exist because translating a real situation into structure is useful, not because traditional worksheets use them.

Use ordinary situations a person can visualize:

```text
groceries
bags
music gear
travel distance
building materials
money
shared objects
containers
```

Avoid endless artificial scale puzzles or absurd stories that distract from the mathematical structure.

The word problem should map cleanly back to the canonical rule.

---

## 26. Rule links from problems

Every generated learner problem should expose which canonical rules are relevant through help/reference links.

A rule link may show:

```text
rule definition
when to use it
why it works
worked example using different numbers
non-example
```

It must not reveal the solution to the current problem.

---

## 27. Explanation worker / future coach layer

A future explanation worker may generate or select explanation variants, but it must remain constrained by canonical rule definitions.

It may change:

```text
analogy
wording
example
visualization
order of supporting explanation
```

It may not change:

```text
what makes the rule valid
when the rule applies
what operation is legal
prerequisite structure
canonical rule ID
```

Free-form AI tutoring must never become a second unofficial curriculum that drifts away from the rule system.

---

## 28. Answer checking

The original problem builder deliberately contains no answer field.

A future authorized checker should independently evaluate learner work rather than exposing generator secrets.

The checker should ideally distinguish:

```text
valid next transformation
invalid transformation
correct arithmetic with wrong rule
correct rule with arithmetic slip
final answer correct
target reasoning demonstrated
target reasoning missing
```

This information feeds State Machine B as evidence.

The checker does not choose the next curriculum action; the router does.

---

## 29. UI map

A minimal usable lesson screen should eventually contain:

```text
+------------------------------------------------+
| Current skill / rule                           |
| short plain-language purpose                   |
+------------------------------------------------+
| Problem                                        |
|                                                |
| learner workspace                              |
|                                                |
+------------------------------------------------+
| [Rule help] [Example] [I don't understand]     |
+------------------------------------------------+
| Next move / explanation input                  |
| [Check]                                        |
+------------------------------------------------+
| Feedback                                       |
| what was right                                 |
| what broke                                     |
| why                                            |
| next action                                    |
+------------------------------------------------+
```

Do not clutter the first screen with every subsystem, score, recall statistic, or curriculum graph.

Understanding the current move has priority.

---

## 30. "I don't understand" path

This must be a first-class path, not an error state.

When selected:

```text
1. stop progression
2. identify current rule
3. identify prerequisite concept most likely missing
4. explain from concrete structure
5. ask one recognition question
6. make one move together
7. verify it
8. return to a fresh problem using the same rule
```

Do not respond with the same explanation repeated verbatim.

---

## 31. Session state

A learner session should eventually preserve at least:

```text
current curriculum location
active rule(s)
mastered rule set
rules in progress
recent error categories
explanation variants already tried
recall records
recent problem IDs
recent seeds
recent outcomes
```

The system should be able to reconstruct the next teaching decision from explicit state rather than hidden model memory.

---

## 32. Persistence

Current core can remain deterministic and local.

Persistence can initially be simple JSON or another transparent local format.

The learner should be able to stop and resume without changing curriculum state unexpectedly.

Persisted state must be versioned so curriculum/rule changes do not silently corrupt old sessions.

---

## 33. Determinism and reproducibility

When debugging the learner, it must be possible to reproduce a problem and route exactly.

Record:

```text
packet_id
seed
rule IDs
constraints
curriculum index
attempt evidence
route decision
```

Given the same starting state and same learner attempts, a deterministic run should produce the same problem sequence and decisions.

---

## 34. Drift prevention

The most important architectural anti-drift rule is:

> Generator, explanations, checker, router, and recall worker must reference the same canonical rule IDs and definitions.

No component may invent a private interpretation of a rule.

When a rule changes, dependent tests should fail until every affected component is reconciled.

---

## 35. Testing map

Tests should exist at several levels.

### Rule tests

Verify:

```text
trigger
legal move
non-example
prerequisite links
```

### Generator tests

Verify:

```text
requested rule present
forbidden rules absent
no unapproved extra rule
deterministic seeds
independent reparse
no answer leak
```

### Router tests

Verify:

```text
correct -> advance
incorrect -> repeat/reduce
repeated conceptual error -> explain
missing target reasoning blocks advance
recall cannot override curriculum
```

### Lesson tests

Verify:

```text
build-up order
lock-down independence
rule links do not leak answer
unsupported vocabulary absent before introduction
```

### End-to-end acceptance

A first usable acceptance path should be:

```text
start app
-> Rule 1 explanation
-> build-up problem 1
-> build-up problem 2
-> build-up problem 3
-> lock-down 1
-> lock-down 2
-> lock-down 3
-> deliberately make one conceptual error
-> receive the correct alternate explanation
-> complete a fresh problem
-> close app
-> reopen
-> continue from correct state
```

---

## 36. Current implementation status

Already implemented or represented in the repository:

- reusable deterministic problem-builder core
- independent generate -> parse -> verify path
- math/basic_equations adapter
- explicit target/allowed/forbidden rule verification
- no-answer generated-problem contract
- State Machine A learner/task lifecycle
- State Machine B evaluator lifecycle
- deterministic Router Loop
- repeated-error route behavior
- six-step Recall Worker under Router authority
- rough curriculum rules 001–002
- learning-style / teaching contract
- Rule 1 Balanced Change lesson branch
- Rule 1 headless demo
- first Rule 1 web card
- Rule 1 lesson tests

Not yet complete:

- full explanation/coach worker
- independent answer checker with transformation-level diagnosis
- persistent learner profile/session storage
- polished unified UI
- complete canonical rule schema in machine-readable form
- expanded algebra curriculum
- coefficients/shared-term lesson family
- word-problem translation layer
- full arithmetic-fact flash-card UI
- learner-facing progress map

---

## 37. Immediate build order

Do not expand sideways until the first lesson loop is genuinely usable.

Recommended order:

```text
1. Stabilize Rule 1 wording and rule ID.
2. Make Rule 1 web lesson follow the required teaching shape.
3. Add explicit "I don't understand" alternate explanation path.
4. Add transformation-level checking for Rule 1 only.
5. Run the complete six-problem Rule 1 acceptance path.
6. Persist completion/session state.
7. Only then add the next rule.
8. Build shared-term / matched-pair logic before coefficient shorthand.
9. Expand generator combinations only when their teaching rules exist.
10. Keep recall subsystem separate and inject it only after understanding.
```

---

## 38. Definition of success

The learner app is succeeding when the learner can say:

```text
I see what is happening.
I know what I am trying to find.
I know which parts matter.
I know why this move is allowed.
I know what changed.
I know what stayed true.
I can check whether I broke the relationship.
I can recognize when this rule applies again.
```

Speed comes after that.

The target is not to get the learner through a lesson.

The target is to make the logic so clear that the learner can carry it into the next one.
