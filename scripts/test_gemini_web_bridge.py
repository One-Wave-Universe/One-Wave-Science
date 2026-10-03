"""Unit tests for Gemini web bridge response normalization."""
from __future__ import annotations

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "One_Wave_Bench" / "hive-pipe"))

from gemini_web_bridge import textual_tool_calls  # noqa: E402


class TextualToolCallTests(unittest.TestCase):
    def test_normalizes_json_text_tool_call(self):
        calls = textual_tool_calls({
            "content": '{"tool_call":{"name":"jetson_run","arguments":{"argv":["pwd"]}}}'
        })
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["function"]["name"], "jetson_run")
        self.assertIn('"argv"', calls[0]["function"]["arguments"])

    def test_plain_text_is_not_a_tool_call(self):
        self.assertEqual(textual_tool_calls({"content": "final answer"}), [])


if __name__ == "__main__":
    unittest.main()