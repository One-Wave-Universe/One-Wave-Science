# ONE-WAVE ANIMATOR — CANONICAL ARCHITECTURE

This file defines what the Animator is, how it is divided into layers, how work is assigned, and how failures are repaired without rebuilding the whole application.

The existing Animator remains a local frame-animation program built around a reel/exposure-sheet model. This document does not replace working implementation or production feature docs. It defines ownership and repair boundaries so the program can move forward without repeatedly rewriting the same subsystems.

## 1. What the Animator is

The Animator is a reusable 2D frame-animation production tool.

It must support:
- calibrated full-screen background images;
- transparent character and prop artwork on independent layers;
- a frame reel / exposure sheet as the source of truth;
- configurable FPS and drawing holds;
- manual frame-by-frame editing;
- reusable motion sequences and motion atlases;
- path and walk construction;
- camera motion;
- onion skin and placement guides;
- chat/director edits that modify the same project state used by manual tools;
- preview and visible real-time playback;
- clip/reel export whose timing and composition match preview;
- project save/load;
- local runnable packaging and launcher support.

The Animator is not a single-image tween shortcut. A changing reel must produce visibly changing rendered frames.

## 2. Canonical layer map

```text
ANIMATOR/
├── 00_RULES/
├── 01_ASSETS/
├── 02_SCENE_AND_LAYERS/
├── 03_TIMELINE_AND_EXPOSURE/
├── 04_MOTION_ATLAS/
├── 05_RENDERER_AND_PLAYBACK/
├── 06_EDITOR_TOOLS/
├── 07_EXPORT_AND_PACKAGING/
├── 08_TESTS/
├── 09_RECEIPTS/
└── 10_INTERFACE/
```

These are responsibility layers. Existing files do not have to be physically moved into new folders merely to satisfy this map. Refactoring directory layout is not required unless there is a concrete implementation reason.

## 3. Layer 00 — RULES

Owns architectural and update rules.

Rules:
1. No total rebuild to fix a local failure.
2. Identify the owning layer before editing.
3. Change the owning layer only unless an explicit interface dependency requires another layer.
4. Preserve all previously passing behavior.
5. A passing test becomes a permanent regression.
6. The reel/timeline is the canonical animation state.
7. Manual editing, motion tools, and future AI/chat directing must mutate the same underlying project/reel state. Do not create parallel incompatible animation state.
8. FPS is real timing, not a label. Do not change target FPS to hide playback problems.
9. Editor overlays such as grids, guides, onion skin, and drift markers must not appear in export unless explicitly designed as artwork.
10. Do not modify source artwork to conceal renderer, timing, or drift defects.
11. Visible playback and exported output are the final behavioral truth. A working UI alone is not an animation pass.

## 4. Layer 01 — ASSETS

Owns imported source material and asset metadata.

Includes:
- background PNG/image import;
- character PNGs;
- props;
- pose images;
- sprite-sheet source material;
- crop/source bounds;
- pivot/origin metadata;
- source dimensions;
- asset identity and references.

Asset models must not contain scene-specific motion merely to compensate for scene/timeline bugs.

If import, crop, source dimensions, transparency, or asset identity is wrong, fix this layer.

## 5. Layer 02 — SCENE AND LAYERS

Owns what is present in the scene and how visual objects are composed.

Includes:
- fixed/full-screen background behavior;
- character/prop instances;
- x/y position;
- scale/depth;
- rotation;
- opacity;
- visibility;
- z/layer order;
- pivot placement;
- camera-relative composition where applicable.

If an object is correct in the asset library but appears in the wrong location, depth, visibility, or layer order, fix this layer.

## 6. Layer 03 — TIMELINE AND EXPOSURE

Owns animation time.

Includes:
- reel frame index;
- target FPS;
- duration;
- drawing holds/exposures;
- keyframes;
- pose changes;
- insertion/deletion/order;
- start/end sections;
- loop ranges;
- timeline events;
- deterministic seek state.

