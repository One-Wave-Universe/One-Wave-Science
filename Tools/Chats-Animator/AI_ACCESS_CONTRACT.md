# ONE-WAVE ANIMATOR — UNIVERSAL AI ACCESS CONTRACT

**Status: REQUIRED / NOT YET FULLY IMPLEMENTED**

This file is the hard acceptance contract for AI access to the One-Wave Animator.

The Animator is not considered complete if only a human can operate the GUI. Any authorized AI client must be able to inspect and operate the same canonical project state through a deterministic machine interface without screen scraping, mouse-coordinate guessing, private model-specific state, or a second incompatible animation format.

This requirement is intentionally aligned with the repository, Jetson/Hive Pipe, CERN, LIGO, and JPL work: a client must have a documented path to inspect the real state, perform bounded operations, receive structured results, and verify what changed.

## 1. Universal-access law

One Animator. One project state. One command contract.

The following classes of client must be able to use the same interface when authorized:

- ChatGPT
- Codex
- Claude
- Gemini
- DeepSeek
- Perplexity
- local models
- future AI clients that can speak the documented command/API contract

No provider gets a privileged hidden format.

A model-specific adapter may translate that provider's tool-call syntax into the Animator contract, but the adapter may not invent a second project model or bypass the canonical reel/timeline state.

## 2. Canonical control path

The preferred architecture is:

```text
AI client
   |
   v
provider adapter / MCP / authenticated terminal lane
   |
   v
Animator deterministic command surface
   |
   v
canonical project transaction engine
   |
   +--> GUI
   +--> reel/timeline
   +--> motion libraries
   +--> renderer/playback
   +--> save/load
   +--> export
```

The GUI and AI are peers over the same project state. Neither owns a private copy that can silently diverge.

## 3. Required machine interface

The Animator must expose a stable machine-operable surface. The implementation may be a CLI, local HTTP/JSON-RPC service, MCP server, or a thin combination of these, but it must satisfy all behavior below.

A CLI is strongly preferred as the lowest common denominator because any AI that already has authorized Jetson/terminal access can call it directly, while MCP/HTTP adapters can wrap the same commands.

The canonical CLI name should be one of:

```text
one-wave-animatorctl
animatorctl
```

Do not create separate command implementations for different AI providers.

## 4. Minimum required operations

The machine interface must support, at minimum:

### Inspect

- `status` — app/project state, version, active project, active frame, FPS, dirty state, playback state.
- `project get` — canonical project metadata and revision.
- `scene get` — background, calibration, layers, camera, active scene state.
- `timeline get` — frames, holds/exposures, active frame, section markers.
- `assets list` — imported backgrounds, characters, props, pose sources, motion libraries.
- `motion list` — available `.owmotion` and `.owatlas` actions.
- `errors` — current structured errors/warnings.

### Edit

- create/open project.
- import/relink an authorized asset.
- add/remove character or prop instance.
- set position, depth, scale, rotation, visibility, layer order, and camera state.
- create, duplicate, delete, reorder, and select reel frames.
- set exposure/hold.
- replace/copy pose.
- insert a named motion sequence/atlas action.
- set path/walk inputs.
- set start/end section markers.
- commit edits as one explicit transaction.
- undo/redo through the same history model used by manual edits.

### Playback and render

- seek to frame.
- play/pause/stop.
- render or inspect a deterministic frame.
- preview a marked section.
- expose playback counters/status required to verify visible change and timing.

### Persistence and export

- save project.
- save-as project.
- reopen project.
- export one frame/image sequence where supported.
- export marked section.
- export full reel.
- return the exact output path and structured result.

## 5. Structured input and output

Every machine operation must have a machine-readable mode. JSON is required even if a human-readable mode is also provided.

Example success envelope:

```json
{
  "ok": true,
  "operation": "frame.set_hold",
  "project_revision_before": 41,
  "project_revision_after": 42,
  "changed": true,
  "result": {
    "frame_id": "frame-007",
    "hold": 3
  },
  "warnings": []
}
```

Example refusal/failure envelope:

```json
{
  "ok": false,
  "operation": "layer.set_position",
  "changed": false,
  "error": {
    "code": "REVISION_CONFLICT",
    "message": "Project changed since the caller's baseline."
  }
}
```

A command must never report success when it did not modify or verify the real Animator state.

## 6. Transaction and revision law

Every edit must pass through the existing canonical transaction/history model.

Required properties:

- explicit actor identity (`human`, `ai:<client>`, or equivalent);
- before/after values;
- project revision before and after;
- deterministic target IDs;
- undo/redo compatibility;
- stale-baseline conflict detection;
- no silent last-writer-wins overwrite when another editor changed the same state.

If an AI edit cannot be expressed as a normal project transaction, the interface is incomplete.

