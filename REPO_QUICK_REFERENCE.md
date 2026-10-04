# Repo quick reference

Read this before the tree.

1. Name the job: Science, Builds, or Mythos.
2. Open the first file in the matching row.
3. Open the next file only if the first does not answer.
4. If no row matches, search the noun in the question.
5. If the file does not contain the claim, ask. Stop. Do not guess.

## Scope

Three jobs. Do not mix them.

| Job | Repo | Allowed to say |
|---|---|---|
| Science | `One-Wave-Science` | Claims, tests, math, sims. Hypothesis until a test passes. |
| Builds | `Builds` | How to make it. Cell, schematics, algorithms, grant build. |
| Mythos | `Mythos-and-Stories` | Story only. No scientific claims. |

Not a fourth job:

| Repo | Allowed to say |
|---|---|
| `Bridge-Comand` | AI relay directions. |
| `Bench` | Private bench notes. Not the grant face. |
| `One-Wave-Universe` | Grant package. Points at Builds. |

Science read order is `AI_CANONICAL_START_HERE.md`. Gate values stay on the node. Do not copy a gate into a summary.

## Map

CERN particle to wave
- Open: `One-Wave-Science/DERIVATION_PHASE_2_CERN_BRIDGE/CERN_TO_WAVE_REFERENCE.md`
- Then: `DERIVATION_PHASE_2_CERN_BRIDGE/README.md`
- Then: `DERIVATION_PHASE_2_CERN_BRIDGE/cern_particle_mapper.py`
- Use for: masses, the conversion chart, particle-to-mode.
- Do not: invent a mass or a formula that is not in the file.

CERN detector hits
- Open: `One-Wave-Science/sims/01-cern-wave-transform/README.md`
- Then: `sims/01-cern-wave-transform/transform.json`
- Use for: raw detector hits as point, path, field.
- Do not: start from reconstructed particle labels.

LIGO, open data
- Open: `One-Wave-Science/ENGINE_EVIDENCE_PIPELINES.md`
- Then: `One_Wave_Bench/data/OPEN_DATA_WAVE_PIPELINE.md`
- Charts: `Nodes/D-414_Four_Interaction_Shell_Simulation/graphs/ligo_events.png`, `ligo_spectrum.png`
- Use for: LIGO and other public-data pipelines.
- Do not: describe a chart you did not open. Cite the path.

Jetson terminal
- Open: `One-Wave-Science/JETSON_ACCESS_AND_TERMINAL.md`
- Then: `AI_JETSON_TOOL_GUIDE.md`
- Then: `CHATGPT_JETSON_TERMINAL_BRIDGE.md`
- Then: `docs/repo_split/08_AI_AGENTS_JETSON_AND_TERMINAL.md`
- Code: `One_Wave_Bench/hive-pipe/chatgpt_terminal_pull.py`
- Use for: how to run the Jetson terminal.
- Do not: invent a command that is not in those files.

Which repo owns this
- Open: `One-Wave-Science/ALL_GITHUB_INTO_THREE.md`
- Builds state: `Builds/MASTER_CURRENT_STATE.md`
- Cell: `Builds/cell-v1/CELL.md`
- Use for: where a thing lives.
- Do not: put a build order in Science, or a story claim in either.

## Miss

No row matched, or the opened file does not contain the claim.

Search the noun. Open the best hit. If it still does not say it, ask for the missing file or fact. Stop.
