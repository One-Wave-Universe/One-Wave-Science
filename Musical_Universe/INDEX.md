# Musical Universe Index

A framework for understanding music as discovered resonance patterns emerging from One-Wave physics.

## Chapters

**Chapter 0: Discovered, Not Invented**  
Framing: humans invent musical systems but discover underlying harmonic relationships. Real physics of string vibration, resonance, and oscillation are independent of cultural notation.
- Historical foundation (Pythagoras, Kepler, modern physics)
- Distinction between discovered (harmonic ratios, resonance) and invented (12-tone equal temperament, notation)

**Chapter 1: The Music Clock (E-510)**  
A rotational coordinate system for harmonic relationships, built on 12-tone equal temperament.
- Root position = zero reference (Ground/Zero principle)
- Clockwise = Expression, Counter-clockwise = Compression
- Foundation for all subsequent chord analysis

**Chapter 2: Chord Rotation (E-511)**  
The function that re-centers any chord onto its own local instance of the Music Clock.
- Converts fixed pitch sets into signed-position relationships
- Produces Oscillation Windows as output
- Tested on A Major and A Minor chords

**Chapter 3: Leaning Direction (E-513)**  
Analyzes the directional asymmetry of a single chord's Oscillation Window.
- Compression vs. Expression dominance
- Both Major and Minor lean backward (toward compression)
- Minor leans harder than Major
- Formalized lean formula: L = Σ|negative positions| - Σ|positive positions|

**Chapter 4: Circle of Fifths (E-514)**  
A DIFFERENT clock system from Chapter 1 — ordered by perfect fifths, not chromatic semitones.
- Per-KEY (not per-chord) analysis
- Functional leaning: Tonic (I), Subdominant (IV), Dominant (V)
- 6 o'clock = tritone = maximum instability
- Real music theory formalized in One-Wave vocabulary

**Chapter 5: Chord Oscillation Windows and Settling Dynamics**  
Comprehensive framework for understanding why different chord types sound and behave differently.

Chord types documented:
- **Power Chord (-1, +1)**: Simplest, settles fastest, direction-neutral
- **Major (-5, +4)**: Asymmetric, leans backward, grounded character
- **Minor (-5, +3)**: Asymmetric, leans harder backward, heavier character
- **Triad (-4, +5)**: Asymmetric, leans forward, unstable/restless character
- **Augmented ±4 (-4, +4)**: Symmetric, medium-fast settling
- **Augmented ±5 (-5, +5)**: Symmetric, maximum reach, medium-fast settling

Why power chords dominate modern music:
- Symmetric window means direction-neutral
- Octave phase-lock creates immediate settling
- Can move to any root without losing character
- Bass line provides direction

## Nodes (Appendix E)

**E-510: Music Clock Harmonic Oscillation**  
Reference frame: 12-position rotational coordinate system for harmonic relationships.

**E-511: Chord Rotation**  
Function: re-centers any chord onto Music Clock, produces Oscillation Window.

**E-512: Oscillation Window**  
Result: signed pair (Compression-side position, Expression-side position) for any chord.

**E-513: Chord Leaning Direction**  
Analysis: directional asymmetry of a chord's Oscillation Window using lean formula.

**E-514: Circle of Fifths Functional Leaning**  
Different system: ordered by perfect fifths (not chromatic), per-key (not per-chord).

**E-534: Settling Dynamics** (NEW)  
Physics: rate and pattern by which multiple frequencies reach phase-lock based on harmonic ratios and octave relationships.

## Working Tools

**chord_architect.html**  
Interactive three-wheel Circle of Fifths interface for exploring chord definitions:
- Root selection (middle wheel, Circle of Fifths order)
- Positive offset selection (outer wheel, +1 to +6)
- Negative offset selection (inner wheel, -1 to -6)
- Real-time chord identification and pitch class calculation

**Python Implementation**
- `triad_brain.py`: CPU-native 3-loop triad state machine (TriadState, cycle operations)
- `rabbit_hop_music.py`: Music coordinate adapter for One-Wave routing system

## Status and Future Work

All chapters: YELLOW audit status — internally coherent, unvalidated against physical measurement.

**High-priority experimental verification:**
1. Measure settling times of power chords, major, minor, triads using high-speed waveform capture
2. Correlate measured settling time with perceived harmonic character in listening tests
3. Analyze real guitar audio to verify power chord interference produces emergent triads
4. Test whether settling dynamics predictions hold across different tuning systems

**Theoretical extensions:**
1. Seventh chords and extended harmonies (more than three pitch classes)
2. Define Oscillation Window for two-note structures (power chords)
3. Formalize connection between settling dynamics and perceived harmonic character
4. Map to B-206b Four Views (Inward/Outward/Across/Over)

## Quick Start

1. Read Chapter 0 for framing (discovered vs. invented distinction)
2. Read Chapter 1 for the foundational Music Clock coordinate system
3. Read Chapters 2-3 for how chords work within this system
4. Read Chapter 4 for the separate Circle of Fifths functional system
5. Read Chapter 5 for the complete chord oscillation physics framework
6. Use chord_architect.html to interactively explore chord definitions

All chapters reference the relevant Appendix E nodes for deeper mathematical and theoretical content.

---

**One wave. Mirror builds.**
