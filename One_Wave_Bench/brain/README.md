# M4 verbal-command brain — CPU reference

This package is the first executable slice of the two-state-machine brain. It
learns and recalls text commands but does not perform speech recognition or
drive physical motors.

## Fixed processing chain

1. **BC–DC:** binary choice and direct command selection.
2. **TC–AC:** ternary `COMPRESS / HOLD / EXPRESS` differential cycle. These
   are the only directional words exposed by this brain layer.
3. **QC–RC:** Inward, Outward, Across, and Over views routed by one of four
   rotational-field phase quadrants.
4. **M4:** fast associative recall and routing between the two state machines.
5. **Dream Engine / Field / expressive:** interprets the cue and proposes.
6. **Administrator / Void / compressive:** checks safety, continuity, and
   permission, then commits or holds.
7. **Consequence feedback:** measured error returns to the next M4 cycle.

The Dream Engine cannot authorize its own motion. The Administrator cannot
silently erase the expressive proposal. `STOP` is committed by the
Administrator even when movement actuators are unavailable.

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
```

The installer uses only Python's standard library, creates a local virtual
environment, initializes the digest-chained receipt archive, and runs a smoke
test that requires a detected Jetson GPU. It does not install a microphone,
motor driver, CUDA kernel, or automatic startup service. The current package
is the safe command/memory/runtime boundary those later adapters connect to.
