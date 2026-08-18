# Goblin Raccoon art lock

This is an animator constraint, not a request to redesign the character.

## Hard rule

Goblin Raccoon (GR) artwork supplied by the creator is canonical input. The animation engine may:

- load an approved GR drawing,
- place it in scene coordinates,
- choose among approved drawings,
- hold or sequence drawings on film frames,
- scale the complete drawing according to background depth,
- translate or rotate the complete drawing when explicitly directed,
- remove a known flat/chroma background when requested,
- reference approved turnarounds to select the correct viewing angle.

The animation engine must **not** silently:

- redraw GR,
- change the face, body proportions, costume, hood, mask, tail, colors, or silhouette,
- substitute a look-alike raccoon,
- make GR younger, cuter, or child-oriented,
- invent anatomy to fill missing views,
- blend two inconsistent GR designs into a new design.

If a needed pose or angle does not exist, report/request that missing art through the art-generation workflow. Generated candidate art remains a candidate until the creator accepts it; it does not automatically become canonical.

## Grounding rule

Every approved full-body drawing needs a bottom-center **ground-contact/feet anchor**. Scene `x` and `ground_y` refer to that anchor, not the image center. Switching drawings must preserve the anchor so pose changes do not make GR float or jump.

## Perspective rule

The background is the world. Apparent character size is derived from the ground-contact position and the background's calibration grid. Perspective guides are editor metadata only and must never be composited into final frames.

## Time rule

Artwork is exposed onto explicit film-frame slots. No hidden container motion, procedural bounce, or invented interpolation may replace the approved drawings. More drawings may be exposed when motion needs to read more smoothly; still reactions may hold the same drawing across many film frames.
