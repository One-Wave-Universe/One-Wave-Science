"""Generic mountable two-state Field/Void loop chassis.

This module separates invariant loop mechanics from domain instances.

Invariant chassis:
    external instance input
      -> adapter.to_local()
      -> Field state machine proposes
      -> router/fast loop transforms or routes
      -> Void/Admin/Checker resolves
      -> optional executor commits/holds/stops
      -> consequence is translated back
      -> shared/local reference updates
      -> receipt emitted

Domain adapters own vocabulary and payload shape. The chassis does not know
whether the mounted instance is a parser Cell, motor controller, memory system,
brain module, animator, or another project version.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, Generic, Mapping, MutableMapping, Optional, Protocol, TypeVar


ExternalIn = TypeVar("ExternalIn")
ExternalOut = TypeVar("ExternalOut")
LocalPayload = TypeVar("LocalPayload")


class Resolution(str, Enum):
    CONFIRM = "CONFIRM"
    DEFER = "DEFER"
    DENY = "DENY"


@dataclass
class LoopState:
    reference: Dict[str, Any] = field(default_factory=dict)
    field_state: Dict[str, Any] = field(default_factory=dict)
    void_state: Dict[str, Any] = field(default_factory=dict)
    fast_state: Dict[str, Any] = field(default_factory=dict)
    cycle: int = 0


@dataclass
class LoopReceipt:
    instance: str
    cycle: int
    input_local: Any
    reference_before: Dict[str, Any]
    field_proposal: Any
    routed: Any
    void_resolution: str
    committed_local: Any
    consequence_local: Any
    reference_after: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


class InstanceAdapter(Protocol[ExternalIn, ExternalOut, LocalPayload]):
    """Translation protocol for mounting a domain instance on the chassis."""

    name: str

    def to_local(self, value: ExternalIn, state: LoopState) -> LocalPayload:
        """Translate domain input into the local loop language."""

    def field_propose(self, local: LocalPayload, state: LoopState) -> Any:
        """Domain-specific Field proposal."""

    def fast_route(self, local: LocalPayload, proposal: Any, state: LoopState) -> Any:
        """Fast/subconscious/local routing step. May be identity at Micro."""

    def void_check(
        self, local: LocalPayload, proposal: Any, routed: Any, state: LoopState
    ) -> Resolution:
        """Void = Administrator = Checker resolution."""

    def commit(
        self, local: LocalPayload, proposal: Any, routed: Any, resolution: Resolution,
        state: LoopState,
    ) -> Any:
        """Resolve the local action/state transition."""

    def consequence(self, committed: Any, state: LoopState) -> Any:
        """Return measured/simulated local consequence."""

    def update_reference(
        self, consequence: Any, resolution: Resolution, state: LoopState
    ) -> Dict[str, Any]:
        """Produce the next local/shared reference."""

    def from_local(self, receipt: LoopReceipt, state: LoopState) -> ExternalOut:
        """Translate the completed receipt back into domain output."""


class TwoStateLoop(Generic[ExternalIn, ExternalOut, LocalPayload]):
    """Reusable Field/Void loop that domain instances mount onto."""

    def __init__(self, adapter: InstanceAdapter[ExternalIn, ExternalOut, LocalPayload]):
        self.adapter = adapter
        self.state = LoopState()

    def cycle(self, value: ExternalIn) -> tuple[ExternalOut, LoopReceipt]:
        self.state.cycle += 1
        before = dict(self.state.reference)

        local = self.adapter.to_local(value, self.state)
        proposal = self.adapter.field_propose(local, self.state)
        routed = self.adapter.fast_route(local, proposal, self.state)
        resolution = self.adapter.void_check(local, proposal, routed, self.state)
        committed = self.adapter.commit(local, proposal, routed, resolution, self.state)
        consequence = self.adapter.consequence(committed, self.state)
        after = self.adapter.update_reference(consequence, resolution, self.state)
        self.state.reference = dict(after)

        receipt = LoopReceipt(
            instance=self.adapter.name,
            cycle=self.state.cycle,
            input_local=local,
            reference_before=before,
            field_proposal=proposal,
            routed=routed,
            void_resolution=resolution.value,
            committed_local=committed,
            consequence_local=consequence,
            reference_after=dict(after),
        )
        return self.adapter.from_local(receipt, self.state), receipt


class MountedInstance(Generic[ExternalIn, ExternalOut, LocalPayload]):
    """Named instance plus its private local loop state."""

    def __init__(self, adapter: InstanceAdapter[ExternalIn, ExternalOut, LocalPayload]):
        self.loop = TwoStateLoop(adapter)

    @property
    def name(self) -> str:
        return self.loop.adapter.name

    def step(self, value: ExternalIn) -> tuple[ExternalOut, LoopReceipt]:
        return self.loop.cycle(value)
