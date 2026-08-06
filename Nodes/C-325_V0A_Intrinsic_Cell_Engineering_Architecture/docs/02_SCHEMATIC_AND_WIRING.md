# Intrinsic Schematic and Wiring Plan

```text
VA ─┐
    ├─ MIRROR GATE ─ LOCAL OSCILLATOR ─ PASS/HOLD/FLIP
VB ─┘                                      │
                                          ▼
                                MAGNETIC TERNARY MEMORY
                                          │
                                          ▼
                                FIVE-STATE MODULATOR
                                          │
                                          ▼
                              INTRINSIC REINJECTION ORGAN
                                          │
                                          ▼
                                  NEIGHBOR COUPLER
```

## Implementation roles

- balanced reference network;
- window comparator and hysteresis;
- LC or active resonant loop;
- analog phase gating or transistor inversion;
- electrical latch for first proof, later magnetic memory;
- five-position analog modulation network;
- envelope detector;
- phase-gated reinjection pulse stage;
- bidirectional coupling path.

No software decides when to refresh, hold, or flip.
