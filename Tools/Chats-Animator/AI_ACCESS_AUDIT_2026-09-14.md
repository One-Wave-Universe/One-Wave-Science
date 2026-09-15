# Animator AI Access Audit — 2026-09-14

## Verdict

**Animator product core: substantial and runnable-looking in-repo.**

**Universal external AI access: IMPLEMENTING, not yet PASSING.**

The current repository already contains most of the right internal pieces, but they are not yet connected into the same kind of externally reachable, provider-neutral machine lane used for Jetson/Hive Pipe and the science data workflows.

## What is already present

### Real Animator product

`Tools/Chats-Animator` contains the current FPS/exposure-sheet Animator with:

- background loading and calibration;
- character/prop placement;
- reel frames and drawing holds;
- pose editing and onion skin;
- batch pose import and sprite-sheet slicing;
- project save/load;
- audio/camera work;
- full WebM export;
- marked-section WebM export;
- reusable motion libraries and motion atlases;
- path/walk tools;
- Ubuntu launcher/install support.

### Deterministic browser-local control surface

`c19-local-control-api.js` exposes `window.OneWaveAnimatorControl` with operations including:

- `get_project`
- `get_scene`
- `get_frame`
- `get_motion_library`
- `add_frame`
- `duplicate_frame`
- `delete_frame`
- `select_frame`
- `set_hold`
- `set_fps`
- `play`
- `stop`
- `set_background`
- `clear_background`
- `add_prop`
- `add_character`
- `remove_selected`
- `capture_motion`
- `insert_motion`
- `restore_project`
- `undo`

This is the correct direction because edits go into the actual browser Animator state instead of a second animation format.

### Provider-neutral assistant plugin slot

`c18-director-dialogue.js` defines `one-wave-assistant-plugin/v1`, including an event bridge intended for desktop hosts, ChatGPT bridges, or future local AIs.

This is also the correct direction: provider syntax can be adapted around one shared Animator contract.

### Existing local assistant server

`assistant_server.py` provides local HTTP endpoints for the current live creative partner and image worker.

It is useful but currently provider-specific for the Director path:

- OpenAI chat endpoint for Director reasoning;
- OpenAI image fallback;
- Ollama image path;
- OpenAI key configuration.

It does **not** currently expose the C19 deterministic Animator control operations as a general authenticated external API.

## What is missing for universal external access

The following gaps block a PASS under `AI_ACCESS_CONTRACT.md`:

1. **No external deterministic control endpoint.**
   `OneWaveAnimatorControl` exists inside the browser, but an external AI client cannot yet call it through a documented CLI/MCP/JSON-RPC/HTTP lane.

2. **No vendor-neutral CLI.**
   There is no `animatorctl` / `one-wave-animatorctl` that Jetson-authorized AI clients can invoke and receive JSON receipts from.

3. **No direct Hive Pipe / MCP tool surface for Animator operations.**
   Existing Jetson AI access can run terminal commands, but the Animator has not yet published bounded Animator tools on top of that lane.

4. **Current assistant server Director path is OpenAI-specific.**
   The in-browser plugin host is provider-neutral, but the included server implementation is not a universal provider adapter.

5. **No shared project revision / stale-baseline conflict contract.**
   C19 keeps a browser-local undo snapshot history, but it does not expose project revision numbers or reject stale external edits.

6. **C19 does not expose the full product loop.**
   The deterministic surface lacks complete machine operations for save-as/reopen/export/section export and explicit output verification.

7. **No external two-client parity test.**
   There is no test proving one external AI edits the project and a second authorized AI can inspect the same saved canonical state through the same contract.

8. **No live GUI ↔ external-AI parity receipt.**
   The repository does not yet contain an automated receipt proving AI edit -> GUI observation -> save/reopen -> same state -> export.

## False-positive removed

Before this audit, `test-animator.sh` printed:

```text
PASS external control API contract
```

when it only grepped for the browser-local `OneWaveAnimatorControl` object and event names.

That wording is now corrected on the audit branch. The static smoke test may certify the browser-local control surface and locked requirements, but it may not certify universal external AI access.

## Required next implementation slice

Do **not** rebuild the Animator.

The smallest correct next slice is:

```text
existing C19 operations
        |
        v
shared transaction-aware adapter
        |
        +--> animatorctl --json
        |
        +--> authenticated local API / MCP adapter
        |
        v
Jetson/Hive Pipe and any authorized AI client
```

The adapter must call the same underlying Animator operations used by the GUI and return structured receipts.

### First mandatory commands

Start with read-only commands so external access can be proven without risking project state:

```text
status
project get
scene get
timeline get
motion list
capabilities
```

Then add bounded mutations:

```text
frame select/add/duplicate/delete
frame hold
fps set
layer transform
motion insert
save
reopen
play/seek/stop
export section
export reel
undo/redo
```

## Required acceptance target

The implementation is not complete until an authorized external client can perform this exact path against the real Animator:

```text
inspect
 -> open/create project
 -> background
 -> character
 -> 3 changing frames
 -> non-default hold
 -> save
 -> reopen
 -> inspect same state
 -> play/seek
 -> export
 -> verify output
 -> GUI sees same final state
 -> second AI client sees same saved state
```

Every step must return structured success/failure and project revision data.

## Status

```text
GUI PRODUCT CORE: PRESENT
BROWSER-LOCAL CONTROL SURFACE: PRESENT
PROVIDER-NEUTRAL PLUGIN HOST: PRESENT
EXTERNAL UNIVERSAL CONTROL LANE: MISSING
JETSON/HIVE PIPE ANIMATOR ADAPTER: MISSING
TWO-CLIENT ACCEPTANCE: MISSING
UNIVERSAL AI ACCESS: IMPLEMENTING
```

This status must remain until executable receipts prove otherwise.
