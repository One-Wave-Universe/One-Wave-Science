# One-Wave Hopfield Melody Cell v1

## Purpose

Test whether one cue tone can settle a Hopfield memory cell into the full
stored melody attractor. This build contains no Boltzmann system.

## Results

- Stored melodies: 3
- Audit trials: 9
- Exact melody recall: 9/9 (100.0%)
- Correct attractor: 9/9 (100.0%)
- Wrong attractors: 0
- Energy non-increasing: 9/9
- Mean settling sweeps: 2.00

## Stored melodies

- `C_FIFTH_RETURN`: C → G → D → G → C
- `E_FIFTH_RETURN`: E → B → F# → B → E
- `F_FIFTH_RETURN`: F → C → G → C → F

## What this proves

It proves only the first brick: deterministic associative recall of short
stored musical patterns from a partial tone cue in this controlled test.
It does not yet prove long-song recall, audio recognition, biological memory,
or autonomous goblin behavior.
