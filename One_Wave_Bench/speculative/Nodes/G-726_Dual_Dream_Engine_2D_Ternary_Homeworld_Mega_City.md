---
node_id: "G-726"
canonical_name: "Dual Dream Engine — Programmed 2D Ternary Homeworld"
namespace: "NODE"
gate: "GREEN"
lifecycle: "PROPOSED_BUILD"
classification: "Non-Cognitive Programmed Dream World / 2D Ternary Simulation / NAS Storage"
claim_gate_detail: "GREEN (role separation) / BROWN (Homeworld implementation)"
metadata_standard: "I-06"
---

# Node G-726: Dual Dream Engine — Programmed 2D Ternary Homeworld Mega City

## Permanent correction

The Homeworld Dream Engine is **not an Administrator** and does not contain an
Administrator. It is a non-cognitive programmed simulation.

The world has **two spatial dimensions**. `3` refers to its ternary local state,
not to three-dimensional space.

## Dual-engine separation

1. **Cognitive Dream Engine** — belongs to the separate M4/Dream/Mind research architecture.
2. **Programmed Dream World** — a non-cognitive 2D Homeworld/Mega-City simulation.

The programmed world does not possess identity, private memory, beliefs,
commitment authority, or a self-model. It executes declared world rules and
returns state, measurements, and rendered scenes.

## 2D ternary world cell

The Homeworld is a planar lattice/grid. Every cell has a three-state update:

`m in {-1,0,+1}`

- `-1 COMPRESS`: decrease, close, cool, remove, contract, or return;
- `0 HOLD`: preserve the current relationship;
- `+1 EXPRESS`: increase, open, heat, add, expand, or propagate.

The sign is always interpreted by the cell's typed channel. Density, traffic,
power, water, vegetation, sound, population, and light can use the same
ternary update without becoming the same quantity.

```text
WorldCell2D {
  id, x, y, layer, channel,
  value, ternary_move,
  point_state, path_state, field_state,
  phase, activation, integrity, polarity,
  boundary_state, revision, provenance
}
```

## 2D Mirror-Gate neighborhood

The native spatial gate is

`3 > 1(0)1 < 6`.

Three planar mirrored axes define six directed neighbor relationships around
the active center. The program must not silently introduce twelve-neighbor 3D
geometry or call time a fourth spatial dimension.

Time is stored as an ordered state trace of the 2D world.

## Homeworld hierarchy

```text
Homeworld map
-> regions
-> Mega City
-> districts
-> blocks
-> buildings / parks / infrastructure
-> rooms or local map cells
-> ternary 2D cells
```

Each level uses Point–Path–Field:

- Point: site, building, junction, or district center;
- Path: road, rail, utility, pedestrian, water, or communication route;
- Field: neighborhood influence, resources, weather layer, power, population,
  visibility, sound, or simulation boundary.

These can be rendered with height, perspective, lighting, sprites, or parallax,
but those are visual projections of the authoritative 2D state.

## No Administrator

World changes follow programmed rules, user commands, and versioned scenario
files. No Administrator module accepts, rejects, moralizes, or promotes world
thoughts. The ordinary program runtime validates file formats and prevents data
corruption; that is software integrity, not a mind role.

## NAS layout

```text
homeworld/
  maps/            authoritative 2D maps and layer manifests
  snapshots/       immutable versioned world states
  chunks/          streamed 2D spatial chunks
  assets/          sprites, tiles, textures, audio, animation
  rules/           versioned deterministic and stochastic world rules
  simulations/     seeds, parameters, measurements, receipts
  renders/         images and videos
  imports/         unverified generated/imported assets
  backups/         recoverable protected copies
```

The NAS is storage, not a cognitive memory system.

## Compute placement

- CPU: 2D world rules, chunk streaming, state database, versioning, networking, and replay.
- GPU: 2D rendering, particles, lighting, large-grid updates, visualization, and video export.
- NPU: optional sprite tagging, navigation hints, animation selection, or procedural suggestions.
- NAS: persistent maps, assets, snapshots, simulation receipts, and backups.

No NPU or cognitive system is required for the programmed world to run.

## Minimum build

1. CPU reference grid with six directed neighbors and ternary updates.
2. Deterministic replay from initial snapshot, scenario, and random seed.
3. Point–Path–Field map schema.
4. Chunked Mega-City map stored locally, then on NAS.
5. GPU-rendered 2D tiles/sprites with zoom from cell to district to full city.
6. Rule editor for traffic, utilities, population, weather, construction, and events.
7. Snapshot, branch, compare, and rollback controls.
8. Optional connection allowing the separate cognitive Dream Engine to observe
   or request a scenario without becoming part of the world's update loop.

## Failure conditions

- the engine introduces an Administrator or claims the world is cognitive;
- ternary `3` is misread as three spatial dimensions;
- the six-neighbor 2D gate is replaced by an undeclared geometry;
- rendered perspective is confused with authoritative spatial dimension;
- NAS loss destroys the only snapshot;
- random evolution cannot be replayed from stored seeds and rules;
- generated assets overwrite authoritative maps without versioning.

