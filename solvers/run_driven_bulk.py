"""Reproduce bounded force/energy controls. No physical mass fit or target input."""
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path
import numpy as np
from bulk_excitation import BulkExcitation, BulkCoefficients
from driven_bulk import DrivenBulk, prepare_linear_packet
from joint_boundary_response import OFFSETS
ROOT=Path(__file__).resolve().parent
SOURCE_HASHES={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['bulk_excitation.py','joint_boundary_response.py','driven_bulk.py','run_driven_bulk.py']}


def run(side,width,force,dt=.02,duration=2.):
    print(f'control side={side} width={width} force={force} dt={dt}',file=sys.stderr,flush=True)
    m=BulkExcitation(side,coefficients=replace(BulkCoefficients(),focusing=0,saturation=0))
    field,leak=prepare_linear_packet(m,1.,width)
    d=DrivenBulk(m,field);d.set_force(field,[force,0,0]);trace=[]
    for step in range(round(duration/dt)+1):
        if step % max(1,round(.5/dt))==0 or step==round(duration/dt):
            r=d.measurements(field)
            trace.append({'time':step*dt,'centroid':r['centroid'],'applied_force':r['applied_force'],
                          'total_energy':r['total_energy'],'energy_balance_residual':r['energy_balance_residual']})
        if step<round(duration/dt):field=d.advance(field,dt)
    result=d.measurements(field)
    # Batch protocol is a single declared switch at t=0; full density receipts
    # are provided by interactive exports. Keep the sweep report bounded.
    result['protocol_events']=[{k:v for k,v in event.items() if k!='density'} for event in result['protocol_events']]
    print('endpoint '+json.dumps({'side':side,'width':width,'f':force,'dt':dt,'displacement':result['centroid']['displacement'],'max_energy_error':result['max_balance_error']}),file=sys.stderr,flush=True)
    return {'side':side,'width':width,'force_coefficient':force,'dt':dt,'duration':duration,
            'initial_projection_leakage':leak,'trace':trace,'result':result,
            'final_field_sha256':hashlib.sha256(field.tobytes()).hexdigest()}


def curvature():
    m=BulkExcitation(8,coefficients=replace(BulkCoefficients(),focusing=0,saturation=0))
    offsets=np.array(OFFSETS)/np.sqrt(2)
    def e(q):return np.linalg.eigvalsh(np.sum(1-np.cos(offsets@q))*m.C/12+m.c.phase_lock*m.R)[0]
    results=[]
    for h in [.02,.01,.005]:
        diag=[(e(np.eye(3)[j]*h)+e(-np.eye(3)[j]*h)-2*e(np.zeros(3)))/h**2 for j in range(3)]
        results.append({'dq':h,'diagonal':diag,'max_error_from_analytic_0_3':float(np.max(abs(np.array(diag)-.3)))})
    return results


def main():
    runs=[]
    for dt in [.04,.02,.01]:
        for f in [0,.01,-.01]:runs.append(run(32,3,f,dt))
    for f in [.005,-.005]:runs.append(run(32,3,f))
    for side,width in [(48,3),(48,4.5),(64,6)]:
        for f in [0,.01,-.01]:runs.append(run(side,width,f))
    if any(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h for p,h in SOURCE_HASHES.items()):
        raise RuntimeError('Source changed while batch was running; report rejected')
    report={'scope':'Dimensionless driven linear constitutive control; no measured/fitted physical mass',
            'analytic_long_wavelength_curvature':.3,'curvature_controls':curvature(),
            'centroid_policy':{'minimum_concentration':.5,'maximum_seam_fraction':.01,
                               'maximum_internal_step_fraction_of_box':.25,
                               'resolved_motion_requires':'branch uncertainty and timestep spread each <10% displacement'},
            'source_sha256':SOURCE_HASHES,
            'runs':runs}
    # Preserve every finite packet result. No threshold is tuned to force 0.3.
    print(json.dumps(report,indent=2,allow_nan=False))

if __name__=='__main__':main()
