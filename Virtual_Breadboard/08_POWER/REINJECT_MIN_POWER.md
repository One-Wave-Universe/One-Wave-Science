# Minimal power via reinjection

You pay for **change**. You should not pay rent on a state you already hold.

```
lean / walk     current in a winding     energy out
STAY            FETs off                 near zero drive
leftover B      remanence / rotor / MEM  state for free
reinject        next lean starts from that leftover
                not from zero
```

A normal drone / speaker / motor **holds by pushing**. Hover current is rent. This cell holds by STAY. Reinjection is the leftover B (or MEM, or Hall bias) that means the next +1 is a tap, not a lift from dead still.

## Where the watts go

| mode | should draw |
|---|---|
| all STAY, balanced | law 10 k + Hall 5 V + brain only |
| one short +1 pulse | pulse energy only |
| PWM to hold position | **fail** — that is rent |
| speaker STAY/STAY | ~0 across coil |
| flight inner loop | FC idle; One-Wave not adding hover |

I_0 at STAY is the lie detector. If I_0 is fat while you claim hold, you are still driving.

## How to actually use less

1. Default all gates STAY. Pull-downs already do this.
2. Pulse width = RC window, then STAY. Do not PWM a hold.
3. Next pulse polarity uses leftover B so you don't cancel and re-spend.
4. Speaker series R and 32 Ω element. Click, don't park DC in the coil.
5. Flight: nerve sends *deltas*, FC holds attitude. Don't nerve-PWM motors to hover.
6. Current knob is a teacher: if STAY trips it, something is ON.

Reinjection only saves power if leftover state is **real**. If Hall dies when current dies, you have no battery in B — every move starts from zero and you will spend like everyone else.

Measure: energy per click = integral of rail current over the pulse. Energy per second at STAY should collapse toward the 10 k + electronics floor.
