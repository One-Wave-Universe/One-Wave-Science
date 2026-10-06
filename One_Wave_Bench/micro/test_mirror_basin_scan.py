import math
import unittest
import numpy as np
from e4_seven_cell import Coeff
from mirror_basin_scan import energy, reduced, solve, finite_hessian

class MirrorBasins(unittest.TestCase):
    def test_exact_reduced_energy(self):
        c=Coeff(eps=0)
        mu,m=0.7,1.0
        for C,S in ((0.0,0.0),(0.3,-0.2),(-0.7,0.1)):
            x=np.zeros(13); x[:7]=1
            for k in range(6):
                t=2*math.pi*k/6
                x[k+1]+=(C*math.cos(t)+S*math.sin(t))/3
            expected=(c.bK+c.bT)/3*(C*C+S*S)+c.aM*S*S+mu*(C*C+S*S-m*m)**2
            self.assertAlmostEqual(energy(x,c,mu,m),expected,places=12)

    def test_below_threshold_collapses(self):
        c=Coeff()
        for sign in (-1,1):
            w=solve(c,0.05,1,sign)
            self.assertTrue(w["stable_physical_slice"])
            self.assertLess(abs(w["C"]),1e-5)

    def test_above_threshold_two_stable_wells(self):
        c=Coeff()
        expected=reduced(c,0.2,1)["C_abs"]
        for sign in (-1,1):
            w=solve(c,0.2,1,sign)
            self.assertTrue(w["stable_physical_slice"])
            self.assertAlmostEqual(w["C"],sign*expected,places=5)

    def test_cross_on_keeps_two_wells(self):
        c=Coeff(chi=0.05)
        a,b=[solve(c,0.2,1,s) for s in (-1,1)]
        self.assertTrue(a["stable_physical_slice"] and b["stable_physical_slice"])
        self.assertLess(a["C"],-0.1); self.assertGreater(b["C"],0.1)
        self.assertAlmostEqual(a["energy"],b["energy"],places=10)

    def test_origin_has_one_unstable_direction_above_threshold(self):
        x=np.zeros(13); x[:7]=1
        ev=np.linalg.eigvalsh(finite_hessian(lambda v:energy(v,Coeff(),0.2,1),x))
        self.assertEqual(sum(ev < -1e-5),1)

    def test_invalid_quartic_parameters(self):
        for mu,m in ((0,1),(1,0),(-1,1)):
            with self.assertRaises(ValueError): solve(Coeff(),mu,m,1)

if __name__=="__main__": unittest.main()
