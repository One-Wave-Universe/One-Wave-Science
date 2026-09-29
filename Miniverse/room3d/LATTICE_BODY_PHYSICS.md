# Miniverse Lattice Body Physics Sandbox

This is a reduced software sandbox for body/lattice interaction inside the Miniverse room.

## Body interaction
A connected body occupying a lattice cell contributes a bounded software mass/load derived from its voxel body volume and scale. The occupied lattice site displaces under that load. Neighbor coupling spreads the disturbance and creates derived strain and pressure.

Each body receives local sensory values:
- displacement
- pressure
- strain
- support
- software mass
- weight signal

These signals can feed M4 and the body sensor lattice.

## State
Each room lattice cell evolves:
```text
u        displacement
v        displacement rate
chi      compression proxy
pressure derived local load/compression
strain   neighbor displacement differential
load     body load currently applied
```

## Update law
The current first implementation is intentionally reduced:
```text
neighbor restoring = stiffness * (neighbor_mean_u - u)
acceleration = -body_load + neighbor_restoring - damping * v
v_next = retention * (v + acceleration * dt)
u_next = u + v_next * dt
```

This gives the room something testable: a body can depress its occupied site, neighboring cells feel differential strain, and removing/moving the body allows restoring response.

## Boundary
This is a software sandbox governed by D-412. It is not evidence for a physical gravity law, particle model, or physical CELL_V1 mechanism. Parameters are simulation controls and must remain independently testable.
