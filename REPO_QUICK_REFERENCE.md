# Repo quick reference

Before the tree: name the job, open the first file, stop if it answers.

Miss path: next file, then search the noun, then ask. Never guess.

Snowball: the opened file names the next file. Open that. It names the one after. Follow the names until the question is answered or the names stop. A verified path joins the map for the next question. Do not jump sideways. Do not invent the next name.

Scale ladder, from `Nodes/G-763_Scalar_to_Harmonic.md`. Six words. No seventh.

scalar → differential → vector → tensor → stratum → harmonic → scalar

Each step contains every step before it. Every earlier step points at the next. Two edges are required, not implied: stratum → harmonic, and harmonic → scalar. Tensor does not point at harmonic. The carry reaches the loop only as tensor → stratum → harmonic. Harmonic is the closed loop that becomes the next-scale scalar. It is not a new gate.

| Step | Contains | Points to | In G-763 |
|---|---|---|---|
| scalar | the point | differential | one number on Ground |
| differential | scalar | vector | two rails, Field minus Void |
| vector | scalar, differential | tensor | the move, a directed edge |
| tensor | scalar through vector | stratum | the carry, quadratic views |
| stratum | scalar through tensor | harmonic | the nest layer. Required edge: stratum → harmonic |
| harmonic | all five | scalar | closed loop. Required edge: harmonic → scalar |

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

Open the first path. Then only if it misses.

Scalar differential vector tensor stratum harmonic
- `One-Wave-Science/Nodes/G-763_Scalar_to_Harmonic.md`
- `Nodes/A-103_Differential.md`
- `Nodes/D-405_Harmonic_Shell.md`
- `Nodes/E-531_Dual_Harmonic_Propagation_Operator.md`
- Six-step scale. Tensor → stratum → harmonic. Stratum → harmonic and harmonic → scalar are required. No direct tensor-to-harmonic edge. No seventh word.

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
