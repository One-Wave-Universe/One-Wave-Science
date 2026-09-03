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

`rabbit_hop_alphabet.py` implements the three currently declared G-721 routes:
the original `N×2`, ascending-after `(N×2)+K`, and ascending-before `(N+K)×2`.
The original is a separate receipt; both ascending ladders use `K=1,2,3,...`.
Every top produces both mandatory wrapper packets `top-1` and `top+1`; there is
no bare or zero-wrapper packet. Odd tops receive even wrappers and even tops
receive odd wrappers. Alphabet orientation supports `A→Z:1→26` and
`Z→A:1→26`; inverting that side-to-side axis also inverts logical up/down.
Polarity, route family, offset, wrapper side, orientation, and traversal remain
separate receipt fields. The authoritative grammar and examples are locked in
`RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md`.

## Rabbit-hop constellation reconstruction

`constellation_memory.py` is the first executable end-to-end reconstruction
slice. It stores overlapping memories as distinct constellation nodes, enters a
cue-linked neighborhood, traverses recorded G-721 odd connectors, performs
deterministic Hopfield-style completion, uses seeded bounded Boltzmann selection
only when ambiguity remains, and returns a context-validation receipt. The
receipt records the exact invertible route and marks probabilistically supplied
features uncertain. A matched flat baseline verifies when the route and
constellation actually improve recall instead of merely adding machinery.

## Test

```bash
python -m unittest One_Wave_Bench.brain.test_command_memory
python -m unittest One_Wave_Bench.brain.test_constellation_memory
python -m unittest One_Wave_Bench.brain.test_rabbit_hop_alphabet
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
