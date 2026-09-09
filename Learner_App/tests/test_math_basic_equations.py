"""Math adapter acceptance tests (issue #40, math adapter items 1-10)."""

from __future__ import annotations

import dataclasses
import unittest

from Learner_App.parser.core import ProblemVerificationError, build_problem
from Learner_App.parser.models import RulePacket
from Learner_App.parser.adapters.math_basic_equations import (
    DOMAIN,
    EQ_ADD_INVERSE,
    EQ_DIV_INVERSE,
    EQ_MUL_INVERSE,
    EQ_SUB_INVERSE,
    MathBasicEquationsAdapter,
    MathParseError,
    SUPPORTED_COMBOS,
    parse_equation_text,
)


def _packet(target_rules, seed=1, **kwargs) -> RulePacket:
    defaults = dict(packet_id="math-test", seed=seed, domain=DOMAIN, target_rules=target_rules)
    defaults.update(kwargs)
    return RulePacket(**defaults)


class MathAdapterAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.adapter = MathBasicEquationsAdapter()

    def test_add_inverse_only_is_one_step_addition(self):
        result = build_problem(_packet([EQ_ADD_INVERSE], seed=10), adapter=self.adapter)
        self.assertEqual(result.rules_used, (EQ_ADD_INVERSE,))
        self.assertEqual(result.structure.var_term.coefficient, 1)
        self.assertIsNone(result.structure.var_term.divisor)
        self.assertEqual(result.structure.constant_term.sign, "+")

    def test_mul_inverse_only_is_one_step_coefficient_equation(self):
        result = build_problem(_packet([EQ_MUL_INVERSE], seed=11), adapter=self.adapter)
        self.assertEqual(result.rules_used, (EQ_MUL_INVERSE,))
        self.assertNotEqual(result.structure.var_term.coefficient, 1)
        self.assertIsNone(result.structure.constant_term)

    def test_add_and_mul_inverse_is_two_step_with_no_extra_family(self):
        result = build_problem(
            _packet([EQ_ADD_INVERSE, EQ_MUL_INVERSE], seed=12), adapter=self.adapter
        )
        self.assertEqual(set(result.rules_used), {EQ_ADD_INVERSE, EQ_MUL_INVERSE})
        self.assertNotIn(EQ_DIV_INVERSE, result.rules_used)
        self.assertNotIn(EQ_SUB_INVERSE, result.rules_used)

    def test_different_seeds_vary_constants_but_keep_structure(self):
        packet_a = _packet([EQ_ADD_INVERSE, EQ_MUL_INVERSE], seed=20)
        packet_b = dataclasses.replace(packet_a, seed=21)
        result_a = build_problem(packet_a, adapter=self.adapter)
        result_b = build_problem(packet_b, adapter=self.adapter)
        self.assertEqual(set(result_a.rules_used), set(result_b.rules_used))
        self.assertNotEqual(result_a.artifact_text, result_b.artifact_text)

    def test_forbidden_division_never_appears(self):
        for seed in range(15):
            packet = _packet([EQ_ADD_INVERSE], seed=seed, forbidden_rules=[EQ_DIV_INVERSE])
            result = build_problem(packet, adapter=self.adapter)
            self.assertNotIn(EQ_DIV_INVERSE, result.rules_used)

    def test_same_rule_in_target_and_forbidden_is_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], forbidden_rules=[EQ_ADD_INVERSE])
        with self.assertRaises(Exception):
            build_problem(packet, adapter=self.adapter)

    def test_malformed_candidate_fails_reparse_and_verification(self):
        class BrokenAdapter(MathBasicEquationsAdapter):
            def generate_candidate(self, packet, rng):
                return "this is not an equation"

        packet = _packet([EQ_ADD_INVERSE], seed=1)
        with self.assertRaises(ProblemVerificationError) as ctx:
            build_problem(packet, adapter=BrokenAdapter())
        self.assertFalse(ctx.exception.verification.well_formed)

    def test_structure_identifies_all_components(self):
        result = build_problem(
            _packet([EQ_ADD_INVERSE, EQ_MUL_INVERSE], seed=30), adapter=self.adapter
        )
        structure = result.structure
        self.assertTrue(structure.var_term.variable.isalpha())
        self.assertIsInstance(structure.var_term.coefficient, int)
        self.assertIsInstance(structure.constant_term.value, int)
        self.assertEqual(len(structure.equality_sides), 2)
        self.assertIsInstance(structure.rhs, int)

    def test_100_generated_problems_across_supported_combos_round_trip(self):
        combos = sorted(SUPPORTED_COMBOS, key=lambda c: sorted(c))
        seed = 0
        successes = 0
        for _ in range(100):
            combo = combos[seed % len(combos)]
            packet = _packet(sorted(combo), seed=seed)
            result = build_problem(packet, adapter=self.adapter)
            self.assertTrue(result.verification.passed)
            reparsed = self.adapter.parse_artifact(result.artifact_text)
            self.assertEqual(reparsed, result.structure)
            successes += 1
            seed += 1
        self.assertEqual(successes, 100)

    def test_no_public_output_reveals_the_solved_unknown(self):
        result = build_problem(
            _packet([EQ_ADD_INVERSE, EQ_MUL_INVERSE], seed=40), adapter=self.adapter
        )
        forbidden_field_names = {"answer", "solution", "solved_value", "x_value"}
        structure_field_names = {f.name for f in dataclasses.fields(result.structure)}
        self.assertFalse(structure_field_names & forbidden_field_names)


