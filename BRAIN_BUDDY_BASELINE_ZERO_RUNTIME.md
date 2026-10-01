# Brain Buddy Baseline-Zero Runtime — branch contract

Branch: `brain-buddy-baseline-zero-runtime`

## Goal

Preserve the successful Gemini + DeepSeek Brain Buddy back-and-forth and add one capability: each AI controls an explicit oversight loop that automatically re-references the current project state before deciding whether to act.

The larger target is multiple AIs that can explore ideas and science, program together, validate one another, and prepare repository updates while each controls its own loop. This branch does not replace the working dialogue transport.

## Runtime path

```text
                         BASELINE ZERO
                 live repo / goal / situation
                              |
                              v
AI turn request ------> VOID OVERSIGHT
                        watch + assess
                         /        \
                      HOLD        ACT
                       |           |
                       |           v
                       |       FIELD LOOP
                       |    talk/research/code
                       |           |
                       +---- result/feedback
                              |
                              v
                     next Baseline-Zero refresh
```

Every AI owns this cycle independently. Baseline Zero is shared reference; it is not a master AI.

## Baseline Zero

It is refreshed from the live checkout immediately before an oversight pass and currently includes:

- repository identity;
- current branch;
- current commit;
- working-tree state;
- recent commits;
- `AI_FOREMAN_WORK_REGISTER.md`;
- `AI_CANONICAL_START_HERE.md`;
- `GENERAL_REFERENCE_RULES.md`.

Task-specific governed nodes and I-06 metadata remain part of the existing repo-first worker contract.

## Void oversight

Void is an explicit, inspectable operational state. It is not hidden chain-of-thought.

It watches the Field task for goal drift, contradiction, stale reference, failure, completion, and other state changes. It emits only:

```text
STATE: ACT | HOLD
REASON: concise operational reason
WATCH: condition being watched
NEXT: one next action
```

HOLD stops that worker turn. ACT hands one action to the existing Field worker.

## Field

Field remains the existing Brain Buddy worker path. Gemini and DeepSeek transports are not rewritten here. The outward worker receives the freshly captured Baseline Zero plus the Void handoff and then uses the existing repo-first reference/research contract.

## Non-goals for this checkpoint

- no new council transport;
- no replacement of the successful back-and-forth;
- no hidden chain-of-thought capture;
- no automatic merge to main;
- no claim that AI agreement proves science;
- no autonomous repo write path yet.

## First checkpoint test

A successful checkpoint must show, for both Gemini and DeepSeek:

1. Baseline Zero reflects the branch and current commit.
2. Void returns a parseable ACT or HOLD.
3. HOLD prevents the Field call.
4. ACT reaches the existing Field call.
5. The next turn refreshes Baseline Zero rather than reusing a stale snapshot.
6. Existing discussion/back-and-forth behavior still works.

Only after this checkpoint passes should the next substantial capability move to another branch.
