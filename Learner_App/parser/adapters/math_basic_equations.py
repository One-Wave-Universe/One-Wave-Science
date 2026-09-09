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
one constant term, more than one occurrence of the variable, a coefficient
combined with a divisor on the same term, or any constraints.number_domain
other than "integer" (the default -- generation and validation both
guarantee the unknown solves to an integer under it).
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

# v1 only knows how to guarantee integer solutions. A packet asking for a
# different number domain is rejected in validate_packet() rather than
# silently producing fractional/irrational unknowns.
SUPPORTED_NUMBER_DOMAINS = {"integer"}
DEFAULT_NUMBER_DOMAIN = "integer"

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
    """Tokenize `text`, rejecting any character the grammar doesn't
    recognize. `re.findall` alone would silently drop unmatched characters
    (e.g. "x + 4 @ = 9" would tokenize identically to "x + 4 = 9"), which
    would let the reparse accept artifact text it never actually validated.
    Every gap between matched tokens (and before/after all of them) must be
    pure whitespace."""
    tokens: list[str] = []
    pos = 0
    for match in _TOKEN_RE.finditer(text):
        gap = text[pos:match.start()]
        if gap.strip():
            raise MathParseError(f"unrecognized character(s) {gap.strip()!r} at position {pos}")
        tokens.append(match.group())
        pos = match.end()
    trailing = text[pos:]
    if trailing.strip():
        raise MathParseError(f"unrecognized character(s) {trailing.strip()!r} at position {pos}")
    return tokens


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
        if divisor == 0:
            # The parser is an input boundary in its own right, not only a
            # round-trip check on this adapter's own generator -- reject
            # division by zero here regardless of whether generation could
            # ever produce it.
            raise MathParseError("divisor cannot be zero")
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


def _is_valid_int_range(value: Any) -> bool:
    return (
        isinstance(value, (tuple, list))
        and len(value) == 2
        and all(isinstance(v, int) and not isinstance(v, bool) for v in value)
        and value[0] <= value[1]
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

        number_domain = packet.constraints.get("number_domain", DEFAULT_NUMBER_DOMAIN)
        if number_domain not in SUPPORTED_NUMBER_DOMAINS:
            errors.append(
                f"unsupported constraints.number_domain for {DOMAIN} v1: {number_domain!r} "
                f"(only {sorted(SUPPORTED_NUMBER_DOMAINS)} supported)"
            )

        # Validate numeric constraint shapes up front so a malformed packet
        # fails cleanly here instead of raising an unpack/randint error
        # later inside generate_candidate().
        if "coefficient_range" in packet.constraints and not _is_valid_int_range(
            packet.constraints["coefficient_range"]
        ):
            errors.append(
                "constraints.coefficient_range must be a 2-item (lo, hi) integer range with lo <= hi"
            )
        if "constant_range" in packet.constraints and not _is_valid_int_range(
            packet.constraints["constant_range"]
        ):
            errors.append(
                "constraints.constant_range must be a 2-item (lo, hi) integer range with lo <= hi"
            )
        if (
            not isinstance(packet.difficulty, int)
            or isinstance(packet.difficulty, bool)
            or packet.difficulty < 1
        ):
            errors.append("difficulty must be a positive integer")

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

        # constraints.number_domain defaults to "integer" (v1's only
        # supported domain, enforced in validate_packet()). When a
        # coefficient is present, the term's value must land on an exact
        # multiple of it or the unknown would come out fractional -- so
        # build the term's value from a hidden integer multiplier rather
        # than picking it independently. The multiplier itself is never
        # returned, stored, or logged anywhere public; only its product
        # (a term value, not the solved unknown) is used.
        if coefficient != 1:
            hidden_multiplier = rng.randint(1, max(1, term_hi // coefficient))
            term_value = coefficient * hidden_multiplier
        else:
            term_value = rng.randint(term_lo, term_hi)

        sign = "+" if EQ_ADD_INVERSE in rules else "-" if EQ_SUB_INVERSE in rules else None
        if sign == "-":
            # rhs = term_value - constant must stay non-negative (v1 has no
            # negative-number support anywhere in the grammar).
            constant = rng.randint(const_lo, max(const_lo, min(const_hi, term_value)))
            rhs = term_value - constant
        elif sign == "+":
            constant = rng.randint(const_lo, const_hi)
            rhs = term_value + constant
        else:
            constant = None
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

        number_domain = packet.constraints.get("number_domain", DEFAULT_NUMBER_DOMAIN)
        if (
            number_domain == "integer"
            and structure.var_term.coefficient != 1
            and structure.var_term.divisor is None
        ):
            # Re-derive the coefficient*x term's value from the publicly
            # printed rhs/constant (not from anything the generator kept
            # around) and independently confirm it is a clean multiple of
            # the coefficient -- i.e. that x itself would be an integer.
            # This never computes or exposes x, only checks divisibility.
            term_value = structure.rhs
            if structure.constant_term is not None:
                if structure.constant_term.sign == "+":
                    term_value -= structure.constant_term.value
                else:
                    term_value += structure.constant_term.value
            if term_value % structure.var_term.coefficient != 0:
                errors.append(
                    "equation has no integer solution under the v1 default integer number_domain"
                )

        # single_target_unknown is a math-adapter concept (exactly one
        # unknown symbol, appearing exactly once) -- it stays here, in
        # adapter-facing metadata, rather than becoming a core-level field
        # that every future domain would have to carry.
        metadata = {
            "single_target_unknown": True,
            "variable": structure.var_term.variable,
            "number_domain": number_domain,
        }

        return (not errors, errors, metadata)
