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
