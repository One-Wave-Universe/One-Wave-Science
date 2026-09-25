import unittest

import numpy as np

from six_gate_extractor import Gate, extract_six_gates


class SixGateExtractorTests(unittest.TestCase):
    def extract(self, t, x, v, e, c, h):
        return extract_six_gates(
            t, x, v, e, c, h,
            center_band=0.1,
            speed_tol=0.1,
            begin_energy_max=0.2,
            hold_energy_min=0.8,
            energy_rate_tol=0.05,
            break_rate_min=0.5,
            coherence_min=0.75,
            heat_max=0.4,
            boundary=1.5,
        )

    def test_each_measured_gate_and_unclassified_are_distinct(self):
        t = np.arange(8.0)
        x = np.array([0.0, 0.2, 0.4, 0.5, 0.8, 1.6, -0.2, -0.3])
        v = np.array([0.0, 0.3, 0.3, 0.0, 0.4, 0.5, -0.4, -0.3])
        e = np.array([0.1, 0.4, 0.9, 0.9, 1.3, 1.8, 0.5, 0.6])
        c = np.array([1.0, 0.9, 0.9, 0.9, 0.4, 0.4, 0.9, 0.9])
        h = np.array([0.0, 0.1, 0.1, 0.1, 0.8, 0.8, 0.1, 0.1])
        gates = [r.gate for r in self.extract(t, x, v, e, c, h)]
        self.assertEqual(gates[:7], [
            Gate.BEGIN,
            Gate.COHERENT_BUILD,
            Gate.COHERENT_BUILD,
            Gate.HOLD,
            Gate.UNSTABLE_BUILD,
            Gate.BREAK,
            Gate.LOOP,
        ])
        self.assertEqual(gates[7], Gate.COHERENT_BUILD)

    def test_center_crossing_without_prior_break_is_not_loop(self):
        r = self.extract(
            np.arange(3.0),
            np.array([-0.2, 0.2, 0.4]),
            np.ones(3) * 0.2,
            np.ones(3) * 0.5,
            np.ones(3),
            np.zeros(3),
        )
        self.assertNotEqual(r[1].gate, Gate.LOOP)
        self.assertTrue(r[1].center_crossing)

    def test_contradictory_or_insufficient_evidence_is_unclassified(self):
        r = self.extract(
            np.arange(2.0),
            np.array([0.5, 0.5]),
            np.array([0.3, 0.3]),
            np.array([0.5, 0.5]),
            np.ones(2),
            np.zeros(2),
        )
        self.assertEqual(r[1].gate, Gate.UNCLASSIFIED)

    def test_boundary_excursion_with_outward_motion_is_break(self):
        r = self.extract(
            np.arange(2.0),
            np.array([1.0, 1.6]),
            np.array([0.2, 0.2]),
            np.array([1.0, 1.1]),
            np.ones(2),
            np.zeros(2),
        )
        self.assertEqual(r[1].gate, Gate.BREAK)
        self.assertTrue(r[1].outward)

    def test_invalid_coherence_is_rejected(self):
        with self.assertRaises(ValueError):
            self.extract(
                np.arange(2.0), np.zeros(2), np.zeros(2), np.zeros(2),
                np.array([1.0, 1.1]), np.zeros(2),
            )


if __name__ == "__main__":
    unittest.main()
