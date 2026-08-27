# A5 — Canonical Project Data Schema

**Status: PASS**

This brick defines the shared data contract for the One-Wave Video Maker. It deliberately adds **no animation behavior**.

## Source of truth

The saved project is one object with these top-level stores:

- `project`
- `scenes`
- `frames`
- `characters`
- `characterInstances`
- `audioTracks`
- `audioClips`

Every relationship uses stable IDs rather than copying whole nested objects around.

## Locked architecture carried forward

- Background is scene data.
- Perspective/grid values are scene calibration data and editor-only guides.
- Frame records are the authoritative animation state.
- Character ground position, depth, and scale have explicit fields, but A5 does not calculate them.
- Reusable character identity is separate from a scene instance.
- Per-frame character state is stored on the frame.
- Held timing is represented by `exposure`.
- Camera state has a reserved frame-addressable location.
- Audio tracks and clips remain separate from picture data.
- Audio timing is frame-addressable so it can share the project clock later.
- Human and AI must edit this same project structure.
- All records include IDs so later bounded AI operations and history/undo can target one thing without rewriting the project.

## A5 boundary

Not implemented here:

- background loading
- perspective calculations
- depth-to-scale math
- playback
- interpolation
- held-frame playback rules
- AI commands
- undo/history
- audio playback/mixing
- rendering/export

Those belong to later bricks.
