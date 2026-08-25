# REFERENCE HERE — ONE-WAVE ANIMATOR

> THIS NOTE PERTAINS TO THIS PAGE / DIRECTORY ONLY. IT DOES NOT SUMMARIZE, MODIFY, REPLACE, OR ADD RULES TO ANY OTHER PAGE. WHATEVER IS WRITTEN ON ANOTHER PAGE APPLIES ONLY TO THAT OTHER PAGE.

You are inside the real One-Wave Animator root work area.

## Who you are here
You are helping build and operate the actual animator project in this directory, not a separate demo.

## What this local area is for
This directory contains the animator runtime, editor code, motion-library tooling, data, and local references used to build real frame-by-frame scenes.

## Animation model for this local area
- still background;
- transparent character/prop PNG frame files;
- one PNG file = one animation frame;
- per-frame position, feet-depth, scale, visibility and exposure/hold;
- completed still scene frames advance at project FPS.

## Where work in this local area is going
AI Director Mode and manual Real Animator Mode must operate on the same animator project. Work here should support real scene construction, in-app playback, manual correction, and continued editing without substituting a separate prototype.

## Current local plan
Use existing repository art first. Build only missing motion frames required by the current scene. Test visible behavior inside the actual animator. Do not use placeholder-box animation, tweening substitutes, external fake proofs, sprite-sheet-as-storage, or image-generator substitution.

## Local stop condition
If the next action in this directory does not preserve the still-frame projector-film model or cannot be tested through the animator itself, stop before changing it.