The same project opened twice with the same state must resolve the same frame content at the same frame index.

If a hold lasts the wrong number of frames, a keyframe fires at the wrong time, or frame order is wrong, fix this layer.

## 7. Layer 04 — MOTION ATLAS

Owns reusable motion knowledge.

Includes:
- `.owmotion` sequences;
- `.owatlas` character motion atlases;
- reusable action definitions;
- cadence data;
- path/walk generation inputs;
- motion composition and override rules;
- character-motion roster bindings.

Required reusable qualification actions include:
- walk toward camera;
- walk away from camera;
- look around;
- kick a can/prop;
- pick up a flower/prop;
- sniff the flower/held prop.

Motion definitions must resolve into ordinary scene/timeline edits. They must not bypass the reel with a second hidden playback system.

If a named motion produces the wrong sequence while timeline/rendering are otherwise correct, fix this layer.

## 8. Layer 05 — RENDERER AND PLAYBACK

Owns turning canonical scene/timeline state into visible frames over time.

Includes:
- frame rendering;
- compositing;
- play/pause;
- seek;
- frame/time counters;
- playback clock;
- actual FPS monitoring where supported;
- dropped/late frame detection where supported;
- preview rendering.

PASS requires visible frame changes whenever the reel contains frame changes.

If the timeline data is correct but playback is static, jittering, stale, or timed incorrectly, fix this layer. Do not rewrite the timeline to make the renderer look correct.

## 9. Layer 06 — EDITOR TOOLS

Owns tools that modify canonical project state.

Includes:
- background calibration grid;
- perspective/depth placement aids;
- manual transforms;
- pose replacement;
- neighboring-frame copy;
- onion skin;
- batch pose import tools;
- sprite-sheet slicing controls;
- path editing;
- prop placement;
- drift guides;
- drift counter/receipts;
- chat/director command translation.

The calibration grid is an editor overlay used for placement and may be hidden after placement.

All editor paths must write through the same project/reel model.

If manual edits work but chat edits create different state, that is an editor/integration failure, not permission to create a second format.

## 10. Layer 07 — EXPORT AND PACKAGING

Owns producing external deliverables and opening the app locally.

Includes:
- full-reel export;
- marked-section/clip export;
- WebM/video output where supported;
- frame/image sequence output where supported;
- preview/export parity;
- project save/load transport where appropriate;
- Ubuntu installer;
- desktop/application launcher;
- local-only startup behavior.

Export must use the same canonical scene/timeline state as preview.

If preview is correct and export is wrong, fix export. Do not alter the renderer or timeline to compensate for an export defect.

## 11. Layer 08 — TESTS

Tests mirror ownership layers.

```text
08_TESTS/
├── assets/
├── scene/
├── timeline/
├── motion/
├── renderer/
├── editor/
├── export/
├── interface/
└── integration/
```

Permanent tests should cover at minimum:
- asset import and transparency;
- background calibration and hidden-grid behavior;
- character/prop placement;
- layer ordering and visibility;
- exposure holds;
- keyframe timing;
- configurable FPS;
- play/pause/seek;
- motion sequence insertion;
- motion atlas recall;
- required demo motions;
- manual edit persistence;
- chat/manual shared-state parity when chat bridge exists;
- drift guide/counter behavior;
- preview/export parity;
- save/load parity;
- launcher opens a runnable Animator.

## 12. Layer 09 — RECEIPTS

Every qualification test emits a receipt:

```text
TEST:
LAYER:
VERSION:
EXPECTED:
ACTUAL:
TOLERANCE:
PASS/FAIL:
DEPENDENCIES:
NOTES:
```

Valid capability states are only:
- MISSING
- IMPLEMENTING
- FAILING
- PASSING

`documented`, `mostly done`, `should work`, and `UI exists` are not implementation states.

## 13. Layer 10 — INTERFACE

Owns presentation and operator controls.

