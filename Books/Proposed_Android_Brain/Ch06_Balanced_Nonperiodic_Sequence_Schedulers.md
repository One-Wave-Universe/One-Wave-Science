# Proposed Android Brain — Chapter 6
# Balanced Nonperiodic Sequence Schedulers

This chapter integrates the G-721b Sturmian family into the normal Android-brain architecture.

## 1. Why a sequence scheduler exists

The reversible route receipt is owned by G-764 through G-771. A scheduler sits above that receipt and proposes an ordered sequence of branch choices. It must not redefine address arithmetic or replace live choice.

G-721a supplies one fixed Fibonacci-word regression route. G-721b generalizes the two-branch scheduler to the Sturmian family.

## 2. Mechanical-word generator

For irrational slope `alpha` and intercept `rho`:

[
b_t=lfloor(t+1)alpha+hofloor-lfloor talpha+hofloorin{0,1}.
]

The token is only a branch symbol.

With declared source `n_t` and declared anchor generation `j_t in {0,1}`:

[
e_t=2(n_t+j_t)
]

[
o_t=e_t+(2b_t-1).
]

So `0` selects the lower wrapper and `1` selects the upper wrapper around the declared anchor.

## 3. Validation before use

A trace is not called Sturmian merely because it looks irregular.

For the infinite mathematical object:

[
p(m)=m+1.
]

Finite receipts must report the tested range, factor complexity, balance, recurrence gaps, period search, and empirical symbol frequency.

## 4. Keep transformations separate

- mirror changes coordinate sign;
- reverse changes traversal order;
- complement changes token identity.

None implies the others.

## 5. Scheduler, not dictator

The correct control chain is:

```text
current state
-> reversible route receipt
-> sequence scheduler proposes branch
-> live choice / sensory correction / safety
-> action, hold, or rejection
-> retained receipt
```

Compare Sturmian scheduling against periodic, random, and learned controls on the same task. Use measured performance rather than assuming the mathematical structure is automatically better.

## Canonical nodes

- G-721b parent Sturmian contract
- G-721b1 generator
- G-721b2 validation
- G-721b3 mirror/reverse/complement separation
- G-721b4 Rabbit-Hop branch scheduler
