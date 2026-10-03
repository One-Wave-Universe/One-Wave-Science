# Brain Buddy Council

## Identity — do not reinterpret

Brain Buddy is the three-AI loop:

```text
Mark = human operator
ChatGPT = origin / return AI
Gemini = peer AI
DeepSeek = peer AI

ChatGPT -> Council -> Gemini <-> DeepSeek -> ChatGPT
```

The Council script orchestrates Gemini and DeepSeek because ChatGPT is the originating/returning AI outside the local worker process. Do not miscount Mark as an AI and do not misdescribe the Python process as the whole three-AI system.

That fixed ChatGPT origin applies to the legacy modes below. In **lead mode** there is no fixed owner: whichever seat the user asked is the lead seat for that request (`BRAIN_BUDDY_CANONICAL_RULES.md` rule 3).

Canonical implementation is `scripts/brain_buddy_council.py`. The Gemini and DeepSeek wrappers are transports/workers, not competing Brain Buddy versions.

## Modes

### Gemini only

```bash
bash scripts/brain_buddy_council.sh gemini "question"
```

### DeepSeek only

```bash
bash scripts/brain_buddy_council.sh deepseek "question"
```

### Both independently

Runs Gemini and DeepSeek in parallel against the same bounded question.

```bash
bash scripts/brain_buddy_council.sh both "question"
```

Use this when you want two independent reviews before either sees the other answer.

### Gemini then DeepSeek

Gemini answers first. DeepSeek then receives the original question plus Gemini's answer and is instructed to check it against the repo, call out disagreements, and give its own answer.

```bash
bash scripts/brain_buddy_council.sh gemini-deepseek "question"
```

### DeepSeek then Gemini

```bash
bash scripts/brain_buddy_council.sh deepseek-gemini "question"
```

Same handoff in the opposite direction.

### Three-way open discussion

Participants:

- user;
- Gemini;
- DeepSeek.

```bash
bash scripts/brain_buddy_council.sh discussion "question" --rounds 3
```

When run in an interactive terminal, after each Gemini + DeepSeek round the user can:

- type a reply or redirection;
- press Enter and let them continue;
- type `/stop` to end the discussion.

Each model sees the previous discussion turns on its next turn.

The peers are not forced to agree. They are explicitly allowed to preserve disagreements and identify the next test needed to resolve them.

### Lead seat (Rule 50 core)

The seat the user asked leads. It answers from the repo, the other seat reviews, and the lead refines while a material objection is active.

```bash
bash scripts/brain_buddy_council.sh lead --seat gemini "question"
bash scripts/brain_buddy_council.sh lead --seat deepseek "question"
```

Loop:

```text
lead answer (repo first)
→ reviewer(s): VERDICT: OBJECTION | VERDICT: NO MATERIAL OBJECTION
→ while an objection is active: lead refinement → review again
→ return to user
```

There is no fixed round count. The loop returns with one of these outcomes:

| Outcome | Meaning |
| --- | --- |
| `NO_ACTIVE_OBJECTION` | every responding reviewer returned `VERDICT: NO MATERIAL OBJECTION` |
| `STALLED_UNRESOLVED` | the same objection came back unchanged, or the lead's refinement did not change; disagreement is shown |
| `NO_REVIEWERS_AVAILABLE` | no reviewer returned a real, verified response; the answer is unreviewed |
| `LEAD_UNAVAILABLE` | the lead did not return a real, verified response |
| `USER_STOPPED` | the user typed `/stop` at a checkpoint (interactive terminal only) |
| `OPERATOR_LIMIT_UNRESOLVED` | the optional `--max-loops` budget was reached with objections still open |

A missing or unparseable verdict counts as unresolved. Agreement is never assumed.

`--timeout` is a **transport** timeout per provider call. Hitting it marks that provider `OUT TO LUNCH`; it never completes the deliberation. `--max-loops` is an optional operator budget for non-interactive callers; reaching it is recorded as unresolved, not agreement.

