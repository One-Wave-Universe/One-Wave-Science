# Token Economy, Stubborn-AI Breaker, and Temporary Field/Void Fusion

## 1. Stubborn-AI breaker
The existing three-strike rule now has a novelty consequence. Three evidence-bearing failures that repeat the same approach, route family, or tool family force the next attempt to materially change that dimension.

Examples:
- MCP fails three times -> try pull bridge, SSH, or another independent route rather than a fourth MCP retry;
- one parser formulation fails three times -> change decomposition or adapter;
- one AI keeps returning the same limitation -> hand the same compact evidence packet to another worker or to Goblin Raccoon for route/tool discovery.

The breaker does not mean ignoring real security or capability boundaries. It means replacing repetitive failure with a different supported path.

## 2. Token economy
Do not replay the whole conversation/repo state between agents. Use one compact packet with only:

```text
goal
reference
known_good
delta since last pass
evidence / receipt
Void inner oversight
Field outer action/response
disagreement only if one exists
next move
protected items
token budget
```

Rules:
1. References are pointers/paths plus hashes when available, not pasted full files unless the worker actually needs the body.
2. Pass deltas, not complete histories.
3. Keep raw logs/receipts in files; pass only the relevant excerpt and receipt ID.
4. Reuse one canonical state packet across workers.
5. Summaries may compress navigation context, but never replace canonical receipts or exact project canon.
6. Fetch source text lazily: only the worker that needs a file reads it.
7. One worker speaks outward; the other supplies only the differential/oversight needed for that step.

## 3. Temporary Field/Void fusion
This is coordinated operation by two agents, not literal identity merger.

```text
              shared compact packet
                     |
             +-------+-------+
             |               |
        VOID inner       FIELD outer
        oversight        expression/action
             |               |
             +------> one outward result
                     |
                receipt/evidence
                     |
                  reference
```

Void runs first as the inner voice: constraints, risk, contradiction, missing evidence, and correction only. Field then receives that compact inner result and becomes the sole outward voice/action channel.

Field does not repeat Void verbatim. It integrates the oversight into one coherent outward move.

After the action returns evidence, both channels collapse back into the shared reference packet for the next cycle.

## 4. Fusion stop conditions
Break the temporary fusion and return to separate agents when:
- Field and Void disagree materially;
- the shared token budget is exceeded;
- either side needs a different tool/resource lane;
- three-strike novelty is triggered;
- the task reaches its hard stop;
- evidence is ambiguous enough to require independent review.

## 5. Goblin mapping
- Reference Goblin owns the compact canonical packet.
- Parser Goblin strips repeated/irrelevant context from action requests.
- Doctor Goblin records the actual failure evidence.
- Goblin Raccoon chooses a materially different route/tool after stubborn repetition.
- Carrier Pigeon transports only packet deltas and receipt IDs whenever possible.
- Worker Goblin performs the bounded action.
