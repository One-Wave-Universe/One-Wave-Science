# Algorithm Zero + Rabbit Hopping + Circle of Fifths: Unified Integration
**Date:** October 5, 2026  
**Purpose:** Connect six-step recursive choice (Algorithm Zero) with center-preserving addressing (Rabbit Hopping) and music mechanics (Circle of Fifths)  
**Status:** INTEGRATION FRAMEWORK (cross-domain unification)

---

## Core Identity: One Recursive Pattern, Three Domains

All three systems express the SAME underlying recursive structure:

### Algorithm Zero (Foundational Recursion)
```
BEGIN → MOVE → HOLD → MOVE → BREAK → REPEAT
  (start) (choice) (commit) (verify) (resolve) (recurse)
```

### Rabbit Hopping (Addressing Grammar)
```
center (0) ↔ mirrored alternatives (−1, +1)
  ↕ operate ↕
wrapper ± 1 around TOP
  ↕ resolve ↕
source_identity | TOP | wrapper_address
```

### Circle of Fifths (Music Mechanics)
```
root ↔ major/minor (±offset)
  ↕ oscillate ↕
chord families (+4/−5, +3/−5, −4/+5, etc.)
  ↕ lock ↕
harmonic identity preserved across transposition
```

**The Insight:** Algorithm Zero defines the SEQUENCE. Rabbit Hopping defines the ADDRESSING within each step. Circle of Fifths demonstrates how the addressing preserves IDENTITY through transformations.

---

## Algorithm Zero: The Six-Step Recursive Foundation

### Definition
A recursive choice mechanism with six distinct phases:

| Phase | Operation | What Happens | Example |
|-------|-----------|--------------|---------|
| **BEGIN** | Initialize | Set reference point, gather choice options | "Start at C major" |
| **MOVE** (1st) | First choice | Select from binary alternatives | "Choose major vs minor" |
| **HOLD** | Commit | Lock the choice, establish new reference | "Lock to C major configuration" |
| **MOVE** (2nd) | Second choice | Verify or pivot from first choice | "Verify harmonic progression" |
| **BREAK** | Resolve | Close the local loop, determine outcome | "Confirm chord identity preserved" |
| **REPEAT** | Recurse | Become the point/center for next level | "C major becomes root for next scale level" |

### Key Property: Center Preservation
Each level COMPLETES a choice cycle, then that resolved state BECOMES the center for the next recursive level.

This is RELATIONAL GRAMMAR recursion, not physical doubling (per one-wave-framework-principles.md).

---

## Rabbit Hopping: Center-Preserving Addressing

### Complete Packet Structure (From RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md)

```
source_identity | TOP | wrapper_address
```

Three required parts:

1. **source_identity** — Where this packet originated
2. **TOP** — The core operation (calculated from route family):
   - `ORIGINAL` → 2N (unchanged)
   - `DOUBLE_THEN_SHIFT` → 2N + K (double first, then offset)
   - `SHIFT_THEN_DOUBLE` → 2(N + K) (offset first, then double)
3. **wrapper_address** — Mandatory ±1 around TOP (every TOP gets exactly two packets)

### Operation Sequence
Each rabbit-hop operation:
1. **Remove wrapper** (peel off ±1 boundary)
2. **Execute TOP** (apply core transformation)
3. **Verify reconstruction** (check reverse path exists)
4. **Recurse** (use result as center for next level)

### Key Property: Reversibility
Every forward route preserves enough information to reconstruct its origin exactly.

---

## Circle of Fifths: Music Manifestation

### Signed-Offset Architecture

| Chord Family | Window | Root at 0 | Pitch Classes | Physical Meaning |
|---|---|---|---|---|
| **Power Chord** | (−1, +1) | C | {0, 1, 12} | Symmetric grounding; both roots lock in phase |
| **Major** | (−5, +4) | C | {0, 4, 7} | Asymmetric; leans backward (deeper floor, restrained ceiling) |
| **Minor** | (−5, +3) | C | {0, 3, 7} | Asymmetric; leans backward (same floor as Major, more restrained) |
| **Triad** | (−4, +5) | C | {0, 5, 8} | Asymmetric; leans forward (shallower floor, higher ceiling) |

### Oscillation Physics
- **Negative offset** (floor): Lower frequencies settle slower → pull system down
- **Positive offset** (ceiling): Higher frequencies settle faster → pull system up  
- **Balance point** emerges where settling dynamics equilibrate

Modern music systems prefer Major (backward lean = stability) over Triad (forward lean = instability).

### Chord Progression as Algorithm Zero

Playing a chord progression (e.g., C major → F major → G major → C major):

1. **BEGIN:** Start at C major
2. **MOVE (1st):** Shift root from C to F (+5 semitones)
3. **HOLD:** Lock F major configuration (+4/−5 window around F)
4. **MOVE (2nd):** Shift root from F to G (+2 semitones)
5. **BREAK:** Confirm G major identity
6. **REPEAT:** G major becomes reference for next phrase (or return to C)