Includes:
- scene panel;
- asset controls;
- timeline/exposure sheet;
- motion library browser;
- preview canvas;
- transport controls;
- frame/time display;
- export controls;
- chat/director panel;
- status/error display.

The interface does not own animation truth.

If underlying reel/render output is correct but the UI displays it incorrectly, fix the interface. If underlying state is wrong, fix the owning lower layer instead of compensating in the UI.

## 14. Work division

Every task must declare:

```text
TARGET LAYER:
SPECIFIC FAILURE OR CAPABILITY:
ALLOWED FILES:
DIRECT DEPENDENCIES:
TESTS TO RUN:
PASS CONDITION:
STOP CONDITION:
```

Suggested parallel ownership:
- Worker A: Assets + Scene/Layers
- Worker B: Timeline + Exposure
- Worker C: Motion Atlas / reusable motion
- Worker D: Renderer + Playback performance
- Worker E: Editor integration + Export/Packaging
- Integrator: cross-layer contracts + regression verification only

The Integrator is not authorized to broadly redesign all layers.

## 15. Bug routing

- wrong import/crop/transparency -> 01 ASSETS
- wrong position/depth/order/visibility -> 02 SCENE_AND_LAYERS
- wrong frame/hold/keyframe timing -> 03 TIMELINE_AND_EXPOSURE
- wrong named/reusable action sequence -> 04 MOTION_ATLAS
- correct reel but static/jittery/wrong-speed playback -> 05 RENDERER_AND_PLAYBACK
- grid/onion/manual/chat edit defect -> 06 EDITOR_TOOLS
- preview correct but exported clip wrong -> 07 EXPORT_AND_PACKAGING
- incorrect test expectation -> 08 TESTS
- display/control wrong while underlying state is correct -> 10 INTERFACE

When a worker finds a defect owned by another layer, record/reproduce it and hand it to that layer. Do not patch around it locally.

## 16. Cross-layer change rule

Before editing:

```text
PRIMARY LAYER:
SECONDARY LAYER IF REQUIRED:
WHY:
FILES EXPECTED TO CHANGE:
TESTS TO RUN:
```

A second layer may be touched only because of a concrete interface requirement.

If a small bug suddenly requires broad edits across unrelated layers, stop and re-triage. That is likely scope drift or an architectural boundary problem.

## 17. Work cycle

```text
OBSERVE FAILURE
      ↓
IDENTIFY OWNING LAYER
      ↓
REPRODUCE
      ↓
MAKE SMALLEST COHERENT FIX
      ↓
RUN LAYER TESTS
      ↓
RUN DIRECT DEPENDENCY REGRESSIONS
      ↓
SAVE RECEIPT
      ↓
PASS OR FAIL
      ↓
STOP
```

Do not turn a local defect into a cleanup/rewrite campaign.

## 18. No-rebuild protection

A total replacement is allowed only if all are true:
1. the current foundation is demonstrably incapable of a required capability;
2. the problem cannot be isolated to a layer or interface;
3. existing passing behaviors have executable regressions;
4. the replacement reproduces those regressions;
5. the reason is documented before replacement begins.

Messy code, personal preference, or a newly requested feature are not sufficient reasons.

Default action: repair or extend the owning layer.

## 19. Qualification gate

The Animator is not qualified merely because the editor opens.

A qualification run must demonstrate:
1. a background loads and remains correctly calibrated;
2. character/prop layers remain independently editable;
3. the reel visibly plays changing frames at the declared FPS within stated tolerance;
4. exposure holds and pose changes occur at intended frames;
5. walk toward, walk away, look, kick, pick-up, and sniff actions can be represented and played;
6. drift is observable through the designated guide/counter rather than silently hidden;
7. manual edits persist through save/load;
8. exported section/reel matches preview timing, frame order, layer transforms, and camera behavior;
9. the local launcher opens a runnable Animator on its supported platform.

## Final rule

Locate the Animator layer that owns the failure. Fix that layer. Test it. Run only the regressions that touch its interfaces. Save the receipt. Move forward.
