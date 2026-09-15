import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import deepseek_web_bridge


class FakeMCP:
    def __init__(self):
        self.calls = []

    def call(self, name, arguments):
        self.calls.append((name, arguments))
        return {
            "ok": True,
            "stdout": "WEB_RELAY_TOOL_OK",
            "stderr": "",
            "exit_code": 0,
            "cwd": "/home/Scales/One-Wave-Science",
        }


class DeepSeekWebBridgeTests(unittest.TestCase):
    def test_normalize_web_base_url(self):
        self.assertEqual(
            deepseek_web_bridge._normalize_web_base_url("http://127.0.0.1:3000/"),
            "http://127.0.0.1:3000",
        )
        with self.assertRaises(ValueError):
            deepseek_web_bridge._normalize_web_base_url("   ")

    def test_load_web_key_from_configured_file(self):
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / ".api-key"
            path.write_text("local-relay-key\n", encoding="utf-8")
            with patch.dict(
                os.environ,
                {
                    "DEEPSEEK_WEB_API_KEY": "",
                    "DEEPSEEK_WEB_API_KEY_FILE": str(path),
                },
                clear=False,
            ):
                self.assertEqual(deepseek_web_bridge._load_web_key(), "local-relay-key")

    def test_agent_maps_web_tool_call_to_hive_pipe_and_returns_final_text(self):
        mcp = FakeMCP()
        requests = []

        def fake_post(url, payload, headers, timeout):
            requests.append((url, payload, headers, timeout))
            if len(requests) == 1:
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "",
                                "tool_calls": [
                                    {
                                        "id": "call-1",
                                        "type": "function",
                                        "function": {
                                            "name": "jetson_run",
                                            "arguments": json.dumps(
                                                {
                                                    "argv": ["git", "status", "--short"],
                                                    "cwd": "/home/Scales/One-Wave-Science",
                                                }
                                            ),
                                        },
                                    }
                                ],
                            }
                        }
                    ]
                }
            return {"choices": [{"message": {"content": "done"}}]}

        agent = deepseek_web_bridge.DeepSeekWebAgent(
            mcp,
            web_api_key="relay-only-key",
            base_url="http://127.0.0.1:3000",
            post_json=fake_post,
        )
        result = agent.run("check status")

        self.assertEqual(result, "done")
        self.assertEqual(
            mcp.calls,
            [
                (
                    "terminal_run",
                    {
                        "argv": ["git", "status", "--short"],
                        "cwd": "/home/Scales/One-Wave-Science",
                    },
                )
            ],
        )
        first_url, first_payload, first_headers, _ = requests[0]
        self.assertEqual(first_url, "http://127.0.0.1:3000/v1/chat/completions")
        self.assertEqual(first_headers["Authorization"], "Bearer relay-only-key")
        self.assertEqual(len(first_payload["tools"]), 3)
        self.assertNotIn("model", first_payload)
        self.assertNotIn("DEEPSEEK_API_KEY", json.dumps(first_payload))
        second_payload = requests[1][1]
        tool_messages = [m for m in second_payload["messages"] if m["role"] == "tool"]
        self.assertEqual(len(tool_messages), 1)
        self.assertIn("WEB_RELAY_TOOL_OK", tool_messages[0]["content"])

    def test_bad_tool_arguments_are_returned_to_model_as_bridge_error(self):
        mcp = FakeMCP()
        requests = []

        def fake_post(url, payload, headers, timeout):
            requests.append(payload)
            if len(requests) == 1:
                return {
                    "choices": [
                        {
                            "message": {
                                "content": "",
                                "tool_calls": [
                                    {
                                        "id": "bad-1",
                                        "type": "function",
                                        "function": {
                                            "name": "jetson_run",
                                            "arguments": "not-json",
                                        },
                                    }
                                ],
                            }
                        }
                    ]
                }
            return {"choices": [{"message": {"content": "saw failure"}}]}

        agent = deepseek_web_bridge.DeepSeekWebAgent(
            mcp,
            web_api_key="relay-only-key",
            post_json=fake_post,
        )
        self.assertEqual(agent.run("bad tool"), "saw failure")
        self.assertEqual(mcp.calls, [])
        tool_messages = [m for m in requests[1]["messages"] if m["role"] == "tool"]
        self.assertEqual(len(tool_messages), 1)
        decoded = json.loads(tool_messages[0]["content"])
        self.assertFalse(decoded["ok"])
        self.assertIn("bridge_error", decoded)


if __name__ == "__main__":
    unittest.main()
