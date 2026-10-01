# Brain Buddy Conversation Continuity Contract

**Status:** Mandatory portable-session contract for Gemini, DeepSeek, ChatGPT bridges, and future Brain Buddy workers.

## Purpose

Brain Buddy must carry a conversation forward across workers and transports without pretending that a model has private memory it was never given.

The portable unit is a **Conversation Envelope**. It is runtime context, not project canon. Durable project decisions still belong once in the canonical repository.

## Conversation Envelope V1

Each session has a stable `session_id` and an append-only sequence of turns.

Required fields:

```json
{
  "schema": "BRAIN_BUDDY_CONVERSATION_V1",
  "session_id": "stable-id",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601",
  "repo": {
    "name": "One-Wave-Universe/One-Wave-Science",
    "ref": "exact commit or branch used",
    "authorities": ["exact canonical paths actually used"]
  },
  "goal": "current user goal",
  "decisions": [
    {"text": "decision", "source": "user|repo|worker", "status": "current|superseded"}
  ],
  "open_questions": ["unresolved question"],
  "constraints": ["active constraint"],
  "turns": [
    {
      "turn_id": 1,
      "speaker": "user|chatgpt|gemini|deepseek|future-worker",
      "text": "verbatim or bounded exact turn",
      "timestamp": "ISO-8601",
      "provenance": "chat|worker-return|repo-receipt"
    }
  ],
  "worker_state": {
    "gemini": {"last_success_receipt": null, "last_turn_id_seen": 0},
    "deepseek": {"last_success_receipt": null, "last_turn_id_seen": 0}
  }
}
```

Future workers add their own key under `worker_state`; the schema must not require code changes merely to recognize a new worker name.

## Context assembly order

Every worker invocation receives context in this order:

1. General repo reference contract.
2. Exact canonical repo authorities for the task.
3. Session goal.
4. Current decisions and constraints.
5. Open questions.
6. Conversation turns the worker has not yet seen, plus enough prior turns to resolve references.
7. Latest peer responses relevant to the current question.
8. Current user request.

Repository authority and conversation state must remain visibly separate.

## Carry-forward rule

After every successful worker return:

1. append the returned text as a new turn;
2. record the exact worker and receipt;
3. advance only that worker's `last_turn_id_seen`;
4. preserve unresolved disagreements;
5. update decisions only when the user or canonical repo actually changes them;
6. write the envelope atomically.

A failed transport may append a transport receipt to logs, but MUST NOT append invented model dialogue.

## Compression rule

Long sessions may be compacted, but compaction may not silently erase decisions, constraints, disagreements, provenance, or open questions.

A compacted state contains:
- immutable/raw transcript reference;
- bounded recent verbatim turns;
- explicit current decisions;
- explicit superseded decisions;
- open questions;
- worker receipts and last-seen cursors;
- canonical repo paths/ref.

A summary is a cache. It is never allowed to outrank the raw receipt or canonical repo.

## No-assumption rules

Never assume:
- a worker remembers a previous Brain Buddy call;
- two workers share hidden context;
- a future worker understands Gemini/DeepSeek-specific formatting;
- the latest response resolved an earlier disagreement;
- conversation text changed repo canon;
- a repo update automatically changed the conversation envelope;
- a transport receipt is a model turn.

If context is missing, label the missing range and recover it from the session transcript/receipt before answering.

## Future-worker interface

A worker adapter needs only:

```text
worker_id
capabilities
invoke(context_packet) -> returned_text + execution_receipt
```

The orchestrator owns continuity. Workers do not own the conversation.

This allows later local models, specialist agents, simulators, research workers, or hardware-control workers to join the same session while receiving only the bounded context they need.

## Privacy / secrets gate

Conversation envelopes must not commit credentials, API keys, passwords, private tokens, or unnecessary personal information to git.

Persistent session files containing private conversation text belong in runtime state excluded from git. Git stores the schema, code, tests, and non-sensitive example fixtures only.

## Required test

A continuity implementation is not complete until this passes:

1. User gives fact/constraint A to worker 1.
2. Worker 1 returns response B.
3. User adds correction C.
4. Worker 2 is invoked for the first time.
5. Worker 2 must receive A, B, C, the canonical repo references, and their provenance.
6. Worker 2 must identify C as newer than A where they conflict.
7. Restart the orchestrator.
8. Invoke a future/mock worker.
9. The mock worker must receive the same current decisions/open questions without relying on process memory.

PASS requires receipts proving all nine steps.

## Final law

**Conversation continuity belongs to the Brain Buddy session layer; truth belongs to the canonical repo; evidence belongs to receipts. Keep all three linked and never collapse them into one another.**
