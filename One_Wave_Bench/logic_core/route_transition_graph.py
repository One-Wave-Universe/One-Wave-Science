"""Candidate transition graphs for the two-choice/three-move primitive.

This module does not declare a physical transition law.  It exposes competing
finite hypotheses so reachability and topology can be measured before one is
promoted into the architecture.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Dict, FrozenSet, Iterable, Mapping, Tuple

from six_route_logic import BinaryChoice, LogicRoute, TernaryMove, all_routes


class TransitionLaw(Enum):
    """Finite hypotheses to compare."""

    PRODUCT = "product"
    CENTER_GATED_FLIP = "center_gated_flip"
    MOVEMENT_ONLY = "movement_only"


Edge = Tuple[int, int]


def _movement_neighbors(route: LogicRoute) -> Iterable[LogicRoute]:
    for move in TernaryMove:
        if abs(int(move) - int(route.move)) == 1:
            yield LogicRoute(route.choice, move)


def _flipped(route: LogicRoute) -> LogicRoute:
    other = BinaryChoice.NO if route.choice is BinaryChoice.YES else BinaryChoice.YES
    return LogicRoute(other, route.move)


def build_edges(law: TransitionLaw) -> FrozenSet[Edge]:
    """Build undirected candidate edges using dense route addresses."""

    edges = set()
    for route in all_routes():
        for neighbor in _movement_neighbors(route):
            edges.add(tuple(sorted((route.address, neighbor.address))))

        allow_flip = law is TransitionLaw.PRODUCT or (
            law is TransitionLaw.CENTER_GATED_FLIP and route.move is TernaryMove.HOLD
        )
        if allow_flip:
            edges.add(tuple(sorted((route.address, _flipped(route).address))))
    return frozenset(edges)


def adjacency(law: TransitionLaw) -> Mapping[int, FrozenSet[int]]:
    graph: Dict[int, set[int]] = {route.address: set() for route in all_routes()}
    for left, right in build_edges(law):
        graph[left].add(right)
        graph[right].add(left)
    return {node: frozenset(neighbors) for node, neighbors in graph.items()}


def distances_from(start: int, law: TransitionLaw) -> Mapping[int, int]:
    graph = adjacency(law)
    if start not in graph:
        raise ValueError(f"unknown route address: {start}")
    distance = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in distance:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)
    return distance


@dataclass(frozen=True)
class GraphReceipt:
    law: str
    node_count: int
    edge_count: int
    connected: bool
    reversible: bool
    absorbing_nodes: Tuple[int, ...]
    diameter: int | None
    degree_sequence: Tuple[int, ...]


def analyze(law: TransitionLaw) -> GraphReceipt:
    graph = adjacency(law)
    all_distances = [distances_from(node, law) for node in graph]
    connected = all(len(distance) == len(graph) for distance in all_distances)
    diameter = (
        max(max(distance.values()) for distance in all_distances) if connected else None
    )
    reversible = all(node in graph[neighbor] for node in graph for neighbor in graph[node])
    return GraphReceipt(
        law=law.value,
        node_count=len(graph),
        edge_count=len(build_edges(law)),
        connected=connected,
        reversible=reversible,
        absorbing_nodes=tuple(sorted(node for node, neighbors in graph.items() if not neighbors)),
        diameter=diameter,
        degree_sequence=tuple(sorted(len(neighbors) for neighbors in graph.values())),
    )


def compare_laws() -> Tuple[GraphReceipt, ...]:
    return tuple(analyze(law) for law in TransitionLaw)


if __name__ == "__main__":
    for receipt in compare_laws():
        print(receipt)

