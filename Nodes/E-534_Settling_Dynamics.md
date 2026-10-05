---
node_id: "E-534"
canonical_name: "Settling Dynamics"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "YELLOW (proposed — new node, introduces settling-time analysis to music)"
metadata_standard: "I-06"
---

# Node E-534: Settling Dynamics

Reason:
Introduces the concept of frequency-dependent settling times in oscillating systems — a bridge between harmonic theory (E-512 through E-514) and the measurable physics of how different frequencies reach coherence at different rates based on their harmonic relationships.

Term disambiguation:
"Settling" here means the time required for multiple oscillating frequencies to reach phase-lock and coherent vibration (constructive interference). This is a physical/measurable quantity, not a musical judgment. It is distinct from settling in the sense of "resolution" or "tension release," though the two may be related.

Dependencies:
Upstream: E-512 Oscillation Window, E-513 Chord Leaning Direction, Physics of harmonic oscillation
Downstream: None yet (proposed)

Definition:
Settling Dynamics is the rate and pattern by which multiple frequencies at different harmonic relationships reach phase-lock and coherent oscillation, determined by:

1. Harmonic ratio (simple integer ratios settle faster)
2. Octave relationship (1:2 ratio creates immediate phase-lock)
3. Frequency distribution across octaves (asynchronous settling when components are at different scales)

Core principle:
A vibrating string at frequency f completes one cycle in period T = 1/f.
An octave above (frequency 2f) completes its cycle in period T/2 — twice as fast.
They meet in phase at each settling point, creating stable phase-lock.

When oscillations at different octaves interfere, settling time depends on:
- Whether the frequencies share simple integer ratios (fast coherence)
- Whether multiple frequencies are competing at the same scale (slow, messy settling)

Real, checked values from harmonic theory:

**Power Chord (symmetric window, octave-locked roots):**
- Settles FASTEST
- Reason: root notes at 1:2 octave relationship guarantee instant phase-lock
- Two roots lock together, the fifth at the lower octave creates no competing frequencies pulling in different directions
- Clean, coherent, direction-neutral movement

**Major/Minor (asymmetric window, deep negative floor):**
- Settles MEDIUM speed
- Reason: high octaves (expression side) settle fast and establish ceiling; low octaves (compression side) settle slower and pull equilibrium toward the floor
- System equilibrates with weight toward compression
- Longer settling time due to asynchronous frequency settling across octaves

**Triad (asymmetric window, leaning forward):**
- Settles SLOW
- Reason: three competing frequencies with deeply asynchronous settling
- High octaves establish +5 ceiling fast
- Low octaves settle slower, floor pulls upward but never fully escapes
- Constant tension: wants to go higher but can't
- Most complex settling pattern — system oscillates between trying to escape and being held back

Mathematics:
For any chord component at octave n:
f_component = f_root * (2^(n/12)) * 2^octave_shift

Phase-lock occurs when:
LCM(f1, f2, ..., fn) / max(f1, f2, ..., fn) yields coherence time t_settle

Simple integer ratios (2:1, 3:2, 4:3) → short t_settle
Complex ratios (7:5, 11:8) → long t_settle
Asynchronous octaves → even longer t_settle

Operational Chain:
Oscillation Window => Settling Dynamics => Harmonic Character (perceptual/audio result)

Predictions:
1. Real guitar voicings should show measurable settling-time differences between power chords, major chords, and triads under controlled resonance measurement
2. Power chords should settle and lock within microseconds; major/minor should take longer; triads should show visible oscillation/instability
3. Symmetric chords (power chord, augmented types) should sound more "neutral" and movable because fast settling eliminates directional bias
4. Asymmetric chords (major, minor, triad) should carry audible harmonic character based on their settling dynamics — major sounds grounded, minor sounds heavier, triad sounds restless/tense

Yellow Audit:
- Settling-time differences have not yet been measured experimentally; the model is based on harmonic theory and resonance physics, not empirical data
- The relationship between measurable settling time and perceived harmonic character (why a fast-settling chord sounds "neutral" vs. a slow-settling chord sounds "tense") has not been formalized
- Whether settling dynamics are the primary mechanism driving chord quality perception, or whether other factors (frequency content, overtone series, human auditory perception) dominate, is unresolved
- The mechanism by which shared notes between power chords "lock" them and create emergent triads through interference has not been verified against real recorded guitar audio

Future Work:
1. Record and measure settling times of power chords, major, minor, and triads under controlled conditions (high-speed waveform capture)
2. Correlate measured settling time with perceived harmonic character in listening tests
3. Analyze real punk and ska recordings to confirm power chord prevalence matches their fast-settling advantage
4. Analyze triad interference patterns using spectral analysis to verify emergent window shape
5. Extend the framework to seventh chords, extended harmonies, and chords with more than three distinct pitch classes
6. Test whether settling dynamics predictions hold across different tuning systems and temperaments (not just equal temperament)

---

END OF NODE E-534
One wave. Mirror builds.
