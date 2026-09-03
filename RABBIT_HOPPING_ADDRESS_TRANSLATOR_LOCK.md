# Rabbit Hopping Address and System-Communication Translator — Locked Core

## Status

- **Locked now:** purpose, packet shape, three currently declared routes,
  mandatory wrappers, route receipts, alphabet inversion, and coupled vertical
  inversion.
- **Open:** the broader role of division. Mechanical recovery from a complete
  receipt is tested, but no larger division theory is claimed here.
- **Extension rule:** there may be more route families later. None may be
  invented, merged into these three, or declared without an explicit update.

## Purpose

Rabbit Hopping is both:

1. an addressing system; and
2. a system-communication translator.

The address packet preserves how an address was produced so it can cross a
system boundary without losing source identity, route, offset, wrapper,
orientation, polarity, or traversal direction.

## Complete packet

Every complete packet has exactly this semantic shape:

`source identity | generated top address | wrapper address`

The source identity does not become the generated number. For example, `A`
carries source rank `1` in the normal run; a packet such as `1 | 4 | 3` means
that source produced top address `4` with wrapper address `3`.

There is no bare packet and no zero-wrapper option. Every top has both wrapper
packets:

- `top - 1`
- `top + 1`

An odd top therefore has even wrappers. An even top has odd wrappers.

## The three currently declared routes

Let `N` be the source rank. Let `K` be a positive ascending step only where a
route declares it.

| Route receipt | Top-address rule | Complete packet rules | K domain |
|---|---|---|---|
| `ORIGINAL` | `N × 2` | `N | N×2 | (N×2)-1` and `N | N×2 | (N×2)+1` | none; stored as `K=0` |
| `ASCENDING_AFTER` | `(N × 2) + K` | `N | (N×2)+K | ((N×2)+K)-1` and `...+1` | `1,2,3,...` |
| `ASCENDING_BEFORE` | `(N + K) × 2` | `N | (N+K)×2 | ((N+K)×2)-1` and `...+1` | `1,2,3,...` |

`ORIGINAL` remains its own route even though substituting `K=0` into either
ascending expression can produce the same number. The route receipt is part of
the address.

For normal `A`, whose source rank is `1`:

| Route | Step | Two complete packets |
|---|---:|---|
| `ORIGINAL` | — | `1 | 2 | 1` and `1 | 2 | 3` |
| `ASCENDING_AFTER` | `K=1` | `1 | 3 | 2` and `1 | 3 | 4` |
| `ASCENDING_AFTER` | `K=2` | `1 | 4 | 3` and `1 | 4 | 5` |
| `ASCENDING_AFTER` | `K=3` | `1 | 5 | 4` and `1 | 5 | 6` |
| `ASCENDING_BEFORE` | `K=1` | `1 | 4 | 3` and `1 | 4 | 5` |
| `ASCENDING_BEFORE` | `K=2` | `1 | 6 | 5` and `1 | 6 | 7` |
| `ASCENDING_BEFORE` | `K=3` | `1 | 8 | 7` and `1 | 8 | 9` |

The two ascending routes are unbounded ladders over positive integer `K`.

## Wrappers are the connectors

Wrappers connect packets regardless of route family or traversal direction.
Top `4` carries wrappers `3` and `5`; top `5` carries wrappers `4` and `6`.
Those packets connect through each other's top/wrapper handoffs. Tops `4` and
`6` share wrapper `5`. The retained route receipt prevents equal numeric tops
from erasing how they were reached.

## Alphabet orientation and coupled inversion

The alphabet can be traversed in either orientation:

| Orientation | Rank run | Original-route endpoints |
|---|---|---|
| normal | `A→Z` carries `1→26` | `A` produces top `2`; `Z` produces top `52` |
| inverted | `Z→A` carries `1→26` | `Z` produces top `2`; `A` produces top `52` |

Whole-run Mirror Gate layouts are `A-Z(0)Z-A` and `Z-A(0)A-Z`. Zero sits
between whole alphabet runs, not inside a letter packet.

Side-to-side alphabet inversion also inverts logical up/down. On the normal
axis, a top `2` has logical lower wrapper `1` and upper wrapper `3`. On the
inverted axis, top `2` has logical lower wrapper `3` and upper wrapper `1`.

These receipt fields stay distinct:

- alphabet orientation: normal or inverted;
- vertical wrapper side: logical lower or upper, coupled to orientation;
- polarity: positive or negative numeric mirror;
- traversal direction: forward or reverse route order;
- route family and `K`.

Reversing traversal does not silently change polarity, route family, or `K`.

## Division boundary

The implementation can mechanically remove a recorded wrapper and recorded
offset, then divide the doubled value to verify the source rank. This is only a
receipt-integrity check. The larger job of division in Rabbit Hopping remains
explicitly unresolved and must not be presented as locked theory.

## Executable lock

The reference implementation is
`One_Wave_Bench/brain/rabbit_hop_alphabet.py`. Regression tests are in
`One_Wave_Bench/brain/test_rabbit_hop_alphabet.py` and lock:

- all three route families;
- positive ascending `K` ladders;
- both mandatory wrappers for every top;
- opposite top/wrapper parity;
- connections within and across route families;
- normal and inverted alphabet endpoints;
- coupled side-to-side and up/down inversion;
- independent polarity and traversal receipts;
- mechanical receipt recovery without claiming a division theory.

