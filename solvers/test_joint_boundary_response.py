import unittest
from dataclasses import replace
import numpy as np
from scipy.linalg import eigvalsh
from joint_boundary_response import Coefficients, JointResponse, OFFSETS


class JointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.model = JointResponse()

    def test_native_geometry_and_reflecting_boundary(self):
        m = self.model
        self.assertEqual(len(OFFSETS), 12); self.assertEqual(len(m.sites), 13)
        self.assertEqual(len(m.neighbors[m.sites.index((0, 0, 0))]), 12)
        np.testing.assert_allclose(m.laplacian.sum(axis=1), 0)
        self.assertGreaterEqual(eigvalsh(m.laplacian)[0], -1e-12)
        for i, j in m.edges:
            self.assertIn(tuple(np.array(m.sites[j])-m.sites[i]), OFFSETS)
            self.assertAlmostEqual(np.linalg.norm(m.xyz[j]-m.xyz[i]), m.spacing)
        self.assertEqual(np.count_nonzero(m.eigenvalues == 0), 1)

    def test_lossless_unitarity_and_reciprocity(self):
        m = self.model
        points = np.r_[np.linspace(.03, 1.4, 25), np.sqrt(m.eigenvalues[1:])*1.00001]
        for frequency in points:
            s = m.scatter(frequency)["S"]
            np.testing.assert_allclose(s.conj().T @ s, np.eye(4), atol=2e-8)
            np.testing.assert_allclose(s, s.T, atol=2e-8)

    def test_damping_passivity_and_actual_ledger(self):
        rng = np.random.default_rng(17)
        for frequency in [.07, .2829, .46, .8, 1.3]:
            a = rng.normal(size=4)+1j*rng.normal(size=4)
            r = self.model.scatter(frequency, a, .02)
            self.assertGreaterEqual(r["internal_loss"], 0)
            self.assertLessEqual(r["power_out"], r["power_in"]+1e-10)
            self.assertAlmostEqual(r["ledger_residual"], 0, places=10)
            self.assertGreaterEqual(eigvalsh(np.eye(4)-r["S"].conj().T @ r["S"])[0], -1e-10)

    def test_effective_inertia_is_schur_derivative(self):
        m = self.model; effective = m.boundary_inertia()
        z = 1e-6
        numeric = -(m.mechanical_schur(z)-m.mechanical_schur(-z))/(2*z)
        np.testing.assert_allclose(numeric, effective["inertia"], rtol=2e-7, atol=2e-7)
        self.assertGreater(effective["internal_min_eigenvalue"], 0)

    def test_exact_discrete_energy_and_time_refinement(self):
        m = self.model; dt = m.stable_dt(.5)
        rng = np.random.default_rng(3)
        previous, current = rng.normal(size=(2, len(m.H)))
        initial = m.energy(previous, current, dt)
        drift = 0
        for _ in range(500):
            previous, current = current, m.advance(previous, current, dt)
            drift = max(drift, abs(m.energy(previous, current, dt)/initial-1))
        self.assertLess(drift, 1e-10)
        eigenvalue = m.eigenvalues[4]
        errors = [abs(2*np.arcsin(h*np.sqrt(eigenvalue)/2)/h-np.sqrt(eigenvalue)) for h in [dt, dt/2, dt/4]]
        self.assertLess(errors[1], errors[0]/3.9); self.assertLess(errors[2], errors[1]/3.9)
        with self.assertRaises(ValueError): m.step_metric(2/np.sqrt(m.eigenvalues.max()))

    def test_carried_tensor_matches_independent_energy_curvature(self):
        m = self.model; dt = m.stable_dt(); tensor = m.carried_tensor(4, dt)
        h = 2e-4; origin = np.zeros(3); baseline = m.cycle_energy(4, dt, origin)
        numeric = np.zeros((3, 3))
        for i in range(3):
            ei = np.eye(3)[i]*h
            numeric[i, i] = (m.cycle_energy(4, dt, ei)+m.cycle_energy(4, dt, -ei)-2*baseline)/h**2
            for j in range(i):
                ej = np.eye(3)[j]*h
                numeric[i, j] = numeric[j, i] = (m.cycle_energy(4, dt, ei+ej)-m.cycle_energy(4, dt, ei-ej)-m.cycle_energy(4, dt, -ei+ej)+m.cycle_energy(4, dt, -ei-ej))/(4*h*h)
        np.testing.assert_allclose(numeric, tensor, rtol=1e-6, atol=1e-7)

    def test_coupling_off_is_diagonal_control(self):
        off = JointResponse(coefficients=replace(Coefficients(), cross=0, phase_lock=0))
        s = off.scatter(.53)["S"]
        np.testing.assert_allclose(s-np.diag(np.diag(s)), 0, atol=1e-12)
        full = self.model.scatter(.53)["S"]
        self.assertGreater(np.max(abs(full-np.diag(np.diag(full)))), 1e-3)
        with self.assertRaises(ValueError): off.scatter(0)

    def test_exact_dark_frequency_is_not_silently_regularized(self):
        m = self.model
        for frequency in np.sqrt(m.eigenvalues[1:8]):
            try:
                r = m.scatter(frequency)
            except ValueError as exc:
                self.assertIn("singular", str(exc))
            else:
                self.assertLess(r["solve_residual"], 1e-10)
                self.assertLess(abs(r["ledger_residual"]), 1e-8)

    def test_global_energy_scale_does_not_fake_spectrum(self):
        scaled = JointResponse(coefficients=replace(Coefficients(), work_unit=4))
        np.testing.assert_allclose(scaled.eigenvalues, self.model.eigenvalues, atol=1e-12)
        np.testing.assert_allclose(scaled.boundary_inertia()["inertia"], 4*self.model.boundary_inertia()["inertia"], atol=1e-11)
        np.testing.assert_allclose(scaled.scatter(.53)["S"], self.model.scatter(.53)["S"], atol=1e-11)

    def test_geometry_refinement_is_real_3d(self):
        fine = JointResponse(spacing=.5)
        self.assertEqual(len(fine.sites), 55)
        self.assertTrue(np.any(abs(fine.xyz[:, 2]) > .1))
        self.assertTrue(np.isfinite(fine.carried_tensor(4, fine.stable_dt())).all())

    def test_invalid_constitutive_input_is_rejected(self):
        with self.assertRaises(ValueError): JointResponse(coefficients=replace(Coefficients(), cross=-1))
        with self.assertRaises(ValueError): self.model.scatter(.5, internal_damping=-1)


if __name__ == "__main__": unittest.main()
