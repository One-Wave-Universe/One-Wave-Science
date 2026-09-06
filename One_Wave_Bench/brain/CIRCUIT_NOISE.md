# Two sides vs noise

## Cancel (stability)

Two rails + stiff midpoint is a differential pair.

- Noise that hits both rails the same (hum, supply ripple, EMI) is common-mode.
- A real virtual ground rejects that. Midpoint current from common-mode ~ 0.
- That is why G-756 said two rails at every step. Not poetry. CMRR.

If the splitter is a soggy resistor divider, common-mode becomes motion and you will swear the lattice is alive. It is not. It is a soft ground.

## Kick (the only noise that should move)

After common-mode dies, what remains is *differential*: one rail or one winding wandering relative to `(0)`.

- Inside the dead-band window: HOLD. Noise is not a move.
- A kick that leaves the window: that *can* request UP or DOWN.
- Hysteresis (G-733) stops chatter from living on the lip.

So: noise does not run the motor. A differential kick can *propose* a crossing. Admin still writes the gates. Dream/Boltzmann may use bounded noise to pick among ties. Unbounded noise is not 3:1.

## Bench test

1. Couple the same sine into both rails. Midpoint must stay quiet. That is cancel.
2. Couple the sine into one winding only. Window comparator should tick. That is kick.
3. If (1) ticks, your ground is junk. Fix the splitter before you name it life.
