# Clock sync protocols

Owner bench: HEX-SPLIT. Hallway picker freezes one pair. This file is the wire.

Not NTP. A follower is in sync when it can name the same
`(phase, m4_pair, lap)` just stamped, or it is in **hold**.

There is no Gate-7 noun. Stamp is stamp: propose / commit / hold / quit.

## Roles

| role | who | may |
|---|---|---|
| coordinator | hallway picker on the CPU | freeze `m4_pair`, stamp a tick, issue quit |
| proposer | Field (Dream for the `1`) | offer polarity `-1/0/+1` |
| follower | BUCKET-R2, a lock sim | copy stamped phase or hold |
| dream | GPU host | simulate; **no stamp** |

## The three hallways

Opposite pyramids. Pick **one**. Do not blur.

```
pair 0: P1 — P4
pair 1: P2 — P5
pair 2: P3 — P6
```

Changing `m4_pair` mid-lap without `stamp=commit` is a protocol fault.

## Generators

| name | step mod 12 | meaning |
|---|---|---|
| hold | 0 | polarity 0. phase frozen |
| chromatic | +1 | neighbor slot. diagnostic only |
| fourth | +5 | reverse weave |
| tritone | +6 | same pyramid, cross the flip zero |
| fifth | +7 | weave walls (default bar clock) |

Default shared generator for BUCKET bars: **+7**.

## One tick

```
if polarity == 0 or hold:
    phase stays
else:
    phase' = (phase + polarity * generator) mod 12
```

A 12-walk is one lap. A 24-walk is two laps = 4π sheet.
`lap` is `0` or `1`.

## Packet

JSON. `proto`: `one-wave-clock/1`.

Fields: `src`, `seq`, `phase`, `polarity`, `generator`, `m4_pair`, `lap`, `hold`, `stamp`, `tonic`, `slot`.

`stamp` ∈ `propose` | `commit` | `hold` | `quit`.

Only `commit` moves a follower’s phase. `propose` is gossip. `quit` forces polarity 0 on every ring that hears it.

Old wire key `gate7` is dead. Do not write it. Readers may still honor it once as `stamp`.

## Sync states (follower)

LISTEN, LOCK, HOLD, DRIFT, QUIT.

Lock rule: predicted phase from last commit using the committed generator equals the new packet phase, and `m4_pair` is unchanged.

Drift rule: do **not** chromatic-slew. Hold, or snap on the next `commit` after a `hold`.

## Hold law

- drive inside the dead belt → polarity 0, `stamp=hold`
- opposed rings → `quit` even if drive is large
- hallway picker may route a proposal. It may not override quit.

`1(0)1` is the written hold. Flip is the connected zero.

## Falsify this protocol

- Phase advances on polarity 0 or `hold=true`.
- `m4_pair` changes without `stamp=commit`.
- Follower slews chromatically to catch a fifths coordinator.
- GPU / Field packet accepted as `commit`.
- A document that needs “Gate-7” to explain a tick.

## Benches

- HEX-SPLIT owns `clock.json` + this protocol + `clock_sync.py`.
- BUCKET-R2 follows: one slot per earned bar. No speak on hold.
- Millivolt MOSFET supplies the ternary write. No extra brand.
- GRAV-LAB `M4_WALK.md` is the hallway essay this wire implements.
