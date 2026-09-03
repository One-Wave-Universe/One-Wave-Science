# Branch Step — Rabbit Hopping Address Translator Lock

## Intent

Correct and lock the Rabbit Hopping core as an addressing system and a
system-communication translator. Preserve the original route plus both
ascending operation-order routes, require the two `±1` wrappers on every top,
and couple alphabet inversion to vertical inversion.

## Starting point

- Base branch: `main`
- Base commit: `524fb05223be600aae2566a7c1ee5c3c8b6db52c`
- Working branch: `state-machines/rabbit-hop-full-ladders`

## Allowed files

- `RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md`
- `AI_CANONICAL_START_HERE.md`
- `AI_Readable_Packs/G-721_Mirrored_Alphabet_Rabbit_Hop.json`
- `ARCHITECTURE_RABBIT_HOPPING_SCALE_TRANSLATOR.md`
- `Nodes/G-721_Mirrored_Alphabet_Rabbit_Hop_Coordinate_Algorithm.md`
- `ONE_WAVE_TERMINOLOGY_LEGEND.md`
- `UPDATED_28_ALPHABET_FIBONACCI_WORD_VALIDATION.md`
- `One_Wave_Bench/brain/README.md`
- `One_Wave_Bench/brain/rabbit_hop_alphabet.py`
- `One_Wave_Bench/brain/test_rabbit_hop_alphabet.py`
- `One_Wave_Bench/brain/constellation_memory.py`
- `One_Wave_Bench/brain/test_constellation_memory.py`
- this branch-step receipt

## Locked acceptance criteria

1. Rabbit Hopping is named as both addressing and system communication.
2. Exactly three current routes are explicit: original `N×2`, ascending-after
   `(N×2)+K`, and ascending-before `(N+K)×2`.
3. `K` begins at `1` on both ascending routes and can continue upward.
4. Every complete packet contains source, top, and one mandatory `±1` wrapper;
   both wrapper choices are generated for every top.
5. Wrappers connect tops across route family and traversal direction.
6. Alphabet runs support `A→Z:1→26` and `Z→A:1→26`.
7. Alphabet inversion also inverts logical up/down wrapper orientation.
8. Division beyond mechanical receipt recovery remains explicitly open.
9. Tests fail on route collapse, missing wrappers, bad parity, or bad inversion.

## Validation

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s One_Wave_Bench -p 'test_*.py'
python -m json.tool AI_Readable_Packs/G-721_Mirrored_Alphabet_Rabbit_Hop.json >/dev/null
```

