# Locked Cell Topology: DC, AC, Virtual Ground, and Three Mirrored Gates

## Status

**LOCKED CONCEPTUAL TOPOLOGY** — design specification and simulation hypothesis. Not established gravity physics.

## 1. Rail order and DC start

```text
forward DC                                             backward DC
    →                                                       ←

    + rail                 0 rail / virtual ground          - rail
    ─────────────────    ───────────────────────    ─────────────────
```

Invariant: `→  +  |  0  |  -  ←`

Center rail is a live reference, not earth, not a Y-junction, not a forward output.

## 2. Center interaction

Rails do not merge into a Y. Center is `+ ↔ 0 ↔ -`. Bidirectional through the mid. Receipt returns on the 0 rail toward the controller. No forward output beyond the center.

## 3. Bidirectional double oscillation

Not a linear conveyor. Oscillator at center, both ways.

```text
0 → +1 → 0 → -1 → 0
0 → -1 → 0 → +1 → 0
```

`-1` / `0` / `+1` after the window. `0` = reclosed at virtual ground; hold (oscillator still live).

## 4. Three mirrored gate regions

`G+` `G0` `G−` — threshold bands, not a serial pipeline.
Bilateral switch for a prototype: back-to-back MOSFETs with opposed body diodes, driven and current-limited for the actual rail. Model first.

## 5. DC → AC → RC → rotational hold

DC bias, AC through G, RC window, gates constrain, magnetic loop retains last route only after sense receipts, mid returns home.

## 6. Controller loop

Closed fold. Controller sets rails, receives mid receipt, sets next cycle. Not source → output.

## 7–11

Axes, JSON receipt, ±3 bands, sim / circuit / physical validation, repo binding: unchanged in intent. See CELL_V1 files under `01_PARTS` … `10_RECEIPTS`.

## 12. Physical layout drawing (CELL_V1)

```
             FORWARD DC →                         ← BACKWARD DC

 + rail  ================================================================
                    [ G+ ]        [ G0 ]        [ G− ]

 0 rail  ================================================================
     virtual-ground center rail / return rail / controller receipt rail

 − rail  ================================================================

             CONTROLLER / RAIL-ORIGIN REGION
             sits at the return end of the 0 rail
```

One cell:

```
 + rail   →───────[ G+ ]─────────[ G0 ]─────────[ G− ]───────
            |               |               |
 0 rail   ←══════════════════════════════════════   to controller
            |               |               |
 − rail   ←───────[ G+ ]─────────[ G0 ]─────────[ G− ]───────
```

Station (same three times):

```
 + — R+ — BIDIR — G — BIDIR — R− — −
              |
         C / RC window
              |
         magnetic sense loop (observe first)
```

This drawing is a layout contract. It does not say one copper pour should carry high current, delicate reference, and logic without buffering.

Bring-up: `09_TESTS/CELL_V1_SAFE_BRINGUP.md`.

## Locked invariant

> Opposed DC rails `→ + | 0 | − ←`. Virtual ground is the middle rail. AC oscillates through the center both ways. Three mirrored stations plus RC decide hold / lean / quit. Magnetic layer retains only after it is measured. Receipt returns on the mid BACK to the controller. Never a forward output past the center.
