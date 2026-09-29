# Proof ledger — Rabbit Hopping arithmetic grammar

Date: 2026-09-29
Status: GREEN for the locked N-based translator arithmetic only.
Physical / neural / astrophysical claims remain YELLOW and are not upgraded by this file.

Reference:
- `ARCHITECTURE_RABBIT_HOPPING_SCALE_TRANSLATOR.md`
- executable suite: `scripts/rabbit_hop_proofs.py`

## What is proved

Exact-integer identities for the declared route families, wrappers, inversion, sign mirrors, receipt distinction, and inverse recovery.

| # | Claim | Result |
|---|---|---|
| 1 | Both families generate complete packets for N=1..26 and offsets 0..5 | PASS |
| 2 | `2N + 2m = 2(N+m)` exactly | PASS |
| 3 | Every ±1 wrapper has opposite parity to its center | PASS |
| 4 | Adjacent nests share `2N+1 = 2(N+1)-1` | PASS |
| 5 | Positive and negative routes are exact sign mirrors | PASS |
| 6 | `N_inv = 27-N` maps A↔Z, B↔Y, and is involutive | PASS |
| 7 | Inverse division reconstructs original N after wrapper/offset removal | PASS |
| 8 | Equal destinations from after vs before keep distinct receipts | PASS |
| 9 | Opposing reverses wrapper side without silently flipping sign | PASS |
| 10 | Wrong wrapper, offset, or family fails reconstruction visibly | PASS |

Command:

```bash
python3 scripts/rabbit_hop_proofs.py
```

Expected last line:

```text
10/10 proofs held
```

## What is not proved

- Point/Path/Field correspondence in a physical domain
- Superfluid-lattice gravity or dark-matter claims
- Hopfield / musical / motor mappings
- Division as a general physical operator (still open in the architecture note)
- Universality across every system

Those remain hypotheses until domain-specific mappings and falsification tests exist.

## Receipt law restated

Equal destination ≠ equal route.

A complete packet is `N | X | X±1`. Bare `N | X` is incomplete.

Mirrored (sign), inverted (`27-N`), and opposing (reverse traversal) stay three different operations.

## Next permitted proof steps (not done here)

1. Word-level Fibonacci / Sturmian branch grammar (G-721a / G-721b) as a separate suite.
2. Nested Point→Path→Field handoff with parent receipts retained across one scale hop.
3. Domain mapping test that can fail: one measured system, one declared hop, one visible miss.