class MathAdapterRejectionTests(unittest.TestCase):
    def setUp(self):
        self.adapter = MathBasicEquationsAdapter()

    def test_unsupported_combo_rejected_before_generation(self):
        packet = _packet([EQ_MUL_INVERSE, EQ_DIV_INVERSE])
        errors = self.adapter.validate_packet(packet)
        self.assertTrue(errors)

    def test_unknown_rule_id_rejected(self):
        packet = _packet(["EQ.NOT_REAL"])
        errors = self.adapter.validate_packet(packet)
        self.assertTrue(errors)

    def test_unsupported_number_domain_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], constraints={"number_domain": "rational"})
        errors = self.adapter.validate_packet(packet)
        self.assertTrue(errors)


class TokenizerCoverageTests(unittest.TestCase):
    """Regression tests: the reparse must reject any artifact text with
    characters the grammar doesn't recognize, not silently ignore them."""

    def test_junk_character_between_tokens_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("x + 4 @ = 9")

    def test_junk_character_inside_a_number_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("x + 4a = 9")

    def test_trailing_junk_character_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("x + 4 = 9!")

    def test_junk_before_first_token_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("x @ + 4 = 9")

    def test_junk_dollar_sign_before_coefficient_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("7$x = 14")

    def test_repeated_equality_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("x = 4 = 9")

    def test_zero_divisor_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("x/0 = 5")

    def test_valid_text_with_whitespace_gaps_still_parses(self):
        structure = parse_equation_text("x   +   4   =   9")
        self.assertEqual(structure.rhs, 9)

    def test_malformed_text_from_build_problem_is_caught_end_to_end(self):
        class InjectingAdapter(MathBasicEquationsAdapter):
            def generate_candidate(self, packet, rng):
                return "x + 4 @ = 9"

        packet = _packet([EQ_ADD_INVERSE], seed=1)
        with self.assertRaises(ProblemVerificationError) as ctx:
            build_problem(packet, adapter=InjectingAdapter())
        self.assertFalse(ctx.exception.verification.well_formed)

    def test_zero_divisor_from_build_problem_is_caught_end_to_end(self):
        class InjectingAdapter(MathBasicEquationsAdapter):
            def generate_candidate(self, packet, rng):
                return "x/0 = 5"

        packet = _packet([EQ_DIV_INVERSE], seed=1)
        with self.assertRaises(ProblemVerificationError) as ctx:
            build_problem(packet, adapter=InjectingAdapter())
        self.assertFalse(ctx.exception.verification.well_formed)

    def test_zero_coefficient_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("0x = 5")

    def test_zero_coefficient_with_constant_is_rejected(self):
        with self.assertRaises(MathParseError):
            parse_equation_text("0x + 3 = 8")

    def test_zero_coefficient_from_build_problem_is_caught_end_to_end(self):
        # Before the fix this raised ZeroDivisionError from
        # validate_structure()'s divisibility check instead of failing
        # verification cleanly.
        class InjectingAdapter(MathBasicEquationsAdapter):
            def generate_candidate(self, packet, rng):
                return "0x = 5"

        packet = _packet([EQ_ADD_INVERSE], seed=1)
        with self.assertRaises(ProblemVerificationError) as ctx:
            build_problem(packet, adapter=InjectingAdapter())
        self.assertFalse(ctx.exception.verification.well_formed)


