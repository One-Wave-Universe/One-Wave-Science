# One-Wave Physics Engine

Canon wave/field mathematics made runnable and tested — **not particle
physics**. See `PROJECT_SPECIFICATION.md` for scope and the working
relationship with `Council_Chamber`.

## Run the tests

```bash
cd Physics_Engine/python
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
pytest -q
```

## What's here

- `physics_engine/harmonic_mirror.py` — the Update 46 harmonic mirror
  system (`harmonic_packet`, `alphabet_packet`, `DrivenMirror`),
  implementing `UPDATED_46_CONTINUOUS_MIRROR_HEARING_AND_ROTATION_CANON.md`
  sections 2 and 5 exactly. Folded in from
  `Updates/Update_46/harmonic_mirror_reference.py`, the reference
  implementation shipped with the canon update itself.
- `tests/test_harmonic_mirror.py` — 10 tests asserting the canon
  document's own worked examples (`A- = 1,4,3`, `A+ = 1,4,5`,
  `C- = 3,8,7`, `C+ = 3,8,9`, ...), the shared-boundary identity
  `H+(n) = H-(n+1)`, and the fixed two-unit mirror width invariant held
  at every step of a 1000-step driven run — not just checked once.

## Working on this from Council_Chamber

```bash
cd Council_Chamber/python
python3 -m council_chamber.tui
```
```
council> create-room physics ../../Physics_Engine/python
council> open codex
council> files
council> cat physics_engine/harmonic_mirror.py
council> propose Codex physics_engine/alphabet_wheel.py "..." --desc "section 4 four-wheel system"
```

Any seat opened in that room can read this project's real files
(`files`, `cat`), propose real changes, and have them tested with a
real `pytest` subprocess against this actual code — the same
propose/approve/test loop as everything else in Council_Chamber,
pointed at this project instead of a scratch directory. Use `branch
physics physics-sandbox` first to try something risky without touching
this project's real files until it's proven.
