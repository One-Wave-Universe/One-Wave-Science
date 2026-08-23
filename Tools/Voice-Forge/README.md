# One-Wave Voice Forge

## Purpose
A standalone character-voice design program. It is separate from the animator. The animator only receives finished dialogue clips plus timing metadata.

## Core rule
Do not begin from a canned TTS/machine voice and hide it with effects. Voice Forge must work from recorded/reference human voices the user has permission to use, or from original generated base voices designed for the project.

Do not clone or impersonate an identifiable real person's voice without authorization. A celebrity/reference can be used as a descriptive target or inspiration, but the saved result should be an original character voice unless rights/permission are available.

## Character voice pipeline
1. Import 1-4 reference takes.
2. Analyze each reference separately.
3. Separate controllable traits instead of baking them together:
   - pitch contour
   - formant / apparent vocal-tract size
   - resonance / body
   - brightness
   - breath / air
   - rasp / grit
   - nasality
   - articulation sharpness
   - speaking rate
   - timing / pause profile
   - dynamics
   - vibrato / instability
4. Blend references by trait, not just waveform volume.
5. Allow continuous A/B blend controls per trait.
6. Apply character finishing:
   - high/low cut
   - body EQ
   - presence
   - de-esser
   - compressor
   - saturation / drive
   - optional doubler
   - optional delay
   - plate/spring/room reverb slots
7. Save a reusable character recipe.
8. Render a clean dialogue file plus metadata for the animator.

## Required controls
- Reference A amount
- Reference B amount
- Optional Reference C/D amount
- Pitch shift
- Formant shift independent of pitch
- Body / chest resonance
- Brightness / presence
- Breathiness
- Rasp / grit
- Nasality
- Articulation
- Timing stretch without pitch change
- Micro-pitch instability
- Layer/doubler amount
- Stereo width
- Dry/wet
- Output gain

## Voice-combiner behavior
The combiner is non-destructive. Each reference stays intact. A character recipe stores trait weights and processing settings. Rendering can always be repeated from the originals.

The program must support:
- solo/mute each source
- A/B instant comparison
- randomize within safe ranges
- save named presets
- lock selected traits while changing others
- undo/redo
- render WAV
- render stem layers
- export a compact recipe JSON alongside the WAV

## Animator handoff
Voice Forge exports:
- dialogue.wav
- dialogue.recipe.json
- optional stems/

The animator imports the finished clip and places it on the reel timeline. The animator must not own voice synthesis internals.

## First implementation target
Desktop/local-first program for Ubuntu/Jetson-compatible environments where possible. Heavy neural inference may run on GPU; basic editing, analysis, mixing, and rendering must work locally without cloud tokens.

## Hard stop for Phase 1
Phase 1 is complete only when two authorized human reference recordings can be loaded, blended with independent pitch/formant/body/brightness controls, previewed A/B, saved as a recipe, and rendered to WAV without using a canned TTS voice as the source.
