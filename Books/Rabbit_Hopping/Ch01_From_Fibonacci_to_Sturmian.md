# Rabbit Hopping — Chapter 1
# From Fibonacci to Sturmian

G-721a gives one fixed Fibonacci-word regression path. G-721b asks the more general question: what happens if the branch trace comes from the full Sturmian family rather than one fixed word?

The important move is **not** to change Rabbit-Hop arithmetic. G-721 keeps the coordinates. G-721b supplies an ordered binary branch trace.

A Sturmian trace is useful because it can be nonperiodic while remaining highly balanced. That makes it a clean test scheduler: more structured than random switching, less repetitive than a periodic alternation.

The architecture is:

```text
Rabbit-Hop source/address
+ declared anchor generation
+ Sturmian branch token
= one scheduled branch receipt
```

The token is not live choice. It is a route grammar presented to the live system.

Next: Chapter 2 defines the token generator itself.
