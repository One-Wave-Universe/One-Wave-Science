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

[executed on device: localhost.localdomain (bc358fe4-7a49-4f2d-b583-3f3aaa27fc71)]