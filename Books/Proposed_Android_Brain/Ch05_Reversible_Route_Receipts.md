# Proposed Android Brain — Chapter 5
# Reversible Route Receipts

The old G-721 monolith mixed address arithmetic, alphabet labels, parity, inversion, sequence scheduling, and movement interpretation. Those jobs are now separated into normal nodes G-764 through G-771.

For the Android architecture, the important object is the **receipt**:

```text
source
-> route family
-> signed K
-> TOP
-> lower/upper wrapper
-> polarity
-> traversal
-> resulting address
```

A movement scheduler may propose a route, but the route does not replace live choice or sensor correction.

The receipt matters because the machine must be able to answer:

- Where did this route come from?
- Which operation order produced it?
- Which side of the wrapper was used?
- Was the route mirrored, inverted, or merely traversed backward?
- Can the source be reconstructed exactly?

G-721b and its sequence-family children sit above this receipt layer as candidate schedulers. They choose ordered branch proposals; they do not redefine the address arithmetic.

That makes route memory reconstructive rather than a pile of anonymous destinations.
