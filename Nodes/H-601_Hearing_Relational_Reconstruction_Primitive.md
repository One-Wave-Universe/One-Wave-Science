# H-601 — Hearing Relational Reconstruction Primitive

Each ordered hearing slot carries:

```text
[pitch_identity, rhythm, cycle_state, mirrored_direction, ground_displacement, phase]
```

Two grounds are preserved:

- local note identity;
- relational displacement from tonic/context.

The raw settled associative state must be reported separately from the Administrator's committed attractor.

```text
input wave -> local cue -> relational route -> associative settling -> raw state -> committed recognition
```
