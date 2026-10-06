"""Analytic, derivative, symmetry, failure-path and orbit checks."""
import contextlib
import io
import unittest
from unittest.mock import patch
import numpy as np
import three_body_control as control
from three_body_solver import ThreeBodyPressureField, euler_restricted_three_body, LyapunovExponent

class ControlTests(unittest.TestCase):
    def test_force_is_negative_potential_gradient(self):
        model=control.NewtonianControl((1.,2.,3.))
        r=np.array([[0.,0,0],[1.2,.2,0],[-.5,.8,.4]])
        a=model.acceleration(r)
        for i in range(3):
            for k in range(3):
                plus,minus=r.copy(),r.copy()
                plus[i,k]+=1e-5; minus[i,k]-=1e-5
                uplus=model.invariants(control.pack(plus,np.zeros((3,3))))[0]
                uminus=model.invariants(control.pack(minus,np.zeros((3,3))))[0]
                self.assertAlmostEqual(a[i,k],-(uplus-uminus)/(2e-5*model.masses[i]),places=8)
        np.testing.assert_allclose(np.sum(model.masses[:,None]*a,axis=0),0,atol=1e-14)

    def test_analytic_euler_acceleration_and_distinct_positions(self):
        s,omega=control.euler_collinear()
        r,_=control.unpack(s)
        self.assertEqual(len(np.unique(r,axis=0)),3)
        np.testing.assert_allclose(control.NewtonianControl().acceleration(r),-omega**2*r,atol=1e-15)
        np.testing.assert_array_equal(euler_restricted_three_body()[0],s)
        with self.assertRaises(ValueError): euler_restricted_three_body(2.)

    def test_three_dimensional_rotation_and_translation(self):
        model=control.NewtonianControl((1.,2.,3.))
        r=np.array([[0.,.2,.1],[1.,0.,-.2],[-.3,1.,.7]])
        q,_=np.linalg.qr(np.array([[1.,2.,3.],[-2.,3.,1.],[3.,1.,2.]]))
        np.testing.assert_allclose(model.acceleration(r@q+[5.,3.,-2.]),model.acceleration(r)@q,atol=1e-13)

    def test_reject_invalid_and_collision(self):
        for masses in [(1,0,1),(1,float('nan'),1),(1,1)]:
            with self.assertRaises(ValueError): control.NewtonianControl(masses)
        model=control.NewtonianControl()
        with self.assertRaises(ValueError): model.acceleration(np.zeros((3,3)))
        with self.assertRaises(ValueError): model.integrate(control.figure_eight(),[0,0])
        with self.assertRaises(ValueError): control.unpack(np.zeros(17))

    def test_legacy_repulsion_is_not_gravity(self):
        s,_=control.euler_collinear()
        a=ThreeBodyPressureField().equations_of_motion(s,0).reshape(3,6)[:,3:]
        self.assertLess(a[0,0],0)
        self.assertGreater(control.NewtonianControl().rhs(0,s).reshape(3,6)[0,3],0)

    def test_insufficient_lyapunov_data_is_inconclusive(self):
        s,_=control.euler_collinear()
        exponent,_,_=LyapunovExponent(ThreeBodyPressureField(),s).compute(.02,.01)
        self.assertTrue(np.isnan(exponent))

    def test_failure_exit(self):
        with patch.object(control,'validate',return_value={'status':'FAIL'}):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(control.main([]),1)

    def test_full_validation(self):
        receipt=control.validate()
        self.assertEqual(receipt['status'],'PASS',receipt['metrics'])
        self.assertTrue(all(receipt['checks'].values()))

if __name__=='__main__': unittest.main()