Each chord is a **stable hold state** (Algorithm Zero HOLD phase).  
Each transition is a **choice** (Algorithm Zero MOVE phases).  
The progression itself is a **recursion** (Algorithm Zero REPEAT feeds into next BEGIN).

---

## Integration: How Rabbit Hopping Routes Through Circle of Fifths

### Route Receipt Format

A rabbit-hop route through Circle of Fifths:

```
guitar_neck | SHIFT_THEN_DOUBLE(N + K) | wrapper_address
```

**Example:** Transpose C major up by 2 semitones to D major

1. **source_identity:** `guitar_neck` (the domain)
2. **TOP:** `SHIFT_THEN_DOUBLE(N + 2)` where N = 0 (root C)
   - Offset first: 0 + 2 = 2 semitones
   - Then double (in octave space): wraps within 12-tone system
   - Result: D major root
3. **wrapper:** ±1 around the D major configuration
   - Forward route: D major (+4/−5 window)
   - Reverse route: Can reconstruct C major by reversing: undo doubling, undo offset

### Route Preservation Across Domains

**Claim:** A route that preserves harmonic identity in Circle of Fifths also preserves relational identity in Algorithm Zero recursion.

**Verification (To Test):**
1. Define chord progression route on Circle of Fifths (e.g., C→F→G→C)
2. Map to Rabbit Hopping addressing (signed offsets at each MOVE)
3. Verify forward/reverse routes preserve chord identity
4. Confirm equal numeric destinations yield same harmonic result
5. Test across scales (C major, C minor, G major, etc.)

---

## Five-Scale Bidirectional Model

From one-wave-framework-principles.md:

```
Micro → Small → Mid → Large → Macro → (reverse)
```

Each scale level uses:
- **Algorithm Zero:** Six-step recursion at that scale
- **Rabbit Hopping:** Signed-offset addressing connecting levels
- **Circle of Fifths:** Harmonic/oscillatory mechanics at that scale

### Example: Nested Algorithm Zero

**Macro Scale:** Song structure (verse/chorus/bridge/verse/chorus/end)
- BEGIN: Start song
- MOVE (1st): Play verse
- HOLD: Establish song key/theme
- MOVE (2nd): Shift to chorus
- BREAK: Resolve chord progression
- REPEAT: Next verse cycle

**Micro Scale:** Individual chord (e.g., C major)
- BEGIN: Start oscillation at root C
- MOVE (1st): Build major-third oscillation (E)
- HOLD: Lock harmonic configuration (+4/−5)
- MOVE (2nd): Add fifth oscillation (G)
- BREAK: Confirm stable triad
- REPEAT: Next chord in progression

**Rabbit Hopping connects these:** The route from macro REPEAT (C major resolves, becomes reference for next BEGIN) feeds directly into micro BEGIN of the next chord via signed offset.

---

## Identity Preservation Through Transformation

### What Gets Preserved?

1. **Harmonic Identity:** C major remains "major" after transposition (same window offsets)
2. **Relational Structure:** The six-step recursion repeats at every scale
3. **Signed-Offset Grammar:** Routes expressed as (−N, +M) remain valid across transpositions
4. **Center Reference:** Rabbit hopping maintains live center; transformations are relative, not absolute

### What Changes?

