"""Reproduce fixed-parameter nonlinear excitation and measurement controls."""
import json,platform,hashlib
from pathlib import Path
from dataclasses import replace
import numpy as np
from bulk_excitation import BulkExcitation,BulkCoefficients

def snapshot(m,f,fit):
    return {'side':m.side,'spacing':m.spacing,'sites':len(m.xyz),'box_length':m.side*m.spacing/np.sqrt(2),**fit,**m.measurements(f),'energy_terms':{k:float(v) for k,v in m.energies(f).items()}}

def run():
    m=BulkExcitation(); f,fit=m.stationary(); base=snapshot(m,f,fit)
    unif,ufit=m.stationary(width=1e6)
    domains=[]
    for side in (8,12,16):
        x=BulkExcitation(side); q,r=x.stationary(); domains.append(snapshot(x,q,r))
    meshes=[]
    for side,a in ((12,1.),(24,.5)):
        x=BulkExcitation(side,a); q,r=x.stationary(); meshes.append(snapshot(x,q,r))
    seeds=[]
    for width,shift in ((.7,(0,0,0)),(2.,(0,0,0)),(1.5,(.353553,.353553,0))):
        q,r=m.stationary(width=width,shift=shift); seeds.append({'seed_width':width,'seed_shift':shift,**snapshot(m,q,r)})
    sweep=[]
    for norm in (2.,5.,10.,20.,40.):
        q,r=m.stationary(norm=norm); sweep.append(snapshot(m,q,r))
    traces={}; rng=np.random.default_rng(20261004)
    inputs={'stationary':f.astype(complex),'phase_perturbed':f*np.exp(.02j*rng.normal(size=f.shape))}
    amplitude=f*(1+.02*rng.normal(size=f.shape)); amplitude*=np.sqrt(m.norm(f)/m.norm(amplitude)); inputs['amplitude_perturbed']=amplitude.astype(complex)
    for name,q in inputs.items():
        _,r=m.evolve(q,100.,.02,stride=250); traces[name]=r
        measured=np.array([complex(x['detector_r1']['amplitude_real'][0],x['detector_r1']['amplitude_imag'][0]) for x in r['trace']])
        times=np.array([x['time'] for x in r['trace']])
        r['detector_r1_phase_slope']=float(np.polyfit(times,np.unwrap(np.angle(measured)),1)[0])
    dtcheck=[]
    for dt in (.04,.02,.01):
        _,r=m.evolve(inputs['phase_perturbed'],10.,dt,stride=int(10/dt)); dtcheck.append({'dt':dt,**r})
    linear=BulkExcitation(coefficients=replace(BulkCoefficients(),focusing=0,saturation=0))
    _,control=linear.evolve(f,20.,.02,stride=50)
    off=BulkExcitation(coefficients=replace(BulkCoefficients(),cross=0,phase_lock=0))
    of,orun=off.stationary()
    hashes={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ('bulk_excitation.py','run_bulk_excitation.py','test_bulk_excitation.py')}
    return {'reference_head':'6fb0e2050a855afc9b09fbaa88a75a747ab49f35','evidence_class':'TESTED HYPOTHETICAL CONSTITUTIVE MODEL; not canonical memory law or measured particle spectrum',
      'dimensional_declaration':{'native':'3D FCC12','projection':'none; numeric volumetric measurements','axis_pairs':6,'directed_routes':12,'reference':'zero field; center measured at density maximum','periodic_boundary':'even Cartesian periods; no reflecting wall','history':'3D state evolution with globalphase alignment; no claimed D410 24-route gate history'},
      'coefficients':vars(m.c),'norm_input':20.,'python':platform.python_version(),'source_sha256':hashes,
      'stationary_search':'Real-amplitude branch optimization, not exhaustive complex-field minimization or vortex search',
      'base':base,'uniform_branch':snapshot(m,unif,ufit),'domain_controls':domains,'spacing_controls':meshes,'seed_and_pinning_controls':seeds,'norm_sweep':sweep,
      'evolution':traces,'timestep_controls':dtcheck,'linear_control':control,'cross_phase_off':snapshot(off,of,orun),
      'limits':['No physical norm selection or absolute units','No three-vortex/topological state constructed','First-order complex closure is not derived from the second-order core update','Periodic images and lattice pinning remain finite-grid controls','Detector sampling is not a collider forward model','No forced Mirror penetration model']}

if __name__=='__main__': print(json.dumps(run(),indent=2))
