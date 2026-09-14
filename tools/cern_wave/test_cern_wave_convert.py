#!/usr/bin/env python3

import csv
import io
import math
import unittest

from cern_wave_convert import (
    C_M_S,
    H_GEV_S,
    HC_GEV_M,
    derive_wave_view,
    iter_converted,
    pair_mass,
)


class WaveTransformTests(unittest.TestCase):
    def test_massive_fourvector(self):
        m = 0.1056583755  # muon mass scale in GeV/c^2, used only as a test fixture
        p = 4.0
        E = math.sqrt(p * p + m * m)
        w = derive_wave_view(E, p, 0.0, 0.0)
        self.assertAlmostEqual(w.p_GeV, p, places=12)
        self.assertAlmostEqual(w.mass_from_fourvector_GeV, m, places=10)
        self.assertAlmostEqual(w.frequency_Hz, E / H_GEV_S, delta=(E / H_GEV_S) * 1e-14)
        self.assertAlmostEqual(w.de_broglie_wavelength_m, HC_GEV_M / p, delta=(HC_GEV_M / p) * 1e-14)
        self.assertLess(w.beta, 1.0)
        self.assertAlmostEqual(w.group_velocity_m_s, w.beta * C_M_S, places=6)
        self.assertFalse(w.beta_gt_one_warning)

    def test_back_to_back_pair_mass(self):
        m = 0.1056583755
        p = 1.5
        E = math.sqrt(p * p + m * m)
        mass = pair_mass((E, p, 0.0, 0.0), (E, -p, 0.0, 0.0))
        self.assertAlmostEqual(mass, 2.0 * E, places=12)

    def test_paired_csv_preserves_source_and_adds_analog(self):
        text = """Run,Event,type1,E1,px1,py1,pz1,pt1,eta1,phi1,Q1,type2,E2,px2,py2,pz2,pt2,eta2,phi2,Q2,M\n1,2,G,2.1,2.0,0,0,2.0,0,0,-1,G,2.1,-2.0,0,0,2.0,0,3.14159,1,4.2\n"""
        reader = csv.DictReader(io.StringIO(text))
        rows = list(
            iter_converted(
                reader,
                source_record="fixture",
                source_url="fixture://test",
                reference_energy_GeV=2.1,
                bench_frequency_Hz=1000.0,
                max_events=None,
            )
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["source_E_GeV"], 2.1)
        self.assertEqual(rows[0]["derivation_class"], "STANDARD_DERIVED")
        self.assertEqual(rows[0]["analog_derivation_class"], "SCALED_ANALOG")
        self.assertAlmostEqual(rows[0]["analog_frequency_Hz"], 1000.0)
        self.assertAlmostEqual(rows[0]["reconstructed_pair_mass_GeV"], 4.2)
        self.assertAlmostEqual(rows[0]["pair_mass_delta_GeV"], 0.0)

    def test_rounding_warning_is_visible(self):
        w = derive_wave_view(1.0, 1.001, 0.0, 0.0, beta_tolerance=5e-4)
        self.assertTrue(w.mass2_negative_warning)
        self.assertTrue(w.beta_gt_one_warning)
        self.assertEqual(w.mass_from_fourvector_GeV, 0.0)


if __name__ == "__main__":
    unittest.main()
