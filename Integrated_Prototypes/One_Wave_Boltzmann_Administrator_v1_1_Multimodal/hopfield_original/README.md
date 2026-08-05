# One-Wave Hopfield Brain v2.1 Final

This is the completed Hopfield-only musical associative-memory architecture.

## What is final here

- local note ground and relational Circle-of-Fifths ground;
- five states kept separate from six mirrored directions;
- note, rhythm, temporal order, state, direction, and displacement encoding;
- overlapping songs and ambiguous cue tests;
- symmetric Hebbian memory;
- seeded asynchronous settling;
- energy descent audit;
- raw settled-state measurements;
- exact committed-attractor playback;
- false-attractor reporting;
- partial-pattern damage;
- symmetric weight damage;
- capacity sweep;
- forgetting and retraining;
- persistent JSON memory;
- autonomous playback from recalled memory.

## Important distinction

The program reports two outputs:

1. **Raw settled state**: the direct neural state after Hopfield convergence. This
   reveals interference and imperfect field reconstruction.
2. **Committed attractor**: the exact stored song selected by the settled state's
   nearest attractor basin. This is what the playback cell performs.

The committed result is never mislabeled as raw exact reconstruction.

## Run

```bash
python One_Wave_Hopfield_Brain_v2_1_Final.py --audit --out results
```

This closes the Hopfield layer. Boltzmann remains deliberately absent.
