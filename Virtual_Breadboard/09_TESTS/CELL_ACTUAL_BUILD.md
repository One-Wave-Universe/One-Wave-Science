# CELL_V1 — actual first board

830 breadboard. 50 mA. Do A and law first. B and C copy A.

## Rails

Top power rail: RED +12  
Bottom power rail: BLACK −12  
BLUE = a jumpered row down the trench, column 1 to 63. That is G.

Col 1: banana wires from the supply. 100 nF RED–BLUE, 100 nF BLACK–BLUE.
Col 3: 10 k RED–BLUE, 10 k BLACK–BLUE.
Col 5–6: I_0. Either DMM in series in BLUE or 1 Ω between col 5 and 6 on the blue jumper line.

## Station A (cols 10–18)

- AO3401 breakout: source to RED, drain to a node called PA (col 14).
- 2N7000 flat toward you, left-to-right S G D (confirm bag). S to BLACK, D to PA.
- 220 Ω in each gate lead.
- 10 k from P-gate node to RED (OFF).
- 10 k from N-gate node to BLACK (OFF).
- 1 k from PA to BLUE (STAR for now is just BLUE).

STAY = both pulldowns only.  
+1 = short P-gate toward BLUE with a jumper.  
−1 = short N-gate toward BLUE.

Never both jumpers.

## Then

Copy station A at cols 25–33 (B) and 40–48 (C).  
STAR = three 1 k (or later coils) tied together and to BLUE.  
Speaker if you want hearing: between PA and PB, 47 Ω in series, **not** to BLUE.

## First DMM

Black on BLUE. RED ~+12, BLACK ~−12, I_0 ~0. Pull one law 10 k. I_0 ~1.2 mA. Plug back.
