#!/usr/bin/env python3

import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest import mock

import gateway
import mudl
import reference_receipt


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.ledger = root / "reference-receipts.jsonl"
        self.ledger_env = mock.patch.dict(os.environ, {
            "REFERENCE_GATE_LEDGER": str(self.ledger),
            "ONE_WAVE_PROJECT_ROOT": str(Path(__file__).resolve().parents[2]),
        })
        self.ledger_env.start()
        self.paths = mock.patch.multiple(
            mudl,
            QUEUE=root,
            PENDING=root / "pending",
            PROCESSING=root / "processing",
            RESULTS=root / "results",
            DONE=root / "done",
        )
        self.paths.start()
        mudl.ensure_dirs()
        self.server = gateway.GatewayServer(("127.0.0.1", 0), ["test-token"])
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.paths.stop()
        self.ledger_env.stop()
        self.temp.cleanup()

    def request(self, path, *, method="GET", body=None, token="test-token", headers=None):
        data = json.dumps(body).encode() if body is not None else None
        request_headers = dict(headers or {})
        if token is not None and not request_headers:
            request_headers["Authorization"] = f"Bearer {token}"
        request = Request(self.base + path, data=data, headers=request_headers, method=method)
        with urlopen(request) as response:
            return response.status, json.loads(response.read())

    def test_requires_authentication(self):
        with self.assertRaises(HTTPError) as caught:
            self.request("/v1/health", token="wrong")
        self.assertEqual(caught.exception.code, 401)

    def test_accepts_api_key_header_for_remote_mcp_clients(self):
        status, health = self.request(
            "/v1/health",
            token=None,
            headers={"X-API-Key": "test-token"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(health["status"], "ok")

    def test_accepts_api_key_authorization_scheme(self):
        status, health = self.request(
            "/v1/health",
            token=None,
            headers={"Authorization": "ApiKey test-token"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(health["status"], "ok")

    def test_health_reports_terminal_tools(self):
        status, health = self.request("/v1/health")
        self.assertEqual(status, 200)
        self.assertEqual(
            set(health["terminal_tools"]),
            {"terminal_reference", "terminal_pwd", "terminal_which", "terminal_run", "python_run", "cpp_compile_run"},
        )

    def test_enqueues_and_returns_named_action(self):
        status, queued = self.request("/v1/jobs", method="POST", body={"action": "health"})
        self.assertEqual(status, 202)
        request_path = mudl.PENDING / f'{queued["id"]}.json'
        claimed = mudl.PROCESSING / request_path.name
        request_path.replace(claimed)
        mudl.execute(claimed)
        status, result = self.request(f'/v1/jobs/{queued["id"]}')
        self.assertEqual(status, 200)
        self.assertEqual(result["action"], "health")
        self.assertEqual(result["exit_code"], 0)

    def test_rejects_raw_command_payload(self):
        with self.assertRaises(HTTPError) as caught:
            self.request("/v1/jobs", method="POST", body={"action": "health", "command": "id"})
        self.assertEqual(caught.exception.code, 400)

    def test_mcp_initialize_and_tools_list(self):
        status, initialized = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}
        })
        self.assertEqual(status, 200)
        self.assertEqual(initialized["result"]["serverInfo"]["name"], "one-wave-hive-pipe")
        self.assertEqual(initialized["result"]["serverInfo"]["version"], "3.2")
        status, listed = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
        })
        self.assertEqual(status, 200)
        tools = {tool["name"]: tool for tool in listed["result"]["tools"]}
        self.assertTrue(set(mudl.ACTIONS).issubset(tools))
        self.assertTrue({"terminal_reference", "terminal_pwd", "terminal_which", "terminal_run", "python_run", "cpp_compile_run"}.issubset(tools))
        self.assertTrue(tools["terminal_pwd"]["annotations"]["readOnlyHint"])
        self.assertFalse(tools["terminal_run"]["annotations"]["readOnlyHint"])

    def test_mcp_terminal_reference_explains_intervention_levels(self):
        status, called = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 19, "method": "tools/call",
            "params": {"name": "terminal_reference", "arguments": {}},
        })
        self.assertEqual(status, 200)
        self.assertFalse(called["result"]["isError"])
        reference = called["result"]["structuredContent"]["reference"]
        self.assertEqual(reference["contract"], "one-wave-terminal-parser-v2")
        self.assertIn("path_authorization", reference["intervention_levels"])
        carded = called["result"]["structuredContent"]
        self.assertEqual(carded["reference_card"]["goblin"], "reference")
        self.assertEqual(carded["response_card"]["goblin"], "checker")
        self.assertEqual(carded["reference_card"]["action_sha256"], carded["response_card"]["action_sha256"])

    def test_mcp_terminal_run_returns_real_output(self):
        status, called = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 20, "method": "tools/call",
            "params": {
                "name": "terminal_run",
                "arguments": {"argv": ["printf", "AI_TERMINAL_OK"], "intention": "Smoke test", "consequence": "Expect AI_TERMINAL_OK"},
            },
        })
        self.assertEqual(status, 200)
        self.assertFalse(called["result"]["isError"])
        result = called["result"]["structuredContent"]
        self.assertEqual(result["stdout"], "AI_TERMINAL_OK")
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("cwd", result)
        phases = [json.loads(line)["phase"] for line in self.ledger.read_text().splitlines()]
        self.assertEqual(phases, ["issued", "observed"])

    def test_mcp_terminal_run_accepts_perplexity_style_bash_lc(self):
        status, called = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 22, "method": "tools/call",
            "params": {
                "name": "terminal_run",
                "arguments": {"argv": ["bash", "-lc", "printf PERPLEXITY_MCP_OK"], "intention": "Smoke test shell wrapper", "consequence": "Expect PERPLEXITY_MCP_OK"},
            },
        })
        self.assertEqual(status, 200)
        self.assertFalse(called["result"]["isError"])
        result = called["result"]["structuredContent"]
        self.assertEqual(result["stdout"], "PERPLEXITY_MCP_OK")
        self.assertEqual(result["exit_code"], 0)

    def test_mcp_python_run_executes_supplied_source(self):
        status, called = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 23, "method": "tools/call",
            "params": {
                "name": "python_run",
                "arguments": {"code": "print(6 * 7)", "intention": "Smoke test Python", "consequence": "Expect 42"},
            },
        })
        self.assertEqual(status, 200)
        self.assertFalse(called["result"]["isError"])
        result = called["result"]["structuredContent"]
        self.assertEqual(result["stdout"].strip(), "42")
        self.assertEqual(result["language"], "python")
        self.assertTrue(result["temporary_source"])

    def test_mcp_cpp_compile_run_executes_supplied_source(self):
        status, called = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 24, "method": "tools/call",
            "params": {
                "name": "cpp_compile_run",
                "arguments": {
                    "code": '#include <iostream>\nint main(){std::cout << 42 << "\\n";}',
                    "standard": "c++20",
                    "intention": "Smoke test C++", "consequence": "Expect 42",
                },
            },
        })
        self.assertEqual(status, 200)
        self.assertFalse(called["result"]["isError"])
        result = called["result"]["structuredContent"]
        self.assertEqual(result["stdout"].strip(), "42")
        self.assertEqual(result["language"], "c++")
        self.assertEqual(result["phase"], "run")

    def test_mcp_terminal_which(self):
        status, called = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 21, "method": "tools/call",
            "params": {"name": "terminal_which", "arguments": {"name": "python3"}},
        })
        self.assertEqual(status, 200)
        self.assertFalse(called["result"]["isError"])
        self.assertTrue(called["result"]["structuredContent"]["path"])

    def test_missing_intention_or_consequence_holds_before_execution(self):
        for args in ({"argv": ["printf", "NEVER"]},
                     {"argv": ["printf", "NEVER"], "intention": "test"}):
            _, response = self.request("/mcp", method="POST", body={
                "jsonrpc": "2.0", "id": 72, "method": "tools/call",
                "params": {"name": "terminal_run", "arguments": args},
            })
            self.assertIn("Reference Goblin HOLD", response["error"]["message"])
        self.assertFalse(self.ledger.exists())

    def test_observed_ledger_failure_reports_uncertain_execution(self):
        original = reference_receipt.record
        def fail_observed(event):
            if event["phase"] == "observed":
                raise OSError("ledger full")
            original(event)
        with mock.patch.object(reference_receipt, "record", side_effect=fail_observed):
            _, response = self.request("/mcp", method="POST", body={
                "jsonrpc": "2.0", "id": 73, "method": "tools/call",
                "params": {"name": "terminal_run", "arguments": {
                    "argv": ["printf", "RAN_ONCE"], "intention": "Verify failure receipt",
                    "consequence": "Report uncertainty without retrying"}},
            })
        content = response["result"]["structuredContent"]
        self.assertTrue(response["result"]["isError"])
        self.assertEqual(content["stdout"], "RAN_ONCE")
        self.assertIn("may have run", content["error"])

    def test_mcp_tool_call_runs_only_named_action(self):
        def worker():
            deadline = __import__("time").monotonic() + 2
            while __import__("time").monotonic() < deadline:
                pending = list(mudl.PENDING.glob("*.json"))
                if pending:
                    claimed = mudl.PROCESSING / pending[0].name
                    pending[0].replace(claimed)
                    mudl.execute(claimed)
                    return
                __import__("time").sleep(0.01)

        thread = threading.Thread(target=worker)
        thread.start()
        status, called = self.request("/mcp", method="POST", body={
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "health", "arguments": {}},
        })
        thread.join()
        self.assertEqual(status, 200)
        self.assertFalse(called["result"]["isError"])
        self.assertEqual(called["result"]["structuredContent"]["action"], "health")

    def test_mcp_rejects_arguments_and_unknown_tools(self):
        for name, arguments in (("health", {"command": "id"}), ("shell", {})):
            status, response = self.request("/mcp", method="POST", body={
                "jsonrpc": "2.0", "id": 4, "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            })
            self.assertEqual(status, 200)
            self.assertEqual(response["error"]["code"], -32602)


if __name__ == "__main__":
    unittest.main()
