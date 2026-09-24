# Motor sensor head — built in, not bolted on later

Every One-Wave winding / motor carries **one puck**. Multiple senses, one reference, one UP cable.
The puck is part of the motor plan. A bare 2212 is not a One-Wave motor.

```
        [ puck ]
     NTC + piezo/IMU + Hall
     all vs local G
           |
        4–5 wires with the phase leads
           |
        BLUE / Void
```

## What lives in the puck

| sense | part (first build) | tells Void |
|---|---|---|
| heat | 10 k NTC 3950, epoxy to the can or stator | winding/driver too hot → engage 0 |
| vibration | 20 mm piezo disc or analog 3-axis breakout | stall, strike, imbalance scream |
| balance / location | SS49E Hall on the bell, or the piezo hash vs the other motors | pair cancel, rotor where |
| optional current | 10–50 mΩ on the phase, Kelvin to puck | load vs heat |

One local cap, one 5 V (or 3.3 V) from the body star. GND of the puck **is** that motor's G tap, not a random earth.

## One cable

```
phase  A / B / C      power
G                     star tap
5 V                   puck power
HEAT                  analog vs G
VIBE                  analog vs G
HALL                  analog vs G
```

That is the nerve bundle. Do not send USB from the can. Analog vs G is the law. A tiny MCU in the puck is allowed later to pack the three analogs; it still talks numbers vs G, not a chat dump.

## Balance is a *pair* of pucks

One puck cannot know balance. Opposite motors share Void:

```
heat_A vs heat_C
vibe_A vs vibe_C
Hall_A vs Hall_C
I_A vs I_C
```

Cancel → hold. One side hot + quiet current → that winding is sick. One side vibe + other still → mechanical, not command.

## First physical puck (no custom PCB yet)

- 20 mm 3D-printed or FR4 disc that straps to the can
- NTC glued metal-to-metal
- piezo taped under the disc
- Hall in a pocket facing a magnet on the bell (one magnet is enough)
- five-wire silicone loom along the phase leads

Later: one 20 mm round PCB, same parts, potting. Still three analogs + G + 5 V.

## Firmware rule

Puck does not stamp. Puck does not arm motors. Puck only UP.
Void reads heat/vibe/Hall and may cut engage. Field never reads puck to invent a lean from a hot can.

## Pass

Spin or click a winding. Heat rises slowly, vibe shows the hit, Hall ticks if a magnet exists. STAY: vibe dies, Hall leftover optional, heat still legal. Opposite puck stays quiet → pair is the balance story.
