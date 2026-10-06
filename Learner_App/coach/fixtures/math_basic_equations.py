"""Coach fixtures for math/basic_equations -- the first Coach domain
fixture, used because Phase 1 already supports this domain's rules (see
issue #47's "Example fixtures" section). These are fixtures, not hardcoded
core logic: the reusable Coach core (coach/models.py, registry.py,
worker.py) knows nothing about algebra, coefficients, or equations.

The rule_id string literals below are written out rather than imported
from Learner_App.parser.adapters.math_basic_equations on purpose: the
Coach package has the same one-way-dependency rule the Recall Worker has
(see coach/models.py's module docstring) -- it never imports parser or
router. Keeping the literals in sync with that adapter's EQ_* constants is
enforced by Learner_App/tests/test_coach_fixtures_math_basic_equations.py,
not by a Python import.
"""

from __future__ import annotations

from ..models import RuleExplanation
from ..registry import register_rule_explanation

# Must match Learner_App.parser.adapters.math_basic_equations's EQ_* values.
EQ_IDENTITY = "EQ.IDENTITY"
EQ_ADD_INVERSE = "EQ.ADD_INVERSE"
EQ_SUB_INVERSE = "EQ.SUB_INVERSE"
EQ_MUL_INVERSE = "EQ.MUL_INVERSE"
EQ_DIV_INVERSE = "EQ.DIV_INVERSE"

# Prerequisite concept cards -- not Phase 1 target rules themselves, just
# reusable explanation scaffolding the operational rules below point back
# to via `prerequisites`. These are exactly the three example fixtures
# issue #47 specifies.
CONCEPT_COEFFICIENT = "EQ.CONCEPT.COEFFICIENT"
CONCEPT_WHOLE_EQUATION_SCALING = "EQ.CONCEPT.WHOLE_EQUATION_SCALING"
CONCEPT_INVERSE_OPERATION = "EQ.CONCEPT.INVERSE_OPERATION"


