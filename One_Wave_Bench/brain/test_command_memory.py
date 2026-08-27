import unittest

from One_Wave_Bench.brain.command_memory import (
    COMMANDS,
    CommandMemory,
    DifferentialDirection,
    LearningReceipt,
    M4DualStateRouter,
    VerbalCommand,
    octave_ratio,
)
from One_Wave_Bench.logic_core.six_route_logic import BinaryChoice


class CommandMemoryTests(unittest.TestCase):
    def test_four_commands_use_settled_binary_ternary_routes(self):
        expected = {
            VerbalCommand.STOP: (BinaryChoice.NO, DifferentialDirection.HOLD),
            VerbalCommand.FOLLOW: (BinaryChoice.YES, DifferentialDirection.HOLD),
            VerbalCommand.HURRY_UP: (BinaryChoice.YES, DifferentialDirection.EXPRESS),
            VerbalCommand.SLOW_DOWN: (BinaryChoice.YES, DifferentialDirection.COMPRESS),
        }
        for command, pair in expected.items():
            definition = COMMANDS[command]
            self.assertEqual((definition.polarity, definition.direction), pair)
            self.assertEqual(len(definition.quadratic_views), 4)

    def test_only_locked_direction_words_are_exposed(self):
        self.assertEqual(
            {direction.name for direction in DifferentialDirection},
            {"COMPRESS", "HOLD", "EXPRESS"},
        )

    def test_exact_commands_recall_without_boltzmann_guessing(self):
        memory = CommandMemory.defaults()
        for phrase, command in (
            ("follow me", VerbalCommand.FOLLOW),
            ("hurry up", VerbalCommand.HURRY_UP),
            ("slow down", VerbalCommand.SLOW_DOWN),
            ("stop", VerbalCommand.STOP),
        ):
            recall = memory.recall(phrase)
            self.assertTrue(recall.executable)
            self.assertIs(recall.command, command)
            self.assertEqual(recall.confidence, 1.0)

    def test_taught_phrase_is_authoritative_and_rebuildable(self):
        memory = CommandMemory.defaults()
        memory.teach("come along", VerbalCommand.FOLLOW)
        lines = [receipt.to_json() for receipt in memory.receipts]
        rebuilt = CommandMemory.rebuild(lines)
        self.assertIs(rebuilt.recall("come along").command, VerbalCommand.FOLLOW)
        self.assertEqual(rebuilt.receipts, memory.receipts)

    def test_receipt_tampering_breaks_rebuild(self):
        memory = CommandMemory.defaults()
        receipt = memory.receipts[0]
        damaged = LearningReceipt(
            receipt.sequence,
            receipt.phrase,
            VerbalCommand.HURRY_UP.value,
            receipt.previous_digest,
            receipt.digest,
        )
        with self.assertRaises(ValueError):
            CommandMemory.rebuild([damaged])

    def test_phrase_identity_cannot_be_silently_retrained(self):
        memory = CommandMemory()
        memory.teach("go with me", VerbalCommand.FOLLOW)
        with self.assertRaises(ValueError):
            memory.teach("go with me", VerbalCommand.STOP)

    def test_weak_or_unrelated_cue_never_proposes_motion(self):
        memory = CommandMemory.defaults()
        recall = memory.recall("purple window")
        self.assertFalse(recall.executable)
        self.assertIsNone(recall.command)
        self.assertIn("hold", recall.reason)

    def test_harmonic_octaves_scale_around_reference(self):
        self.assertEqual(octave_ratio(COMMANDS[VerbalCommand.SLOW_DOWN].octave), 0.5)
        self.assertEqual(octave_ratio(COMMANDS[VerbalCommand.FOLLOW].octave), 1.0)
        self.assertEqual(octave_ratio(COMMANDS[VerbalCommand.HURRY_UP].octave), 2.0)

    def test_rotational_field_phases_cover_four_quadrants(self):
        quadrants = {definition.phase_quadrant for definition in COMMANDS.values()}
        self.assertEqual(quadrants, {0, 1, 2, 3})

    def test_m4_routes_through_expressive_then_compressive_state_machines(self):
        router = M4DualStateRouter(CommandMemory.defaults())
        receipt = router.route("hurry up")
        self.assertIs(receipt.expressive_after.proposed_command, VerbalCommand.HURRY_UP)
        self.assertIs(receipt.compressive_after.committed_command, VerbalCommand.HURRY_UP)
        self.assertTrue(receipt.compressive_after.permission)
        self.assertEqual(receipt.expressive_after.cycle, 1)
        self.assertEqual(receipt.compressive_after.cycle, 1)

    def test_administrator_can_hold_without_erasing_expressive_proposal(self):
        router = M4DualStateRouter(CommandMemory.defaults())
        receipt = router.route("follow me", boundary_clear=False)
        self.assertIs(receipt.expressive_after.proposed_command, VerbalCommand.FOLLOW)
        self.assertIs(receipt.compressive_after.committed_command, VerbalCommand.STOP)
        self.assertFalse(receipt.compressive_after.permission)
        self.assertIn("boundary", receipt.compressive_after.reason)

    def test_stop_bypasses_motion_permission_but_not_the_administrator(self):
        router = M4DualStateRouter(CommandMemory.defaults())
        receipt = router.route("stop", actuator_ready=False, boundary_clear=False)
        self.assertIs(receipt.expressive_after.proposed_command, VerbalCommand.STOP)
        self.assertIs(receipt.compressive_after.committed_command, VerbalCommand.STOP)
        self.assertTrue(receipt.compressive_after.permission)
        self.assertIn("Administrator", receipt.compressive_after.reason)

    def test_consequence_feedback_returns_to_compressive_state(self):
        router = M4DualStateRouter(CommandMemory.defaults())
        first = router.route("follow", consequence_error=0.25)
        second = router.route("slow down", consequence_error=0.1)
        self.assertEqual(first.compressive_after.consequence_error, 0.25)
        self.assertEqual(second.compressive_before, first.compressive_after)
        self.assertEqual(second.compressive_after.consequence_error, 0.1)

    def test_jetson_brains_keep_device_provenance(self):
        router = M4DualStateRouter(
            CommandMemory.defaults(),
            m4_device="JETSON_ACCELERATOR",
            expressive_device="JETSON_GPU",
            compressive_device="JETSON_CPU",
        )
        receipt = router.route("follow")
        self.assertEqual(receipt.expressive_after.device, "JETSON_GPU")
        self.assertEqual(receipt.compressive_after.device, "JETSON_CPU")
        self.assertEqual(receipt.m4_device, "JETSON_ACCELERATOR")


if __name__ == "__main__":
    unittest.main()
