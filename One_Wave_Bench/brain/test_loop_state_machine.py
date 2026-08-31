import unittest

from One_Wave_Bench.brain.loop_state_machine import (
    EventReceipt,
    Lifecycle,
    LoopPhase,
    LoopStateMachine,
    Profile,
    canonical_cycle,
    parse_line,
)


class ParserTests(unittest.TestCase):
    def test_parser_is_case_and_spacing_stable(self):
        a = parse_line("  COMPRESS   Micro  ")
        b = parse_line("compress micro")
        self.assertEqual(a, b)
        self.assertEqual(a.canonical_json(), b.canonical_json())

    def test_parser_rejects_macro_expression(self):
        with self.assertRaisesRegex(ValueError, "Macro is not repeated"):
            parse_line("EXPRESS macro")

    def test_memory_value_can_be_quoted(self):
        event = parse_line('REMEMBER cue "red door"')
        self.assertEqual(event.key, "cue")
        self.assertEqual(event.value, "red door")


class LoopTests(unittest.TestCase):
    def test_complete_field_cycle(self):
        machine = LoopStateMachine()
        machine.run(canonical_cycle(Profile.FIELD))
        self.assertEqual(machine.state.profile, Profile.FIELD)
        self.assertEqual(machine.state.lifecycle, Lifecycle.IDLE)
        self.assertEqual(machine.state.phase, LoopPhase.PHASE)
        self.assertEqual(machine.state.cycle, 1)

    def test_complete_void_cycle(self):
        machine = LoopStateMachine()
        machine.run(canonical_cycle(Profile.VOID))
        self.assertEqual(machine.state.profile, Profile.VOID)
        self.assertEqual(machine.state.cycle, 1)

    def test_expression_must_reverse_compression(self):
        machine = LoopStateMachine()
        machine.run("""
        PROFILE field
        COMPRESS micro
        COMPRESS small
        COMPRESS mid
        COMPRESS large
        COMPRESS macro
        MIRROR
        RELEASE
        """)
        with self.assertRaisesRegex(ValueError, "expected large"):
            machine.apply(parse_line("EXPRESS mid"))

    def test_release_cannot_skip_mirror(self):
        machine = LoopStateMachine()
        machine.run("""
        COMPRESS micro
        COMPRESS small
        COMPRESS mid
        COMPRESS large
        COMPRESS macro
        """)
        with self.assertRaisesRegex(ValueError, "mirror turnaround"):
            machine.apply(parse_line("RELEASE"))

    def test_phase_requires_full_return(self):
        machine = LoopStateMachine()
        machine.run("""
        COMPRESS micro
        COMPRESS small
        COMPRESS mid
        COMPRESS large
        COMPRESS macro
        MIRROR
        RELEASE
        EXPRESS large
        """)
        with self.assertRaisesRegex(ValueError, "Large->Micro"):
            machine.apply(parse_line("PHASE"))

    def test_illegal_lifecycle_transition_is_rejected(self):
        machine = LoopStateMachine()
        with self.assertRaisesRegex(ValueError, "expected primed"):
            machine.apply(parse_line("STATE executing"))

    def test_profile_cannot_silently_flip(self):
        machine = LoopStateMachine()
        machine.run("PROFILE field")
        with self.assertRaisesRegex(ValueError, "cannot silently change"):
            machine.apply(parse_line("PROFILE void"))


class RebuildTests(unittest.TestCase):
    def test_receipt_rebuild_restores_exact_process_state_and_memory(self):
        machine = LoopStateMachine()
        machine.run(canonical_cycle(Profile.FIELD))
        machine.run('REMEMBER cue "partial constellation"\nREMEMBER route "2N+1"')
        serialized = [receipt.to_json() for receipt in machine.receipts]
        rebuilt = LoopStateMachine.rebuild(serialized)
        self.assertEqual(rebuilt.state.snapshot(), machine.state.snapshot())
        self.assertEqual(
            [receipt.digest for receipt in rebuilt.receipts],
            [receipt.digest for receipt in machine.receipts],
        )

    def test_corrupted_receipt_is_rejected(self):
        machine = LoopStateMachine()
        machine.run("PROFILE field\nREMEMBER cue intact")
        raw = machine.receipts[-1].to_json().replace("intact", "changed")
        with self.assertRaisesRegex(ValueError, "invalid event receipt"):
            EventReceipt.from_json(raw)

    def test_broken_chain_is_rejected(self):
        machine = LoopStateMachine()
        machine.run("PROFILE field\nREMEMBER cue intact")
        receipts = list(machine.receipts)
        second = receipts[1]
        forged = EventReceipt.create(second.sequence, second.event(), "WRONG")
        with self.assertRaisesRegex(ValueError, "chain is broken"):
            LoopStateMachine.rebuild([receipts[0], forged])


if __name__ == "__main__":
    unittest.main()
