# One-Wave Hopfield Melody Cell v1

This is the first strict associative-memory brick.

## What it does

It stores three five-note melodies in a Hopfield weight matrix. A single cue
tone activates the cell, unknown melody fields begin at the grounded hold state
`0`, and seeded asynchronous settling reconstructs the complete pattern.

The stored pattern includes:

- distributed pitch identity;
- ordered note position;
- signed Circle-of-Fifths displacement from tonic ground;
- one cue-tone field.

## Run

```bash
python One_Wave_Hopfield_Melody_Cell_v1.py --out results
```

Custom five-note melodies can be supplied as JSON:

```json
{
  "MELODY_A": ["C", "G", "D", "G", "C"],
  "MELODY_B": ["E", "B", "F#", "B", "E"]
}
```

```bash
python One_Wave_Hopfield_Melody_Cell_v1.py \
  --melodies melodies.json \
  --out results
```

## Audit tests

1. One cue tone with every other melody slot unknown.
2. Middle-note deletion.
3. Two internal-note deletions.

The program reports exact sequence recall, nearest attractor, wrong-attractor
count, settling sweeps, overlap, and whether Hopfield energy stayed
non-increasing.

## Deliberate limits

This version has no Boltzmann sampling, no microphone input, no full audio
waveform recognition, and no goblin survival world. It establishes the memory
kernel first, because piling unfinished systems together is how software becomes
an archaeological site.
