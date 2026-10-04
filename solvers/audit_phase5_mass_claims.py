#!/usr/bin/env python3
"""Reproduce the Phase 5 mass-input/calibration audit; no physics promotion."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy

def run():
    from quark_mass_solver import QuarkMassSpectrum, QuarkTopology, FourInteractionCalculator
    from proton_compression_simulator import EnergyBalanceSimulator
    from proton_mirror_gate_calibration import ProtonConfiguration, MirrorGateCalibration
    spectrum=QuarkMassSpectrum().compute_spectrum(lambda_scale=0.976)
    ablation={}
    for flavor in spectrum:
        topology=QuarkTopology(flavor)
        old=topology.mass_scale
        topology.mass_scale=1.0
        ablation[flavor]={'original_mass_scale_input':old,'mass_scale_control':1.0,
                          'control_output_MeV':FourInteractionCalculator(topology).quark_mass_MeV()}
    simulator=EnergyBalanceSimulator(ProtonConfiguration())
    scans=[]
    for size in [50,200,2000,20000]:
        xi,energy=simulator.find_threshold_from_energy_curve(size)
        scans.append({'grid_points':size,'xi':float(xi),'energy_GeV':float(energy),'target_GeV':125.0})
    # Any positive global multiplier leaves flavor ratios invariant.
    intervals={f:[0.9*r['PDG_mass']/r['mass_MeV'],1.1*r['PDG_mass']/r['mass_MeV']]
               for f,r in spectrum.items()}
    lower=max(v[0] for v in intervals.values());upper=min(v[1] for v in intervals.values())
    multiplier=4.0
    implemented=MirrorGateCalibration().predict_calibrated_quark_mass(1.0,multiplier)
    canonical_work_metric_scaling=multiplier
    source_dir=Path(__file__).resolve().parent
    sources={name:hashlib.sha256((source_dir/name).read_bytes()).hexdigest() for name in
             ['quark_mass_solver.py','proton_compression_simulator.py','proton_mirror_gate_calibration.py']}
    report={'scope':'code-dependency and arithmetic audit; not physical validation',
            'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
            'source_sha256':sources,'spectrum_against_legacy_in_code_targets':spectrum,
            'target_mass_scale_ablation':ablation,'threshold_grid_scan':scans,
            'global_multiplier_10_percent_intervals':intervals,
            'common_multiplier_intersection':[lower,upper],
            'common_multiplier_exists':lower<=upper,
            'work_metric_scaling_control':{'lambda':multiplier,'implemented_mass_multiplier':implemented,
                'canonical_fixed_profile_multiplier':canonical_work_metric_scaling},
            'findings':{'equal_scale_five_flavors_collapse':all(np.isclose(ablation[f]['control_output_MeV'],ablation['up']['control_output_MeV']) for f in ['strange','charm','bottom','top']),
                'no_single_multiplier_fits_legacy_targets_at_10_percent':lower>upper,
                'threshold_overshoot_shrinks_under_refinement':abs(scans[-1]['energy_GeV']-125)<abs(scans[1]['energy_GeV']-125),
                'implemented_sqrt_scaling_disagrees_with_fixed_profile_W_scaling':not np.isclose(implemented,canonical_work_metric_scaling)}}
    if not all(report['findings'].values()):
        raise RuntimeError('Audit premise changed: inspect the source and re-evaluate conclusions')
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();report=run();raw=json.dumps(report,indent=2,sort_keys=True,default=lambda value:value.item())+'\n'
    if args.output:args.output.write_text(raw)
    print(raw)
