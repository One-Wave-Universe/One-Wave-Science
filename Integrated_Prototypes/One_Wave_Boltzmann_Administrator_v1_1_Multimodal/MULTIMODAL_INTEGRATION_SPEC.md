# Multimodal Hopfield/Boltzmann Integration Spec

## Locked principle

One memory may be represented simultaneously as internal dialogue, sound,
image/spatial scene, body pressure/breath, and movement/gaze. These are not five
separate memories. They are five recoverable views of one attractor.

## Storage allocation

Each modality owns one equal-width Hopfield block:

```text
Dialogue       20%
Sound          20%
Image          20%
Body pressure  20%
Movement/gaze  20%
```

No modality may steal permanent storage from another during this prototype.
That protects weak or faint channels from disappearing during training.

## Live allocation

The current recall loop may redistribute access. One example profile is:

```text
Dialogue       strong
Sound          medium-high
Image          faint but nonzero
Body pressure  medium-high
Movement/gaze  medium
```

This is implemented as an access bias over equal storage, with a minimum live
share for every modality.

## Representation examples

- Dialogue: a running internal transcript, words, fragments, questions, answers.
- Sound: rhythm, pitch relationships, pressure contours, abstract auditory form.
- Image: persistent scene state, boundaries, motion, occlusion, vague overlapping imagery.
- Body pressure: held breath, compression, release, tension, relief, internal pressure.
- Movement/gaze: eye movement, direction, approach, withdrawal, imagined motion.

## Hopfield job

Hopfield reconstructs the complete stored attractor from any usable mixture of
modalities. Missing vision must not prevent recall when dialogue, sound, body
pressure, or movement provide enough structure.

## Boltzmann job

Boltzmann receives the current NEW oversight and previous OLD reference,
compresses their hidden relationship, reconstructs candidate state, and resolves
through the six-line Administrator.

The first build does not let Boltzmann rewrite the Hopfield memory bank. It may
propose candidate missing structure; Hopfield confirms whether that proposal
settles into a known attractor.

## M4 boundary for the next build

M4 will:

- operate the transmission switchboard;
- maintain State and Scale;
- read Caution and Drive pressures;
- mix memory modalities into the five duplex pathways;
- route NEW oversight upward and OLD reference downward on every flip-flop;
- run the subconscious loop-existence heartbeat;
- hold external speech while internal dialogue, sound, and images continue;
- release speech only after the think-before-speaking gate permits it.

The M4 mapping must be calibrated. This package deliberately does not pretend
that memory modality number equals transmission pathway number.
