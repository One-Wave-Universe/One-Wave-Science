# CELL_V1 Physical Netlist

Companion to `../CELL_V1_FULL_BUILD.md`.

## Rails

```text
NET_P    +5 V absolute bench rail; +2.5 V relative to CENTER
NET_G    ~2.5 V absolute; CENTER / virtual-ground spine / controller receipt
NET_N     0 V absolute bench rail; -2.5 V relative to CENTER
```

`VGBUF.OUT -> NET_G` at the controller/home end. Do not daisy-chain NET_G around the three stations.

## Logical Mirror station template

Each logical station `GX` where X is `PLUS`, `ZERO`, or `MINUS` uses one local midpoint `GX_TAP`:

```text
NET_P
  |
GX_RU 1k
  |
GX_UP_A.D
GX_UP_A.S --- GX_UP_B.S      <- common-source node GX_UP_S
GX_UP_B.D
  |
GX_TAP
  |
GX_LOW_A.D
GX_LOW_A.S -- GX_LOW_B.S     <- common-source node GX_LOW_S
GX_LOW_B.D
  |
GX_RL 1k
  |
NET_N

GX_TAP -- GX_RG 10 ohm -- NET_G
GX_TAP -- GX_RRC 1k -- GX_HOLD
GX_HOLD -- GX_C 10uF -- NET_G
GX_HOLD -- GX_RBLEED 100k -- NET_G
```

For each source-to-source bilateral pair:

```text
GX_UP_A.G = GX_UP_B.G = GX_UP_GATE
GX_UP_GATE -- 100k -- GX_UP_S
floating upper drive negative -> GX_UP_S
floating upper drive positive -> switch -> 220 ohm -> GX_UP_GATE

GX_LOW_A.G = GX_LOW_B.G = GX_LOW_GATE
GX_LOW_GATE -- 100k -- GX_LOW_S
floating lower drive negative -> GX_LOW_S
floating lower drive positive -> switch -> 220 ohm -> GX_LOW_GATE
```

The exact MOSFET D/S/G physical pins must come from the actual manufacturer's datasheet. Do not infer pin order from another TO-92 part.

## Station instances

```text
GPLUS_TAP   -> NET_G through GPLUS_RG 10 ohm
GZERO_TAP   -> NET_G through GZERO_RG 10 ohm
GMINUS_TAP  -> NET_G through GMINUS_RG 10 ohm
```

All three station taps star independently to the same NET_G spine.

## Midpoint host

For the documented TLE2426 F0 host:

```text
TLE2426 IN      -> NET_P
TLE2426 COMMON  -> NET_N
TLE2426 OUT     -> NET_G home
100nF bypass    -> NET_P to NET_N close to TLE2426
10uF bulk       -> NET_P to NET_N close to TLE2426
```

The 8-pin noise-reduction option is documented separately. Do not place a random large capacitor directly on OUT without checking stability for the exact package/load.

## Current paths

Balanced station:

```text
NET_P -> RU -> upper bilateral pair -> GX_TAP -> lower bilateral pair -> RL -> NET_N
```

CENTER receipt only:

```text
GX_TAP -> RG -> NET_G
```

Therefore the full P-to-N station current does not have to pass through the midpoint host. Only the mismatch between the upper and lower arms appears as `I_G`.

Measure:

```text
I_GX = (V(GX_TAP) - V(NET_G)) / 10 ohm
```

## Count invariant

```text
3 logical Mirror gates
x 2 mirrored electrical legs per station
x 2 MOSFET devices per bilateral leg
= 12 physical MOSFETs
```

Physical device count does not alter the canonical logical count: **three bidirectional Mirror gates / six traversals**.