Provider states are shown as `[STATE] seat: STATE — reason` and recorded in the receipt:

```text
LISTENING · PENDING · ACTIVE · OUT TO LUNCH · OFFLINE · AUTH FAILURE · INVALID RETURN
```

Failure mapping: no transport response, quota/rate limit, or other bridge failure → `OUT TO LUNCH`; relay unreachable → `OFFLINE`; 401/403 or missing token/key → `AUTH FAILURE`; malformed relay response, empty reply, or a reply that does not carry its turn's `RETURN_ID` → `INVALID RETURN`.

Return-path check: every prompt carries `REQUEST_ID`, `BASELINE` (repo `HEAD`), and a fresh per-turn `RETURN_ID` that the provider must echo. A reply without its own `RETURN_ID` is not counted as participation.

Lead mode always writes a compact JSON receipt to `External_Work/brain_buddy/outbox/<request_id>.json`: request ID, baseline, lead, every turn with seat, kind, state, exit code, elapsed time, return-ID verification, and response hash/text, plus the outcome and any open objections. A receipt proves execution, not correctness.

Currently callable seats: Gemini and DeepSeek. ChatGPT and Claude adapters are later work.

Deterministic tests (orchestration only; they do not prove a live return path):

```bash
python3 -m unittest scripts/test_brain_buddy_council.py
```

## Interactive menu

Running without arguments opens the menu:

```bash
bash scripts/brain_buddy_council.sh
```

The menu offers:

1. Gemini only
2. DeepSeek only
3. both independently
4. Gemini then DeepSeek
5. DeepSeek then Gemini
6. open three-way discussion
7. lead seat

## Reference contract

Every Council task carries the common reference contract:

```text
GENERAL_REFERENCE_RULES.md
    ↓
AI_CANONICAL_START_HERE.md
    ↓
I-06 metadata authority
    ↓
task-specific files
    ↓
worker answer
    ↓
validate
    ↓
return to reference
```

DeepSeek still uses its free web relay + Hive Pipe.

Gemini still uses the bounded Gemini CLI wrapper.

Council itself does not create another repository checkout, source canon, or model credential store.

## Discussion behavior

The discussion transcript is deliberately cumulative.

A worker receives:

- the original user question;
- canonical reference rules;
- prior user turns;
- prior Gemini turns;
- prior DeepSeek turns.

Each new worker turn is asked to address the peer's strongest point rather than merely restating its own answer.

Useful turn endings are:

```text
AGREEMENT: ...
DISAGREEMENT: ...
OPEN QUESTION: ...
```

This makes unresolved claims visible instead of hiding them inside a blended answer.

## Save a discussion receipt

By default Council prints responses but does not create a persistent transcript.

To deliberately save a receipt:

```bash
bash scripts/brain_buddy_council.sh discussion "question" --rounds 2 --save
```

The receipt is written under:

```text
External_Work/brain_buddy/outbox/
```

This is runtime/output evidence, not a second canonical source.

## Examples

Two independent science reviews:

```bash
bash scripts/brain_buddy_council.sh both \
  "Compare the falsifiability of Nodes/E-533_Superfluid_Transport_Time_Dilation.md and Nodes/C-309_Friction_Limit.md."
```

DeepSeek proposes, Gemini checks:

```bash
bash scripts/brain_buddy_council.sh deepseek-gemini \
  "What is the smallest mathematical attack on the time-dilation transport hypothesis?"
```

Open discussion:

```bash
bash scripts/brain_buddy_council.sh discussion \
  "Can the current One-Wave time-dilation transport claim be made quantitatively falsifiable without new experimental data?" \
  --rounds 3
```

## Hard boundaries

Council must not:

- treat either model as canonical authority;
- call agreement proof;
- hide disagreement by averaging answers;
- let one model's answer silently become the other model's reference source;
- bypass the repo-first reference contract;
- merge model edits automatically;
- expose credentials;
- fabricate receipts.

The user remains the controlling participant. The repository remains the reference authority.
