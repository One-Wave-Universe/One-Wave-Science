# CELL_V1 bench — the actual board

5–12 V. Current-limited supply. If it is not limited, do not turn it on.

## Buy

| qty | what | why |
|---|---|---|
| 1 | bench supply with a current knob, or a 9 V brick + 100 Ω series + fuse | cap the fault |
| 1 | TLE2426CLP or TLE2426CP | mid host |
| 1 | solderless breadboard + hookup wire |
| 2 | 10 kΩ 1% resistors | + to G and − to G |
| 2 | 100 Ω resistors | drain series, so a short does not dump the brick |
| 2 | small N-MOSFET same date code (2N7000 / BS170 class) | one bilateral pair |
| 2 | 10 kΩ | gate pulldown to common source |
| 1 | 0.1 µF ceramic | IN–COMMON on the TLE |
| 1 | DMM that can read mA |
| 1 | scope if you have one; DMM if you don't |

Do not buy a drone motor yet. Do not buy a coil pack. Mid first.

## Wire — night 1 (no FETs)

```
SUPPLY+ ── IN(TLE) ── 10k ── OUT(TLE) = G = breadboard rail labeled 0
SUPPLY− ── COMMON(TLE) = breadboard rail labeled −
SUPPLY+ also = breadboard rail labeled +

+ ── 10k ── G
− ── 10k ── G

0.1 µF from IN to COMMON
```

Set supply to 9 V. Current knob ~50 mA.

Measure, black probe on G:

- V+ should be about +4.5 V
- V− should be about −4.5 V
- current in/out of OUT should be near 0 (hold)

Unplug one 10 k. Current appears at OUT. V_G should barely move. That is lean.
Plug it back. Current dies. That is hold.

If OUT sags more than a few tens of mV under that swap, stop. Mid is not Ground.

## Wire — night 2 (one station at G0)

```
+ ── 100 Ω ── D1
                    S1 ══ S2     common source = gate-return
− ── 100 Ω ── D2

G1 and G2 tied. 10 k from gates to common source (OFF).
To turn ON: 5 V from common source to gates (n-MOS). Not 5 V to earth.
```

OFF: same tests as night 1. No 0.7 V path either way (DMM diode mode D1↔D2 both ways should not look like a single diode).
ON: lean test still works; current now also has a 2 Rds path if you add a load + to − through the pair.

Do not PWM yet. Do not add G+ or G−. Do not add a coil.

## What "it works" means on this board

- G sits at Vin/2
- equal 10 k → I_OUT ≈ 0
- one 10 k pulled → I_OUT takes a sign, G stays
- pair OFF does not clamp at 0.7 V
- pair ON does not walk G when the 10 k are equal

Write those five numbers on paper. That is the receipt.

## After that (not tonight)

Copy the station twice (G+, G−). Star every mid tap to G. Then a small AC on top of DC. Then a sense coil. Then, and only then, a small 3-winding actuator whose currents stay under the 20 mA mid budget *or* whose winding returns do not use the TLE as the motor ground.