## 7. Same-state parity law

An AI operation is not accepted until the GUI can immediately observe the same state, and a manual GUI edit is not accepted as AI-accessible until the machine interface can immediately observe it.

Required parity checks:

```text
AI edit -> GUI sees exact edit
GUI edit -> AI inspection sees exact edit
save -> close/reopen -> both see same state
undo/redo -> both see same state
```

No browser-only hidden state may be the sole source of truth for a feature that AI is expected to operate.

If browser `localStorage` or in-memory state is used as a cache, it must reconcile with the canonical project model rather than becoming a second authority.

## 8. No screen-scraping substitute

The following do not count as universal AI access:

- vision model clicking approximate UI coordinates;
- DOM scraping that bypasses the transaction model;
- editing `.owav` JSON blindly without validation/history/conflict checks;
- a model-specific chat panel that only one provider can use;
- terminal commands that merely launch the GUI but cannot inspect/edit project state;
- generating a second animation representation and importing it later;
- claiming an AI could theoretically use the app without an executable verification path.

Computer-use automation may be a fallback for unsupported edge cases, not the canonical control path.

## 9. Jetson / Hive Pipe integration

Because the Jetson already has an authenticated AI terminal path, the Animator must be operable through that path without special casing individual providers.

Minimum Jetson acceptance:

```text
AI client
 -> Hive Pipe / authorized terminal lane
 -> animatorctl JSON command
 -> canonical Animator transaction
 -> structured result
```

A future dedicated Animator MCP surface may proxy the same operations directly, but it must call the same underlying command/transaction implementation rather than duplicating logic.

## 10. Security boundary

Universal AI access does not mean unrestricted machine access.

Requirements:

- project/asset paths are explicit and validated;
- writes outside authorized project/output locations are rejected;
- API keys/tokens are never stored in `.owav`, `.owmotion`, `.owatlas`, scene files, or exported media;
- each remote client may have its own authentication token;
- destructive operations are explicit and return receipts;
- arbitrary shell execution is not part of the Animator API;
- the existing Jetson/Hive Pipe security boundary remains authoritative for terminal access.

## 11. Capability discovery

The interface must expose its own capabilities and version so an AI does not guess.

Required discovery information:

```text
Animator version
project schema version
command/API version
supported operations
supported export formats
supported motion operations
current project revision
platform/runtime
```

Unsupported operations must return a structured `NOT_IMPLEMENTED`/`UNSUPPORTED` result rather than silently substituting a different action.

## 12. Required universal-AI acceptance test

A build cannot be called universally AI-accessible until one automated acceptance run proves this exact path:

1. launch/open the real Animator runtime;
2. query status through the machine interface;
3. create or open a test project;
4. load a background;
5. add a character image;
6. place/scale the character;
7. create at least three reel frames with an actual pose or position change;
8. set at least one non-default exposure/hold;
9. save the project;
10. close/reopen or reload the canonical project;
11. verify the same state through the machine interface;
12. play/seek enough to prove the changing reel is being used;
13. export a marked section or reel;
14. verify the output exists and the export operation reports success;
15. verify the GUI observes the same final project state;
16. have a second client session inspect the same saved project through the same public contract without provider-specific state.

The test must emit a receipt with exact commands/requests, revisions, outputs, and PASS/FAIL.

## 13. Existing Animator product gate remains in force

Universal AI access is an additional gate, not a replacement for the product gate.

The Animator still must pass:

```text
install -> open -> build scene -> save -> reopen -> play -> export
```

And the production feature set remains anchored in the canonical architecture and current `Tools/Chats-Animator` implementation.

## 14. Implementation order

Do not rebuild the Animator.

Implement the smallest coherent bridge in this order:

1. expose/read the canonical project/reel state through one transaction-aware command module;
2. add JSON `status`, `project get`, `scene get`, and `timeline get`;
3. add bounded edit transactions;
4. add save/reopen controls;
5. add playback/seek controls;
6. add export controls;
7. wrap the same command surface for MCP/HTTP if useful;
8. add provider adapters only after the provider-neutral core passes.

The existing GUI, renderer, motion tools, and export system are not to be rewritten merely to add AI access.

## 15. Capability state

Until the acceptance test above passes, universal AI access must be reported as:

```text
IMPLEMENTING
```

not `PASSING`.

Existing model-specific or older AI-director experiments are evidence and reusable material, but they do not by themselves satisfy this contract unless they operate the current canonical Animator through the same provider-neutral state/transaction path.

## Final law

If a human can do an Animator operation through the supported product workflow, an authorized AI must be able to inspect and perform the equivalent operation through a documented deterministic interface, against the same canonical state, with a structured receipt.

No provider lock-in. No hidden second state. No screen-scraping as the foundation. No claiming success without the real state change and verification.
