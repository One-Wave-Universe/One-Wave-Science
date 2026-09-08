"""math/basic_equations: the first domain adapter for the problem-builder core.

Generates and independently reparses one-variable linear equations that
exercise a small, explicit set of adapter rule recipes:

    EQ.IDENTITY      -- x = c
    EQ.ADD_INVERSE   -- x + b = c
    EQ.SUB_INVERSE   -- x - b = c
    EQ.MUL_INVERSE   -- a*x = c
    EQ.DIV_INVERSE   -- x/a = c

These rule IDs are adapter fixtures used to prove the worker contract. They
are not the learner curriculum -- the router owns that.

v1 explicitly does NOT support: variables on both sides, parentheses,
exponents, non-integer coefficients, negative numbers anywhere, more than
one constant term, more than one occurrence of the variable, or a
coefficient combined with a divisor on the same term.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from typing import Any

from ..models import RulePacket

DOMAIN = "math/basic_equations"

EQ_IDENTITY = "EQ.IDENTITY"
EQ_ADD_INVERSE = "EQ.ADD_INVERSE"
EQ_SUB_INVERSE = "EQ.SUB_INVERSE"
EQ_MUL_INVERSE = "EQ.MUL_INVERSE"
EQ_DIV_INVERSE = "EQ.DIV_INVERSE"

KNOWN_RULES = {
    EQ_IDENTITY,
    EQ_ADD_INVERSE,
    EQ_SUB_INVERSE,
    EQ_MUL_INVERSE,
    EQ_DIV_INVERSE,
}

# The only target-rule combinations v1 knows how to build. Anything else is
# rejected by validate_packet() before generation is attempted -- this is
# also what keeps EQ_MUL_INVERSE and EQ_DIV_INVERSE from ever being
# requested together, since a single term cannot carry both in v1.
SUPPORTED_COMBOS = {
    frozenset({EQ_IDENTITY}),
    frozenset({EQ_ADD_INVERSE}),
    frozenset({EQ_SUB_INVERSE}),
    frozenset({EQ_MUL_INVERSE}),
    frozenset({EQ_DIV_INVERSE}),
    frozenset({EQ_ADD_INVERSE, EQ_MUL_INVERSE}),
    frozenset({EQ_SUB_INVERSE, EQ_MUL_INVERSE}),
    frozenset({EQ_ADD_INVERSE, EQ_DIV_INVERSE}),
    frozenset({EQ_SUB_INVERSE, EQ_DIV_INVERSE}),
}

DEFAULT_VARIABLE_NAMES = ("x",)
DEFAULT_COEFFICIENT_RANGE = (2, 9)
DEFAULT_CONSTANT_RANGE = (1, 20)
DEFAULT_TERM_VALUE_RANGE = (1, 40)

_TOKEN_RE = re.compile(r"\d+|[a-zA-Z]|[+\-/=]")


@dataclass(frozen=True)
class VarTerm:
    coefficient: int
    variable: str
    divisor: int | None


@dataclass(frozen=True)
class ConstantTerm:
    sign: str  # "+" or "-"
    value: int


@dataclass(frozen=True)
class EquationStructure:
    """Independently reparsed structure of a one-variable linear equation.

    Nothing on this object is the solved value of the variable -- rhs is
    the constant already printed on the right of the "=" in the artifact
    text, not an answer derived from solving.
    """

    var_term: VarTerm
    constant_term: ConstantTerm | None
    rhs: int
    equality_sides: tuple[str, str]  # rendered lhs text, rendered rhs text


class MathParseError(ValueError):
    """Raised by parse_artifact() when text does not match the v1 grammar."""


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text)


def _parse_var_term(tokens: list[str], i: int) -> tuple[VarTerm, int]:
    if i >= len(tokens):
        raise MathParseError("expected a variable term, found end of input")

    coefficient = 1
    if tokens[i].isdigit() and i + 1 < len(tokens) and tokens[i + 1].isalpha():
        coefficient = int(tokens[i])
        i += 1

    if i >= len(tokens) or not tokens[i].isalpha():
        raise MathParseError(f"expected a variable symbol at position {i}")
    variable = tokens[i]
    i += 1

    divisor = None
    if i < len(tokens) and tokens[i] == "/":
        i += 1
        if i >= len(tokens) or not tokens[i].isdigit():
            raise MathParseError("expected an integer divisor after '/'")
        divisor = int(tokens[i])
        i += 1

    return VarTerm(coefficient=coefficient, variable=variable, divisor=divisor), i


def parse_equation_text(text: str) -> EquationStructure:
    """Parse `text` from scratch. Deliberately independent of anything a
    generator might have used to build it -- this only looks at tokens."""
    tokens = _tokenize(text)
    if not tokens:
        raise MathParseError("empty artifact text")

    var_term, i = _parse_var_term(tokens, 0)

    constant_term = None
    if i < len(tokens) and tokens[i] in ("+", "-"):
        sign = tokens[i]
        i += 1
        if i >= len(tokens) or not tokens[i].isdigit():
            raise MathParseError("expected an integer constant after sign")
        constant_term = ConstantTerm(sign=sign, value=int(tokens[i]))
        i += 1

    if i >= len(tokens) or tokens[i] != "=":
        raise MathParseError("expected '=' after left-hand side")
    i += 1

    if i >= len(tokens) or not tokens[i].isdigit():
        raise MathParseError("expected an integer right-hand side")
    rhs = int(tokens[i])
    i += 1

    if i != len(tokens):
        raise MathParseError(f"unexpected trailing tokens: {tokens[i:]}")

    lhs_text, _, rhs_text = text.partition("=")
    return EquationStructure(
        var_term=var_term,
        constant_term=constant_term,
        rhs=rhs,
        equality_sides=(lhs_text.strip(), rhs_text.strip()),
    )


def _rules_present(structure: EquationStructure) -> list[str]:
    rules: list[str] = []
    if structure.var_term.coefficient != 1:
        rules.append(EQ_MUL_INVERSE)
    if structure.var_term.divisor is not None:
        rules.append(EQ_DIV_INVERSE)
    if structure.constant_term is not None:
        rules.append(EQ_ADD_INVERSE if structure.constant_term.sign == "+" else EQ_SUB_INVERSE)
    if not rules:
        rules.append(EQ_IDENTITY)
    return rules


class MathBasicEquationsAdapter:
    domain = DOMAIN

    def validate_packet(self, packet: RulePacket) -> list[str]:
        errors: list[str] = []

        all_named = (
            set(packet.target_rules) | set(packet.allowed_support_rules) | set(packet.forbidden_rules)
        )
        unknown = sorted(all_named - KNOWN_RULES)
        if unknown:
            errors.append(f"unknown rule id(s) for {DOMAIN}: {unknown}")

        if not packet.target_rules:
            errors.append("target_rules must not be empty")

        combo = frozenset(packet.target_rules)
        if combo and combo not in SUPPORTED_COMBOS:
            errors.append(f"unsupported target-rule combination for {DOMAIN} v1: {sorted(combo)}")

        variable_names = packet.constraints.get("variable_names", DEFAULT_VARIABLE_NAMES)
        if not variable_names or any(
            not isinstance(v, str) or len(v) != 1 or not v.isalpha() for v in variable_names
        ):
            errors.append("constraints.variable_names must be a non-empty list of single letters")

        return errors

    def generate_candidate(self, packet: RulePacket, rng: random.Random) -> str:
        rules = set(packet.target_rules)
        variable_names = packet.constraints.get("variable_names", DEFAULT_VARIABLE_NAMES)
        variable = rng.choice(list(variable_names))

        coeff_lo, coeff_hi = packet.constraints.get("coefficient_range", DEFAULT_COEFFICIENT_RANGE)
        const_lo, const_hi = packet.constraints.get("constant_range", DEFAULT_CONSTANT_RANGE)
        const_hi = const_hi * max(1, packet.difficulty)
        term_lo, term_hi = DEFAULT_TERM_VALUE_RANGE
        term_hi = term_hi * max(1, packet.difficulty)

        coefficient = (
            rng.randint(max(2, coeff_lo), max(coeff_hi, coeff_lo + 1)) if EQ_MUL_INVERSE in rules else 1
        )
        divisor = (
            rng.randint(max(2, coeff_lo), max(coeff_hi, coeff_lo + 1)) if EQ_DIV_INVERSE in rules else None
        )

        sign = "+" if EQ_ADD_INVERSE in rules else "-" if EQ_SUB_INVERSE in rules else None
        constant = rng.randint(const_lo, const_hi) if sign else None

        if sign == "-":
            # rhs = term_value - constant must stay non-negative (v1 has no
            # negative-number support anywhere in the grammar).
            term_value = rng.randint(max(constant, term_lo), max(term_hi, constant + 1))
            rhs = term_value - constant
        elif sign == "+":
            term_value = rng.randint(term_lo, term_hi)
            rhs = term_value + constant
        else:
            term_value = rng.randint(term_lo, term_hi)
            rhs = term_value

        if divisor is not None:
            lhs = f"{variable}/{divisor}"
        elif coefficient != 1:
            lhs = f"{coefficient}{variable}"
        else:
            lhs = variable

        if sign is not None:
            lhs = f"{lhs} {sign} {constant}"

        return f"{lhs} = {rhs}"

    def parse_artifact(self, text: str) -> EquationStructure:
        return parse_equation_text(text)

    def inspect_rules(self, structure: EquationStructure) -> list[str]:
        return _rules_present(structure)

    def validate_structure(
        self, structure: EquationStructure, packet: RulePacket
    ) -> tuple[bool, list[str], dict[str, Any]]:
        errors: list[str] = []

        if structure.var_term.coefficient != 1 and structure.var_term.divisor is not None:
            errors.append("both a coefficient and a divisor present; unsupported in v1")

        variable_names = packet.constraints.get("variable_names", DEFAULT_VARIABLE_NAMES)
        if structure.var_term.variable not in variable_names:
            errors.append(
                f"variable {structure.var_term.variable!r} not in allowed "
                f"variable_names {list(variable_names)}"
            )

        if structure.rhs < 0:
            errors.append("right-hand side is negative; unsupported in v1")

        # single_target_unknown is a math-adapter concept (exactly one
        # unknown symbol, appearing exactly once) -- it stays here, in
        # adapter-facing metadata, rather than becoming a core-level field
        # that every future domain would have to carry.
        metadata = {
            "single_target_unknown": True,
            "variable": structure.var_term.variable,
        }

        return (not errors, errors, metadata)
