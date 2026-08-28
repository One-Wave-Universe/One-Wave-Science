import tempfile
import unittest
from pathlib import Path

from One_Wave_Bench.brain.command_memory import VerbalCommand
from One_Wave_Bench.brain.cli import memory_health
from One_Wave_Bench.brain.conversation_loop import ConversationLoop, SystemSpeaker
from One_Wave_Bench.brain.receipt_store import ReceiptStore


class RecordingSpeaker(SystemSpeaker):
    def __init__(self):
        super().__init__(enabled=False)
        self.messages = []

    def say(self, text):
        self.messages.append(text)


class ConversationLoopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = ReceiptStore(Path(self.temp.name) / "memory.jsonl")
        self.speaker = RecordingSpeaker()
        self.loop = ConversationLoop(self.store, self.speaker)

    def tearDown(self):
        self.temp.cleanup()

    def test_known_command_may_respond(self):
        self.assertTrue(self.loop.process("follow"))
        self.assertEqual(self.speaker.messages, ["follow"])

    def test_unknown_cue_is_heard_without_question_or_response(self):
        self.loop.process("come scoot with me")
        self.assertEqual(self.loop.state.unresolved_cue, "come scoot with me")
        self.assertEqual(self.speaker.messages, [])

    def test_repeated_temporal_relation_is_learned_without_question(self):
        for _ in range(2):
            self.loop.process("come scoot with me")
            self.loop.process("follow")
        self.assertIs(self.store.load().recall("come scoot with me").command, VerbalCommand.FOLLOW)
        self.assertEqual(self.loop.state.teachings, 1)

    def test_unchanged_relation_can_remain_silent(self):
        self.loop.process("follow")
        self.loop.process("follow")
        self.assertEqual(self.speaker.messages, ["follow"])
        self.assertEqual(self.loop.state.silent_cycles, 1)

    def test_never_mode_hears_and_learns_without_speaking(self):
        loop = ConversationLoop(self.store, self.speaker, responses="never")
        loop.process("follow")
        loop.process("stop")
        loop.process("quiet unknown")
        self.assertEqual(self.speaker.messages, [])
        self.assertEqual(loop.state.cycles, 3)

    def test_stop_repeats_in_changes_mode(self):
        self.loop.process("stop")
        self.loop.process("stop")
        self.assertEqual(self.speaker.messages, ["stop", "stop"])

    def test_quit_preserves_archive_and_never_mode_stays_silent(self):
        before = self.store.initialize().receipts
        loop = ConversationLoop(self.store, self.speaker, responses="never")
        self.assertFalse(loop.process("quit"))
        self.assertEqual(self.store.load().receipts, before)
        self.assertEqual(self.speaker.messages, [])

    def test_memory_health_exposes_silent_activity(self):
        loop = ConversationLoop(self.store, self.speaker, responses="never")
        loop.process("unfamiliar sound")
        loop.process("follow")
        health = memory_health(self.store)
        self.assertTrue(health["healthy"])
        self.assertTrue(health["receipt_chain_valid"])
        self.assertEqual(health["heard_records"], 2)
        self.assertEqual(health["association_records"], 1)
        self.assertEqual(health["experience_records"], 3)
        self.assertGreater(health["archive_bytes"], 0)


if __name__ == "__main__":
    unittest.main()
