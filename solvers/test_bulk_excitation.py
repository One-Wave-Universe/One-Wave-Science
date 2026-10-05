import unittest
import numpy as np
from dataclasses import replace
from bulk_excitation import BulkExcitation, BulkCoefficients

class BulkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m=BulkExcitation(8); cls.f,cls.fit=cls.m.stationary()

    def test_native_periodic_shell(self):
        m=self.m
        self.assertEqual(len(m.xyz),8**3//2)
        np.testing.assert_allclose(m.linear(np.ones((len(m.xyz),4))),0,atol=1e-14)
        self.assertEqual(len(set(map(tuple,m.xyz))),len(m.xyz))
        with self.assertRaises(ValueError): BulkExcitation(7)

    def test_complex_energy_gradient(self):
        m=self.m; rng=np.random.default_rng(23)
        f=m.seed().astype(complex)*np.exp(1j*rng.normal(size=(len(m.xyz),4)))
        d=rng.normal(size=f.shape)+1j*rng.normal(size=f.shape); d/=np.linalg.norm(d)
        h=1e-5
        numeric=(m.energy(f+h*d)-m.energy(f-h*d))/(2*h)
        analytic=2*m.volume*np.vdot(d,m.gradient(f)).real
        self.assertAlmostEqual(numeric,analytic,places=7)

    def test_stationary_excitation_and_roles(self):
        self.assertLess(self.fit['stationary_residual'],1e-6)
        self.assertLess(self.fit['mu'],0)
        self.assertGreater(self.m.measurements(self.f)['core_fraction_r2'],.9)
        self.assertTrue(all(n>0 for n in self.m.measurements(self.f)['role_norms']))
        self.assertGreater(self.m.energies(self.f)['spatial_cross'],0)
        self.assertGreater(self.m.energies(self.f)['phase_lock'],0)

    def test_norm_and_energy_time_refinement(self):
        m=self.m; rng=np.random.default_rng(4)
        f=self.f.astype(complex)*np.exp(.02j*rng.normal(size=self.f.shape))
        errors=[]
        for dt in (.04,.02,.01):
            _,r=m.evolve(f,4.,dt)
            self.assertLess(r['max_norm_relative_error'],1e-10)
            errors.append(r['max_energy_relative_error'])
        self.assertLess(errors[1],errors[0]/3.5); self.assertLess(errors[2],errors[1]/3.5)

    def test_time_reversal(self):
        f=self.f.astype(complex); f[0,0]+=.01j
        np.testing.assert_allclose(self.m.step(self.m.step(f,.02),-.02),f,atol=1e-12)

    def test_translation_is_a_lattice_symmetry(self):
        m=self.m; x=m.full(self.f)
        shifted=np.roll(x,(1,1,0),axis=(0,1,2))[m.mask]
        self.assertAlmostEqual(m.energy(shifted),m.energy(self.f),places=11)

    def test_detector_reads_without_changing_state(self):
        f=self.f.copy(); a=self.m.detector(f,1); b=self.m.detector(f,2)
        self.assertGreater(b['intensity'],a['intensity'])
        np.testing.assert_array_equal(f,self.f)
        rotated=self.m.detector(f*np.exp(.7j),1)
        self.assertAlmostEqual(rotated['intensity'],a['intensity'],places=12)

    def test_cell_volume_enters_norm(self):
        m=BulkExcitation(8,.5)
        f=np.ones((len(m.xyz),4))
        self.assertAlmostEqual(m.norm(f),m.volume*len(m.xyz)*4)
        self.assertAlmostEqual(m.norm(m.seed(norm=20)),20)

    def test_invalid_evolution_parameters(self):
        for duration,dt,stride in ((-1,-.02,1),(1,0,1),(1,.02,0),(float('nan'),.02,1)):
            with self.assertRaises(ValueError): self.m.evolve(self.f,duration,dt,stride)

    def test_unforced_linear_control(self):
        linear=BulkExcitation(8,coefficients=replace(BulkCoefficients(),focusing=0,saturation=0))
        f=linear.seed(width=.6)
        initial=linear.measurements(f)['core_fraction_r2']
        final,r=linear.evolve(f,4,.02)
        self.assertLess(linear.measurements(final)['core_fraction_r2'],initial)
        self.assertLess(r['max_energy_relative_error'],1e-10)

if __name__=='__main__': unittest.main()
