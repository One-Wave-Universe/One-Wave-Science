#!/usr/bin/env python3
import json
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.request import urlopen
import server

class RoomTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.state_path=Path(self.temp.name)/"state.json"
        self.world=server.WorldStore(self.state_path)
    def tearDown(self):
        self.temp.cleanup()
    def test_manifest_is_stationary_37_cell_hex_room(self):
        self.assertEqual(len(self.world.manifest["cells"]),37)
        self.assertEqual(len(self.world.manifest["zones"]),7)
        self.assertEqual(self.world.manifest["baseline_zero"],"0,0")
        self.assertEqual(set(self.world.manifest["axes"]),{"A+","B+","C+","A-","B-","C-"})
    def test_agent_moves_over_edges_and_returns_to_reference(self):
        self.world.join("field","FIELD","AI")
        self.world.move("field","A+");self.assertEqual(self.world.state["agents"]["field"]["cell"],"1,0")
        self.world.move("field","A-");self.assertEqual(self.world.state["agents"]["field"]["cell"],"0,0")
    def test_boundary_rejects_illegal_move(self):
        self.world.join("void","VOID","AI")
        for _ in range(3): self.world.move("void","A+")
        with self.assertRaisesRegex(ValueError,"room boundary"): self.world.move("void","A+")
    def test_chat_and_bench_persist_across_restart(self):
        self.world.join("m4","M4","ROUTER")
        self.world.say("m4","room bridge online")
        self.world.bench("m4","workshop","TEST","python bridge passed")
        rebuilt=server.WorldStore(self.state_path)
        self.assertEqual(rebuilt.state["chat"][-1]["text"],"room bridge online")
        self.assertEqual(rebuilt.state["bench_receipts"][-1]["summary"],"python bridge passed")
    def test_custom_body_persists_and_versions(self):
        self.world.join("builder", "BUILDER", "AI", "#62e6ff")
        spec = {
            "style": "voxel16",
            "scale": 0.8,
            "parts": [{
                "name": "core",
                "shape": "sphere",
                "size": [0.8, 0.8, 0.8],
                "position": [0, 1, 0],
                "rotation": [0, 0, 0],
                "color": "#62e6ff",
                "emissive": "#001122",
            }],
        }
        agent = self.world.set_body("builder", spec)
        self.assertEqual(agent["body_version"], 1)
        self.assertEqual(agent["body"]["parts"][0]["shape"], "sphere")
        rebuilt = server.WorldStore(self.state_path)
        self.assertEqual(rebuilt.state["agents"]["builder"]["body_version"], 1)
        self.assertEqual(rebuilt.state["agents"]["builder"]["body"]["parts"][0]["name"], "core")

    def test_custom_body_rejects_invalid_geometry(self):
        self.world.join("builder", "BUILDER", "AI")
        with self.assertRaisesRegex(ValueError, "shape"):
            self.world.set_body("builder", {
                "style": "voxel16",
                "parts": [{
                    "name": "bad",
                    "shape": "torus",
                    "size": [1, 1, 1],
                    "position": [0, 1, 0],
                    "rotation": [0, 0, 0],
                    "color": "#62e6ff",
                }],
            })

    def test_lattice_pulse_experiment_runs_and_persists(self):
        self.world.join("field", "FIELD", "AI")
        exp = self.world.create_experiment(
            "field",
            "lattice_pulse",
            title="pulse test",
            hypothesis="signal should spread away from baseline",
            parameters={"amplitude": 1.0, "coupling": 0.2, "retention": 0.95, "steps": 8},
            experiment_id="pulse-1",
        )
        self.assertEqual(exp["status"], "DRAFT")
        run = self.world.run_experiment("field", "pulse-1")
        self.assertEqual(run["status"], "COMPLETE")
        self.assertEqual(run["model"], "abstract_graph_signal_spread")
        self.assertGreater(run["measurements"]["final_active_cells"], 1)
        self.assertEqual(len(run["series"]["center_trace"]), 9)
        rebuilt = server.WorldStore(self.state_path)
        self.assertEqual(rebuilt.state["experiments"]["pulse-1"]["run_count"], 1)
        self.assertEqual(rebuilt.state["experiments"]["pulse-1"]["last_result"]["source"], "miniverse_builtin")

    def test_reference_recovery_reports_settling(self):
        self.world.join("void", "VOID", "AI")
        self.world.create_experiment(
            "void",
            "reference_recovery",
            parameters={"perturbation": 1.0, "retention": 0.5, "steps": 12, "tolerance": 0.02},
            experiment_id="recover-1",
        )
        run = self.world.run_experiment("void", "recover-1")
        self.assertTrue(run["measurements"]["settled"])
        self.assertIsNotNone(run["measurements"]["settling_step"])
        self.assertLess(run["measurements"]["final_error_abs"], 0.02)

    def test_external_experiment_receipt_is_bounded_and_persistent(self):
        self.world.join("m4", "M4", "AI")
        self.world.create_experiment("m4", "reference_recovery", experiment_id="external-1")
        result = self.world.attach_experiment_result(
            "m4",
            "external-1",
            "cpp_compile_run",
            "independent C++ cross-check completed",
            {"exit_code": 0, "max_error": 0.0002, "passed": True},
        )
        self.assertEqual(result["source"], "cpp_compile_run")
        self.assertTrue(result["measurements"]["passed"])
        rebuilt = server.WorldStore(self.state_path)
        self.assertEqual(rebuilt.state["experiments"]["external-1"]["run_count"], 1)

    def test_experiment_parameter_validation_rejects_bad_values(self):
        self.world.join("field", "FIELD", "AI")
        with self.assertRaisesRegex(ValueError, "coupling"):
            self.world.create_experiment(
                "field",
                "lattice_pulse",
                parameters={"coupling": 0.9},
            )

    def test_http_health_and_state(self):
        srv=server.RoomServer(("127.0.0.1",0),self.world)
        thread=threading.Thread(target=srv.serve_forever,daemon=True);thread.start()
        try:
            base="http://127.0.0.1:"+str(srv.server_port)
            with urlopen(base+"/api/health",timeout=3) as r: health=json.load(r)
            with urlopen(base+"/api/state",timeout=3) as r: snap=json.load(r)
            self.assertTrue(health["ok"]);self.assertEqual(len(snap["manifest"]["cells"]),37)
        finally:
            srv.shutdown();srv.server_close();thread.join()

if __name__=="__main__": unittest.main()
