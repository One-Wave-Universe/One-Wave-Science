# Rabbit Hopping — Chapter 5
# Scheduling Rabbit Hops Without Replacing Choice

G-721b4 is a scheduler, not a dictator.

A validated Sturmian token may present a lower or upper Rabbit-Hop branch at each step. The live system still retains its own control layers.

```text
source / current state
-> declared Rabbit-Hop anchor
-> Sturmian token proposes lower or upper branch
-> live -1(0)+1 choice
-> validation / safety / current reference
-> action, hold, or rejection
-> receipt
```

This separation lets us compare schedulers honestly.

Test the same target task with:
- periodic branch switching;
- random switching;
- Sturmian switching;
- learned switching.

Then compare measurable consequences such as coverage, recurrence, balance, stability, error, or task performance.

If Sturmian scheduling is useful, that should appear in the measurement. The mathematics itself does not guarantee a better motor controller.
