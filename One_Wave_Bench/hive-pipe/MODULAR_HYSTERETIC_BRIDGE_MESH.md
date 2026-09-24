# One-Wave Modular Hysteretic Bridge Mesh

## Purpose
Every bridge action begins from a reference, chooses an authenticated route, and requires a matching receipt before that route is treated as healthy.

## Hysteretic route law
Successful routes gain weight. Failed routes lose weight. The active route is held until its score falls below a leave threshold, then a replacement route must cross an enter threshold before becoming preferred.

## Route modules
Each route module must expose the same concepts: reference, probe, execute, receipt, repair, source, target, and direction.

Route families:
- Hive Pipe MCP
- ChatGPT GitHub pull bridge
- GitHub Actions command lane
- direct HTTPS helper
- Gemini / Perplexity / DeepSeek adapters
- SSH recovery
- peer bridge between Dell and Jetson

## Reference card
Before an outbound bridge action, record:
- timestamp
- source identity
- target identity
- direction
- repository root / branch / HEAD when repository work is involved
- reference file(s)
- intention
- consequence
- selected route
- fallback route(s)
- protected state

If required reference fields are absent, hold the action and return the missing fields plus the next safe setup step.

## Failure handling
When a route fails:
1. record the exact failure;
2. do not loop indefinitely on the same path;
3. after three evidence-bearing failures, switch to a materially different route family;
4. if no alternate is configured, create a bounded setup/repair task;
5. require a real target receipt before marking the route healthy;
6. add or update the canonical instructions so the same recovery is available to later AI sessions.

## Bidirectional proof
Each direction is independent. For example, Dell -> Jetson does not prove Jetson -> Dell. Maintain separate receipts and route scores for both directions.

## Canonical instruction propagation
Every new route or repair procedure must be linked from:
- `One_Wave_Bench/AI_BRIDGE_START_HERE.md`
- `One_Wave_Bench/hive-pipe/BRIDGE_DIRECTIONS.md`
- root `AI_BRIDGE_START_HERE.md`
- bridge reference output / help text
- browser extension reference panel when present

No bridge module is complete until its usage, verification, and recovery directions are posted at the canonical entry points.


## Goblin control roles
Read `One_Wave_Bench/hive-pipe/GOBLIN_BRIDGE_ROLES.md` for Doctor, Parser, Reference/Worker two-state machine, Carrier Pigeon, and Goblin Raccoon behavior.


## Token economy and temporary Field/Void fusion
Read `One_Wave_Bench/hive-pipe/TOKEN_ECONOMY_AND_FIELD_VOID_FUSION.md`. Repeated same-path failure triggers the novelty breaker. Field/Void may temporarily operate from one compact shared packet with Void as inner oversight and Field as the sole outward voice/action channel; return to separate operation on material disagreement, token-budget overflow, hard stop, or novelty-triggered route/tool change.
