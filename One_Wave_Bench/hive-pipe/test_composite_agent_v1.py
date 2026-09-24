import tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import composite_agent_v1 as cav

class FakeAgent:
    def __init__(self, replies): self.replies=list(replies)
    def call(self, role, packet): return self.replies.pop(0)

class FakeTools:
    def execute(self, action, state): return {"ok":True,"echo":action}

class CompositeLoopTests(unittest.TestCase):
    def test_full_cycle(self):
        field=FakeAgent([
            {"perception":"heard user","proposal":{"kind":"noop"},"speech_draft":"draft"},
            {"action":{"kind":"noop"},"speech":"done"},
        ])
        void=FakeAgent([
            {"decision":"ALLOW","inner_voice":"safe","permissions":{"act":True}},
            {"commit":True,"reason":"receipt matches"},
        ])
        state=cav.CompositeState(session_id="t",goal="test",reference="ref")
        loop=cav.CompositeLoop(field,void,FakeTools())
        old_state,old_ledger=cav.STATE_PATH,cav.LEDGER_PATH
        with tempfile.TemporaryDirectory() as td:
            cav.STATE_PATH=Path(td)/"state.json"; cav.LEDGER_PATH=Path(td)/"ledger.jsonl"
            out=loop.cycle_once(state,"hello")
            self.assertEqual(out.phase,"OUTPUT")
            self.assertEqual(out.output,"done")
            self.assertTrue(out.void["commit"])
            self.assertEqual(out.strikes,0)
        cav.STATE_PATH, cav.LEDGER_PATH=old_state,old_ledger

    def test_void_hold_blocks_action(self):
        field=FakeAgent([{"perception":"x","proposal":{},"speech_draft":""}])
        void=FakeAgent([{"decision":"HOLD","reason":"missing reference"}])
        state=cav.CompositeState(session_id="t")
        old_state,old_ledger=cav.STATE_PATH,cav.LEDGER_PATH
        with tempfile.TemporaryDirectory() as td:
            cav.STATE_PATH=Path(td)/"state.json"; cav.LEDGER_PATH=Path(td)/"ledger.jsonl"
            out=cav.CompositeLoop(field,void,FakeTools()).cycle_once(state,"hello")
            self.assertEqual(out.output,"missing reference")
            self.assertEqual(out.action,{})
        cav.STATE_PATH,cav.LEDGER_PATH=old_state,old_ledger

if __name__=="__main__": unittest.main()
