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
