# Goblin Bridge Roles

These goblins are modular control roles for the bridge mesh. They are helpers around authenticated routes; none may bypass credentials, parser restrictions, reference gates, or receipt requirements.

## Doctor Goblin
Diagnoses what actually failed: service, authentication, target receipt, route health, or configuration. It repairs known user-level services and then re-runs the same probe. It never treats a running process as proof of a live target.

## Parser Goblin
Normalizes the requested action into the bounded parser contract. It rejects malformed actions before execution and sends a normalized request to the Reference state.

## Reference Goblin
Fail-closed gate. It requires source, target, direction, reference, intention, and consequence. Missing fields produce `HOLD`. It owns the original immutable receipt ledger.

## Reference / Worker Goblins — two-state machine

```text
REFERENCE --approved--> WORKER
REFERENCE <--receipt--- WORKER
```

REFERENCE establishes the known state and authorizes exactly one bounded movement. WORKER performs it. WORKER may not self-certify success; it must return a matching receipt to REFERENCE. No receipt means the machine remains in WORKER_HOLD and Doctor Goblin diagnoses the path.

## Carrier Pigeon Goblin
Carries request envelopes and receipts between machines/routes. Every envelope has a message ID, source, target, direction, and selected route. A sent message without its matching return receipt stays `IN_FLIGHT`, never `DONE`.

## Goblin Raccoon
Scout/adapter strategist. When a route repeatedly fails, Raccoon looks for an independent configured route family with usable evidence. If one exists it proposes a probe. If none exists it proposes a bounded adapter/setup task. Its job is to find clever safe paths, not to bypass authentication or fabricate access.

## Cooperation loop

```text
Reference Goblin
  -> Parser Goblin
  -> Reference state
  -> Worker state
  -> Carrier Pigeon
  -> target
  -> return receipt
  -> Doctor Goblin
  -> route memory
  -> Goblin Raccoon when degraded
  -> alternate route probe
  -> Reference Goblin
```

## Three-strike behavior
After three evidence-bearing failures on the same route family, Raccoon must prefer a materially different family. The failed path remains in memory with a lower weight and may recover later after Doctor Goblin proves it healthy again.

## Rule posting
This role map must be linked from every canonical bridge entry point and from the browser reference-gate help panel.
