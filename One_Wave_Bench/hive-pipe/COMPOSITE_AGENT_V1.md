# COMPOSITE_AGENT_V1 Adapter Contract

`composite_agent_v1.py` is the controller. Model/provider code is replaceable.

## Shared cycle

```text
INPUT
  -> FIELD_PERCEIVE
  -> VOID_ADMIN
  -> FIELD_ACT
  -> RESULT
  -> VOID_COMMIT
  -> OUTPUT
  -> next INPUT
```

## Field adapter responsibilities
`FIELD_PERCEIVE` receives compact shared state and returns:
- `perception`
- `proposal`
- optional `plan`
- optional `speech_draft`

`FIELD_ACT` receives the same state plus Void admin output and returns:
- `action` object for the tool/body adapter
- `speech` for outward communication

Field owns senses, expression, and action proposals. It does not authorize itself.

## Void adapter responsibilities
`VOID_ADMIN` returns:
- `decision`: ALLOW, CORRECT, OVERRIDE, HOLD, or ESCALATE
- compact `inner_voice`
- optional `correction`
- `permissions`
- optional `outward_instruction` only when Field must not act

`VOID_COMMIT` receives the action result and returns:
- `commit` boolean
- `reason`
- optional `next_state`
- optional updated `goal` / `reference`

Void owns authority, continuity, inhibition, and commit. It does not speak outward during normal execution.

## Tool/body adapter
The tool adapter receives only the structured `action` object and current state. It returns a structured evidence/result object. It must not silently mutate the shared state.

## Persistent shared self
Both agents read the same state file and transition ledger. They do not keep separate canonical memories. Provider-private context may exist, but only committed shared state controls the composite agent.

## Token law
Adapters receive compact packets only. Full files/logs are fetched lazily by the side that needs them. Raw evidence stays in files/receipts and is referenced by ID/path whenever possible.

## Provider mapping examples
- local model A = Void, model B = Field
- Claude = Void, Gemini = Field
- same provider with two system roles = Void + Field
- OpenClaw local CPU lane = Void, GPU lane = Field

The provider pairing is configuration, not architecture.
