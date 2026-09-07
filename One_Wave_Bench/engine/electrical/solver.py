"""
Real DC nodal solver for resistive networks with ideal voltage sources
(Modified Nodal Analysis). No dependency on numpy/scipy -- a small,
self-contained Gauss-Jordan elimination with partial pivoting, the same
technique (and the same reasoning for using partial pivoting: small
matrices with wildly different-magnitude entries, e.g. a milliohm wire
next to a megohm leakage path, are exactly where naive elimination without
pivoting silently loses precision) already proven in this repo's sibling
Virtual_Breadboard/js/circuit.js `solveLinear()`.

This module NEVER hard-codes a circuit's answer. It assembles Kirchhoff's
current law at every real node and Ohm's law for every real resistor, then
solves the resulting linear system. A caller who wants a particular voltage
must build a circuit that actually produces it.
"""
from __future__ import annotations
from dataclasses import dataclass, field


class UnionFind:
    """Merges node names that a Wire declares equal. Every other lookup
    goes through find() so it never matters which of two wired names a
    component happened to use."""

    def __init__(self):
        self._parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        self._parent.setdefault(x, x)
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self._parent[ra] = rb


def _solve_linear(A: list[list[float]], b: list[float]) -> list[float]:
    """Gauss-Jordan elimination with partial pivoting. Returns x such that
    A @ x == b for a real, well-posed (non-singular) system."""
    n = len(b)
    # augmented matrix
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        pivot_row = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot_row][col]) < 1e-15:
            raise ValueError(
                "Circuit is under-constrained or singular (e.g. a node with "
                "no real path to the reference) -- this is a real modeling "
                "error in the circuit, not a solver bug to paper over."
            )
        if pivot_row != col:
            M[col], M[pivot_row] = M[pivot_row], M[col]
        pivot_val = M[col][col]
        for r in range(n):
            if r == col:
                continue
            factor = M[r][col] / pivot_val
            if factor == 0:
                continue
            for c in range(col, n + 1):
                M[r][c] -= factor * M[col][c]
    return [M[i][n] / M[i][i] for i in range(n)]


@dataclass
class SolveResult:
    voltages: dict[str, float]
    source_currents: dict[str, float]  # amps; + = source discharging into the external circuit
    reference_node: str
    uf: UnionFind = field(repr=False)


def solve_dc(circuit) -> SolveResult:
    """Solve a DC resistive network built from Resistor/DCVoltageSource/
    Wire/Ground components (see components.py).

    Reference-node selection (deliberate, not an accident): an explicit
    Ground component wins if present; otherwise the first voltage source's
    negative terminal (matching how a real bench references "ground" to
    the supply's own return); otherwise the first node encountered. This
    mirrors Virtual_Breadboard's own solver and its own documented
    floating-reference lesson: whichever node is picked, only VOLTAGE
    DIFFERENCES and CURRENTS are physically meaningful on their own --
    reading one node's absolute value is only meaningful once you know
    which node was chosen as the 0V reference, which this function always
    reports back as `reference_node`.
    """
    uf = UnionFind()
    for w in circuit.wires:
        uf.union(w.a, w.b)

    all_nodes: set[str] = set()
    for r in circuit.resistors:
        all_nodes.add(r.a)
        all_nodes.add(r.b)
    for s in circuit.sources:
        all_nodes.add(s.pos)
        all_nodes.add(s.neg)
    for g in circuit.grounds:
        all_nodes.add(g.node)

    if not all_nodes:
        raise ValueError("Circuit has no components -- nothing to solve.")

    roots = sorted({uf.find(n) for n in all_nodes})

    if circuit.grounds:
        reference = uf.find(circuit.grounds[0].node)
    elif circuit.sources:
        reference = uf.find(circuit.sources[0].neg)
    else:
        reference = roots[0]

    node_index: dict[str, int] = {}
    idx = 0
    for root in roots:
        if root == reference:
            continue
        node_index[root] = idx
        idx += 1
    n_nodes = idx
    n_src = len(circuit.sources)
    size = n_nodes + n_src

    A = [[0.0] * size for _ in range(size)]
    b = [0.0] * size

    def gi(node: str) -> int:
        root = uf.find(node)
        return node_index.get(root, -1)  # -1 means "the reference node itself"

    def stamp_g(i: int, j: int, val: float) -> None:
        if i >= 0 and j >= 0:
            A[i][j] += val

    for r in circuit.resistors:
        g = 1.0 / r.ohms
        i, j = gi(r.a), gi(r.b)
        stamp_g(i, i, g)
        stamp_g(j, j, g)
        stamp_g(i, j, -g)
        stamp_g(j, i, -g)

    for k, s in enumerate(circuit.sources):
        row = n_nodes + k
        p, n = gi(s.pos), gi(s.neg)
        if p >= 0:
            A[p][row] += 1
            A[row][p] += 1
        if n >= 0:
            A[n][row] -= 1
            A[row][n] -= 1
        b[row] += s.volts

    x = _solve_linear(A, b) if size > 0 else []

    voltages = {reference: 0.0}
    for root, i in node_index.items():
        voltages[root] = x[i]
    full_voltages = {n: voltages[uf.find(n)] for n in all_nodes}

    # The raw MNA unknown x[row] comes out as the current flowing from
    # pos to neg THROUGH the source's own internal branch (i.e. INTO the
    # source at its + terminal) -- the negative of the conventional
    # "discharging into the load" direction. Flip it so a source actually
    # delivering power into the circuit reads positive, matching real
    # bench-meter convention (and Virtual_Breadboard/js/circuit.js's
    # battery model, which uses the same convention for the same reason).
    source_currents = {s.id: -x[n_nodes + k] for k, s in enumerate(circuit.sources)}

    return SolveResult(
        voltages=full_voltages,
        source_currents=source_currents,
        reference_node=reference,
        uf=uf,
    )
