#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import chatgpt_terminal_pull as bridge
import terminal_parser


class FakeClock:
    def __init__(self):
        self.value = 100.0

    def __call__(self):
        return self.value


class TerminalBridgeV2Tests(unittest.TestCase):
    def test_routes_are_ordered_and_deduplicated(self):
        routes = bridge.parse_routes("primary=origin:one,again=origin:one,backup=mirror:two")
        self.assertEqual([r.key for r in routes], ["origin:one", "mirror:two"])

    def test_transport_quarantines_then_reopens_failed_route(self):
        with tempfile.TemporaryDirectory() as td:
            store = bridge.StateStore(Path(td) / "state.json")
            routes = bridge.parse_routes("primary=origin:one,backup=origin:two")
            clock = FakeClock()
            transport = bridge.TransportStateMachine(routes, store, clock=clock)
            transport.failure(routes[0], "network is unreachable")
            self.assertEqual([r.key for r in transport.ordered()], ["origin:two"])
            self.assertEqual(transport.health(routes[0])["guidance"]["code"], "TRANSPORT_ROUTE_FAILOVER_ACTIVE")
            clock.value += 6
            self.assertIn(routes[0], transport.ordered())

    def test_executing_request_recovers_without_repeating_command(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            store = bridge.StateStore(root / "state.json")
            store.data["requests"] = {
                "dangerous-once": {
                    "phase": "executing",
                    "digest": "abc",
                    "request_commit": "123",
                    "source_route": "origin:one",
                }
            }
            store.save()
            route = bridge.parse_routes("primary=origin:one")[0]
            transport = bridge.TransportStateMachine([route], store)
            machine = bridge.RequestStateMachine(store, transport)
            with mock.patch.object(bridge, "OUTBOX_DIR", root / "outbox"):
                machine.recover()
                result = bridge.load_result("dangerous-once")
            self.assertEqual(store.data["requests"]["dangerous-once"]["phase"], "completed")
            self.assertEqual(result["execution_state"], "uncertain_after_restart")
            self.assertTrue(result["guidance"]["higher_level_required"])

    def test_parser_reference_explains_operation_and_intervention(self):
        reference = terminal_parser.reference()
        self.assertEqual(reference["contract"], terminal_parser.PARSER_CONTRACT)
        self.assertIn("path_authorization", reference["intervention_levels"])
        guidance = terminal_parser.explain_failure(error="cwd is not a directory: /work/new")
        self.assertEqual(guidance["code"], "PATH_CREATION_OR_CORRECTION_REQUIRED")
        self.assertTrue(guidance["higher_level_required"])

    def test_result_delivery_uses_alternate_back_route(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            store = bridge.StateStore(root / "state.json")
            routes = bridge.parse_routes("primary=origin:one,backup=origin:two")
            transport = bridge.TransportStateMachine(routes, store)
            machine = bridge.RequestStateMachine(store, transport)
            store.data["requests"] = {
                "route-test": {"phase": "completed", "source_route": routes[0].key}
            }
            store.save()
            with mock.patch.object(bridge, "OUTBOX_DIR", root / "outbox"):
                bridge.write_result({"id": "route-test", "ok": True})
                with mock.patch.object(
                    bridge, "publish_result", side_effect=[RuntimeError("primary down"), None]
                ) as publish:
                    self.assertTrue(machine.deliver("route-test", routes[0]))
            self.assertEqual(publish.call_count, 2)
            self.assertEqual(store.data["requests"]["route-test"]["delivered_route"], routes[1].key)

    def test_shell_wrapper_cannot_hide_blocked_program(self):
        with self.assertRaisesRegex(ValueError, "program is disabled"):
            terminal_parser._validate_argv(["bash", "-lc", "printf ok; sudo true"])

    def test_unique_request_digest_is_stable(self):
        raw = json.dumps({"id": "x", "argv": ["printf", "ok"], "cwd": str(Path.home()), "timeout": 30,
                          "intention": "Verify pull execution", "consequence": "Expect ok and exit zero"})
        first = bridge.validate_request(raw)
        second = bridge.validate_request(raw)
        self.assertEqual(first["digest"], second["digest"])


if __name__ == "__main__":
    unittest.main()
