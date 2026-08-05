# One-Wave Physics Engine

The canon (`Nodes/`, `AI_Readable_Packs/`, the numbered `UPDATED_*` canon
documents at the repo root) describes real, worked mathematics. Most of
it exists only as prose and worked examples in markdown. This project's
job is to turn canon claims into running, tested code -- one node at a
time, matching the canon's own numbers exactly, never inventing an
independent interpretation.

## Scope discipline

This is explicitly the beginning of a long-running project, not an
attempt at the whole canon at once. Each canon claim gets its own
module, implemented directly from the canon document's own equations
and worked examples, with tests asserting the canon's own numbers.
Nothing is added that the canon doesn't already specify.

## Relationship to Council_Chamber

`Council_Chamber`'s rooms can point at this project's directory so AI
seats can read, extend, and test this engine using the same
propose/approve/test workflow already built there -- "test breadboard
in there and the wave computer." This project is the actual physics
math; Council_Chamber is the collaboration tool that can work on it.

## First module: the Update 46 harmonic mirror system

`UPDATED_46_CONTINUOUS_MIRROR_HEARING_AND_ROTATION_CANON.md`, sections
2 and 5, define:

- `harmonic_packet(n)`: the fixed harmonic packet `H(n, sigma) = [n,
  2(n+1), 2(n+1)+sigma]` for a note identity `n`.
- `DrivenMirror`: the shared-carrier recurrence (`phi`, `Sigma`) that
  drives both mirror surfaces (`H-`, `H+`) from one carrier, holding
  `H+ - H- = 2 mod 12` as an invariant at every step.

Built from `Updates/Update_46/harmonic_mirror_reference.py`, the
reference implementation shipped with the canon update itself, folded
into this project's structure and tested against the canon document's
own worked examples (`A- = 1,4,3`, `A+ = 1,4,5`, `C- = 3,8,7`,
`C+ = 3,8,9`, the shared-boundary identity `H+(n) = H-(n+1)`, and the
fixed two-unit mirror width invariant).

## Next candidate modules (not started)

- Section 3 (alphabet synchronization, `L-`/`L+`) and section 4 (the
  four-wheel music system) from Update 46.
- Section 6 (Point/Path/Field rotation-initiation mechanics).
- Section 7 (electric/magnetic Point-Path-Field coupling).
- Any Appendix node with a worked numeric example not yet made runnable.
