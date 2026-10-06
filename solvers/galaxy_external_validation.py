#!/usr/bin/env python3
"""Source-locked external circular-speed evaluation; no fitting or data fallback.

A failed scientific discrepancy screen exits 1, malformed/stale input exits 2.
A successful numerical execution never means the physical model is confirmed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
import numpy as np
from galaxy_rotation_constant_inherited_velocity import GalaxyRotationConstantInherited

ROOT = Path(__file__).resolve().parent
CONTRACT = ROOT / 'data/mw_dr3plus_contract.json'
KPC_IN_KM = 3.085677581491367e16


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_inputs(contract_path=CONTRACT):
    contract = json.loads(Path(contract_path).read_text())
    for relative, expected in contract['sha256'].items():
        if sha256(ROOT / relative) != expected:
            raise ValueError(f'Source/input drift: {relative}')
    values = np.loadtxt(ROOT / 'data/mw_dr3plus_2023.csv', delimiter=',', skiprows=1)
    if values.shape != (45, 3) or not np.all(np.isfinite(values)):
        raise ValueError('Expected 45 finite radius/speed/error rows')
    if np.any(values <= 0) or not np.allclose(np.diff(values[:, 0]), 0.5):
        raise ValueError('Invalid positive ordered cohort')
    return contract, values


def centered_dispersion(velocities):
    """Population LOS dispersion after removing the system mean velocity."""
    v = np.asarray(velocities, dtype=float)
    return float(np.sqrt(np.mean((v - np.mean(v)) ** 2)))


def evaluate(contract_path=CONTRACT):
    contract, data = load_inputs(contract_path)
    radius, observed, error = data.T
    results = []
    for variant in contract['variants']:
        model = GalaxyRotationConstantInherited('Milky Way', radius, variant['velocity_scale_factor'])
        if model.v_inherited_constant != variant['mw_inherited_velocity_kms']:
            raise ValueError('Inherited velocity drift')
        prediction = model.compute_rotation_velocity()
        local = prediction['v_local']
        residual = observed - prediction['v_total']
        rms = float(np.sqrt(np.mean(residual**2)))
        relative_rms = rms / float(np.mean(observed))
        # A115/C320 necessary radial constraint, conditioned on circular balance.
        # 1 (km/s)^2/kpc = 1000/KPC_IN_KM m/s^2.
        g_required = observed**2 / radius
        g_missing = (observed**2 - local**2) / radius
        rows = [dict(radius_kpc=float(r), observed_circular_speed_kms=float(v),
                     quoted_error_kms=float(e), predicted_circular_speed_kms=float(p),
                     local_speed_kms=float(l), residual_kms=float(d),
                     required_radial_acceleration_m_s2=float(g * 1000 / KPC_IN_KM),
                     missing_radial_acceleration_m_s2=float(m * 1000 / KPC_IN_KM),
                     required_additive_speed_kms=float(v-l))
                for r,v,e,p,l,d,g,m in zip(radius,observed,error,prediction['v_total'],local,residual,g_required,g_missing)]
        results.append(dict(name=variant['name'], parameters=variant, rows=rows,
                            count=len(rows), excluded_rows=[], rms_residual_kms=rms,
                            relative_rms=relative_rms,
                            mean_absolute_percentage_error=float(np.mean(np.abs(residual)/observed)*100),
                            diagonal_chi_squared=float(np.sum((residual/error)**2)),
                            chi_squared_interpretation='Diagnostic only: no full covariance, no p-value or detection significance',
                            discrepancy_screen='PASS' if relative_rms <= contract['diagnostic_screen']['relative_rms_max'] else 'FAIL',
                            interpretation='External evaluation of this fixed candidate only; not a full One-Wave theory test'))
    velocities = [-30., -10., 5., 12., 23.]
    return dict(schema_version=1, source=contract['source'], observable=contract['observable'],
                independence=contract['independence'], assumptions=contract['assumptions'],
                hashes={'contract':sha256(contract_path), 'runner':sha256(__file__), **contract['sha256']},
                runtime={'python':platform.python_version(), 'numpy':np.__version__},
                model_fit_performed=False, variants=results,
                boost_control={'velocities_kms':velocities,'uniform_boost_kms':110.,
                               'dispersion_before_kms':centered_dispersion(velocities),
                               'dispersion_after_kms':centered_dispersion(np.array(velocities)+110),
                               'scope':'A common bulk velocity cancels from internal dispersion. A spatially varying wake is not tested by this identity.'},
                inverse_constraint={'equation':'alpha_g * (K_L grad chi)_R = v_c^2/R',
                                    'sign':'outward radial gradient component on left; inward acceleration magnitude on right',
                                    'units':'m/s^2',
                                    'status':'Necessary empirical requirement under circular balance, not a prediction or a source derivation',
                                    'unknowns':['source J_source','alpha_g and constitutive coefficients','K_L from independent magnetic observations','boundary/initial conditions','physical length/time calibration','stellar tracer distribution and projection']})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'galaxy_external_validation_receipt.json')
    args = parser.parse_args()
    try:
        receipt = evaluate()
    except (ValueError, OSError, KeyError) as error:
        print(f'INVALID: {error}', file=sys.stderr)
        return 2
    args.output.write_text(json.dumps(receipt, indent=2, allow_nan=False)+'\n')
    for result in receipt['variants']:
        print(f"{result['name']}: {result['discrepancy_screen']}; N={result['count']}, RMS={result['rms_residual_kms']:.6f} km/s, relative RMS={result['relative_rms']:.6%}")
    return int(any(x['discrepancy_screen']=='FAIL' for x in receipt['variants']))

if __name__ == '__main__':
    raise SystemExit(main())
