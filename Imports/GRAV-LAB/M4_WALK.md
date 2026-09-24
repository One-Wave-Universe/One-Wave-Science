# M4 polarity walk

M4 is not memory. M4 picks the **jamb** and walks polarity along it.
G-724: center-origin, dual six-gate, Gate-7 commit on CPU. Mirror = phase rotation, never an ontology-side swap.

## What walks

Polarity ≠ Field/Void.

```
field_void     what the site is
polarity       which way a write is allowed to face
M4             which axis-pair is the hallway this tick
hold (0)       no walk
```

Three possible hallways (HEX opposite pyramids):

```
pair 0:  P0 — P3
pair 1:  P1 — P4
pair 2:  P2 — P5
```

`header.m4_pair` freezes one hallway so 3, 6, 12 stay lined up across floors.
You may *step* which pair is active. You may not blur two pairs into one route.

## One tick

Clock is 12 = face×flip of the six.

```
phase' = (phase + polarity) mod 12
```

- polarity `+1` — walk toward the high face of the frozen pair
- polarity `-1` — walk toward the opposite / flip
- polarity `0`  — sit. phase does not advance. hold belt.

Even phase = face note of the current pyramid.
Phase `+6` = flip of that pyramid (tritone, STI / conjugate).

A full 12-walk is one clock lap. A 6-walk is face-only, no sheet change.
A 24-walk (two laps) is the 4π sheet: same facing, other wind (`q` vs `-q`).
POINT-SPIN: six 60° steps = 2π = minus sheet. Twelve 60° steps = 4π = plus sheet.

## Dual six-gate

Two rings share one M4:

```
      1             1'
    6   2         6'  2'
      M4    —       M4     (same coordinator, two bodies)
    5   3         5'  3'
      4             4'
```

G-724 Gate-7 = CPU-committed coupling of the two complete six-gates.
That *is* TwoRubiks admin: if the two rings scream opposite at full volume, polarity becomes `0`. Walk stops. Quit.

NPU: fast propose (Down/Stay/Up).
GPU: dream / Field sim — no vote.
CPU: receipts, safety, Gate-7 commit.

Binary memory roles (permission / block / stop / isolate) may *forbid* a walk. They do not choose the hallway.

## Walk along the scale jambs

Frozen pair is the core `3`.

```
polarity on pair     →  which of 6 neighbors gets the write     (1:6)
face vs flip         →  which of 12 clock slots                 (1:12)
octave step          →  L,R divide, 1(0)1 stays                 (12←24)
```

Parent write is multiply: `q_parent * q_child` along the current polarity.
Conjugate is the flip slot, not a different particle.

If parent*child and child*parent never differ on a lock receipt, order was decoration — walk had no hallway.

## Hold law

Same as `gate.py` and `parent_lock.py`:

- |drive| < dead → polarity 0, phase frozen
- |facing| and |spin| in belt → spin damps, walk over
- admin opposed rings → polarity 0 even if drive is large

M4 can route a *proposal*. It cannot override quit.

## Falsify

- Phase advances on polarity 0.
- Pair index changes mid-lap without a Gate-7 commit.
- Mirror implemented as swapping Field/Void instead of rotating phase.
- 2π and 4π land on the same `q` (sheet dropped).
- Fast NPU loop commits without CPU Gate-7 when two six-gates disagree.
