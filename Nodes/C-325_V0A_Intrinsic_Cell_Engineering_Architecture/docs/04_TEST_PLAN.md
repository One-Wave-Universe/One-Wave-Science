# Test Plan

## Architectural pass/fail

The cell fails if it requires an external processor or clock to keep operating.

External instruments may observe only.

## Required proofs

- stable dual references;
- reliable ternary resolution;
- autonomous oscillation;
- intrinsic phase crossing;
- pass / hold / flip generated locally;
- five distinct modulation levels;
- intrinsic reinjection maintains amplitude;
- maintenance does not rewrite memory;
- deliberate rewrite changes memory;
- neighbor transfer preserves polarity, phase, and modulation;
- local handedness can flip without forcing global reversal.