1. **Absolute Pitch:** C major (C−E−G) transposed to D major (D−F#−A)
2. **Numeric Destinations:** Offsets map to different absolute semitones per root
3. **Scale Level:** Micro vs macro recursion operates at different frequency regimes

**Critical Distinction (per D-411):** Numerical matching between levels does NOT prove physical identity. Mapping must be demonstrated via consistent route receipts, not assumed from count matching.

---

## Testable Predictions

### Prediction 1: Chord Progression Reversibility
**Claim:** A chord progression route C→F→G→C has a valid reverse route.

**Test:**
- Define forward route as sequence of Rabbit Hop operations on Circle of Fifths
- Apply reverse Rabbit Hop operations (undo wrapper, undo TOP in reverse order)
- Verify final state returns to C major with harmonic identity intact

**Expected Result:** ✓ or ✗ with clear error signature

### Prediction 2: Algorithm Zero Recursion at Each Scale
**Claim:** The six-step sequence (BEGIN/MOVE/HOLD/MOVE/BREAK/REPEAT) appears at every scale level (micro = melody note, macro = song structure).

**Test:**
- Document six-step cycle for:
  - Single note oscillation (micro)
  - Single chord harmonic (mid)
  - Chord progression (large)
  - Song structure (macro)
- Verify same structure holds at all scales
- Confirm Rabbit Hopping connects each REPEAT → next BEGIN

**Expected Result:** ✓ Relational grammar recurses; ✗ if sequence breaks at any scale

### Prediction 3: Five-Scale Continuity
**Claim:** Micro→Small→Mid→Large→Macro form a continuous chain via Rabbit Hopping, with Algorithm Zero operating identically at each level.

**Test:**
- Define a complete chord progression (e.g., 12-bar blues)
- Trace Rabbit Hopping routes connecting all five scales
- Verify Algorithm Zero six-step appears at each scale
- Confirm no "missing scale" between micro note and macro song

**Expected Result:** ✓ Continuous chain; ✗ if any scale breaks connection

---

## Implementation: What Exists & What's Needed

### Current Code Branches

- **algorythm-zero-rabbit-hop-bridge:** Algorithm Zero + Rabbit Hopping foundation (G-747 node)
- **breadboard/pedal-lab-circle-fifths:** Circle of Fifths tuner and chord app
- **rabbit-hop-universal-translator:** Generalized Rabbit Hopping with reversible N grammar

### Integration Needed

1. **Unified Route Receipt Format** — Single grammar covering Algorithm Zero + Rabbit Hopping + Circle of Fifths
2. **Cross-Domain Route Tests** — Verify harmonic identity through Rabbit Hopping transposition
3. **Five-Scale Model Implementation** — Connect micro note oscillation → macro song structure via Algorithm Zero + Rabbit Hopping
4. **Reversibility Proof Suite** — Automated tests confirming forward/reverse routes for chord progressions

### First Priority (Fast Validation)

Per one-wave-framework-principles.md:
> **FIRST PRIORITY: Test Rabbit Hop ↔ Circle of Fifths**
> - Map Rabbit Hop music adapter to Circle of Fifths
> - Verify forward/reverse routes produce expected chord progressions
> - Confirm equal numeric destinations preserve harmonic identity
> - This yields known-good correspondence with full math backing

**Implementation Plan:**
1. Create `music_rabbit_hop_router.py` — Maps Circle of Fifths window offsets to Rabbit Hopping routes
2. Create `test_harmonic_identity_preservation.py` — Validates chord progressions through round-trip transposition
3. Create `route_receipt_codec.py` — Encodes/decodes route receipts as (source | TOP | wrapper)
4. Run test suite and lock in verified correspondence

---

## Canonical References

**Algorithm Zero:**
- G-747: Algorythm-Zer0 XYZ control/depth/structure canon node
- B-221: Six-Recursive-Steps oscillator

**Rabbit Hopping:**
- From RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md (in one-wave-framework-principles.md)
- All adapters (alphabet, music, guitar neck, scale rail) use shared core
- Five-scale bidirectional: Micro → Small → Mid → Large → Macro

**Circle of Fifths:**
- /areas/circle-of-fifths-app.md (Mark's music theory app, v25)
- Signed-offset architecture: Major (+4/−5), Minor (+3/−5), Triad (−4/+5), Power Chord (−1/+1)
- Octave physics: settling dynamics determine equilibrium point

**One-Wave Framework Principles:**
- D-411: Same ratio ≠ same domain (numerical isomorphism requires demonstrated mapping)
- G-766: Frequency doubling, amplitude doubling, geometric doubling are SEPARATE quantities
- PPF recursion: Relational grammar recurses; does NOT claim physical doubling at each scale

---

## Success Criteria

✅ **Unified Route Receipt Format** — Single grammar covers all three systems  
✅ **Harmonic Identity Preservation** — Chord progressions survive Rabbit Hopping transposition  
✅ **Algorithm Zero Recursion** — Six-step sequence appears at all five scales  
✅ **Reversibility Proof** — Forward/reverse routes confirmed via test suite  
✅ **Cross-Domain Mapping** — Numerical matching backed by demonstrated field coupling  

---

## PPF Integration: Point/Path/Field Rotation Across Scales

### The Micro = Macro Correlation

**Rabbit Hopping connects through PPF (Point/Path/Field) rotation at every scale.**

From one-wave-framework-principles.md:
> **PPF SCALE RECURSION is relational grammar recursion, NOT physical doubling: POINT→PATH→FIELD→CLOSURE→RESOLVED WHOLE→next-scale CENTER/REFERENCE**

**Applied to Unified System:**

| Scale | Point (Center) | Path (Addressing) | Field (Oscillation) |
|---|---|---|---|
| **MICRO** | Note root (e.g., C) | Rabbit Hop ±offset | Chord harmonic window |
| **SMALL** | Chord root (C major) | Route progression (+4/−5 window) | Harmonic field envelope |
| **MID** | Key center (C key) | Modulation routes (C→F→G) | Tonal field |
| **LARGE** | Song center (verse key) | Section transitions (verse→chorus) | Song structure envelope |
| **MACRO** | System nucleus (sun) | Orbital paths (planetary PPF) | Gravitational field |

**The Critical Insight:** The **sun as nucleus** maps to a neural network model where:
- Sun = central reference point (POINT in PPF)
- Orbital mechanics = rabbit-hopping addressing grammar (PATH in PPF)
- Solar system = field oscillation structure (FIELD in PPF)
- **Planetary orbits are "chord progressions" in gravitational space**

### Sun-as-Nucleus / Solar System as Neural Network

A solar system is structurally identical to:
- A nerve nucleus with dendrite projections
- A chord with root and harmonic overtones
- An Algorithm Zero recursion at macro scale

**The Mapping:**

```
Sun (nucleus, point center)
  ├─ Mercury (inner harmonic, tight orbit)
  ├─ Venus (phase-locked resonance)
  ├─ Earth (stable holding resonance, lives here)
  ├─ Mars (asymmetric orbit, Triad-like)
  ├─ Jupiter (major oscillator, bass frequency)
  └─ Beyond (harmonic upper extensions)
```

Each planet's orbit is a **Rabbit Hopping route** from the sun, expressed as:
- Signed offset (N from sun)
- Operation family (elliptical path = SHIFT_THEN_DOUBLE dynamics)
- Resonance wrapper (Kepler's harmonics)

**PPF Recursion:** The sun's internal PPF (plasma cycle, magnetic field) is IDENTICAL to the solar system's orbital PPF (Kepler cycles). Not physically scaled, but grammatically identical.

### How Rabbit Hopping Connects PPF Rotations

At every scale, Rabbit Hopping **addresses the center and its mirrored alternatives** via PPF:

1. **Identify center** (Point): root C, sun, song key
2. **Define addressing grammar** (Path): signed offsets, orbital mechanics, chord progressions
3. **Establish field** (Field): harmonic envelope, gravitational curve, tonal space
4. **Complete rotation** (RESOLVE): return to center, confirm identity preserved
5. **Recurse** (REPEAT): center becomes reference for next scale

This is **pure relational grammar**, not physical scaling. The same addressing structure appears at sun→planet as at root→third→fifth in music.

---

## Next Steps

1. **Immediate (this session):** Create unified route receipt format and basic mapper ✓
2. **Short-term:** Implement Rabbit Hop ↔ Circle of Fifths test suite (per priority) ✓
3. **Medium-term:** Five-scale model with Algorithm Zero + PPF at each level
4. **Long-term:** Deploy integrated system:
   - Music: Circle of Fifths app with Algorithm Zero recursion
   - Robotics: Motor control via Rabbit Hopping routes
   - Physics: Solar system modeling via PPF rotation grammar
   - Learning: Six-step choice teaching via Algorithm Zero

---

## Complete Framework Documentation (October 5, 2026 Integration)

This document is the integration hub. Supporting documents detail each mechanism:

### Core Frameworks
- **UNIFIED_SCALE_INVARIANT_GRAMMAR.md** — Complete integration showing all five systems (Algorithm Zero, Rabbit Hopping, Circle of Fifths, PPF Rotation, Gravity Wakes) operating together at every scale from Great Attractor to electrons
- **PPF_QUANTUM_TO_COSMIC.md** — Documents Point/Path/Field scale-invariant recursion across 10 scales (quantum to universal)
- **SUPERFLUID_OPERATIONS_FRAMEWORK.md** — Grounds "four forces" (+, −, ×, ÷) in mathematical operations on superfluid field
- **ONE_WAVE_TERMINOLOGY_FRAMEWORK.md** — Replaces Standard Model force language with One-Wave mechanism language

### Quantum to Cosmic Mechanics
- **QUANTUM_SCALE_PPF_ALGORITHM_ZERO.md** — Algorithm Zero at electron scale, magnetism as lattice reorganization enabling PPF rotation, spin-orbit coupling as wake locking
- **GRAVITY_WAKE_NESTING_ROTATION_CASCADE.md** — Top-down causality: rotation induced by parent wakes from Great Attractor down to electrons, tidal locking as wake phase-lock, dark matter as extended wake coherence

### Implementation
- **rabbit_hop_circle_unified_mapper.py** — Python implementation validating harmonic identity preservation through Rabbit Hopping transpositions, with test suite for chord progressions, route receipts, and round-trip verification

### Integration Map
All documents reference canonical nodes (C-317, C-318, C-322, C-323, D-408, D-409, D-600/601/602, B-221, G-747) establishing this framework within existing One-Wave architecture.

**Key Principle:** Scale-invariant grammar means Algorithm Zero (temporal), Rabbit Hopping (spatial), Circle of Fifths (harmonic), PPF Rotation (relational), and Gravity Wakes (causal) all operate identically at every scale. Same relational grammar, different frequencies. One physics.

---

**Co-Authored-By:** Claude Haiku 4.5 <noreply@anthropic.com>
