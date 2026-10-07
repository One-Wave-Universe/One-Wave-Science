Musical Universe, Chapter 5: Chord Oscillation Windows and Settling Dynamics

Version: 1.0
Date: October 5, 2026
Class: E-Series Application
Status: YELLOW

Dependencies: E-510 Music Clock, E-511 Chord Rotation, E-512 Oscillation Window, E-513 Chord Leaning Direction, E-514 Circle of Fifths Functional Leaning, E-534 Settling Dynamics

---

## Gray — Standard Physics Reference

A vibrating string at frequency f completes one full cycle in period T = 1/f. An octave above (frequency 2f) completes its cycle in period T/2 — twice as fast. When oscillations at different octaves interfere, they settle at different rates. A 1:2 harmonic relationship (octave) creates phase-lock: the higher frequency completes two cycles in the time the lower frequency completes one, and they meet in phase at each settling point.

Destructive and constructive interference patterns emerge when multiple frequencies are present. Simple harmonic relationships (small integer ratios) create fast coherence; complex relationships create longer, messier settling times.

---

## The Oscillation Window Framework

All chords in the One-Wave music system are defined by two parameters: a **negative offset** (compression side, how far down the ring the oscillation reaches) and a **positive offset** (expression side, how far up the ring it reaches). The root is always at position 0.

The window notation is: **(negative) (0) positive**

### Fundamental Chord Types

**Augmented ±1: (-1, +1)** (semitone reading; not a root-and-fifth power chord)

- Simplest oscillation envelope
- Root (0), one semitone below (-1 = B around C), one semitone above (+1 = C♯ around C)
- Symmetric, centered, **direction-neutral**
- Settling speed: hypothesis only (see Yellow Audit)

Pitch classes: {0, 1, 11} (root, one semitone up, one semitone down)

Note: under the semitone reading this window does not contain a perfect fifth. The earlier "power chord" label described a root-fifth-root voicing that the window does not produce.

**Major: (-5, +4)**

- Asymmetric window **leaning backward**
- Deep negative floor (-5), restrained positive ceiling (+4)
- Pitch classes: {0, 4, 7} = Root, Major Third, Perfect Fifth
- Settles medium speed: the asymmetry requires the deeper floor to find equilibrium
- System wants to stay grounded, resists movement
- Harmonic character: stable, grounded, anchored

**Minor: (-5, +3)**

- Asymmetric window leaning backward (like Major)
- Deep negative floor (-5), even more restrained positive (+3)
- Pitch classes: {0, 3, 7} = Root, Minor Third, Perfect Fifth
- Settles medium-slow: deeper floor means longer settling time for low frequencies
- More grounded than Major, pulls even harder to stay put
- Harmonic character: dark, heavy, grounded

**Triad: (-4, +5)**

- Asymmetric window **leaning forward**
- Raised floor (-4, not -5), extended ceiling (+5)
- Pitch classes: {0, 5, 8} = Root, Perfect Fourth, Augmented Fifth
- Settles slower: three competing frequencies with **asynchronous settling**
- High octaves settle fast, establish +5 ceiling
- Low octaves settle slower, eventually pull floor up from -5 to -4
- System wants to escape upward but floor holds it back
- Harmonic character: unstable, restless, tension-seeking

**Augmented ±4: (-4, +4)**

- Symmetric window, centered on root
- Equal reach negative and positive: 4 steps each direction
- Pitch classes: {0, 4, 8} = Root, Major Third, Augmented Fifth
- Settles medium-fast: symmetric reduces complexity
- Direction-neutral like power chord but with larger envelope
- Harmonic character: balanced but strange, wider than power chord

**Augmented ±5: (-5, +5)**

- Symmetric window, maximum symmetric reach
- Equal 5-step reach both directions
- Pitch classes: {0, 5, 7} = Root, Augmented Fourth, Perfect Fifth
- Settles medium-fast: symmetric envelope
- Direction-neutral, larger than ±4
- Harmonic character: wide, open, symmetrically unstable

---

## Settling Dynamics and Harmonic Behavior

### Why Power Chords Settle Fastest

The power chord's magic: root notes at 1:2 octave relationship guarantee **instant phase-lock**. The lower note settles at its natural period, the higher completes two cycles in that same time, they synchronize. No asynchronous interference, no competing frequencies at odd ratios.

