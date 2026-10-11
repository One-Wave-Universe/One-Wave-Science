# Dual-butterfly harmonic coordinates: A/E power chord

**Status:** Musical interval arithmetic ESTABLISHED under 12-TET, A4=440 Hz. Butterfly interpretation, envelope lean and settling direction UNVERIFIED. **Date:** 2026-10-10. **Scope:** science only; no CELL_V1 or breadboard modifications.

## User-proposed coordinate grammar

Each played note has a *separate* butterfly with two moving curved lines, both anchored at the same top/bottom points on a vertical zero axis. Each midpoint moves horizontally, passes through zero, reverses, and may damp. This is a visualization of selected oscillatory coordinates, **not a measured string mode**.

Major: `-5 (0) +4`; minor: `-5 (0) +3`; mirror/tritone: `-6 (0) +6`; equal-third augmented structure: `-4 (0) +4`. All offsets are signed semitones from the butterfly's *own* reference, not a third interval between outer notes. These coordinate labels are proposed and do not uniquely determine physical envelopes. Conventional chord names depend on root/inversion; e.g. A-centered F-A-C# is F augmented, not A augmented.

A/E power chord as two *complete* butterflies:

- A butterfly `-5 (A4=0) +4` = E4, A4, C#5.
- E butterfly `-5 (E5=+7 relative A4) +4` = B4, E5, G#5.
- This is **two played notes**, A4 and E5, not six independently played notes. The four flank frequencies are coordinate predictions, not established measured partials.

## Reproducible calculation

12-TET mapping: `f(n) = 440 * 2^(n/12) Hz`, with signed semitone offset n from A4. For steady zero-phase sinusoids, adjacent zero crossings are separated by `1/(2f)` seconds; initial phase shifts the crossing schedule.

| Coordinate | Offset n from A4 | f (Hz) | Zero-crossing spacing (ms) |
|---|---:|---:|---:|
| E4 | -5 | 329.627557 | 1.516863 |
| A4 | +0 | 440.000000 | 1.136364 |
| C#5 | +4 | 554.365262 | 0.901932 |
| B4 | +2 | 493.883301 | 1.012385 |
| E5 | +7 | 659.255114 | 0.758432 |
| G#5 | +11 | 830.609395 | 0.601968 |

E5/A4 frequency ratio = `2^(7/12) = 1.498307077`; all corresponding E-butterfly components are scaled by the same factor. Octave wrapping: +7 is pitch-class equivalent to -5, but **not the same absolute frequency**. +6/-6 are mirror positions in log-frequency and an octave apart in absolute frequency; 2:1 timing does not imply identical crossings at all instants.

## Baseline physically interpretable models

1. Fixed-end ideal string fundamental: `y(x,t)=q(t) sin(pi*x/L)`, midpoint displacement `q(t)`, with stationary ends. A mirrored pair of drawn curves is a visualization, not proof of two intrinsic components.
2. Free damped mode: `q''+2 gamma q'+omega0^2 q=0`. For underdamping, amplitude decays exponentially while oscillation frequency remains constant. Ordinary damping does not continuously slow the frequency.
3. For physically changing frequency, explicitly specify changing stiffness/tension or nonlinear dynamics, and test independently. Do not present a prescribed frequency ramp as a prediction.
4. Acoustic superposition: `p_total(t)=sum_j p_j(t)`. Interference is not automatically energy transfer.
5. Coupled-string energy transfer requires a mechanical/acoustic coupling model with masses, stiffnesses, damping, bridge/body response and an energy ledger. The raw note-coordinate sums do not imply a physical high/low settling bias.
6. Each plucked string's measured spectrum can contain many harmonics; its C#-like fifth harmonic is approximately 5 times the A fundamental, NOT automatically C# at +4 semitones in the immediately higher octave. Do not assert minor-third components appear merely because the chord is minor.

## Test gates

- Unit test semitone wrap: `f(n+12)=2*f(n)`, and `f_E5/f_A4=2^(7/12)`.
- Zero-crossing test: synthetic steady sinusoids at all six mapped frequencies; phase offsets measured explicitly.
- Compare pure 3:2 fifth to equal-tempered 2^(7/12); distinguish exact phase closure from approximate recurrence.
- Record isolated A4 and E5 strings, microphone and bridge pickup; estimate actual FFT partials, envelopes, relative phases and decay, with windowing/calibration.
- Compare isolated recordings summed offline to simultaneous playing. Differences beyond linear superposition motivate coupling analysis, not automatic proof of new physics.
- Test coupled oscillator models against controls; fit energy ledger and identify whether frequency slowing is observed.
- **Pass** only numerical arithmetic and control equations until recordings/simulation receipts exist. One-Wave physical envelope/lean interpretation remains **UNVERIFIED**.

## References / governance

See `AI_CANONICAL_START_HERE.md`, `GENERAL_REFERENCE_RULES.md`, `AI_FOREMAN_WORK_REGISTER.md`. This node is an experimental candidate and must not alter established physics or engineering canon without evidence. No automatic extension from musical pitch-class symmetry to physical field dynamics.
