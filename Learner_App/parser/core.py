"""Reusable rule-driven problem-builder core.

This module contains no domain knowledge -- no algebra, no music, nothing.
It accepts a RulePacket from the router, resolves the requested adapter,
drives generation, and independently reparses and verifies the result
before ever returning it. See adapters/ for domain-specific behavior.

Pipeline:

    RulePacket
      -> generic contradiction check (target/forbidden overlap)
      -> resolve adapter
      -> adapter.validate_packet()
      -> adapter.generate_candidate(packet, seeded_rng)   [construction]
      -> adapter.parse_artifact(artifact_text)             [independent reparse]
      -> adapter.inspect_rules(structure)
      -> adapter.validate_structure(structure, packet)
      -> verifier.build_verification(...)
      -> return GeneratedProblem only if verification.passed
"""

from __future__ import annotations

import random

from .adapter import ProblemAdapter, get_adapter
from .models import GeneratedProblem, RulePacket, VerificationResult
from .verifier import build_verification


class PacketRejectedError(ValueError):
    """Raised when a packet is contradictory or unsupported, before generation."""

    def __init__(self, reasons: list[str]):
        self.reasons = list(reasons)
        super().__init__("; ".join(self.reasons))


class ProblemVerificationError(RuntimeError):
    """Raised when a generated candidate fails independent verification.

    The core never returns an unverified problem -- callers see this
    instead of a GeneratedProblem whose verification.passed is False.
    """

    def __init__(self, packet: RulePacket, verification: VerificationResult, artifact_text: str):
        self.packet = packet
        self.verification = verification
        self.artifact_text = artifact_text
        super().__init__(
            f"packet {packet.packet_id!r} failed verification: {list(verification.errors)}"
        )


def _check_generic_contradictions(packet: RulePacket) -> None:
    """The only rejection rule the core can enforce without domain knowledge:
    a rule cannot be both required and forbidden."""
    overlap = sorted(set(packet.target_rules) & set(packet.forbidden_rules))
    if overlap:
        raise PacketRejectedError(
            [f"rule(s) {overlap} present in both target_rules and forbidden_rules"]
        )


def build_problem(packet: RulePacket, *, adapter: ProblemAdapter | None = None) -> GeneratedProblem:
    """Run the full generate -> reparse -> verify pipeline for one packet.

    Raises PacketRejectedError if the packet is contradictory or the
    adapter rejects it before generation. Raises ProblemVerificationError
    if the generated candidate fails independent verification. Only ever
    returns a GeneratedProblem that passed verification.

    `adapter` is normally resolved from the registry via packet.domain;
    it can be passed explicitly (tests use this to exercise a deliberately
    broken adapter without touching the registry).
    """
    _check_generic_contradictions(packet)

    resolved_adapter = adapter if adapter is not None else get_adapter(packet.domain)

    adapter_errors = resolved_adapter.validate_packet(packet)
    if adapter_errors:
        raise PacketRejectedError(adapter_errors)

    rng = random.Random(packet.seed)
    artifact_text = resolved_adapter.generate_candidate(packet, rng)

    well_formed = True
    structure = None
    parse_errors: list[str] = []
    try:
        structure = resolved_adapter.parse_artifact(artifact_text)
    except Exception as exc:  # the reparse must catch bad generation/serialization
        well_formed = False
        parse_errors.append(f"reparse failed: {exc}")

    rules_used: list[str] = []
    adapter_valid = False
    structure_errors: list[str] = []
    structure_metadata: dict = {}
    if well_formed:
        rules_used = resolved_adapter.inspect_rules(structure)
        adapter_valid, structure_errors, structure_metadata = resolved_adapter.validate_structure(
            structure, packet
        )

    verification = build_verification(
        rules_used=rules_used,
        packet=packet,
        well_formed=well_formed,
        adapter_valid=adapter_valid,
        errors=[*parse_errors, *structure_errors],
    )

    if not verification.passed:
        raise ProblemVerificationError(packet, verification, artifact_text)

    return GeneratedProblem(
        problem_id=f"{packet.packet_id}:{packet.seed}",
        seed=packet.seed,
        domain=packet.domain,
        artifact_text=artifact_text,
        structure=structure,
        rules_requested=tuple(packet.target_rules),
        # v1 has no separate operation-token vocabulary from the rule-ID
        # vocabulary, so operations_present mirrors rules_used. A future
        # adapter is free to report a richer operations list through
        # validate_structure()'s metadata without changing this core.
        rules_used=tuple(rules_used),
        operations_present=tuple(rules_used),
        verification=verification,
        metadata=structure_metadata,
    )