_EXPLANATIONS: tuple[RuleExplanation, ...] = (
    RuleExplanation(
        rule_id=CONCEPT_COEFFICIENT,
        title="Coefficient",
        pattern="a term written as number × variable",
        if_text="IF a term is number × variable",
        then_text="THEN the numeric factor is the coefficient",
        why_text=(
            "WHY: it tells how many copies/scaled units of the variable are in that term"
        ),
        only_when_text=(
            "ONLY WHEN the number is multiplying that variable as part of the same term"
        ),
        do_not_use_when_text=(
            "DO NOT USE WHEN the number is a separate added/subtracted constant"
        ),
        examples=("in 4y, 4 is the coefficient of y",),
        counterexamples=("in y + 4, the 4 is an added constant, not a coefficient",),
        concept_first_note=(
            "Look at what is directly stuck to the variable, multiplying it, "
            "versus what is only added or subtracted next to it."
        ),
        formal_terms=("coefficient",),
    ),
    RuleExplanation(
        rule_id=CONCEPT_WHOLE_EQUATION_SCALING,
        title="Whole-equation scaling",
        pattern="an equation that needs a matching term/coefficient",
        if_text=(
            "IF you need one equation in a system to have a matching term/coefficient"
        ),
        then_text=(
            "THEN multiply every term on both sides of THAT equation by the same "
            "nonzero factor"
        ),
        why_text="WHY: you create an equivalent equation representing the same relationship",
        only_when_text="ONLY WHEN the entire chosen equation is scaled consistently",
        do_not_use_when_text=(
            "DO NOT USE WHEN you would multiply only one term, or mix factors inside "
            "the equation arbitrarily"
        ),
        prerequisites=(CONCEPT_COEFFICIENT,),
        examples=(
            "2p + q = 7 scaled by 3 on both whole sides becomes 6p + 3q = 21",
        ),
        counterexamples=(
            "multiplying only the left side of 2p + q = 7 by 3 breaks the relationship",
        ),
        concept_first_note=(
            "Multiplying an entire equation by the same number does not change what "
            "it claims -- it only changes how the claim is written."
        ),
    ),
    RuleExplanation(
        rule_id=CONCEPT_INVERSE_OPERATION,
        title="Inverse operation",
        pattern="a variable group with extra baggage attached by one operation",
        if_text="IF a variable group has extra baggage attached by one operation",
        then_text=(
            "THEN use the inverse operation on the whole matching equation structure "
            "to remove that baggage"
        ),
        why_text="WHY: inverse operations undo each other while equality is preserved",
        only_when_text=(
            "ONLY WHEN the operation is applied legally to both sides of that equation"
        ),
        do_not_use_when_text=(
            "DO NOT USE WHEN you are changing only one side or only one arbitrary term"
        ),
        examples=(
            "y + 5 = 12 has 5 added to y -- subtract 5 from both whole sides",
        ),
        counterexamples=(
            "subtracting 5 from only the left side of y + 5 = 12 breaks the relationship",
        ),
        concept_first_note=(
            "Find what was attached to the unknown and by which operation, then undo "
            "exactly that operation on the whole equation, not just one piece."
        ),
        formal_terms=("inverse operation",),
    ),
    RuleExplanation(
        rule_id=EQ_IDENTITY,
        title="Already isolated",
        pattern="x = c",
        if_text=(
            "IF the unknown already stands alone on one whole side with nothing "
            "added, subtracted, multiplying, or dividing it"
        ),
        then_text=(
            "THEN no operation is needed -- the equation already states the "
            "unknown's value directly"
        ),
        why_text="WHY: the equation is already a direct same-value claim between the unknown and a number",
        only_when_text="ONLY WHEN the unknown has no other operation attached to it on that side",
        do_not_use_when_text=(
            "DO NOT USE WHEN the unknown has any amount added, subtracted, "
            "multiplying, or dividing it -- an inverse-operation rule applies first"
        ),
        examples=("x = 9 already states the unknown's value directly",),
        counterexamples=("x + 2 = 9 still has an operation attached to x",),
        concept_first_note="Check whether anything is still attached to the unknown before assuming you are done.",
    ),
    RuleExplanation(
        rule_id=EQ_ADD_INVERSE,
        title="Undo an added amount",
        pattern="x + b = c",
        if_text="IF the unknown has a positive amount added to it on one whole side",
        then_text="THEN subtract that same amount from both whole sides",
        why_text=(
            "WHY: subtracting the same amount from both sides changes both sides by "
            "the same amount, so the relationship stays true while the unknown's "
            "side loses its extra baggage"
        ),
        only_when_text=(
            "ONLY WHEN the amount is added to the entire side the unknown is on, and "
            "the same subtraction is applied to the entire other side"
        ),
        do_not_use_when_text=(
            "DO NOT USE WHEN the amount is multiplying the unknown instead of being "
            "added to it, or when you would only change part of one side"
        ),
        prerequisites=(CONCEPT_INVERSE_OPERATION,),
        examples=("y + 7 = 15 -> subtract 7 from both whole sides -> y + 7 - 7 = 15 - 7",),
        counterexamples=("4 * y = 15 is multiplication, not addition -- this rule does not apply",),
        concept_first_note=(
            "You have the unknown, and something extra got added onto it. First see "
            "what is attached, then undo only that addition, on the whole equation."
        ),
        formal_terms=("additive inverse",),
    ),
    RuleExplanation(
        rule_id=EQ_SUB_INVERSE,
        title="Undo a subtracted amount",
        pattern="x - b = c",
        if_text="IF the unknown has a positive amount subtracted from it on one whole side",
        then_text="THEN add that same amount to both whole sides",
        why_text=(
            "WHY: adding the same amount to both sides changes both sides by the "
            "same amount, so the relationship stays true while the unknown's side "
            "loses its missing piece"
        ),
        only_when_text=(
            "ONLY WHEN the amount is subtracted from the entire side the unknown is "
            "on, and the same addition is applied to the entire other side"
        ),
        do_not_use_when_text=(
            "DO NOT USE WHEN the amount is dividing the unknown instead of being "
            "subtracted from it, or when you would only change part of one side"
        ),
        prerequisites=(CONCEPT_INVERSE_OPERATION,),
        examples=("y - 6 = 4 -> add 6 to both whole sides -> y - 6 + 6 = 4 + 6",),
        counterexamples=("y / 6 = 4 is division, not subtraction -- this rule does not apply",),
        concept_first_note=(
            "You have the unknown, and something is missing from it. First see what "
            "was taken away, then add it back on the whole equation."
        ),
        formal_terms=("additive inverse",),
    ),
    RuleExplanation(
        rule_id=EQ_MUL_INVERSE,
        title="Undo a multiplying coefficient",
        pattern="a*x = c",
        if_text=(
            "IF the unknown is being multiplied by a number (its coefficient) on "
            "one whole side"
        ),
        then_text="THEN divide both whole sides by that same coefficient",
        why_text=(
            "WHY: dividing both sides by the same nonzero number changes both sides "
            "by the same scale, so the relationship stays true while the coefficient "
            "is removed from the unknown's side"
        ),
        only_when_text=(
            "ONLY WHEN that number is multiplying the unknown as part of the same "
            "term, and you divide the entire other side by it too"
        ),
        do_not_use_when_text=(
            "DO NOT USE WHEN the number is a separate added or subtracted constant "
            "rather than a multiplier on the unknown's own term"
        ),
        prerequisites=(CONCEPT_INVERSE_OPERATION, CONCEPT_COEFFICIENT),
        examples=("3y = 21 -> divide both whole sides by 3 -> 3y / 3 = 21 / 3",),
        counterexamples=("y + 3 = 21 has 3 added, not multiplying -- this rule does not apply",),
        concept_first_note=(
            "A number is scaling the unknown. First recognize that number as the "
            "coefficient, then undo the scaling on the whole equation."
        ),
        formal_terms=("multiplicative inverse", "coefficient"),
    ),
    RuleExplanation(
        rule_id=EQ_DIV_INVERSE,
        title="Undo a dividing factor",
        pattern="x/a = c",
        if_text="IF the unknown is being divided by a number on one whole side",
        then_text="THEN multiply both whole sides by that same number",
        why_text=(
            "WHY: multiplying both sides by the same nonzero number changes both "
            "sides by the same scale, so the relationship stays true while the "
            "division is removed from the unknown's side"
        ),
        only_when_text=(
            "ONLY WHEN that number is dividing the unknown as part of the same term, "
            "and you multiply the entire other side by it too"
        ),
        do_not_use_when_text=(
            "DO NOT USE WHEN the number is a separate added or subtracted constant "
            "rather than a divisor on the unknown's own term"
        ),
        prerequisites=(CONCEPT_INVERSE_OPERATION,),
        examples=("y/4 = 5 -> multiply both whole sides by 4 -> (y/4) * 4 = 5 * 4",),
        counterexamples=("y - 4 = 5 has 4 subtracted, not dividing -- this rule does not apply",),
        concept_first_note=(
            "The unknown is being split into parts. First see what number it is "
            "divided by, then undo that division on the whole equation."
        ),
        formal_terms=("multiplicative inverse",),
    ),
)


def register_default_explanations(*, replace: bool = False) -> None:
    """Register every math/basic_equations Coach fixture. Explicit call,
    no import-time registration -- mirrors
    parser.adapters.register_default_adapters()."""
    for explanation in _EXPLANATIONS:
        register_rule_explanation(explanation, replace=replace)


__all__ = [
    "CONCEPT_COEFFICIENT",
    "CONCEPT_INVERSE_OPERATION",
    "CONCEPT_WHOLE_EQUATION_SCALING",
    "EQ_ADD_INVERSE",
    "EQ_DIV_INVERSE",
    "EQ_IDENTITY",
    "EQ_MUL_INVERSE",
    "EQ_SUB_INVERSE",
    "register_default_explanations",
]
