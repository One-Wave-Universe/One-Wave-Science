# Hearing and vision

Same brain. Two UP nerves. One DOWN mouth.
Field lists. Void checks. G is the reference for both senses.

```
 camera  →  gray world   →  lean candidate     \  Field
 mic     →  air pressure →  lean candidate     /    ↓
                                              Void  engage
                                                 ↓
                              speaker PA—PB     mouth DOWN
                              I_0 / Hall        proprioception UP
```

BUCKET already said this in one loop: see → beat → hit → hear → word. This file is that loop on the cell.

## Vision (UP)

First eye: USB camera forced **grayscale**, small frame (160×120 is enough). No color pipeline.

What leaves the eye is not a jpeg to Void. It is a **lean candidate**:

- mean gray vs mid gray (128) → sign of lean
- change vs last frame → whether anything moved (engage worth asking)
- left-half vs right-half mean → live gate 0 vs 1 (or A vs B for the speaker pair)

That is 2-state vision: brighter/darker, left/right, still/moved. Full RGB classification is not the first eye.

Reference: camera GND / USB GND starred to BLUE if the Nano is on this body. A laptop camera is isolated — then the lean is a number in software, not a voltage on G. Both are legal. Do not inject USB 5 V noise into BLUE without a star point.

BUCKET `senses.py` grayscale stub is the same eye.

## Hearing (UP)

Electret mic. 2 kΩ to 5 V. GND to BLUE. Output through 0.1 µF to an analog pin vs BLUE.

What leaves the ear is also a lean candidate:

- amplitude vs belt → is there a sound (ask engage)
- sign of short-window mean → push vs pull if you care
- onset (beat) → stamp-worth click on the mouth

The **mouth** is the balanced speaker (PA—PB). That is DOWN. Do not use the same element as mic and speaker at once on this first body.

If I_0 jumps when the mouth clicks, the pair is not balanced. Void can refuse the next click (`vagus too loud`).

## Seeing and hearing together

One Thought per window:

```
want_lean, want_live = Field(vision_lean, audio_lean)   # explorer combines
engage, why = Void(want_lean, I_0, Hall, override, audio_too_loud)
mouth = push / pull / silence from engage + sign(lean)
```

Field may listen to the eye more than the ear, or the beat more than the gray. That is a weight, not a third hemisphere.
Void may ignore a pretty frame if I_0 is screaming.

Hold: both senses quiet and no override needed → STAY/STAY, silence, no walk.

## Parts (sense only)

| qty | item |
|---|---|
| 1 | USB cam or Nano-side OV7670-class gray |
| 1 | electret mic + 2 kΩ + 0.1 µF |
| 1 | balanced speaker as SPEAKER_BUILD.md |
| 1 | laptop or Nano to run Field/Void |

## Illegal

- Color net as the first eye
- Speaker return on BLUE
- Mic GND on earth while analog is vs BLUE (fake sound)
- Mouth and ear on one transducer
- Vision model stamping engage
