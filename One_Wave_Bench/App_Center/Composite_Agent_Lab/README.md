# Composite Agent Lab

Local App Center-style package for testing the software CELL_V1-inspired Field/Void composite agent.

## Run

```bash
python3 app.py --open
```

Open `http://127.0.0.1:8788/`.

## Plugin layout

- `providers/*.py` — local/cloud AI adapters. Each exports `PLUGIN` metadata and `call(role, packet)`.
- `parsers/*.py` — parser adapters. Each exports `PLUGIN` and `parse_input(value)`.
- `runtime.py` — one-cycle composite state machine.
- `app.py` — local UI/API shell.

The default plugins are deterministic and require no cloud keys, so the loop can be tested safely before adding real providers.

## Software-cell mapping

- Void = admin/reference/inhibition/commit
- Field = sensing/proposal/action/speech
- shared packet = common cell state
- parser = threshold/input normalization
- result = feedback/reinjection into next state
- sandbox = prevents arbitrary provider code from receiving broad machine authority by default

Cloud/local provider credentials belong outside git in user config/environment files.


## M4 simulated body

M4 is the persistent processing substrate, not merely a scheduler.

It owns:

- hysteretic action and commit gates
- lean / polarity
- pressure / arousal
- resistance
- confidence
- retained reference memory
- recent successful and failed patterns
- result reinjection into the next cycle

Field supplies sensory drive and outward action/speech. Void supplies administrative brake/support/contradiction. M4 integrates both, decides whether the action threshold is crossed, and retains the committed result.

This is a software architecture experiment inspired by CELL_V1 concepts; it is not evidence that the physical CELL_V1 mechanism has been demonstrated.


## One-Wave Local AI

The first project-owned local AI provider is `providers/one_wave_local.py`.

It is intentionally model-agnostic. The local model provides bounded language inference while One-Wave owns M4 state, hysteresis, memory, Field/Void roles, reference control, quality gates, and sandboxed action authority.

See `ONE_WAVE_LOCAL_AI.md`.


## AI council workspace
The structured council protocol is defined in `One_Wave_Bench/App_Center/Composite_Agent_Lab/AI_COUNCIL_PROTOCOL.md`. M4 is chair/body state, Void is admin/inner oversight, Field is the sole outward voice/action, and specialist AIs contribute bounded evidence/proposals through the shared room state.
