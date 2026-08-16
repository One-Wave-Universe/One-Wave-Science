import math
import unittest

import numpy as np

from vortex_diagnostics import (
    leapfrog_invariant,
    leapfrog_step,
    line_vortex_continuum_energies,
    toroidal_core_radius,
    wrapped_winding,
)


class VortexDiagnosticsTests(unittest.TestCase):
    def test_exact_line_vortex_integrals(self):
        i1, i3, scale = line_vortex_continuum_energies(2.0)
        self.assertAlmostEqual(i1, 5.0 * math.pi**1.5)
        self.assertAlmostEqual(i3, 35.0 / 8.0 * math.pi**1.5)
        self.assertAlmostEqual(scale, math.sqrt(7.0 / 8.0))

    def test_wrapped_winding(self):
        angle = np.linspace(0.0, 2.0 * math.pi, 360, endpoint=False)
        self.assertAlmostEqual(wrapped_winding(angle), 1.0)
        self.assertAlmostEqual(wrapped_winding(-2.0 * angle), -2.0)

    def test_leapfrog_invariant_is_conserved(self):
        rng = np.random.default_rng(4)
        psi0 = rng.normal(size=(8, 8, 8)) + 1j * rng.normal(size=(8, 8, 8))
        dx, dt = 0.5, 0.005
        # Zero-velocity centered initialization.
        from vortex_diagnostics import positive_spatial_operator
        psi1 = psi0 - 0.5 * dt**2 * positive_spatial_operator(psi0, dx)
        reference = leapfrog_invariant(psi0, psi1, dx, dt)
        previous, current = psi0, psi1
        for _ in range(100):
            following = leapfrog_step(previous, current, dx, dt)
            measured = leapfrog_invariant(current, following, dx, dt)
            self.assertAlmostEqual(measured, reference, places=9)
            previous, current = current, following

    def test_annulus_search_finds_ring_not_outer_boundary(self):
        n, length, major, sigma = 64, 20.0, 3.0, 2.0
        axis = np.linspace(-length/2, length/2, n, endpoint=False)
        x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
        rho = np.sqrt(x*x + y*y)
        core_distance = np.sqrt((rho-major)**2 + z*z)
        psi = core_distance/sigma * np.exp(-core_distance**2/(2*sigma**2))
        measured = toroidal_core_radius(psi, axis, (2.0, 4.0), radial_bins=128)
        self.assertLess(abs(measured-major), 0.05)


if __name__ == "__main__":
    unittest.main()

