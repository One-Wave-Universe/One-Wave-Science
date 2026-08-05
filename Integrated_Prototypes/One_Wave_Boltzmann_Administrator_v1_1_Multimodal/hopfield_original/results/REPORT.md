# One-Wave Hopfield Brain v2 Complete Audit

## Scope

Hopfield-only musical associative memory. No Boltzmann system is included.

## Core results

- Stored songs: 6
- Pattern vector size: 656
- Recall trials: 12
- Correct attractors: 11/12
- Raw fully exact note/rhythm/state patterns: 1/12
- Committed exact stored patterns: 11/12
- False attractors: 1
- Energy non-increasing: 12/12

## Ambiguity

- Shared one-tone cue correct: 1/2
- Same cue plus one context slot correct: 2/2

A shared single tone is inherently ambiguous when multiple stored songs use it.
The audit therefore reports ambiguity rather than pretending one note uniquely identifies
every song. One additional contextual slot is tested as the disambiguating cue.

## Damage and persistence

- Damaged-pattern recall: 6/6
- Persistence round-trip: True
- Forget/retrain test: True

### Symmetric weight damage

| Weight loss | Correct attractor | Full exact | Exact notes | Overlap |
|---:|:---:|:---:|---:|---:|
| 1% | True | False | 6/8 | 0.826 |
| 3% | True | False | 6/8 | 0.838 |
| 5% | True | False | 6/8 | 0.826 |
| 10% | True | False | 6/8 | 0.835 |

## Capacity sweep

| Patterns | Correct attractors | Exact patterns | False attractors |
|---:|---:|---:|---:|
| 2 | 2 | 2 | 0 |
| 4 | 4 | 0 | 0 |
| 6 | 6 | 0 | 0 |
| 8 | 8 | 0 | 0 |
| 10 | 10 | 0 | 0 |
| 12 | 12 | 0 | 0 |

## Architecture included

- local pitch ground;
- relational Circle-of-Fifths ground;
- five states kept separate from six mirrored directions;
- note, rhythm, state, direction, and ground-displacement fields;
- symmetric Hebbian weights with zero diagonal;
- seeded asynchronous settling;
- Hopfield energy audit;
- false-attractor reporting;
- forgetting and persistence;
- weight-matrix damage;
- autonomous playback from the recalled attractor.

## Deliberate boundary

This completes the Hopfield-only architecture layer. It does not claim arbitrary
audio recognition, unlimited song capacity, biological equivalence, or a
Boltzmann reconstruction layer.
## Performance note

A 50-seed asynchronous-update-order stress test was attempted, but the dense 656-node pure-Python weight matrix exceeded the execution window. The default architecture audit completed successfully. This is a performance limitation of the reference implementation, not a missing Hopfield feature. A NumPy or sparse-matrix backend should be used before large repeated sweeps.
