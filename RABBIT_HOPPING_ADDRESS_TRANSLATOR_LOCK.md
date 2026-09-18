# Rabbit Hopping Address Translator — Legacy Consolidated Reference

This file is retained for historical links only. The Rabbit-Hop grammar has been decomposed into the normal One-Wave node system.

Canonical ownership is now:

- **G-764** — complete reversible address packet
- **G-765** — route families and operation order
- **G-766** — opposite-parity wrapper and shared boundary
- **G-767** — route provenance and exact inverse reconstruction
- **G-768** — mirror, inversion, and traversal separation
- **G-769** — alphabet coordinate adapter
- **G-770** — bounded 1..12 / 12..24 doubling-division rail
- **G-771** — cross-domain adapter contract

Executable arithmetic remains authoritative in:

```text
One_Wave_Bench/brain/rabbit_hop_core.py
```

The old consolidated rules have not been discarded; they are distributed among those nodes so each responsibility has one owner.

## Core invariant

```text
source identity | TOP | wrapper
```

with route family, signed K, wrapper side, polarity, traversal direction, and exact reconstruction retained.

No domain adapter may duplicate the arithmetic or erase route-of-origin.

For explanatory reading, use the normal book chapters listed by G-721.
