# Animator Rebuild Base

## Main goal
Build the simplest correct frame-by-frame animator before adding anything else.

## Canon scene behavior
1. Background is one PNG scene layer.
2. Grid appears only during prop/animation-still placement and sizing.
3. Grid disappears when placement is confirmed.
4. Props and animation stills are transparent PNG/WebP assets.
5. Background remains unchanged while the reel advances.
6. True 24 fps project clock.
7. Each reel frame stores only asset pose/state: image, x, feet-depth y, scale, visibility, exposure/hold.
8. Drawings can be held on 1s, 2s, 3s, or longer.
9. Animation is transparent stills laid frame by frame over the same background.
10. No moving cropped screenshot panels. No baked background inside character frames.

## Placement flow
Load PNG background → enter placement mode → temporary perspective grid appears → place/resize prop or animation still → confirm placement → grid disappears.

## Branch discipline
Every feature gets its own branch. Each branch must have a hard start, hard stop, runtime test, drift check, and next permitted branch. If a branch drifts, abandon it and return to the last PASS branch.

## Planned branches
- animator-rebuild-base — rules only
- animator-rebuild-a1-background-grid
- animator-rebuild-a2-transparent-assets
- animator-rebuild-a3-24fps-reel
- animator-rebuild-a4-frame-pose-state
- animator-rebuild-a5-depth-scale
- animator-rebuild-a6-onion-skin
- animator-rebuild-a7-motion-library
- animator-rebuild-a8-project-save-load
- animator-rebuild-a9-export
- animator-rebuild-a10-audio-bridge
- animator-rebuild-a11-ai-edit-api
- animator-rebuild-a12-forest-acting-test

## Hard stop for base
No app code on this branch.
