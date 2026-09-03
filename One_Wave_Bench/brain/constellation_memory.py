"""Executable rabbit-hop constellation memory reconstruction.

The jobs stay separate:

* constellation edges select a relational neighborhood;
* G-721 coordinates provide reversible navigation receipts;
* Hopfield settling completes partial cues inside that neighborhood;
* bounded Boltzmann sampling exposes unresolved ambiguity;
* context validation accepts, holds, or rejects the proposal.

This is a CPU reference implementation.  It does not authorize an actuator and
it never rewrites the exact stored memories during recall.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from math import exp
from random import Random
from typing import Iterable

from One_Wave_Bench.brain.rabbit_hop_alphabet import (
    AlphabetOrientation,
    MirrorPolarity,
    RabbitHopCoordinate,
    RouteFamily,
    wrapper_pair,
)


class ValidationDecision(str, Enum):
    ACCEPT = "accept"
    HOLD = "hold"
    REJECT = "reject"


@dataclass(frozen=True, slots=True)
class MemoryNode:
    memory_id: str
    address: str
    features: frozenset[str]
    contexts: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.memory_id or not self.features:
            raise ValueError("memory_id and at least one feature are required")


@dataclass(frozen=True, slots=True)
class RabbitHopStep:
    source_memory: str
    target_memory: str
    source: RabbitHopCoordinate
    target: RabbitHopCoordinate

    @property
    def connector(self) -> int:
        if self.source.wrapper_address != self.target.wrapper_address:
            raise ValueError("rabbit-hop step does not share a wrapper address")
        return self.source.wrapper_address

    def reversed(self) -> "RabbitHopStep":
        return RabbitHopStep(
            self.target_memory,
            self.source_memory,
            self.target.opposed(),
            self.source.opposed(),
        )


@dataclass(frozen=True, slots=True)
class RebuildReceipt:
    cue: tuple[str, ...]
    route_handle: str | None
    constellation_neighborhood: tuple[str, ...]
    route: tuple[RabbitHopStep, ...]
    hopfield_scores: tuple[tuple[str, float], ...]
    boltzmann_probabilities: tuple[tuple[str, float], ...]
    associative_completion: tuple[str, ...]
    probabilistic_fill: tuple[str, ...]
    uncertain_features: tuple[str, ...]
    selected_memory: str | None
    baseline_memory: str | None
    validation: ValidationDecision
    reason: str

    def inverted_route(self) -> tuple[RabbitHopStep, ...]:
        return tuple(step.reversed() for step in reversed(self.route))


@dataclass(frozen=True, slots=True)
class RebuildResult:
    memory: MemoryNode | None
    receipt: RebuildReceipt


class ConstellationMemory:
    """Exact memory nodes plus reconstructive recall over reversible routes."""

    def __init__(self, nodes: Iterable[MemoryNode] = ()) -> None:
        self._nodes: dict[str, MemoryNode] = {}
        self._addresses: dict[str, str] = {}
        for node in nodes:
            self.store(node)

    @property
    def nodes(self) -> tuple[MemoryNode, ...]:
        return tuple(self._nodes.values())

    def store(self, node: MemoryNode) -> None:
        address = node.address.upper()
        if node.memory_id in self._nodes:
            raise ValueError(f"duplicate memory_id: {node.memory_id}")
        if address in self._addresses:
            raise ValueError(f"duplicate rabbit-hop address: {address}")
        # wrapper_pair performs the canonical A-Z validation.
        wrapper_pair(address)
        normalized = MemoryNode(
            node.memory_id,
            address,
            frozenset(node.features),
            frozenset(node.contexts),
        )
        self._nodes[normalized.memory_id] = normalized
        self._addresses[address] = normalized.memory_id

    @staticmethod
    def _shared_step(
        source: MemoryNode,
        target: MemoryNode,
        alphabet_orientation: AlphabetOrientation,
        polarity: MirrorPolarity,
    ) -> RabbitHopStep | None:
        source_pair = wrapper_pair(
            source.address,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
            route_family=RouteFamily.ORIGINAL,
            k=0,
        )
        target_pair = wrapper_pair(
            target.address,
            alphabet_orientation=alphabet_orientation,
            polarity=polarity,
            route_family=RouteFamily.ORIGINAL,
            k=0,
        )
        for source_coordinate in source_pair:
            for target_coordinate in target_pair:
                if (
                    source_coordinate.wrapper_address
                    == target_coordinate.wrapper_address
                    and source_coordinate.source_rank != target_coordinate.source_rank
                ):
                    return RabbitHopStep(
                        source.memory_id,
                        target.memory_id,
                        source_coordinate,
                        target_coordinate,
                    )
        return None

    def rabbit_neighbors(
        self,
        memory_id: str,
        *,
        alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
        polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    ) -> tuple[RabbitHopStep, ...]:
        source = self._nodes[memory_id]
        steps = (
            step
            for target in self._nodes.values()
            if target.memory_id != memory_id
            for step in (
                self._shared_step(source, target, alphabet_orientation, polarity),
            )
            if step is not None
        )
        return tuple(sorted(steps, key=lambda step: step.target_memory))

    def _route(
        self,
        start: str,
        target: str,
        alphabet_orientation: AlphabetOrientation,
        polarity: MirrorPolarity,
    ) -> tuple[RabbitHopStep, ...] | None:
        if start == target:
            return ()
        queue = deque([(start, ())])
        visited = {start}
        while queue:
            current, route = queue.popleft()
            for step in self.rabbit_neighbors(
                current,
                alphabet_orientation=alphabet_orientation,
                polarity=polarity,
            ):
                if step.target_memory in visited:
                    continue
                next_route = route + (step,)
                if step.target_memory == target:
                    return next_route
                visited.add(step.target_memory)
                queue.append((step.target_memory, next_route))
        return None

    def constellation_neighbors(self, cue: frozenset[str]) -> tuple[MemoryNode, ...]:
        """Enter the relational neighborhood without inventing an edge."""

        direct = {
            node.memory_id
            for node in self._nodes.values()
            if node.features.intersection(cue)
        }
        expanded = set(direct)
        for memory_id in direct:
            features = self._nodes[memory_id].features
            expanded.update(
                node.memory_id
                for node in self._nodes.values()
                if node.features.intersection(features)
            )
        return tuple(self._nodes[memory_id] for memory_id in sorted(expanded))

    @staticmethod
    def _hopfield_scores(
        cue: frozenset[str], candidates: tuple[MemoryNode, ...]
    ) -> dict[str, float]:
        """Settle a partial cue against intact bipolar stored attractors.

        Unknown cue dimensions are zero, so missing evidence is not treated as
        negative evidence.  The returned normalized dot product is deterministic.
        """

        vocabulary = sorted(set().union(*(node.features for node in candidates)))
        if not vocabulary:
            return {}
        cue_vector = tuple(1 if feature in cue else 0 for feature in vocabulary)
        known = max(1, sum(abs(value) for value in cue_vector))
        return {
            node.memory_id: sum(
                cue_value * (1 if feature in node.features else -1)
                for cue_value, feature in zip(cue_vector, vocabulary)
            ) / known
            for node in candidates
        }

    @staticmethod
    def _unique_peak(scores: dict[str, float]) -> str | None:
        if not scores:
            return None
        peak = max(scores.values())
        winners = [memory_id for memory_id, score in scores.items() if score == peak]
        return winners[0] if len(winners) == 1 else None

    def baseline_recall(self, cue: Iterable[str]) -> MemoryNode | None:
        """Matched no-constellation/no-rabbit baseline for validation."""

        cue_set = frozenset(cue)
        winner = self._unique_peak(
            self._hopfield_scores(cue_set, tuple(self._nodes.values()))
        )
        return None if winner is None else self._nodes[winner]

    def rebuild(
        self,
        cue: Iterable[str],
        *,
        route_handle: str | None = None,
        context: str | None = None,
        alphabet_orientation: AlphabetOrientation = AlphabetOrientation.NORMAL,
        polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
        temperature: float = 0.35,
        seed: int = 0,
    ) -> RebuildResult:
        if temperature <= 0:
            raise ValueError("temperature must be positive")
        cue_set = frozenset(cue)
        neighborhood = self.constellation_neighbors(cue_set)
        baseline = self.baseline_recall(cue_set)

        start_id: str | None = None
        routed: tuple[tuple[MemoryNode, tuple[RabbitHopStep, ...]], ...] = ()
        if route_handle is not None:
            address = route_handle.upper()
            start_id = self._addresses.get(address, route_handle)
            if start_id not in self._nodes:
                raise ValueError(f"unknown route handle: {route_handle}")
            routes = []
            for node in neighborhood:
                route = self._route(
                    start_id, node.memory_id, alphabet_orientation, polarity
                )
                # A hop handle opens another location; it is not the routine itself.
                if route:
                    routes.append((node, route))
            if routes:
                shortest = min(len(route) for _, route in routes)
                routed = tuple(pair for pair in routes if len(pair[1]) == shortest)

        candidates = tuple(node for node, _ in routed) or neighborhood
        scores = self._hopfield_scores(cue_set, candidates)
        selected_id = self._unique_peak(scores)
        probabilities: tuple[tuple[str, float], ...] = ()
        probabilistic = False
        if selected_id is None and scores:
            peak = max(scores.values())
            weights = {
                memory_id: exp((score - peak) / temperature)
                for memory_id, score in scores.items()
            }
            total = sum(weights.values())
            probabilities = tuple(sorted(
                ((memory_id, weight / total) for memory_id, weight in weights.items()),
                key=lambda pair: (-pair[1], pair[0]),
            ))
            selected_id = Random(seed).choices(
                [pair[0] for pair in probabilities],
                weights=[pair[1] for pair in probabilities],
                k=1,
            )[0]
            probabilistic = True

        selected = None if selected_id is None else self._nodes[selected_id]
        route = ()
        if selected is not None and start_id is not None:
            route = self._route(
                start_id, selected.memory_id, alphabet_orientation, polarity
            ) or ()

        missing = () if selected is None else tuple(sorted(selected.features - cue_set))
        if selected is None:
            validation = ValidationDecision.HOLD
            reason = "no reconstructable candidate"
        elif not selected.contexts:
            validation = ValidationDecision.ACCEPT
            reason = "candidate has no context restriction"
        elif context is None:
            validation = ValidationDecision.HOLD
            reason = "candidate requires context"
        elif context in selected.contexts:
            validation = ValidationDecision.ACCEPT
            reason = "candidate matches active context"
        else:
            validation = ValidationDecision.REJECT
            reason = "candidate conflicts with active context"

        receipt = RebuildReceipt(
            cue=tuple(sorted(cue_set)),
            route_handle=route_handle.upper() if route_handle else None,
            constellation_neighborhood=tuple(node.memory_id for node in neighborhood),
            route=route,
            hopfield_scores=tuple(sorted(scores.items())),
            boltzmann_probabilities=probabilities,
            associative_completion=() if probabilistic else missing,
            probabilistic_fill=missing if probabilistic else (),
            uncertain_features=missing if probabilistic else (),
            selected_memory=selected_id,
            baseline_memory=None if baseline is None else baseline.memory_id,
            validation=validation,
            reason=reason,
        )
        return RebuildResult(selected, receipt)


def demo_constellation() -> ConstellationMemory:
    """Small overlapping memory set used by the executable acceptance test."""

    return ConstellationMemory((
        MemoryNode(
            "approach_flower", "A",
            frozenset({"flower", "garden", "approach", "steady"}),
            frozenset({"garden"}),
        ),
        MemoryNode(
            "sniff_flower", "B",
            frozenset({"flower", "garden", "sniff", "scent"}),
            frozenset({"garden"}),
        ),
        MemoryNode(
            "inspect_can", "C",
            frozenset({"can", "street", "inspect", "metal"}),
            frozenset({"street"}),
        ),
    ))