class ConstraintValidationTests(unittest.TestCase):
    """Malformed numeric constraints must fail cleanly in validate_packet(),
    not later as an unpack/randint crash inside generate_candidate()."""

    def setUp(self):
        self.adapter = MathBasicEquationsAdapter()

    def test_reversed_coefficient_range_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], constraints={"coefficient_range": (9, 2)})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_non_tuple_coefficient_range_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], constraints={"coefficient_range": 5})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_non_integer_coefficient_range_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], constraints={"coefficient_range": (1.5, 9)})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_reversed_constant_range_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], constraints={"constant_range": (20, 1)})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_zero_difficulty_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], difficulty=0)
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_negative_difficulty_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], difficulty=-1)
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_non_integer_difficulty_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], difficulty="high")
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_valid_constraints_accepted(self):
        packet = _packet(
            [EQ_ADD_INVERSE, EQ_MUL_INVERSE],
            constraints={"coefficient_range": (2, 5), "constant_range": (1, 10)},
            difficulty=2,
        )
        self.assertEqual(self.adapter.validate_packet(packet), [])


class IntegerSolutionTests(unittest.TestCase):
    """Regression tests: EQ.MUL_INVERSE equations must keep the unknown an
    integer under the v1 default number_domain, not just a random rhs."""

    def setUp(self):
        self.adapter = MathBasicEquationsAdapter()

    def _solved_value_is_integer(self, structure):
        term_value = structure.rhs
        if structure.constant_term is not None:
            if structure.constant_term.sign == "+":
                term_value -= structure.constant_term.value
            else:
                term_value += structure.constant_term.value
        return term_value % structure.var_term.coefficient == 0

    def test_mul_inverse_only_always_has_integer_solution(self):
        for seed in range(50):
            result = build_problem(_packet([EQ_MUL_INVERSE], seed=seed), adapter=self.adapter)
            self.assertTrue(self._solved_value_is_integer(result.structure))

    def test_add_and_mul_inverse_always_has_integer_solution(self):
        for seed in range(50):
            result = build_problem(
                _packet([EQ_ADD_INVERSE, EQ_MUL_INVERSE], seed=seed), adapter=self.adapter
            )
            self.assertTrue(self._solved_value_is_integer(result.structure))

    def test_sub_and_mul_inverse_always_has_integer_solution(self):
        for seed in range(50):
            result = build_problem(
                _packet([EQ_SUB_INVERSE, EQ_MUL_INVERSE], seed=seed), adapter=self.adapter
            )
            self.assertTrue(self._solved_value_is_integer(result.structure))


