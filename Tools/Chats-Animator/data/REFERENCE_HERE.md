# REFERENCE HERE — ANIMATOR DATA AREA

> THIS NOTE PERTAINS TO THIS PAGE / DIRECTORY ONLY. IT HAS NOTHING TO DO WITH RULES OR UPDATES FOR ANY OTHER PAGE. DO NOT SUMMARIZE ANOTHER PAGE INTO THIS ONE, AND DO NOT APPLY THIS NOTE OUTSIDE THIS DATA AREA.

## Who you are here
You are inside the One-Wave Animator data area.

## What this local area does
This directory holds animator project/library data used by the real frame-by-frame workflow.

## Data model in this local area
- one saved PNG asset represents one animation frame;
- sequences reference individual frame files;
- project/reel state stores the order and exposure/hold of completed frame states;
- do not reinterpret data here into a sprite-sheet-as-frame model;
- do not create placeholder/demo data and use it as proof of the animator.

## Plan in this local area
Keep data compatible with both AI Director edits and manual animator edits to the same project. Add motion data only as needed for real scenes and preserve reusable completed frame sequences.

## Test expectation in this local area
Data is only useful when the actual animator can load it, manually edit it, and play the referenced real frames at project FPS.
