# CELL_V1 DC / AC / RC Cycle

The cycle is not a one-way conveyor. The outer rails are opposed around a live CENTER reference and each logical Mirror station is bilateral.

```text
DC   establishes opposed rail bias       + | G | -
AC   changes the signed differential      positive <-> center <-> negative
RC   stores/damps a differential briefly  then resolves toward CENTER
```

## Electrical sequence

1. Establish a stiff `NET_G` midpoint.
2. With station arms symmetric, the local tap sits near G and its 10-ohm receipt is near zero.
3. Introduce a controlled lean by changing drive or one arm resistance.
4. The local tap moves relative to G and a signed `I_G` receipt appears.
5. The RC branch integrates that tap-to-G differential.
6. Return the electrical drive to balance.
7. The capacitor decays toward G with the measured time constant.
8. Only after this behavior is stable should slow polarity reversals be repeated as an AC/counter-motion test.

## F0 RC branch

```text
station tap -- 1 k -- HOLD
                     |
                   10 uF
                     |
NET_G ===============+
                     |
                   100 k
                     |
NET_G ===============+
```

Nominal fast time constant:

```text
tau ~= 1 k × 10 uF ~= 10 ms
```

The real breadboard value must be measured because electrolytic tolerance, MOSFET resistance, source impedance, and instrument loading change the result.

## Outcome language

For F0 receipts use electrical terms first:

```text
HOLD      = station re-closes near CENTER and the RC state decays predictably
MODULATE  = signed differential persists/changes inside the allowed window
BREAK     = reference/gate condition leaves the accepted window or the loop is intentionally opened
```

The higher One-Wave mechanical language — push / squeeze / mirror / pull / tension — is a proposed interpretation of these measured relations. Do not substitute that language for voltage/current/time receipts.

## Do not confuse storage modes

```text
capacitor voltage after command removal   = RC storage
inductor current immediately after change = inductive energy / decay
remanent field after drive removal        = magnetic-hold candidate only after controls
```

Only the last can enter the magnetic-memory test, and even then it requires repeatable polarity reversal and controls.
