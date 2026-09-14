# Rotating field, hold, reinjection

Three windings at the star **are** a rotating magnetic field when you walk live-gate around A→B→C.
That rotation is not decoration. It is how state is carried and how it is put back.

```
DC          opposed rails
AC          live winding ±1, others STAY
RC          window before stamp
rotating B  three-phase walk of that AC
hold        B that remains when all STAY
reinject    leftover B is the next cycle's baseline
QC          views UP (what B is now)
            actions DOWN (torque / spin from the same flip)
```

One flip. Field turns. New view of B goes up. Last torque goes down. Same `seq`.

## How the rotation is made

Not a fourth organ. The ternary layer already has three legs.

```
seq n    live A  +1     B STAY  C STAY     B-vector toward A
seq n+1  live B  +1     C STAY  A STAY     vector steps 120°
seq n+2  live C  +1     ...                another 120
```

Opposite lean (−1) walks the other way. That is bidirectional at center, in flux.
Hold = all STAY. Drive current dies. If the core / rotor / remanence **keeps an orientation**, that is state hold. If it forgets the instant current dies, you had torque, not a hold loop.

Reinjection: the next engage does not start from zero. It starts from the B that stayed. DC clothes the same. AC leans on top of that leftover. That is the loop, folded home on G.

## Quadratic

```
views UP     what the mid and the flux read now     (memristor / Hall / I_0 + probe)
actions DOWN what the shaft / spin did              (torque, step, sound)
```

Same crossing. Spintronics here means: the action layer is the magnetic motion, not a UART packet. It is not a special IC you buy to make the sentence true.

## What has to be true on the bench

1. Three windings (or three coils) on one star = G.
2. Walk live +1 around A B C. Probe (Hall or a search coil) must show the vector step. That is rotation.
3. All STAY. Probe for leftover. If it drops to noise in one RC window, hold is empty — only the winding current was the memory.
4. Engage again with lean = 0. If the leftover B still biases I_0 or the next twitch, reinjection is real.
5. Views and action share seq on a moving flip.

A toroid with one turn of hookup wire will fail 3. A rotor with reluctance or a core with remanence is the bet for 3–4.

## Same object

```
rotating B     = AC walked around three gates
hold           = STAY + remanence
reinject       = leftover B is next baseline
I_0            = vagus of that field
quadratic      = one flip both ways
```
