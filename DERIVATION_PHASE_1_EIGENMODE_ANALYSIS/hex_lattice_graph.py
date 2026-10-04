"""D1 — 2D triangular / sixfold graph for 3 > 1(0)1 < 6.

Sites live on the D-408 lattice:
    a1 = a(1, 0)
    a2 = a(1/2, sqrt(3)/2)

Interior coordination is 6. Three opposite neighbor pairs give the
axis-pair view 3:1. The seven-cell cluster is one center plus six ring sites.

This is a graph, Laplacian, and incidence construction. It is not a 3D
or 4D object and it is not a Mass Effect derivation.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple

Site = Tuple[int, int]


A1 = (1.0, 0.0)
A2 = (0.5, math.sqrt(3.0) / 2.0)
NEIGHBOR_OFFSETS: Tuple[Site, ...] = (
    (1, 0),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (0, -1),
    (1, -1),
)
AXIS_PAIRS: Tuple[Tuple[Site, Site], ...] = (
    ((1, 0), (-1, 0)),
    ((0, 1), (0, -1)),
    ((-1, 1), (1, -1)),
)


def site_xy(site: Site, a: float = 1.0) -> Tuple[float, float]:
    m, n = site
    return (a * (m * A1[0] + n * A2[0]), a * (m * A1[1] + n * A2[1]))


def neighbor(site: Site, offset: Site) -> Site:
    return (site[0] + offset[0], site[1] + offset[1])


def disk_sites(radius: int) -> List[Site]:
    if radius < 0:
        raise ValueError("radius must be >= 0")
    sites = []
    for m in range(-radius, radius + 1):
        for n in range(-radius, radius + 1):
            if max(abs(m), abs(n), abs(m + n)) <= radius:
                sites.append((m, n))
    return sites


def seven_cell() -> List[Site]:
    return [(0, 0)] + [neighbor((0, 0), off) for off in NEIGHBOR_OFFSETS]


def adjacency(sites: Sequence[Site]) -> Dict[Site, List[Site]]:
    present = set(sites)
    adj: Dict[Site, List[Site]] = {}
    for site in sites:
        nbrs = [neighbor(site, off) for off in NEIGHBOR_OFFSETS if neighbor(site, off) in present]
        adj[site] = nbrs
    return adj


def edge_list(sites: Sequence[Site]) -> List[Tuple[Site, Site]]:
    present = set(sites)
    edges = []
    for site in sites:
        for off in NEIGHBOR_OFFSETS:
            other = neighbor(site, off)
            if other in present and site < other:
                edges.append((site, other))
    return edges


def incidence_matrix(sites: Sequence[Site]) -> List[List[int]]:
    edges = edge_list(sites)
    index = {site: i for i, site in enumerate(sites)}
    rows = [[0] * len(edges) for _ in sites]
    for j, (u, v) in enumerate(edges):
        rows[index[u]][j] = -1
        rows[index[v]][j] = 1
    return rows


def laplacian(sites: Sequence[Site]) -> List[List[int]]:
    adj = adjacency(sites)
    index = {site: i for i, site in enumerate(sites)}
    n = len(sites)
    L = [[0] * n for _ in range(n)]
    for site in sites:
        i = index[site]
        nbrs = adj[site]
        L[i][i] = len(nbrs)
        for nbr in nbrs:
            L[i][index[nbr]] = -1
    return L


def laplacian_spectrum(sites: Sequence[Site]) -> List[float]:
    return _eigenvalues_symmetric(laplacian(sites))


def _eigenvalues_symmetric(matrix: Sequence[Sequence[float]]) -> List[float]:
    n = len(matrix)
    a = [list(map(float, row)) for row in matrix]
    v = [[float(i == j) for j in range(n)] for i in range(n)]
    for _ in range(64 * n * n):
        p = q = 0
        best = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > best:
                    best = abs(a[i][j])
                    p, q = i, j
        if best < 1e-12:
            break
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        tau = (aqq - app) / (2.0 * apq)
        t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        for k in range(n):
            if k != p and k != q:
                akp, akq = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c * akp - s * akq
                a[k][q] = a[q][k] = s * akp + c * akq
        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            vip, viq = v[k][p], v[k][q]
            v[k][p] = c * vip - s * viq
            v[k][q] = s * vip + c * viq
    return sorted(a[i][i] for i in range(n))


def directed_routes(center: Site = (0, 0)) -> List[Site]:
    return [neighbor(center, off) for off in NEIGHBOR_OFFSETS]


def axis_pairs(center: Site = (0, 0)) -> List[Tuple[Site, Site]]:
    return [(neighbor(center, left), neighbor(center, right)) for left, right in AXIS_PAIRS]


def coordination(sites: Sequence[Site], site: Site) -> int:
    return len(adjacency(sites)[site])
