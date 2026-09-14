# ONE-WAVE CELL — BUILD POSTER

Three windings = ternary layer. Star = G. Rotating B = reinjection + hold.

```
+12 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ RED
        high A          high B          high C
         |               |               |
       PHASE A         PHASE B         PHASE C
         |               |               |
        low A           low B           low C
-12 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ BLACK

PHASE A ── winding A ─┐
PHASE B ── winding B ─┤ STAR ══ BLUE ═ G ═ I_0 ═ supply 0
PHASE C ── winding C ─┘

RED — 10k — BLUE — 10k — BLACK
```

Per winding: +1 = high ON, 0 = both OFF, −1 = low ON. Never both ON.
Live one winding. Others STAY. Walk A→B→C to rotate B.
All STAY = hold. Leftover B = next baseline.

Parts: ±12 V current-limited, 3× high + 3× low FET (2N7000 first),
gate resistors + pulldowns, 2× 10k law, I_0 shunt in blue at home,
three coils or a small star motor whose stall fits the FETs.
High-side N-MOS needs real gate drive. First load = three resistors to star.
