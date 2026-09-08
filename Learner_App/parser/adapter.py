"""Adapter contract and registry for the problem-builder core.

Domain-specific syntax and semantics live in adapters, not here. This module
defines the interface every adapter must satisfy and a small explicit
registry adapters are added to by name. There is no plugin discovery magic:
an adapter is only usable after something calls register_adapter().
"""

from __future__ import annotations

import random
from typing import Any, Protocol, runtime_checkable

from .models import RulePacket


class AdapterError(Exception):
    """Base class for adapter-related failures."""


class UnknownAdapterError(AdapterError):
    """Raised when a packet names a domain with no registered adapter."""


class AdapterAlreadyRegisteredError(AdapterError):
    """Raised when a domain name is registered twice without explicit replace."""


@runtime_checkable
class ProblemAdapter(Protocol):
    """The contract every domain adapter must implement.

    Generation and verification are deliberately separate operations:
    generate_candidate() builds a candidate artifact's external text, and
    parse_artifact() must reconstruct structure from that text alone, with
    no access to whatever internal object generate_candidate() used to
    build it. The core relies on that separation so a bad generator or a
    bad serialization step gets caught by the reparse instead of trusted.
    """

    domain: str

    def validate_packet(self, packet: RulePacket) -> list[str]:
        """Return rejection reasons, or an empty list if the packet is
        acceptable to this adapter. Must not generate anything."""
        ...

    def generate_candidate(self, packet: RulePacket, rng: random.Random) -> str:
        """Return the external artifact text for this packet, using only
        the given seeded RNG for randomness."""
        ...

    def parse_artifact(self, text: str) -> Any:
        """Independently reparse artifact text into a structure object."""
        ...

    def inspect_rules(self, structure: Any) -> list[str]:
        """Return the rule IDs the reparsed structure demonstrates."""
        ...

    def validate_structure(
        self, structure: Any, packet: RulePacket
    ) -> tuple[bool, list[str], dict[str, Any]]:
        """Return (adapter_valid, errors, metadata).

        `metadata` is opaque to the core -- it is merged straight into the
        returned GeneratedProblem.metadata. Domain-specific validation
        facts (e.g. the math adapter's single-unknown check) belong here,
        not as a new core-level field.
        """
        ...


_REGISTRY: dict[str, ProblemAdapter] = {}


def register_adapter(domain: str, adapter: ProblemAdapter, *, replace: bool = False) -> None:
    """Register `adapter` under `domain`. Explicit call, no discovery magic."""
    if not replace and domain in _REGISTRY:
        raise AdapterAlreadyRegisteredError(
            f"domain {domain!r} is already registered; pass replace=True to override"
        )
    _REGISTRY[domain] = adapter


def get_adapter(domain: str) -> ProblemAdapter:
    try:
        return _REGISTRY[domain]
    except KeyError as exc:
        raise UnknownAdapterError(f"no adapter registered for domain {domain!r}") from exc


def registered_domains() -> list[str]:
    return sorted(_REGISTRY)


def unregister_adapter(domain: str) -> None:
    """Remove a registration. Mainly useful for test isolation."""
    _REGISTRY.pop(domain, None)
