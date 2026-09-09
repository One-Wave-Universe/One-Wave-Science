"""A minimal non-equation adapter used only by tests.

It exists to prove the core/adapter contract is not secretly algebra-shaped:
its artifacts are plain space-separated words, not equations, and it plugs
into the exact same build_problem() pipeline with zero changes to
parser/core.py, parser/adapter.py, or parser/verifier.py.
"""

from __future__ import annotations

import random
from typing import Any

from Learner_App.parser.models import RulePacket

DOMAIN = "test/trivial_echo"

ECHO_PRESENT = "ECHO.PRESENT"
ECHO_ABSENT_OK = "ECHO.ABSENT_OK"

KNOWN_RULES = {ECHO_PRESENT, ECHO_ABSENT_OK}

WORDS = ("alpha", "bravo", "charlie", "delta", "foxtrot")


class TrivialEchoStructure:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens


class TrivialEchoAdapter:
    domain = DOMAIN

    def validate_packet(self, packet: RulePacket) -> list[str]:
        errors = []
        unknown = sorted((set(packet.target_rules) | set(packet.forbidden_rules)) - KNOWN_RULES)
        if unknown:
            errors.append(f"unknown rule id(s): {unknown}")
        if not packet.target_rules:
            errors.append("target_rules must not be empty")
        return errors

    def generate_candidate(self, packet: RulePacket, rng: random.Random) -> str:
        word_count = 1 + packet.difficulty
        words = [rng.choice(WORDS) for _ in range(word_count)]
        if ECHO_PRESENT in packet.target_rules:
            words.append("echo")
        return " ".join(words)

    def parse_artifact(self, text: str) -> TrivialEchoStructure:
        tokens = text.split()
        if not tokens:
            raise ValueError("empty artifact text")
        return TrivialEchoStructure(tokens=tokens)

    def inspect_rules(self, structure: TrivialEchoStructure) -> list[str]:
        return [ECHO_PRESENT] if "echo" in structure.tokens else [ECHO_ABSENT_OK]

    def validate_structure(
        self, structure: TrivialEchoStructure, packet: RulePacket
    ) -> tuple[bool, list[str], dict[str, Any]]:
        if not structure.tokens:
            return False, ["empty artifact"], {}
        return True, [], {"token_count": len(structure.tokens)}