Modern music (punk, ska, metal) uses power chords because:
1. They settle immediately
2. They're direction-neutral (no lean)
3. They move freely to any root
4. The bass line **provides direction**, not the chord
5. Fast coherence = powerful, cutting sound

### Why Modern Music Wants to Settle on the Floor

Most music since the industrial era settles toward deep, grounded bass. Deep -5 floor (Major, Minor) creates stability and presence. The oscillation energy prefers to anchor low.

Triads, by contrast, want to settle high (+5 reach). This creates **tension**: they're fighting against modern music's bias toward grounding. Triads are rare, unusual, unstable.

### Asymmetric Leaning Explained

The difference between Major (-5, +4) and Triad (-4, +5) is a **directional lean**:

**Major leans back** (down): floor deeper (-5), ceiling shorter (+4)
- High octaves settle fast, establish +4
- Low octaves settle slower, establish -5
- System equilibrates with weight toward the negative

**Triad leans forward** (up): floor shallower (-4), ceiling extended (+5)
- High octaves settle fast, establish +5
- Low octaves settle slower, pull floor up to -4
- System equilibrates with weight toward the positive
- Constant tension: wants to go higher but can't

---

## Why Triads Emerge from Power Chord Interference

When two power chords are played in the same octave and share a note (e.g., A power chord A-E-A with E also played in the E power chord E-B-E):

1. The shared note (E) **locks** the two chords together
2. Different frequency components (A, E, B) settle at different rates
3. The interference pattern creates an **emergent third pitch class**
4. The combined oscillation envelope becomes asymmetric
5. Result: Triad window (-4, +5)

The triad is not a "base" chord type; it emerges from the interference of simpler power chords across octaves and shared resonance points.

---

## The Window Hierarchy

From simplest to most complex settling:

1. **Power Chord (-1, +1)**: Fast, symmetric, direction-neutral
2. **Augmented ±4 (-4, +4)**: Medium, symmetric, slightly larger
3. **Augmented ±5 (-5, +5)**: Medium, symmetric, maximum span
4. **Major (-5, +4)**: Medium-slow, asymmetric, leans back (grounded)
5. **Minor (-5, +3)**: Slow, asymmetric, leans back hard
6. **Triad (-4, +5)**: Slow, asymmetric, leans forward (unstable)

---

## Mathematics

**Chord window**: (neg, 0, pos) where neg ≤ 0 ≤ pos

**Pitch classes**: sorted set of {(i % 12) for i in [neg, 0, pos]}

**Settling character**:
- Symmetric (pos = -neg): direction-neutral, fast
- Asymmetric (pos ≠ -neg): has a lean, requires matching settling times

**Harmonic lock**: octave relationships (1:2, 2:4, etc.) guarantee phase-lock

---

## Predictions

1. If this model is correct, real guitar voicings should show measurable settling time differences between power chords, major chords, and triads under controlled resonance measurement.

2. The forward lean of triads should be audibly detectable as a sense of upward tension or instability compared to the grounded character of major chords.

3. Symmetric chords (augmented types, power chords) should sound more "neutral" and movable than asymmetric chords, because they carry no directional bias.

4. Bass-driven music (punk, ska) should predominantly use power chords because of their fast settling and direction-neutrality, letting the bass line carry harmonic movement.

---

## Yellow Audit

- The settling-time differences between chord types have not yet been measured experimentally; the model is based on harmonic theory and guitar physics, not empirical data
- The "lean" metaphor (Major leans back, Triad leans forward) is intuitive but has not been formalized as a testable quantity
- The mechanism by which shared notes between power chords "lock" them and create emergent triads has not been verified against real recorded guitar audio
- Whether the ±4 window is equivalent to traditional "augmented" chord quality (musically and harmonically) requires independent verification

---

## Future Work

1. Record and measure settling times of power chords, major, minor, and triads under controlled conditions
2. Verify that symmetric chords (power chord, augmented) are audibly more "neutral" than asymmetric ones
3. Analyze real punk and ska recordings to confirm power chord prevalence
4. Test whether the forward lean of triads is consistently audible as tension/instability
5. Map the emergence of triads from power chord interference using spectral analysis
6. Extend the framework to seventh chords, extended harmonies, and chords with more than three distinct pitch classes

---

END OF MUSICAL UNIVERSE, CHAPTER 5
One wave. Mirror builds.
