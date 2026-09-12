# G spine mechanics

G is not a ground pour you dump returns into. It is the **organizing reference** and the **only home** for leftover current.

```
station tap ─ local G ─ ring ─ SPINE ─ I_0 shunt ─ supply 0 / TLE OUT
```

The spine is one conductor. Low resistance. No series C. No speaker or motor return except leftover that *could not* cancel in a pair.

## What rides it

- Reference: every station restates ± vs this wire (free update).
- Imbalance: I_0 = what the pairs did not cancel.
- Not: winding current of a balanced push-pull, not USB 5 V return if you can star that separately, not scope earth.

If I_0 is fat at STAY, a tap is using the spine as a sewer.

## Geometry

Star: each tap has its own short jumper to the spine. Daisy-chain around the rim adds inductance and a voltage gradient so two “G” points disagree — fake lean.

Stack: rings tap the *vertical* spine the same way. Height is length. Keep it short. One meter at the controller end. Optional per-floor shunt if Void must see which floor spoke.

## Stiffness

Dual ±12: spine *is* the 0 post. Stiff.
9 V + TLE2426: spine is OUT, ~20 mA. Then the spine cannot swallow motor current. F0 only, or a stronger buffer.

Voltage along a skinny spine: IR drop looks like lean. Thick short wire, or I_0 is a lie.

## Law

Referenced at every step = touch local G, which is a tap of this spine.
Reinjection lives in the cell (leftover B), not as charge stored *in* the spine.
Void reads I_0 at the home end. That is vagus for the whole stack.
