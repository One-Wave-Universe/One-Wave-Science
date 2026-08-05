# One-Wave Boltzmann Administrator v1.1 Multimodal

This build locks down the **compressive six-line Boltzmann Administrator** while
preserving the complete **Hopfield Brain v2.1** unchanged.

## What is alive in this package

- A joint Restricted Boltzmann Machine over five NEW-up and five OLD-down signed pathways.
- The six-line chain: `4 tells 5 → 5 tells 6 → 6 tells everybody`.
- Constant reference-loop feedback for at least 1,200 tested cycles.
- Waking, daydream, and dream-sleep temperatures.
- External-output inhibition during daydream and dream sleep.
- A Goblin survival arena comparing the learned Administrator against random action.
- A five-bank multimodal Hopfield companion for mixed memory recall.

## Five equal memory reserves

Every stored multimodal attractor reserves exactly 20% for each representation:

1. internal dialogue / language-like trace
2. sound / rhythm / auditory abstraction
3. image / spatial scene
4. body pressure / breath / interoceptive state
5. movement / gaze / proprioceptive trace

The **reserved storage remains 20/20/20/20/20**. Live recall does not have to be
equal. A dialogue-heavy or sound-heavy system can dynamically allocate more
attention there while faint imagery remains available instead of being deleted.

This distinction matters:

- **reserved capacity** protects every kind of memory;
- **live attention** describes what dominates the current internal experience.

## Hopfield preservation

The original `One_Wave_Hopfield_Brain_v2_1_Final.py` is included under
`hopfield_original/` and is hash-checked against the supplied source. It is not
rewritten, summarized, or replaced. The multimodal attractor is a companion
layer around it.

## Important architectural boundary

The five memory banks are **not yet declared identical to the five M4 pathways**.
M4 is the later fast subconscious operator that will mix, route, inhibit, and
release these memory forms according to State, Scale, Caution, Drive, timing,
and the think-before-speaking gate.

## Run all tests

```bash
python -m unittest -v test_boltzmann_administrator.py test_multimodal_memory.py
```

## Run the Boltzmann audit

```bash
python one_wave_boltzmann_administrator.py --audit --out results
```

## Run the multimodal memory audit

```bash
python run_multimodal_audit.py
```

## Current audit result

- Boltzmann held-out action accuracy: 83.56%
- Constant reference loop: 1,200 cycles passed
- Goblin survival: 40/40 Boltzmann runs vs 20/40 random runs
- Multimodal recall: 3/3 damaged-cue cases correct
- Recall without visual input: passed
- Recall from dialogue plus body-pressure input only: passed
- Original Hopfield v2.1 source hash: preserved exactly
