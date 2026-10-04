"""Algebraic proof obligations; these tests do not validate physical geometry."""
import unittest
import numpy as np
from mirror_gate_coupling import CHANNELS, operator, respond


class CouplingTests(unittest.TestCase):
    def test_random_conservation_and_reversal(self):
        rng = np.random.default_rng(20261004)
        for _ in range(40):
            raw = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
            h = (raw + raw.conj().T) / 2
            a = rng.normal(size=4) + 1j * rng.normal(size=4)
            s = operator(h, 0.73)
            np.testing.assert_allclose(s.conj().T @ s, np.eye(4), atol=1e-12)
            np.testing.assert_allclose(operator(h, -0.73) @ s @ a, a, atol=1e-12)
            self.assertAlmostEqual(respond(h, a)["ledger_residual"], 0, places=11)

    def test_uncoupled_phase_changes_without_transfer(self):
        a = np.array([1, 0, 0, 0], complex)
        b = respond(np.diag([0.4, 0.8, 0.2, 0.1]), a)["amplitudes"]
        np.testing.assert_allclose(b, [np.exp(-0.4j), 0, 0, 0], atol=1e-12)

    def test_exact_two_channel_transfer(self):
        h = np.zeros((4, 4)); h[0, 1] = h[1, 0] = np.pi / 4
        r = respond(h, [1, 0, 0, 0])
        np.testing.assert_allclose(r["amplitudes"], [2**-0.5, -1j * 2**-0.5, 0, 0], atol=1e-12)
        self.assertEqual(tuple(r["channels"]), CHANNELS)
        self.assertAlmostEqual(r["power_out"], 1)

    def test_reject_unaccounted_gain_and_invalid_inputs(self):
        for h in [np.eye(4) * 1j, np.zeros((3, 3)), np.full((4, 4), np.nan)]:
            with self.assertRaises(ValueError): operator(h)
        with self.assertRaises(ValueError): operator(np.eye(4), np.inf)
        with self.assertRaises(ValueError): respond(np.eye(4), [1, 2])


if __name__ == "__main__":
    unittest.main()
