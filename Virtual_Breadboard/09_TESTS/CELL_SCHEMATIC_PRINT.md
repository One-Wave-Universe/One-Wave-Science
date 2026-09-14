# CELL_V1 — print

```
+12 ── highA ─ PA ─ 1k/winding A ┬
+12 ── highB ─ PB ─ 1k/winding B ┤ STAR ═ BLUE ═ I_0 ═ supply 0
+12 ── highC ─ PC ─ 1k/winding C ┴
              lowA/B/C ─ −12

RED — 10k — BLUE — 10k — BLACK
100 nF at posts. RC across station. No cap in BLUE.

+1 high ON   STAY both OFF   −1 low ON   both ON illegal
Live one winding. 20 mA first, 50 mA only after resistor-load receipts.
```

## Actual first-phase gate wiring — no Nano yet

P-MOS high side: source=+12, drain=PA.
- OFF: 10 k gate→+12/source.
- ON: add 10 k gate→BLUE. Gate≈+6 V, VGS≈−6 V.

2N7000 low side: source=−12, drain=PA.
- OFF: 10 k gate→−12/source.
- ON: add 10 k gate→BLUE. Gate≈−6 V, VGS≈+6 V.

STAY = both command-to-BLUE resistors removed. Never command both devices ON together.

**Do not wire BLUE-referenced 0/5 V GPIO directly to these ±12 V gates.** It cannot turn either device fully OFF in this topology. Nano control requires a separate level-shifted or isolated gate driver.
