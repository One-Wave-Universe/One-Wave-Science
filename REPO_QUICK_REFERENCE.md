# Repo quick reference

Before the tree: name the job, open the first file, stop if it answers.

If it misses: next file, then search the noun, then ask. Never guess.

Snowball: the opened file names the next file. Follow those names. A file that actually opened joins the map. Do not invent the next name.

## Scale

Source: `Nodes/G-763_Scalar_to_Harmonic.md`. Yellow. Six words. No seventh.

```text
scalar        differential      vector
tensor        stratum           harmonic
```

Top row is Field. Bottom row is Void, the next copy. Same three moves, twice.

| Pair | Move |
|---|---|
| scalar ↔ tensor | intersect. Same shape, cut. |
| differential ↔ stratum | oppose. Pair against layer. |
| vector ↔ harmonic | invert. The move becomes the standing cycle. |

Chain, each step holding every step under it:

scalar → differential → vector → tensor → stratum → harmonic → scalar

| Step | Holds | Points to | Node says |
|---|---|---|---|
| scalar | the point | differential | one number on Ground |
| differential | scalar | vector | two rails, Field minus Void |
| vector | scalar, differential | tensor | the move along a directed edge |
| tensor | scalar through vector | stratum | the carry, M_ij, W_ij |
| stratum | scalar through tensor | harmonic | the nest: cell, chip, cube, Rubik |
| harmonic | all five | scalar | closed loop, next-scale DC |

Required edges: stratum → harmonic, and harmonic → scalar.

Tensor does not point at harmonic. The carry reaches the loop only through the nest: tensor → stratum → harmonic. Harmonic then returns to scalar. That return is the next scale, not a seventh word.

Harmonic geometry and propagation stay in their own nodes. `Nodes/D-405_Harmonic_Shell.md` quantizes a closed path, not energy. `Nodes/E-531_Dual_Harmonic_Propagation_Operator.md` steps frequency labels. It does not set mass. Both yellow.

## Scope

| Job | Repo | Says | Does not say |
|---|---|---|---|
| Science | `One-Wave-Science` | Claims, tests, math, sims. Hypothesis until a test passes. | Build orders, stories. |
| Builds | `Builds` | How to make it. Cell, schematics, algorithms, grant build. | Untested science, stories. |
| Mythos | `Mythos-and-Stories` | Story only. | Scientific claims. |

| Also | Says |
|---|---|
| `Bridge-Comand` | AI relay directions. |
| `Bench` | Private bench notes. Not the grant face. |
| `One-Wave-Universe` | Grant package. Points at Builds. |

Science order: `AI_CANONICAL_START_HERE.md`. Gate values stay on the node.

## Map

Open the first path. Open the next only if it misses.

Scalar differential vector tensor stratum harmonic
- `One-Wave-Science/Nodes/G-763_Scalar_to_Harmonic.md`
- `Nodes/A-103_Differential.md`
- `Nodes/D-405_Harmonic_Shell.md`
- `Nodes/E-531_Dual_Harmonic_Propagation_Operator.md`
- Path: tensor → stratum → harmonic → scalar. No direct tensor-to-harmonic edge.

CERN particle to wave
- `One-Wave-Science/DERIVATION_PHASE_2_CERN_BRIDGE/CERN_TO_WAVE_REFERENCE.md`
- `DERIVATION_PHASE_2_CERN_BRIDGE/README.md`
- `DERIVATION_PHASE_2_CERN_BRIDGE/cern_particle_mapper.py`
- Masses, conversion chart, particle-to-mode. No mass or formula that is not in the file.

CERN detector hits
- `One-Wave-Science/sims/01-cern-wave-transform/README.md`
- `sims/01-cern-wave-transform/transform.json`
- Raw hits as point, path, field. Not reconstructed particle labels.

LIGO, open data
- `One-Wave-Science/ENGINE_EVIDENCE_PIPELINES.md`
- `One_Wave_Bench/data/OPEN_DATA_WAVE_PIPELINE.md`
- `Nodes/D-414_Four_Interaction_Shell_Simulation/graphs/ligo_events.png`
- `Nodes/D-414_Four_Interaction_Shell_Simulation/graphs/ligo_spectrum.png`
- Public-data pipelines. Cite a chart. Do not describe one you did not open.

Jetson terminal
- `One-Wave-Science/JETSON_ACCESS_AND_TERMINAL.md`
- `AI_JETSON_TOOL_GUIDE.md`
- `CHATGPT_JETSON_TERMINAL_BRIDGE.md`
- `docs/repo_split/08_AI_AGENTS_JETSON_AND_TERMINAL.md`
- `One_Wave_Bench/hive-pipe/chatgpt_terminal_pull.py`
- How to run the terminal. No command that is not in these files.

Which repo owns this
- `One-Wave-Science/ALL_GITHUB_INTO_THREE.md`
- `Builds/MASTER_CURRENT_STATE.md`
- `Builds/cell-v1/CELL.md`
- Where it lives. No build order in Science. No story claim in Science or Builds.
