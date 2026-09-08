# Rabbit-hop translator variants and signed XY atlas

User handoff, 2026-09-08. These are **system translation/addressing** proposals. Read the unchanged `RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md` for accepted runtime behavior. Original wording is preserved in [source.txt](source.txt).

Open [atlas.html](atlas.html) directly: no server, model, network or dependency is required. Select the 26-letter or 12-label domain, every route, K=1..1000, normal/inverted orientation, forward/opposing traversal, and intersection overlay. Both negative and positive coordinates appear in every view. Hover points, expand the complete table, or export SVG/CSV. The generated exact-fraction corpus covers 120 views for K=1/2/3 (duplicate K choices for fixed routes excluded). This is finite display coverage of unbounded K ladders; it is not a claim to enumerate infinity.

## Families preserved

| Family | Top | Wrapper candidates | Status |
|---|---|---|---|
| Original/even up | 2N | 2N−1, 2N+1 | existing locked route |
| Odd up | 2N+1 | 2N, 2N+2 | label for ASCENDING_AFTER K=1, not a fourth locked route |
| Ascending after | 2N+K | (2N+K)±1 | existing lock; K=1,2,3,… |
| Ascending before | 2(N+K) | 2(N+K)±1 | existing lock; K=1,2,3,… |
| Halve | N/2 | N/2±1 shown as candidates | bare N/2 preserved as calculation, not complete packet |
| Subtract then halve | (N−K)/2 | ((N−K)/2)±1 | user-clarified division family |
| Halve then subtract | N/2−K | (N/2−K)±1 | separate operation order |

The Python companion uses exact fractions. Rational coordinates have no parity until integral; do not coerce them into the locked 12–24 integer-address return rail. Do not silently replace the rail's odd-address neighboring-source logic with these exploratory formulas. `(N−K)/2` and `N/2−K` are not interchangeable. The literal `N−K/2` parse was discarded after the user's clarification: subtract and divide are ordered like the multiplication families. Equal destinations still retain route/K/source/orientation/wrapper metadata.

## Graph conventions and transforms

For each source rank N, X = sign×N, Y_top = sign×top(N), Y_wrapper = sign×(top(N)+orientation_sign×logical_side). Sign is ±1; normal orientation_sign=+1, inverted=−1; logical_side is lower=−1 or upper=+1.

Alphabet labels run A..Z normally and Z..A inverted. The **display adapter** for 12 chromatic labels runs A,A#,B,C,C#,D,D#,E,F,F#,G,G#; reverse puts A at source rank 12. This makes no tuning/frequency or Circle-of-Fifths claim. Source identity is not its doubled top: A at rank 1 can produce top 2 or 3; inverted A at rank 26 can produce 52, etc.

Polarity changes sign of the complete packet. Alphabet inversion couples logical upper/lower. Opposing reverses traversal order while retaining coordinates and receipts. Intersecting means actual shared plotted XY points; it is a relation between routes, not a newly defined SCLFS transform. These display conventions do not settle SCLFS INVERT/OPPOSE/ROTATE or physical mirror behavior.

The eight horizontal rails render the supplied whole runs: A–Z(0)Z–A, Z–A(0)A–Z, G#–A(0)A–G#, A–G#(0)G#–A, 1–26(0)26–1, 26–1(0)1–26, 1–12(0)12–1, 12–1(0)1–12. On these label layouts, left is negative and right positive; do not confuse whole-run label order with the packet plot's X=source rank convention.

## Corrections and interpretation record

The user explicitly corrected odd-up B to `(2,5,6)` and asked us to map the intended pattern rather than reproduce typos. The working atlas therefore consistently uses both ±1 wrappers. Original wording remains unchanged in source.txt as provenance, not competing executable authority.

| Original example | Existing ±1 grammar comparison |
|---|---|
| `1 2 -1` and `-1 -2 1` | normalized by the clarified ±1 pattern to (1,2,1) and (−1,−2,−1); this follows the existing lock |
| “A is 3 would get a 2 and 3 wrapper” | normalized to 3→2/4, matching the later explicit packets |
| odd B `2 5 4`, `2 5 3` | explicitly corrected by user: (2,5,4) and (2,5,6) |
| `N-1/2`, `N-2/2` | clarified as (N−K)/2, each followed by ±1; N/2−K stays its separate stated family |
| `(1)2-25(26)25-2(1)…???` | tentative endpoint bounce shown as a proposal, not a locked periodic closure |

The tentative loop has step-index X and rank Y; it is not a new signed-axis law. Circle of Fifths is pending separate source material; none is invented here.

## Complete inverse mapping

Undo polarity and logical wrapper first: T = sign×Y_wrapper − orientation_sign×logical_side. Then recover N with the recorded family:

| Family | Recover N |
|---|---|
| 2N | T/2 |
| 2N+1 | (T−1)/2 |
| 2N+K | (T−K)/2 |
| 2(N+K) | T/2−K |
| N/2 | 2T |
| (N−K)/2 | 2T+K |
| N/2−K | 2(T+K) |

The counterpart identity is `(N−2K)/2 = N/2−K`, just as `2N+2K = 2(N+K)`. Equal answers are distinct routes. Multiplication gives integer centers; halving an odd N gives a half-integer center and half-integer ±1 wrappers. An integer down-axis connection requires an additional declared projection or the existing bounded odd-address rule; no rounding is inferred. Parity alternates across K in 2N+K; 2(N+K) remains even. Negative signs do not change integer parity.

## Reproduce

```bash
python3 -m unittest discover -s docs/rabbit_hop_variants -p 'test_*.py' -v
python3 docs/rabbit_hop_variants/translator_variants.py
```

The second command generates `atlas-data.json`, the complete exact-fraction packet corpus for every nonduplicate selector combination. This output is reproducible and need not be committed. The existing alphabet and scale-rail test suites must also remain passing. Numerical translator identities are software tests, not proof of universal or physical translation.
