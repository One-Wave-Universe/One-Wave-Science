#!/usr/bin/env python3
from sandbox_experiments import run_all
from sandbox_lattice import HexLattice, LatticeWorld


def test_all_50_sandbox_experiments_pass():
    results=run_all()
    assert len(results)==50
    failed=[r for r in results if not r.passed]
    assert failed==[], [(r.id,r.name,r.metrics) for r in failed]


def test_rest_topology_survives_heavy_dynamic_activity():
    world=LatticeWorld(radius=4,seed=42)
    before=world.lattice.topology_digest()
    for i in range(120):
        if i%9==0:
            world.inject((0,0),0.2 if (i//9)%2==0 else -0.2)
        world.step()
        if i%20==0:
            world.checkpoint()
    assert world.lattice.topology_digest()==before
    assert world.lattice.rest_unchanged()


def test_hex_reference_has_unique_ids_and_reciprocal_edges():
    lattice=HexLattice(4)
    ids=[c.id for c in lattice.cells.values()]
    assert len(ids)==len(set(ids))
    for pos in lattice.cells:
        for nbr in lattice.neighbors(pos):
            assert pos in lattice.neighbors(nbr)
