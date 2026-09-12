import dataclasses
import unittest

from boundary_release_bench import Config, is_steady, simulate


class BoundaryReleaseBenchTests(unittest.TestCase):
    def test_control_reaches_steady_state_without_reversal(self):
        cfg = Config()
        result = simulate(cfg, "control")
        self.assertTrue(is_steady(cfg, result.t_s, result.t_cor, "control"))
        self.assertLessEqual(result.t_cor, result.t_s)

    def test_hypothesis_reaches_steady_state_with_reversal(self):
        cfg = Config()
        result = simulate(cfg, "hypothesis")
        self.assertTrue(is_steady(cfg, result.t_s, result.t_cor, "hypothesis"))
        self.assertGreater(result.t_cor, result.t_s)

    def test_control_never_reverses_across_conduction_strengths(self):
        # Pure conduction must not be able to fake T_cor > T_s regardless
        # of how strongly the two layers are coupled: heat conducts from
        # hot to cold, it does not invert the ordering at steady state.
        for k_cond in (0.05, 0.2, 0.8, 3.0, 10.0):
            cfg = dataclasses.replace(Config(), k_cond=k_cond)
            result = simulate(cfg, "control")
            self.assertLessEqual(
                result.t_cor, result.t_s,
                msg=f"control mode reversed at k_cond={k_cond}",
            )

    def test_release_fraction_zero_matches_control_shape(self):
        # With no release channel, "hypothesis" mode must not produce a
        # reversal either -- the release fraction is what does the work,
        # not some other hidden asymmetry in the two loss terms.
        cfg = dataclasses.replace(Config(), release_fraction=0.0)
        result = simulate(cfg, "hypothesis")
        self.assertLessEqual(result.t_cor, result.t_s)

    def test_reversal_strengthens_with_release_fraction(self):
        # Sanity check that the gap grows monotonically with how much
        # power is diverted into the release channel, rather than being
        # an artifact of one specific parameter choice.
        gaps = []
        for frac in (0.0, 0.2, 0.4, 0.6, 0.8):
            cfg = dataclasses.replace(Config(), release_fraction=frac)
            result = simulate(cfg, "hypothesis")
            gaps.append(result.t_cor - result.t_s)
        self.assertEqual(gaps, sorted(gaps))

    def test_energy_is_conserved(self):
        for mode in ("control", "hypothesis"):
            cfg = Config()
            result = simulate(cfg, mode)
            residual = result.energy_in - result.energy_out - result.energy_stored
            relative = abs(residual) / max(result.energy_in, 1e-9)
            self.assertLess(relative, 1e-6, msg=f"energy not conserved in {mode} mode")

    def test_series_stay_finite(self):
        cfg = Config()
        for mode in ("control", "hypothesis"):
            result = simulate(cfg, mode)
            for value in result.t_s_series + result.t_cor_series:
                self.assertTrue(value == value)  # not NaN
                self.assertLess(value, 1e6)


if __name__ == "__main__":
    unittest.main()
