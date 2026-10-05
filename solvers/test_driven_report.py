"""Fast source-binding and declared-control checks on the retained full sweep."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent

class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.report=json.loads((ROOT/'driven_bulk_results.json').read_text())

    def test_source_binding_and_complete_controls(self):
        r=self.report
        for path,sha in r['source_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),sha,path)
        self.assertEqual(len(r['runs']),20)
        for run in r['runs']:
            self.assertEqual(run['trace'][-1]['time'],run['duration'])
            self.assertLess(run['result']['max_norm_relative_error'],1e-10)
            self.assertTrue(run['result']['centroid']['valid'])

    def test_timestep_ledger_and_direction(self):
        runs=self.report['runs']
        def get(f,dt):return next(x for x in runs if x['side']==32 and x['width']==3 and x['force_coefficient']==f and x['dt']==dt)
        errors=[get(.01,dt)['result']['max_balance_error'] for dt in [.04,.02,.01]]
        self.assertLess(errors[0],1e-8)
        self.assertLess(errors[1],errors[0]/3.5)
        self.assertLess(errors[2],errors[1]/3.5)
        baseline=get(0,.02)['result']['centroid']['displacement'][0]
        self.assertGreater(get(.01,.02)['result']['centroid']['displacement'][0]-baseline,0)
        self.assertLess(get(-.01,.02)['result']['centroid']['displacement'][0]-baseline,0)
        # Direction and convergence do not identify physical inertia or mass.

if __name__=='__main__':unittest.main()
