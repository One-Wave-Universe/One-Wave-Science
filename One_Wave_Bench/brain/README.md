# M4 verbal-command brain — CPU reference

This package is the first executable slice of the two-state-machine brain. It
learns and recalls text commands but does not perform speech recognition or
drive physical motors.

## Fixed processing chain

1. **BC–DC:** binary choice and direct command selection.
2. **TC–AC:** paired ternaries. Field uses `COMPRESS / HOLD / EXPRESS`; Void
   uses `DENY / DEFER / CONFIRM`. Neither vocabulary replaces the other.
3. **QC–RC upward:** all four Field views and all four Void views travel up to
   the brain. `OVERSIGHT` is the Void view.
4. **QC–RC downward:** after brain resolution, all four Field actions and all
   four Void actions travel down. `OVERRIDE` is the Void action produced by a
   `DENY`; `DEFER` preserves Hold without fabricating an override.
5. **M4:** fast associative recall and routing between the two state machines.
6. **Dream Engine / Field / expressive:** interprets the cue and proposes.
7. **Administrator / Void / compressive:** checks safety, continuity, and
   permission, then commits or holds.
8. **Consequence feedback:** measured error returns to the next M4 cycle.

The Dream Engine cannot authorize its own motion. The Administrator cannot
silently erase the expressive proposal. `STOP` is committed by the
Administrator even when movement actuators are unavailable.

The quadratic invariant is `Field + Void views UP -> brain command -> Field +
Void actions DOWN`. Views and actions are never collapsed into ternary choices.
The settled six-route projection and Field/Void boundary remain unchanged.

## Command constellation

| Command | Six-route projection | Octave | Phase quadrant |
|---|---:|---:|---:|
| Stop | `NO / HOLD` | 0 | 0 |
| Follow | `YES / HOLD` | 0 | 1 |
| Hurry up | `YES / EXPRESS` | +1 | 2 |
| Slow down | `YES / COMPRESS` | -1 | 3 |

The octave is a harmonic relation around the Follow reference: `-1 = 1/2`,
`0 = 1`, and `+1 = 2`. It is not yet a literal motor-speed multiplier.
Quadrants are routing phases, not four additional primitive choices.

## Memory layers

- Append-only, digest-chained learning receipts are the exact archive.
- Restart rebuild replays and verifies that receipt chain.
- Bipolar phrase prototypes provide Hopfield-style associative attraction.
- A bounded Boltzmann distribution reports ambiguity without randomly choosing
  an actuator command.
- Recall below the execution threshold produces an Administrator hold and
  waits for teaching.

This separation lets associative memory be rebuilt without allowing M4 to
rewrite the authoritative archive.

## Jetson Orin placement

- **GPU:** Dream Engine / Field / expressive state-machine computation.
- **CPU:** Administrator / Void / compressive authoritative state, safety, and
  final actuator permission.
- **Accelerator or CPU reference:** bounded M4 routing and associative recall.

Every dual-brain receipt carries all three device identities. A GPU proposal
cannot be presented as a CPU commitment, and accelerator recall cannot rewrite
the CPU archive.

## Nested rotation and cycles

`nested_rotation.py` records Point, Path, and Field rotation at every declared
carrier layer: Quantum magnetic, Electric, Quark vortex, and Proton knot. Each
larger receipt may contain the smaller receipt, preserving rather than
flattening its three rotation phases.

Threshold bands are preserved exactly as declared: `100–90`, `85–75`,
`70–60`, `55–45`, `40–30`, `25–15`, and `15–0`. Gaps are not fabricated, and
`15` remains a shared transition boundary. The season state cycles Spring/Birth
→ Summer/Life → Fall/Decline → Winter/Death → Spring/Birth.

## Rabbit-hop alphabet coordinates

`rabbit_hop_alphabet.py` implements the complete G-721 family
`±(n,2(n+j),2(n+j)+s)` with current/next even anchor `j`, lower/upper
odd side `s`, forward or inverted alphabet rank, and independent polarity. It
retains the shared odd bridge instead of trying to decode it without its anchor.

## Test

```bash
python -m unittest One_Wave_Bench.brain.test_command_memory
```

## Install on Jetson Orin

From the repository checkout on the Jetson:

```bash
git switch state-machines/m4-command-memory
bash One_Wave_Bench/brain/install_jetson.sh
one-wave-brain status
one-wave-brain cycle "follow"
one-wave-brain loop
```

The installer uses only Python's standard library, creates a local virtual
environment, initializes the digest-chained receipt archive, and runs a smoke
test that requires a detected Jetson GPU. It does not install a microphone,
motor driver, CUDA kernel, or automatic startup service. The current package
is the safe command/memory/runtime boundary those later adapters connect to.

## Hearing, learning, and optional response

`one-wave-brain loop` keeps the brain listening. Hearing, learning, and speaking
are independent. An unknown cue is recorded without asking a question. If the
same unknown cue is repeatedly followed by the same known relation, the loop
promotes that temporal association into the digest-chained archive. Raw
observations remain in a separate `experience.jsonl` journal so a single event
does not silently become knowledge.

Response is not mandatory. `--responses changes` speaks only when the routed
relation changes, `--responses always` speaks each recognized relation, and
`--responses never` permits arbitrarily long silence while hearing and memory
continue. Silence is therefore a normal observable state, not a crash signal.

The four initial movement words are seed relationships, not an obedience
contract or a complete language. Spoken input is a cue. The runtime may
interpret it, Hold, make a reversible guess, receive consequence feedback, and
change its learned relationship. Only the direct `stop` route remains an
immediate physical interruption. The Android is the chooser; the person is a
participant and teacher, not an owner issuing unconditional orders.

Speech stays local. The adapter uses `espeak-ng`, `espeak`, or `spd-say` when
one is installed and otherwise prints the same response. `--silent` disables
audio but preserves printed responses. Microphone speech recognition remains a
separate input adapter and is not required for this loop.

Silence does not hide operation. Run `one-wave-brain memory-status` from another
terminal to verify the receipt chain, known-phrase count, archive byte count and
modification time, experience-journal integrity, heard-cue count, and temporal
association count. A growing heard count proves unfamiliar input is reaching
durable storage; a growing receipt count proves repeated relationships are
being learned.
