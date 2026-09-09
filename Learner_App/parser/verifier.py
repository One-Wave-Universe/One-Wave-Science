"""Pure verification helpers.

These functions only compare already-reparsed structural facts (rule IDs
present, well-formedness, adapter-reported validity) against the packet's
requested/forbidden rules. They never look at how the candidate was
generated -- that is the whole point of the reparse-then-verify pipeline
in core.py.
"""

from __future__ import annotations

from .models import RulePacket, VerificationResult


def check_requested_rules_present(rules_used: list[str], packet: RulePacket) -> bool:
    return all(rule in rules_used for rule in packet.target_rules)


def check_forbidden_rules_absent(rules_used: list[str], packet: RulePacket) -> bool:
    return not any(rule in rules_used for rule in packet.forbidden_rules)


def check_no_unapproved_rules(rules_used: list[str], packet: RulePacket) -> bool:
    """The worker must never silently add a rule the router did not permit.

    A rule showing up in `rules_used` is only acceptable if the router
    named it a target or explicitly allowed it as support -- being merely
    "not forbidden" is not enough, since the router may simply not have
    thought to forbid it.
    """
    approved = set(packet.target_rules) | set(packet.allowed_support_rules)
    return all(rule in approved for rule in rules_used)


def build_verification(
    *,
    rules_used: list[str],
    packet: RulePacket,
    well_formed: bool,
    adapter_valid: bool,
    errors: list[str],
) -> VerificationResult:
    requested_present = check_requested_rules_present(rules_used, packet)
    forbidden_absent = check_forbidden_rules_absent(rules_used, packet)
    no_unapproved_rules = check_no_unapproved_rules(rules_used, packet)

    all_errors = list(errors)
    if not requested_present:
        missing = [r for r in packet.target_rules if r not in rules_used]
        all_errors.append(f"requested rules not demonstrated in structure: {missing}")
    if not forbidden_absent:
        present = [r for r in packet.forbidden_rules if r in rules_used]
        all_errors.append(f"forbidden rules present in structure: {present}")
    if not no_unapproved_rules:
        approved = set(packet.target_rules) | set(packet.allowed_support_rules)
        unapproved = [r for r in rules_used if r not in approved]
        all_errors.append(f"rule(s) present that the router did not target or allow: {unapproved}")

    return VerificationResult(
        requested_rules_present=requested_present,
        forbidden_rules_absent=forbidden_absent,
        well_formed=well_formed,
        adapter_valid=adapter_valid,
        errors=tuple(all_errors),
    )
