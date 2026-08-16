import unittest

from commitment_map import CommitmentParameters, read_commitment_level
from noise_hysteresis_audit import audit_observations, monte_carlo_audit


class NoiseHysteresisAuditTests(unittest.TestCase):
    def test_public_readout_rejects_invalid_history(self):
        with self.assertRaises(ValueError):
            read_commitment_level(0.0, 1)

    def test_hysteresis_removes_small_partial_threshold_chatter(self):
        observations = (0.39, 0.41) * 20
        audit = audit_observations(observations, initial_level=2)
        self.assertEqual(audit.hysteretic_transitions, 0)
        self.assertEqual(audit.memoryless_transitions, 39)

    def test_large_excursion_still_exits_partial_state(self):
        audit = audit_observations((0.45, 0.35, 0.27), initial_level=2)
        self.assertEqual(audit.hysteretic_levels, (2, 2, 0))

    def test_seeded_monte_carlo_shows_chatter_reduction(self):
        audit = monte_carlo_audit(0.45, 0.05, initial_level=2, trials=64, samples_per_trial=256)
        self.assertGreater(audit.chatter_reduction_fraction, 0.90)

    def test_false_full_entry_grows_with_noise(self):
        quiet = monte_carlo_audit(0.70, 0.01, initial_level=2, trials=64, samples_per_trial=128)
        noisy = monte_carlo_audit(0.70, 0.08, initial_level=2, trials=64, samples_per_trial=128)
        self.assertEqual(quiet.full_entry_probability, 0.0)
        self.assertGreater(noisy.full_entry_probability, 0.5)

    def test_invalid_audit_parameters_are_rejected(self):
        with self.assertRaises(ValueError):
            monte_carlo_audit(0.0, -0.1, 0)

    def test_deterministic_seed_replays_exactly(self):
        left = monte_carlo_audit(0.45, 0.05, 2, trials=8, samples_per_trial=32, seed=4)
        right = monte_carlo_audit(0.45, 0.05, 2, trials=8, samples_per_trial=32, seed=4)
        self.assertEqual(left, right)


if __name__ == "__main__":
    unittest.main()

