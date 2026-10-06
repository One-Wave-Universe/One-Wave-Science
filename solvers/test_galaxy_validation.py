"""Regression checks for bounded galaxy validation repairs."""
import contextlib
import importlib
import io
import unittest
import numpy as np
from satellite_galaxy_velocity_validator import MW_SATELLITES, SatelliteVelocityPredictor

class FixedParameterTests(unittest.TestCase):
    def test_import_is_silent(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            module = importlib.import_module('satellite_galaxy_validator_em_coherence_fixed')
            importlib.reload(module)
        self.assertEqual(stream.getvalue(), '')

    def test_ring_interface_and_frozen_predictions_survive_rename(self):
        from satellite_galaxy_validator_em_coherence_fixed import DistanceDependentPredictorWithEMCoherence
        from galaxy_external_validation import evaluate
        model = DistanceDependentPredictorWithEMCoherence()
        for satellite in MW_SATELLITES:
            result = model.predict_satellite_velocity(satellite)
            self.assertAlmostEqual(result['v_total'], result['v_local'] + result['v_wake'])
        results = evaluate()['variants']
        for result, expected in zip(results, [86.283139, 81.647035]):
            self.assertAlmostEqual(result['rms_residual_kms'], expected, places=5)
            self.assertEqual(result['discrepancy_screen'], 'FAIL')

    def test_declared_fixed_scale_is_used(self):
        from satellite_galaxy_validator_em_coherence_fixed import DistanceDependentPredictorWithEMCoherence
        model = DistanceDependentPredictorWithEMCoherence()
        self.assertEqual(model.velocity_scale_factor, 38.69)
        for satellite in MW_SATELLITES:
            result = model.predict_satellite_velocity(satellite)
            self.assertAlmostEqual(result['v_local'], np.log10(satellite.stellar_mass_solar + 1e6) / 10 * 38.69)
        self.assertEqual(SatelliteVelocityPredictor().velocity_scale_factor, 39.23)


class ExternalEvaluationTests(unittest.TestCase):
    def test_complete_frozen_cohort(self):
        from galaxy_external_validation import load_inputs
        contract, values = load_inputs()
        self.assertEqual(values.shape, (45, 3))
        np.testing.assert_array_equal(values[0], [5.25, 226.8, 1.9])
        np.testing.assert_array_equal(values[-1], [27.25, 176.9, 8.2])
        self.assertEqual(contract['cohort']['excluded_rows'], [])

    def test_uniform_bulk_motion_does_not_change_dispersion(self):
        from galaxy_external_validation import centered_dispersion
        v = np.array([-30., -10., 5., 12., 23.])
        self.assertAlmostEqual(centered_dispersion(v), centered_dispersion(v+110.))
        self.assertNotAlmostEqual(centered_dispersion(v), centered_dispersion(v+np.arange(5)*10))

    def test_input_hash_drift_rejected(self):
        import json
        import tempfile
        from pathlib import Path
        from galaxy_external_validation import CONTRACT, load_inputs
        contract = json.loads(CONTRACT.read_text())
        contract['sha256']['data/mw_dr3plus_2023.csv'] = '0'*64
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'contract.json'
            path.write_text(json.dumps(contract))
            with self.assertRaisesRegex(ValueError, 'drift'):
                load_inputs(path)

    def test_forward_model_and_units(self):
        from galaxy_external_validation import evaluate, KPC_IN_KM
        receipt = evaluate()
        self.assertFalse(receipt['model_fit_performed'])
        for result in receipt['variants']:
            self.assertEqual(result['count'], 45)
            # This exact hash-locked fixture rejects both frozen candidates.
            self.assertEqual(result['discrepancy_screen'], 'FAIL')
            self.assertGreater(result['relative_rms'], 0.1)
            for row in result['rows']:
                self.assertAlmostEqual(row['predicted_circular_speed_kms'], row['local_speed_kms'] + 110)
                expected = row['observed_circular_speed_kms']**2 / row['radius_kpc'] * 1000 / KPC_IN_KM
                self.assertAlmostEqual(row['required_radial_acceleration_m_s2']/expected, 1.)
                self.assertGreater(row['required_radial_acceleration_m_s2'], row['missing_radial_acceleration_m_s2'])

class CommandLineTests(unittest.TestCase):
    def test_legacy_report_does_not_claim_physical_confirmation(self):
        from satellite_galaxy_validator_em_coherence_fixed import main
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            main()
        output = stream.getvalue()
        self.assertIn('INVALID_COMPARISON', output)
        self.assertIn('MW In-Cascade: Mean error = 26.1%', output)
        self.assertIn('M31 In-Cascade: Mean error = 3.1%', output)
        for unsupported in ['proof that', 'Pattern confirmed', 'explains asymmetry']:
            self.assertNotIn(unsupported, output)

    def test_rejected_scientific_screen_has_nonzero_exit_and_receipt(self):
        import json
        from pathlib import Path
        import subprocess
        import sys
        import tempfile
        from galaxy_external_validation import ROOT
        with tempfile.TemporaryDirectory() as folder:
            receipt = Path(folder) / 'result.json'
            run = subprocess.run([sys.executable, str(ROOT/'galaxy_external_validation.py'),
                                  '--output', str(receipt)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1, run.stderr)
            result = json.loads(receipt.read_text())
            self.assertEqual([v['count'] for v in result['variants']], [45, 45])
            self.assertEqual([v['discrepancy_screen'] for v in result['variants']], ['FAIL', 'FAIL'])


if __name__ == '__main__':
    unittest.main()
