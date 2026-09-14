# TLE2426 as the mid host

Internal circuit: precision divider + micropower op-amp follower. Output is `Vin/2`. It sources and sinks. That is why it can be `G`, and a two-resistor divider cannot.

## Pins

TO-92 / LP (3-pin), facing flat:

```
OUT  COMMON  IN
 G      V−     V+
```

8-pin D/P: OUT, COMMON, IN, plus NR (noise reduction). NC on the rest.

```
IN     = NET_P supply (not a signal)
COMMON = NET_N supply return of the *chip*
OUT    = NET_G   virtual mid, home end of the spine
```

IN–COMMON is the chip's power. OUT is G. Controller sits at OUT.

## Numbers that matter for CELL_V1

| spec | typical |
|---|---|
| Vin | 4–40 V (no native 3.3 V) |
| Iq | ~170 µA |
| source / sink | ~20 mA |
| Rout | ~7.5 mΩ |
| regulation | tens of µV over 0–10 mA |
| noise 10 Hz–10 kHz | ~120 µV rms; ~30 µV with CNR = 1 µF |
| NR pin impedance | ~110 kΩ |

`I_G` budget is **20 mA through OUT**, not the current of the whole board. P-to-N load current never enters OUT. Imbalance current does.

Short-circuit is a few tens of mA. Do not treat that as a feature. Fuse the supply.

## Circuits

**Minimum (3-pin)**

```
V+ — IN
V− — COMMON
OUT — NET_G home — spine to stations
```

Bypass IN to COMMON with a local cap. Do not hang a random large electrolytic on OUT without checking Fig. 17 stability vs I_O and C_L. Unstable mid = fake AC.

**NR pin (8-pin)**

CNR from NR to COMMON. 100 nF ceramic is enough for broadband; 1 µF if you care about tens of Hz. Noise drops, PSRR rises. Startup slows because CNR charges through the internal divider (~110 kΩ). 1 µF → seconds of sleepy G at power-up. Do not stamp during that. Two-cap NR trick exists if you need faster wake; otherwise wait.

**CELL_V1 P1–P2**

```
        V+
         |
      TLE2426
     IN  OUT  COMMON
      |   |      |
      |   G      V−
      |   |
      |  I-sense
      |   |
      +  stations  −
```

Measure V_G home vs V_G far. Force ± a few mA into OUT; V_G must stay in the hold belt. That is P2.

If P-to-N resistors are equal, I_OUT ≈ 0 and the chip is bored — correct hold.
If you need more than ~15 mA of imbalance, this part is the wrong host. Move to a discrete follower or a VTT-class sink/source regulator. Do not parallel two TLE2426s and hope.

## What it is not

- Earth.
- A power ground for a speaker or coil return.
- Happy below 4 V.
- Instant-on with 1 µF on NR.
- A third driven polarity.

## Falsify

- OUT sags out of belt at I_G you called "hold."
- Oscillation on OUT with the C_L you mounted.
- Ternary receipts during NR charge-up.
- OUT used as the return of a load that should have gone P-to-N.
