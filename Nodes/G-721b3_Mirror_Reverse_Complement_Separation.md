---
node_id: "G-721b3"
canonical_name: "Mirror Reverse Complement Separation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Route Identity / Anti-Collapse Rule"
claim_gate_detail: "Locked separation rule inside G-721b; implementation still requires receipt tests"
metadata_standard: "I-06"
---

# Node G-721b3: Mirror Reverse Complement Separation

## Parent
G-721b Sturmian Binary Branch Grammar.

## Purpose
Prevent three different operations from collapsing into one another.

### Coordinate sign mirror
[
(n,r)mapsto(-n,-r).
]

### Route reversal
[
(b_0,ldots,b_{N-1})mapsto(b_{N-1},ldots,b_0).
]

### Token complement
[
bmapsto1-b.
]

No one of these operations implies either of the other two.

## Receipt rule
A route receipt must separately preserve:
- sign / polarity;
- traversal direction;
- token value;
- token convention;
- Rabbit-Hop anchor generation and wrapper metadata supplied by G-721.

## Failure condition
Any implementation that changes sign and silently reverses traversal, complements tokens during reversal, or infers mirror side from token identity fails this node.
