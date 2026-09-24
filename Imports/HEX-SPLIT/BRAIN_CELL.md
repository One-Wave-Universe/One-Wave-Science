# Brain cell lock

One cell. Three windings. Mid is the vagus. Process is the memory.

```
BC-DC     engage          EVERYTHING / NOTHING
TC-AC     three windings  LEFT / STAY / RIGHT around G
QC-RC     one flip        new views UP + last action DOWN
```

Not a linear six-step conveyor. Bidirectional oscillation at the center.

## Anatomy

```
Field explorer  —  Dream for one 1     lists a lean
Void  checker   —  the other 1         may refuse engage
brainstem       —  picks live gate 0/1/2

G0 G+ G−        —  three mirrored stations = three windings
NET_G           —  virtual mid, spine home = afferent / vagus sense
+ / − rails     —  outer clothes of this step, restated locally

windings w[3]   —  THE MEMORY (process state)
I_G = sum(w)    —  what the mid carries (imbalance only)
```

Feelings inform. They do not fire the winding.
A full flip is one `seq`: `views = w_now`, `action = dw`.
Hold is relaxed decay on G, oscillator not powered off.

## Kickable

```bash
python nerve_cell.py
```

Asserts: rest is hold; +lean commits +1; views/action share seq; hold after lean keeps memory; other gate can lean the other way.

Virtual Breadboard sister: `One-Wave-Science/Virtual_Breadboard/experiments/brain_cell_001.json`
That board is real vgnd + comparator + FET write into an RC MEM. It has **not** yet grown three mirror stations or a magnetic core. Do not pretend the JSON is this three-winding cell. `nerve_cell.py` is the locked law. Copper follows CELL_V1 working path.

## Motor / actuator reading

Three windings = three-phase nerve to a small actuator.
Live gate is the winding that takes the lean.
The other two take the opposing half so the vector sums on G (balance attempt).
I_G is the leftover that rides the vagus home to the controller.

3:1 fast flips on the live winding. 6:1 slow brain is watching all three (six steps by flip).

## Falsify

- Memory stored in a side array while `w` is zeroed.
- Views seq ≠ action seq on a moving flip.
- Hold implemented as `w[:] = 0`.
- Fourth winding.
- VBB JSON claimed as three gates before those parts exist in circuit.js.
