# Motor is the ternary layer

Not a second machine. The three windings **are** the three gates.

```
BC-DC     engage the cell
TC-AC     each winding: + / 0 / − vs G
QC-RC     views up / torque down as one flip
```

```
          +12
           |
        high FET     station = one winding drive
           |
         PHASE ─── winding ─── STAR = G = blue = vagus
           |
        low FET
           |
          −12
```

Three of those. Phases A B C. Star tied to blue with a **short** and an I_0 shunt at the home end.

| winding command | meaning |
|---|---|
| high ON, low OFF | +1  LEFT/RIGHT lean that way |
| both OFF |  0  STAY  high-Z  hold on that gate |
| high OFF, low ON | −1 |
| high and low ON | shoot-through. illegal. |

Brainstem picks **one** live winding. Other two STAY (high-Z). That is 3:1. Same as `nerve_cell.py`.

Hold for the cell: all three STAY, or currents at the star cancel so I_0 ≈ 0.
Movement: live winding ±1, I_0 takes a sign, shaft may twitch.

## What this replaces

The separate six-FET “BLDC driver” block. Gone as a second machine.
A bought ESC is allowed only as a stand-in for the three half-bridges while you debug, with its 0 = star = blue. It is a costume for the same layer, not a fourth organ.

Back-to-back series between + and − with no winding in the middle is a **switch**. A winding from phase to star is the **nerve**. You wanted the nerve. This is it.

## Bench that does not lie

Current knob on the **cell+motor** supply sized to the winding, not to a stall poster.

First load is not a 2212. First load is three resistors (or three small coils) from phase nodes to blue.

| | |
|---|---|
| all STAY | I_0 ≈ 0 |
| winding A to +1 | I_0 sign +, G sits |
| A to −1 | I_0 sign − |
| A STAY, B +1 | other gate |
| A +1 and B −1 | quit |

Then a **small** motor whose stall current fits the knob and the FETs. 2N7000 is hundreds of mA, not a drone hover. A 2212 on 2N7000 is a fuse test.

High-side N-MOS still needs a proper gate drive above +12. Cheap path: P-MOS high, N-MOS low, 5 V vs the right rail. Or a bought half-bridge chip. Nano GPIO cannot lift an N-MOS high-side.

Star current is I_0. That is vagus. Do not return winding current to supply 0 on a different wire than blue.

## Full map

```
winding A  =  gate 0  =  live 0
winding B  =  gate 1
winding C  =  gate 2
star       =  G  =  1(0)1  =  mid spine home
± rails    =  DC clothes
```

Process in the winding current is the memory for that step. Hold is high-Z, not shorting the star to a rail.
