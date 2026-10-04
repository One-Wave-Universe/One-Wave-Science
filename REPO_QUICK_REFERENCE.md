# Repo quick reference

Use this before the tree. Scope first. Then one file for the question. If that file does not say it, search. If search misses, ask. Do not fill a gap with a guess.

## Scope

Three jobs. Do not mix them.

| Job | Repo | What it is allowed to say |
|---|---|---|
| Science | `One-Wave-Science` | Claims, tests, math, sims. A file here is a hypothesis until a test passes. |
| Builds | `Builds` | How to make it. Cell, schematics, algorithms, grant-facing build. |
| Mythos | `Mythos-and-Stories` | Story only. No scientific claims. |

Also on the account, not a fourth job:

| Repo | Use |
|---|---|
| `Bridge-Comand` | AI relay directions. |
| `Bench` | Private bench notes. Not the grant face. |
| `One-Wave-Universe` | Grant package. Points at Builds. |

Read Science in the order `AI_CANONICAL_START_HERE.md` gives. Gate values stay on the node. Do not copy them into a summary.

## Map

Open the first file. Use the next files only if the first one does not answer.

CERN particle to wave
Open `One-Wave-Science/DERIVATION_PHASE_2_CERN_BRIDGE/CERN_TO_WAVE_REFERENCE.md`
Then `DERIVATION_PHASE_2_CERN_BRIDGE/README.md`
Then `DERIVATION_PHASE_2_CERN_BRIDGE/cern_particle_mapper.py`
Use for masses, the conversion chart, and particle-to-mode.

CERN detector hits
Open `One-Wave-Science/sims/01-cern-wave-transform/README.md`
Then `sims/01-cern-wave-transform/transform.json`
Use for raw detector hits. Do not start from reconstructed particle labels.

LIGO, open data
Open `One-Wave-Science/ENGINE_EVIDENCE_PIPELINES.md`
Then `One_Wave_Bench/data/OPEN_DATA_WAVE_PIPELINE.md`
Charts: `Nodes/D-414_Four_Interaction_Shell_Simulation/graphs/ligo_events.png` and `ligo_spectrum.png`
Use for LIGO and other public-data pipelines. Cite the chart path. Do not describe a plot you did not open.

Jetson terminal
Open `One-Wave-Science/JETSON_ACCESS_AND_TERMINAL.md`
Then `AI_JETSON_TOOL_GUIDE.md`
Then `CHATGPT_JETSON_TERMINAL_BRIDGE.md`
Then `docs/repo_split/08_AI_AGENTS_JETSON_AND_TERMINAL.md`
Code: `One_Wave_Bench/hive-pipe/chatgpt_terminal_pull.py`
Use for how to run the Jetson terminal.

Which repo owns this
Open `One-Wave-Science/ALL_GITHUB_INTO_THREE.md`
Builds state: `Builds/MASTER_CURRENT_STATE.md`
Cell: `Builds/cell-v1/CELL.md`
Use when the question is where something lives.

## If the map misses

Search with the noun in the question. Open the best file. If that file does not contain the claim, ask for the missing file or fact. Stop there.
