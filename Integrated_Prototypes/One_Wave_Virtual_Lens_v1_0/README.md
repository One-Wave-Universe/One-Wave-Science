# One-Wave Virtual Lens v1.0

A runnable synthetic visual brain with its own local loop and local associative
memory. It uses no physical camera.

## What it does

- renders a 256×256 synthetic world;
- exposes only a fixed 64×64 virtual lens;
- converts local brightness differences into ON/OFF events;
- updates one persistent 256×256 internal visual field;
- maintains confidence, age, velocity, and a predicted-position field;
- continues prediction while the dot is hidden behind a wall;
- compresses local visual state into a 256-unit pattern;
- stores and reconstructs visual attractors using the same core Hopfield rules:
  symmetric Hebbian weights, asynchronous settling, energy descent, and a
  separate committed-nearest-attractor result;
- flips a low-cost reference phase every tick to confirm the local loop exists;
- reports exact RAM used by its current arrays instead of assigning arbitrary
  memory percentages;
- exports a compact visual state packet for later M4 routing.

## What it deliberately does not do

- no camera or microphone;
- no audio integration;
- no M4 operator yet;
- no Boltzmann decision coupling yet;
- no claim that visual metrics equal the five M4 pathways;
- no modification of the finished Hopfield v2.1 brain.

The exact original Hopfield package is included under `hopfield_original/` and
verified with `ORIGINAL_HOPFIELD_SHA256.txt`.

## Run

```bash
python one_wave_virtual_lens.py --out results --ticks 90
python -m unittest -v test_virtual_lens.py
```

The demo writes:

- `results/virtual_lens_demo.gif`
- `results/virtual_lens_final.png`
- `results/summary.json`
- `results/packets.json`

## Local loop

```text
synthetic world
  → limited virtual lens
  → brightness-change events
  → persistent internal visual field
  → confidence / age / prediction
  → local visual Hopfield memory
  → corrected local reference
  → repeat
```

The visual brain keeps raw sensory history local. Later, M4 should receive only
compact state packets and operate the cross-brain switchboard.
