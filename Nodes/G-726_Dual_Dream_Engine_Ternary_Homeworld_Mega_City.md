---
node_id: "G-726"
canonical_name: "Dual Dream Engine — Ternary Homeworld Mega City"
namespace: "NODE"
gate: "GREEN"
lifecycle: "PROPOSED_BUILD"
classification: "Persistent World Simulation / Cognitive Boundary / Distributed Storage"
claim_gate_detail: "GREEN (role separation) / BROWN (Homeworld implementation)"
metadata_standard: "I-06"
---

# Node G-726: Dual Dream Engine — Ternary Homeworld Mega City

## Purpose

Create two Dream Engines with a hard cognitive boundary:

1. **Cognitive Dream Engine** — generates internal candidates for the M4 and
   Administrator loop.
2. **Non-Cognitive 3D Dream Engine** — generates and simulates a persistent
   external Homeworld/Mega-City environment without owning identity,
   commitment, private memory, or self-state.

The second engine is a world model and renderer. It is not declared conscious
and is not permitted to modify the cognitive system's Reference Ground.

## Runtime separation

### Cognitive engine

- private Working Ground;
- imagery, association, counterfactuals, and action candidates;
- M4/Hopfield coherence loop;
- Administrator-approved promotion into committed state;
- no direct write access to the Homeworld authoritative database.

### Non-cognitive 3D engine

- terrain, architecture, infrastructure, weather, lighting, inhabitants, and traffic simulation;
- 3D Point–Path–Field state for objects, routes, and districts;
- procedural city generation and visual rendering;
- physics and behavior sandboxes;
- no private identity store;
- no autonomous authority over real hardware, money, people, or cognitive memory.

## Ternary world cell

Every simulated cell/node has a local move:

`m in {-1,0,+1}`

- `-1 COMPRESS`: remove, close, cool, descend, return, consolidate;
- `0 HOLD`: preserve, stabilize, occupy, synchronize, wait;
- `+1 EXPRESS`: add, open, heat, rise, extend, propagate.

The sign is interpreted by a typed subsystem. A building-density cell and a
traffic-flow cell may both use `+1`, but they do not share units or mechanisms.

Minimum cell record:

```text
WorldCell {
  id, parent_id, native_dimension, position, scale,
  point_state, path_state, field_state,
  ternary_move, phase, activation, integrity, polarity,
  material_type, boundary_state, revision, provenance
}
```

## Homeworld hierarchy

```text
Homeworld
-> regions
-> Mega City
-> districts
-> blocks
-> buildings and infrastructure
-> rooms / machines / agents
-> ternary cells
```

Every level is recursively Point–Path–Field:

- Point: local object, junction, building, or district center;
- Path: road, rail, utility, pedestrian, communication, or movement route;
- Field: neighborhood influence, resource distribution, weather, power,
  population, visibility, or simulation boundary.

## Dimensional Mirror Gates

The world engine preserves the locked dimensional architecture:

- `1:1`: ultimate compressed whole / one committed Homeworld snapshot;
- 2D: `3 > 1(0)1 < 6` for planar neighborhood coordination;
- 3D: `6 > 1(0)1 < 12` for volumetric shell coordination;
- 4D recurrence: `12 > 1(0)1 < 24` for state-over-time recurrence routes.

The 4D layer stores change/recurrence and is not silently rendered as twenty-four spatial neighbors.

## NAS storage architecture

The NAS is authoritative for world assets and snapshots, not for live cognitive
identity. Recommended logical layout:

```text
homeworld/
  canonical/       accepted world manifests and checksums
  snapshots/       immutable versioned world states
  chunks/          spatial world-cell and geometry chunks
  assets/          meshes, textures, audio, animation, materials
  simulations/     seeds, parameters, receipts, and ablation results
  renders/         generated frames and videos
  imports/         quarantined external/generated material
  backups/         recoverable protected copies
```

Generated assets enter `imports/` first. CPU validation promotes accepted files
into canonical manifests. The engine never edits a committed snapshot in place.

## CPU/GPU/NPU split

- CPU: world database, chunk scheduling, authoritative commits, permissions,
  manifests, hashes, rollback, and network service.
- GPU: 3D rendering, geometry generation, physics batches, Field tensors,
  agents, lighting, and visual export.
- NPU: optional bounded inference for navigation, semantic tagging, animation,
  and pattern completion. It is not required for core world integrity.
- NAS: persistent assets, chunks, snapshots, receipts, and backups.

The cognitive M4 NPU and non-cognitive world inference must use separate model
sessions, memory namespaces, permissions, and event streams.

## Connection between engines

Only typed requests cross the boundary:

```text
CognitiveRequest {
  requester, intent, permitted_context, world_query_or_proposal,
  privacy_scope, expiration, receipt_id
}

WorldResponse {
  source_snapshot, generated_delta, confidence, affected_chunks,
  cost, provenance, preview_only
}
```

The cognitive system may visit, query, design, or propose changes. The world
engine returns previews. The Administrator must approve canonical world commits.

## Minimum build

1. Local CPU-only chunk database using SQLite and content-addressed files.
2. Ternary 3D voxel/cell reference simulation.
3. Point–Path–Field city schema.
4. GPU renderer with district streaming.
5. NAS adapter configured by environment variables, never hard-coded credentials.
6. Immutable snapshots and rollback.
7. Cognitive/world request boundary with privacy scopes.
8. Mega-City procedural generator and visual editor.
9. Multi-user/agent connection only after permissions and conflict resolution work.

## Failure conditions

- world generation can overwrite cognitive Reference Ground;
- cognitive private memory is copied into world assets without explicit scope;
- a generated render is treated as an authoritative state without a receipt;
- `-1/0/+1` loses typed subsystem meaning;
- NAS failure destroys the only copy;
- mutable files replace immutable snapshots;
- the non-cognitive engine gains undeclared real-world actuator authority.