class CoefficientRangeExactnessTests(unittest.TestCase):
    """Regression tests: the worker must never repair an infeasible
    coefficient_range by widening it -- it must reject the packet instead
    of silently drawing a coefficient/divisor outside the router's exact
    requested range."""

    def setUp(self):
        self.adapter = MathBasicEquationsAdapter()

    def test_mul_with_range_one_one_is_infeasible(self):
        packet = _packet([EQ_MUL_INVERSE], constraints={"coefficient_range": (1, 1)})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_div_with_range_zero_one_is_infeasible(self):
        packet = _packet([EQ_DIV_INVERSE], constraints={"coefficient_range": (0, 1)})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_mul_with_range_two_two_always_uses_coefficient_two(self):
        for seed in range(20):
            packet = _packet(
                [EQ_MUL_INVERSE], seed=seed, constraints={"coefficient_range": (2, 2)}
            )
            result = build_problem(packet, adapter=self.adapter)
            self.assertEqual(result.structure.var_term.coefficient, 2)

    def test_mul_with_range_four_six_always_stays_within_range(self):
        for seed in range(30):
            packet = _packet(
                [EQ_MUL_INVERSE], seed=seed, constraints={"coefficient_range": (4, 6)}
            )
            result = build_problem(packet, adapter=self.adapter)
            self.assertIn(result.structure.var_term.coefficient, (4, 5, 6))

    def test_div_with_range_four_six_always_stays_within_range(self):
        for seed in range(30):
            packet = _packet(
                [EQ_DIV_INVERSE], seed=seed, constraints={"coefficient_range": (4, 6)}
            )
            result = build_problem(packet, adapter=self.adapter)
            self.assertIn(result.structure.var_term.divisor, (4, 5, 6))


class ConstantRangeFeasibilityTests(unittest.TestCase):
    """Regression tests: a large constant_range for EQ.SUB_INVERSE must
    either always produce a valid equation, or be rejected up front -- not
    intermittently raise ProblemVerificationError from a packet that
    validate_packet() already declared acceptable."""

    def setUp(self):
        self.adapter = MathBasicEquationsAdapter()

    def test_sub_inverse_with_large_constant_range_always_succeeds(self):
        packet_kwargs = dict(constraints={"constant_range": (1000, 2000)})
        for seed in range(30):
            packet = _packet([EQ_SUB_INVERSE], seed=seed, **packet_kwargs)
            result = build_problem(packet, adapter=self.adapter)
            self.assertTrue(result.verification.passed)
            self.assertGreaterEqual(result.structure.rhs, 0)

    def test_sub_and_mul_inverse_with_large_constant_range_always_succeeds(self):
        packet_kwargs = dict(constraints={"constant_range": (500, 600)})
        for seed in range(30):
            packet = _packet([EQ_SUB_INVERSE, EQ_MUL_INVERSE], seed=seed, **packet_kwargs)
            result = build_problem(packet, adapter=self.adapter)
            self.assertTrue(result.verification.passed)
            self.assertGreaterEqual(result.structure.rhs, 0)


class ConstantRangeSignTests(unittest.TestCase):
    """Regression tests: a constant_range that could produce a negative
    constant must be rejected up front, not accepted and then either fail
    later in the independent parser or (for a mixed-sign range) only fail
    intermittently depending on seed."""

    def setUp(self):
        self.adapter = MathBasicEquationsAdapter()

    def test_negative_only_constant_range_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], constraints={"constant_range": (-5, -1)})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_mixed_sign_constant_range_rejected(self):
        packet = _packet([EQ_ADD_INVERSE], constraints={"constant_range": (-2, 5)})
        self.assertTrue(self.adapter.validate_packet(packet))

    def test_mixed_sign_constant_range_rejected_across_seeds(self):
        # Before the fix, a mixed range like this could pass validation and
        # then only fail generation/verification for some seeds -- prove
        # rejection is unconditional, not seed-dependent.
        for seed in range(10):
            packet = _packet(
                [EQ_ADD_INVERSE], seed=seed, constraints={"constant_range": (-2, 5)}
            )
            self.assertTrue(self.adapter.validate_packet(packet))

    def test_zero_lower_bound_constant_range_accepted(self):
        # 0 is a legal (if trivial) constant -- only negative bounds are
        # rejected, not zero.
        packet = _packet([EQ_ADD_INVERSE], constraints={"constant_range": (0, 5)})
        self.assertEqual(self.adapter.validate_packet(packet), [])

    def test_zero_constant_generates_a_valid_problem(self):
        for seed in range(20):
            packet = _packet(
                [EQ_ADD_INVERSE], seed=seed, constraints={"constant_range": (0, 0)}
            )
            result = build_problem(packet, adapter=self.adapter)
            self.assertTrue(result.verification.passed)
            self.assertEqual(result.structure.constant_term.value, 0)


if __name__ == "__main__":
    unittest.main()
