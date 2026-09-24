import json, unittest
from pathlib import Path
import lattice_body_physics as lbp

class LatticeBodyPhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest=json.loads((Path(__file__).resolve().parent/"room_manifest.json").read_text())

    def test_loaded_body_displaces_site(self):
        sim=lbp.LatticeBodySandbox(self.manifest)
        agents={"a":{"cell":"0,0","connected":True,"scale":1.0}}
        sim.step(agents,3)
        self.assertLess(sim.state["0,0"].u,0.0)
        self.assertGreater(sim.state["0,0"].pressure,0.0)

    def test_neighbor_feels_strain(self):
        sim=lbp.LatticeBodySandbox(self.manifest)
        agents={"a":{"cell":"0,0","connected":True,"scale":1.0}}
        sim.step(agents,5)
        self.assertGreater(sim.state["1,0"].strain,0.0)

    def test_body_gets_weight_signal(self):
        sim=lbp.LatticeBodySandbox(self.manifest)
        agents={"a":{"cell":"0,0","connected":True,"scale":1.0}}
        sim.step(agents,2)
        sense=sim.senses(agents)["a"]
        self.assertGreater(sense["weight_signal"],sense["mass"])

if __name__=="__main__": unittest.main()
