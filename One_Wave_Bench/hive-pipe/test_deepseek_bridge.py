#!/usr/bin/env python3

import json
import unittest

import deepseek_bridge


class FakeMCP:
    def __init__(self):
        self.calls = []

    def call(self, name, arguments):
        self.calls.append((name, arguments))
        return {"ok": True, "name": name, "arguments": arguments}


class DeepSeekBridgeTests(unittest.TestCase):
    def test_mcp_url_normalization(self):
        self.assertEqual(
            deepseek_bridge._normalize_mcp_url("https://example.test"),
            "https://example.test/mcp",
        )
        self.assertEqual(
            deepseek_bridge._normalize_mcp_url("https://example.test/mcp/"),
            "https://example.test/mcp",
        )

    def test_hive_pipe_uses_json_rpc_tools_call(self):
        seen = {}

        def fake_post(url, payload, headers, timeout):
            seen.update(url=url, payload=payload, headers=headers, timeout=timeout)
            return {
                "jsonrpc": "2.0",
                "id": payload["id"],
                "result": {
                    "isError": False,
                    "structuredContent": {"ok": True, "stdout": "BRIDGE_OK"},
                },
            }

        client = deepseek_bridge.HivePipeClient(
            url="http://127.0.0.1:8765/mcp",
            token="test-token",
            post_json=fake_post,
        )
        result = client.call("terminal_run", {"argv": ["printf", "BRIDGE_OK"], "intention": "Smoke test", "consequence": "Expect BRIDGE_OK"})
        self.assertEqual(result["stdout"], "BRIDGE_OK")
        self.assertEqual(seen["payload"]["method"], "tools/call")
        self.assertEqual(
            seen["payload"]["params"],
            {
                "name": "terminal_run",
                "arguments": {"argv": ["printf", "BRIDGE_OK"], "intention": "Smoke test", "consequence": "Expect BRIDGE_OK"},
            },
        )
        self.assertEqual(seen["headers"]["Authorization"], "Bearer test-token")

    def test_only_three_terminal_functions_are_exposed(self):
        names = {tool["function"]["name"] for tool in deepseek_bridge.DEEPSEEK_TOOLS}
        self.assertEqual(names, {"jetson_pwd", "jetson_which", "jetson_run"})

    def test_dispatch_maps_deepseek_to_hive_pipe_names(self):
        mcp = FakeMCP()
        result = deepseek_bridge.dispatch_tool(
            mcp,
            "jetson_run",
            {"argv": ["git", "status", "--short"], "timeout": 30, "intention": "Inspect status", "consequence": "Read status without editing"},
        )
        self.assertTrue(result["ok"])
        self.assertEqual(
            mcp.calls,
            [
                (
                    "terminal_run",
                    {"argv": ["git", "status", "--short"], "timeout": 30, "intention": "Inspect status", "consequence": "Read status without editing"},
                )
            ],
        )

    def test_rejects_unknown_tool_and_bad_arguments(self):
        mcp = FakeMCP()
        with self.assertRaises(ValueError):
            deepseek_bridge.dispatch_tool(mcp, "anything_else", {})
        with self.assertRaises(ValueError):
            deepseek_bridge.dispatch_tool(mcp, "jetson_run", {"argv": "git status"})
        with self.assertRaises(ValueError):
            deepseek_bridge.dispatch_tool(
                mcp,
                "jetson_run",
                {"argv": ["git", "status"], "timeout": 999},
            )

    def test_agent_preserves_reasoning_content_across_tool_rounds(self):
        mcp = FakeMCP()
        requests = []

        def fake_post(url, payload, headers, timeout):
            requests.append(payload)
            if len(requests) == 1:
                return {
                    "choices": [
                        {
                            "message": {
                                "role": "assistant",
                                "content": "",
                                "reasoning_content": "I need repo status.",
                                "tool_calls": [
                                    {
                                        "id": "call_1",
                                        "type": "function",
                                        "function": {
                                            "name": "jetson_run",
                                            "arguments": json.dumps(
                                                {"argv": ["git", "status", "--short"], "intention": "Inspect status", "consequence": "Read status without editing"}
                                            ),
                                        },
                                    }
                                ],
                            }
                        }
                    ]
                }
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Repo checked.",
                            "reasoning_content": "The tool returned successfully.",
                            "tool_calls": None,
                        }
                    }
                ]
            }

        agent = deepseek_bridge.DeepSeekAgent(
            mcp,
            api_key="deepseek-test-key",
            post_json=fake_post,
        )
        answer = agent.run("Check repo status.")
        self.assertEqual(answer, "Repo checked.")
        self.assertEqual(len(requests), 2)
        second_messages = requests[1]["messages"]
        assistant_turn = next(
            item
            for item in second_messages
            if item.get("role") == "assistant" and item.get("tool_calls")
        )
        self.assertEqual(assistant_turn["reasoning_content"], "I need repo status.")
        tool_turn = next(item for item in second_messages if item.get("role") == "tool")
        self.assertEqual(tool_turn["tool_call_id"], "call_1")
        self.assertEqual(mcp.calls[0][0], "terminal_run")


if __name__ == "__main__":
    unittest.main()
