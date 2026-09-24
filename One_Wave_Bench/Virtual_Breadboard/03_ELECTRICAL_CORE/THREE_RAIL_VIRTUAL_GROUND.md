# Three-Rail CENTER / Virtual Ground

CELL_V1 uses three physical rails but only two supply endpoints.

```text
single 5 V F0 supply

NET_P = +5.0 V absolute  = +2.5 V relative to CENTER
NET_G = +2.5 V absolute  =  0     CENTER / reference / receipt
NET_N =  0.0 V absolute  = -2.5 V relative to CENTER

relative view:  +  |  0  |  -
```

`NET_G` is **made**. It is not earth ground and it is not allowed to wander with the load.

For the first single-supply build, use the documented TLE2426 source/sink midpoint host at the controller end. A true split low-voltage supply with a real midpoint is also valid for an F0 control build. A two-resistor divider is not a dynamic CENTER rail.

## Spine rule

Run one low-impedance NET_G spine from the controller/home end to the far end. Each logical Mirror station has one local tap and stars to the spine independently through its own receipt resistor:

```text
G+ TAP ---- 10 ohm ----+
                       |
G0 TAP ---- 10 ohm ----+==== NET_G spine ==== midpoint host
                       |
G- TAP ---- 10 ohm ----+
```

Do not route the G0 receipt through G+ or the G- receipt through G0.

## Observable

For each station:

```text
I_GX = [ V(GX_TAP) - V(NET_G) ] / 10 ohm
```

Balanced upper/lower arms should make `I_GX` small. A deliberate resistor mismatch should create a signed receipt while the midpoint host keeps NET_G near half supply.

Always record both:

```text
V_G_HOME
V_G_FAR
V_G_FAR - V_G_HOME
```

A large home/far difference is wiring/reference failure, not a useful state.

## F0 limits

- unloaded CENTER target: within 10 mV of half supply;
- controlled lean target: within 25 mV of half supply;
- initial midpoint imbalance current: keep comfortably below the host source/sink limit;
- no unexplained oscillation on NET_G.

These are prototype acceptance limits, not fundamental constants.

## Scope warning

Do not automatically connect a mains-earth oscilloscope ground clip to NET_G. If scope earth or supply negative is earth bonded, that can short the synthesized midpoint to another reference and invalidate or damage the test. Use a verified safe common, differential probe, or isolated/battery instrument.

See `TLE2426_VIRTUAL_GROUND.md`, `../CELL_V1_FULL_BUILD.md`, and `../09_TESTS/CELL_V1_SAFE_BRINGUP.md`.
