# Rabbit-Hop Executable Core

This directory is the executable owner for generic rabbit-hop route arithmetic.

Rabbit hopping is a **reversible relational addressing / scale-route mechanism**. It is not the memory store, not Hopfield completion, not Boltzmann fill, not a motor command, and not a physical-law proof.

## Canonical grammar

Two operation-order families remain distinct:

```text
DOUBLE_FIRST:  R_after(N,m)  = 2N + m
SHIFT_FIRST:   R_before(N,m) = 2(N + m)
```

The same numerical destination may be reached by different routes:

```text
2N + 2m = 2(N + m)
```

The receipt retains the route family, so numerical equality does not erase path identity.

A selected center `X` may be wrapped:

```text
X-1, X, X+1
```

and mirrored by polarity:

```text
address = p * (X + s)
p in {-1,+1}
s in {-1,0,+1}
```

Mirroring changes polarity only. Opposing traversal changes traversal identity only. Alphabet inversion is handled by the alphabet adapter and is a third separate operation.

## Files

- `route_core.py` — generic reversible arithmetic and receipts.
- `test_route_core.py` — round-trip, parity, shared-boundary, route-identity, sign-mirror, opposition, corruption, and large-offset tests.
- `../brain/rabbit_hop_alphabet.py` — A..Z / G-721 adapter over this core.
- `../../RABBIT_HOPPING_CANONICAL.md` — repository-wide entry point and inventory.

## Run

```bash
python -m unittest One_Wave_Bench.rabbit_hop.test_route_core -v
python -m unittest One_Wave_Bench.brain.test_rabbit_hop_alphabet -v
```

## Current executable guarantees

The core currently checks that:

1. both route families invert to the original `N` when their receipt is supplied;
2. the `-1/0/+1` wrapper is not silently discarded;
3. adjacent shift-first nests retain the shared boundary `2N+1 = 2(N+1)-1`;
4. positive and negative routes are exact sign mirrors;
5. opposing traversal is not confused with mirroring;
6. equal destinations reached by different operation orders retain different receipts;
7. corrupted receipts fail visibly;
8. the offset is not given an arbitrary finite cap.

The next integration test is memory reconstruction: use these exact route receipts inside a damaged-constellation rebuild, then compare reconstruction against exact archive history and a no-rabbit-hop baseline.
