# Wave Computing Node v1

Experimental software model of the working multi-radix cycle:

**BC-DC -> TC-AC -> 4 Actions -> 4 Views -> TC Return -> BC Closure**

## What this version fixes

- preserves the sign of the ternary motion instead of using `abs()`;
- keeps the four Actions and four Views as separate quadratic states;
- gives each octave/scale its own moving reference;
- evaluates a ternary return state after the quadratic layer;
- keeps binary closure binary: return `0` means the closure gate does not fire (`HOLD`);
- passes a signed differential packet into the next octave so scales can diverge.

## Important status

This is a software experiment / falsifiable model. It is **not** proof that a physical circuit will automatically implement the same dynamics.

## Run

```bash
python wave_computing_node.py
```

Requires NumPy.
