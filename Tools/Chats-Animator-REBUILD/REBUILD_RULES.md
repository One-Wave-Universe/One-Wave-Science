# One-Wave Animator Rebuild — Core Rules

## Why this rebuild exists
The previous animator drifted into moving/scaling precomposed rectangular image panels instead of animating transparent character stills over a stable background. That architecture is rejected.

## Canon production model
1. Scene background is one dedicated locked layer.
2. Characters and props are transparent PNG/WebP assets only.
3. Animation is authored frame by frame on a true 24 fps timeline.
4. A drawing may be held on 1s, 2s, 3s, or longer. Timing is explicit per reel frame.
5. Character pose, position, depth, scale, facing, and visibility may change frame to frame.
6. Background does NOT change merely because the reel advances.
7. Camera movement is a camera transform over the scene, not a sequence of baked screenshot backgrounds.
8. Reusable motion libraries are separate from active scene projects.
9. Each character/body variant owns its own motion corpus.
10. Audio/voice editing is a separate program/workstation connected to the animator through timed clips.
11. Project save/load must preserve editable scene state, not only rendered output.
12. Video export must render the same layered state shown in the editor.

## Required character motion corpora
- Goblin Raccoon
- Nexus
- Scales
- Noobs
- Cerberus Giant
- Cerberus Modulated-Down

Cerberus Giant and Cerberus Modulated-Down are separate acting/motion bodies. Modulated-Down is not just Giant scaled smaller.

## First production benchmark
One fixed forest-path background. Goblin Raccoon must:
- walk into scene;
- change scale correctly with depth;
- look at environmental points;
- point;
- wave;
- turn;
- flip something off;
- walk away/return;
- remain on the same background the entire time unless camera motion is explicitly authored.

## Hard failure conditions
- character frame contains baked background scenery;
- background changes because pose frame changes;
- animation created by moving cropped storyboard panels;
- fake interpolation replaces authored pose timing by default;
- export differs materially from editor composition;
- reusable motion is mixed destructively into the active scene;
- audio preview and export use different timing/mix paths.

## Rebuild order
A1 Scene model
A2 Transparent asset importer/validator
A3 24 fps exposure sheet/reel
A4 Frame state + pose replacement
A5 Position/depth/scale controls
A6 Onion skin
A7 Camera track
A8 Motion-library insert/capture
A9 Multi-character atlas roster
A10 Project save/load
A11 Export renderer
A12 Audio timeline bridge
A13 AI scene-state API
A14 Forest acting benchmark

Do not copy old architecture merely to save time. Reuse only isolated code that obeys these rules.
