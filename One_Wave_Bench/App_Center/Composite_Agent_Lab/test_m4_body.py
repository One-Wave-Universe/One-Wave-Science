import tempfile, unittest
from pathlib import Path
import m4_body

class M4BodyTests(unittest.TestCase):
    def test_action_hysteresis_holds_then_releases(self):
        b=m4_body.M4Body()
        r=b.integrate({"drive":0.9,"friction":0.0},{"brake":0.0,"support":0.9,"contradiction":0.0})
        self.assertTrue(r["action_open"])
        b.integrate({"drive":0.2,"friction":0.0},{"brake":0.0,"support":0.2,"contradiction":0.0})
        self.assertTrue(b.action_gate.active)
        b.integrate({"drive":0.0,"friction":0.0},{"brake":0.8,"support":0.0,"contradiction":0.0})
        self.assertFalse(b.action_gate.active)

    def test_reinject_writes_memory(self):
        b=m4_body.M4Body()
        out=b.reinject({"ok":True,"evidence_strength":1.0,"expected_match":1.0})
        self.assertTrue(out["committed"])
        self.assertTrue(b.memory.successful_patterns)

if __name__=="__main__": unittest.main()
