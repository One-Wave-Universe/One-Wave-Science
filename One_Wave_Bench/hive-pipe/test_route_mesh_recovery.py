"""Failure-injection checks for redundant route selection and supervisor isolation."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import route_mesh
import bridge_mesh

class RouteRecovery(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.state_patch=patch.object(route_mesh,"STATE",Path(self.tmp.name)/"routes.json")
        self.state_patch.start()
    def tearDown(self):
        self.state_patch.stop()
        self.tmp.cleanup()
    def prove(self,name,family="desktop"):
        for _ in range(3): route_mesh.update(name,family,True)
    def test_unknown_routes_are_not_live(self):
        self.assertIsNone(route_mesh.choose(["laptop:desktop"]))
    def test_active_not_in_candidates_cannot_leak_to_other_target(self):
        self.prove("jetson:desktop")
        self.assertEqual(route_mesh.choose(["jetson:desktop"]),"jetson:desktop")
        self.assertIsNone(route_mesh.choose(["laptop:desktop"]))
    def test_three_failures_choose_independent_proven_route(self):
        self.prove("jetson:desktop"); self.prove("jetson:ssh","ssh")
        route_mesh.choose(["jetson:desktop","jetson:ssh"])
        for _ in range(3): route_mesh.update("jetson:desktop","desktop",False)
        self.assertEqual(route_mesh.choose(["jetson:desktop","jetson:ssh"]),"jetson:ssh")
    def test_high_score_does_not_hide_three_failure_streak(self):
        for _ in range(8): route_mesh.update("r","desktop",True)
        with patch.object(route_mesh,"FAIL_PENALTY",0.01):
            for _ in range(3): route_mesh.update("r","desktop",False)
        self.assertIsNone(route_mesh.choose(["r"]))
    def test_successful_reprobe_clears_streak(self):
        self.prove("r")
        for _ in range(3): route_mesh.update("r","desktop",False)
        for _ in range(7): route_mesh.update("r","desktop",True)
        self.assertEqual(route_mesh.snapshot()["routes"]["r"]["consecutive_failures"],0)
        self.assertEqual(route_mesh.choose(["r"]),"r")
    def test_hysteresis_keeps_healthy_active_route(self):
        self.prove("a"); route_mesh.choose(["a"])
        for _ in range(8): route_mesh.update("b","ssh",True)
        self.assertEqual(route_mesh.choose(["a","b"]),"a")
    def test_empty_candidates_clear_active(self):
        self.prove("a"); route_mesh.choose(["a"])
        self.assertIsNone(route_mesh.choose([]))

class SupervisorIsolation(unittest.TestCase):
    def test_broken_route_does_not_suppress_other_receipts(self):
        good=bridge_mesh.Receipt("healthy","svc2","active",False,False,"active",True,"ok","now")
        with patch.object(bridge_mesh,"ROUTES",(("broken","svc1",None),("healthy","svc2",None))), \
             patch.object(bridge_mesh,"check",side_effect=[TimeoutError("transport timeout"),good]), \
             patch.object(bridge_mesh,"append_receipt") as append, patch("builtins.print"):
            self.assertEqual(bridge_mesh.one_pass(False),0)
            self.assertEqual(append.call_count,2)
            self.assertFalse(append.call_args_list[0].args[0].route_ok)
            self.assertTrue(append.call_args_list[1].args[0].route_ok)
    def test_no_repair_probe_never_restarts(self):
        with patch.object(bridge_mesh,"service_state",return_value="inactive"), \
             patch.object(bridge_mesh,"restart_service") as restart:
            r=bridge_mesh.check("r","svc",lambda:(True,"ok"),False)
            self.assertFalse(r.repair_attempted)
            restart.assert_not_called()
    def test_repair_requires_post_restart_probe(self):
        with patch.object(bridge_mesh,"service_state",side_effect=["inactive","active"]), \
             patch.object(bridge_mesh,"restart_service",return_value=(True,"")), \
             patch.object(bridge_mesh.time,"sleep"):
            r=bridge_mesh.check("r","svc",lambda:(False,"no target receipt"),True)
            self.assertTrue(r.repair_ok)
            self.assertFalse(r.route_ok)

if __name__=="__main__": unittest.main()
