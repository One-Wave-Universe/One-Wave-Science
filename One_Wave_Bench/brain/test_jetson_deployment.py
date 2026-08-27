import tempfile
import unittest
from pathlib import Path

from One_Wave_Bench.brain.cli import run_smoke_test
from One_Wave_Bench.brain.command_memory import VerbalCommand
from One_Wave_Bench.brain.receipt_store import ReceiptStore, default_phrase_count


class JetsonDeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = ReceiptStore(Path(self.temp.name) / "memory.jsonl")

    def tearDown(self):
        self.temp.cleanup()

    def test_initialize_and_restart_rebuild(self):
        first = self.store.initialize()
        second = self.store.load()
        self.assertEqual(len(first.receipts), default_phrase_count())
        self.assertEqual(first.receipts, second.receipts)

    def test_teaching_is_persistent(self):
        self.store.teach("stay with me", VerbalCommand.FOLLOW)
        rebuilt = self.store.load()
        self.assertIs(rebuilt.recall("stay with me").command, VerbalCommand.FOLLOW)

    def test_non_jetson_smoke_test_exercises_logic_without_claiming_hardware(self):
        result = run_smoke_test(self.store, require_jetson=False)
        self.assertTrue(result["ready"])
        self.assertTrue(all(result["checks"]["command_checks"].values()))
        self.assertTrue(result["checks"]["field_void_quadratic_routing"])
        self.assertTrue(result["checks"]["archive_rebuilt"])
        if not result["profile"]["is_jetson"]:
            self.assertEqual(result["profile"]["expressive_device"], "CPU_FALLBACK")


if __name__ == "__main__":
    unittest.main()
