# P0 Hexagon Layout - Physical and Electrical

## Geometric Layout (Pointy Hexagon)

```
              a+ (12 o'clock)
             /  \
           /      \
    c- (10)        b+ (2 o'clock)
    o'clock        
       /              \
      |      V_0       |
      |    (nucleus)   |
       \              /
    b- (8)          c+ (4 o'clock)
    o'clock        
           \      /
             \  /
          a- (6 o'clock)
```

## Clockwise Vertex Sequence
1. a+ (top, 12 o'clock)
2. b+ (top-right, 2 o'clock)  
3. c+ (bottom-right, 4 o'clock)
4. a- (bottom, 6 o'clock)
5. b- (bottom-left, 8 o'clock)
6. c- (top-left, 10 o'clock)

## Three Phases (Opposite Vertex Pairs)

### Phase A: Vertical (12 ↔ 6)
```
    a+ ————→ L_A_pos ————→ mid_A_pos ————→ R_A_pos ————→ nucleus
                                                              ↑
                                                              |
                                                            R_A_neg
                                                              |
                                                          mid_A_neg
                                                              ↑
                                                           L_A_neg
                                                              |
                                                            a-
```

### Phase B: Diagonal (2 ↔ 8)
```
    b+ ————→ L_B_pos ————→ mid_B_pos ————→ R_B_pos ————→ nucleus
                                                              ↑
                                                              |
                                                            R_B_neg
                                                              |
                                                          mid_B_neg
                                                              ↑
                                                           L_B_neg
                                                              |
                                                            b-
```

### Phase C: Diagonal (4 ↔ 10)
```
    c+ ————→ L_C_pos ————→ mid_C_pos ————→ R_C_pos ————→ nucleus
                                                              ↑
                                                              |
                                                            R_C_neg
                                                              |
                                                          mid_C_neg
                                                              ↑
                                                           L_C_neg
                                                              |
                                                            c-
```

## Half-Bridge Configuration at Each Vertex

```
        +V (5V supply)
         |
       PMOS (gate controlled, high-side)
         |
      hex_node ←→ to phase winding
         |
       NMOS (gate controlled, low-side)  
         |
        GND
```

**Gate Control Logic:**
- When gate_voltage = 0.0V:
  - PMOS: Vgs = 0.0 - V_node < -1.0V → **ON** (conducts +V to node)
  - NMOS: Vgs = 0.0 - 0 = 0.0V < 1.0V → **OFF**
  
- When gate_voltage = 0.5V:
  - PMOS: Vgs = 0.5 - V_node < -1.0V if V_node > 1.5V → **ON** (conducts +V to node)
  - NMOS: Vgs = 0.5 - 0 = 0.5V < 1.0V → **OFF**

- When gate_voltage = 1.5V:
  - PMOS: Vgs = 1.5 - V_node. If V_node = 2.5V, then Vgs = -1.0V → **BORDERLINE**
  - NMOS: Vgs = 1.5 - 0 = 1.5V > 1.0V → **ON** (conducts node to GND)

**Problem:** No single gate voltage keeps BOTH FETs off when node is at 2.5V.
- PMOS OFF requires: gate > 1.5V
- NMOS OFF requires: gate < 1.0V
- **No overlap = no true neutral point**

## Required Fix

To establish a neutral zone where neither FET conducts:

**Option 1:** Reduce NMOS threshold from 1.0V to 0.5V
- PMOS OFF: gate > 1.5V  
- NMOS OFF: gate < 0.5V
- Still no overlap

**Option 2:** Use biased gate control (two separate signals per vertex)
- PMOS gate tied to one signal (high when +V → node is wanted)
- NMOS gate tied to separate signal (high when node → GND is wanted)
- Can ensure they're never both ON simultaneously

**Option 3:** Widen the node voltage swing
- Allow nodes to swing 0V to 5V instead of 1.25V to 3.75V
- Allows 2.5V neutral point without MOSFET overlap

**Option 4:** Change supply configuration
- Use ±2.5V supply instead of single +5V
- Naturally centered at 0V, more symmetric control
