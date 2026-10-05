"""Finite-window recurrence search under the unchanged reciprocal FCC law."""
import json
import numpy as np
from native_compression_bridge import FCC


def run(amplitude, width=1., eta=2., side=8, dt=.02, duration=40.):
    g=FCC(side)
    coords=np.indices(g.mask.shape)
    d=np.minimum(coords,side-coords)/np.sqrt(2)
    radius=np.sqrt(np.sum(d*d,axis=0))
    psi=amplitude*np.exp(-radius**2/(2*width**2))*g.mask
    u=np.zeros(g.mask.shape+(3,));vp=np.zeros_like(psi);vu=np.zeros_like(u)
    initial=psi.copy();initial_size=g.dot(initial,initial)
    energy0=g.energy(psi,u,eta=eta)
    max_error=0.;trace=[];best=(float('inf'),None);completed=True
    def observe(t):
        activity=psi**2+vp**2
        displacement_activity=np.sum(u*u+vu*vu,axis=-1)
        total=float(activity.sum())
        frac=float(activity[radius<=2].sum()/max(total,1e-300))
        dtotal=float(displacement_activity.sum())
        dfrac=float(displacement_activity[radius<=2].sum()/dtotal) if dtotal>1e-24 else None
        error=float(np.sqrt((g.dot(psi-initial,psi-initial)+g.dot(vp,vp)+g.dot(u,u)+g.dot(vu,vu))/initial_size))
        return {'t':t,'excitation_activity_inside_radius2':frac,'displacement_activity_inside_radius2':dfrac,
                'full_state_return_error':error,'peak_amplitude':float(abs(psi).max()),
                'excitation_activity':g.volume*total,'compression_sum':float(g.chi(u).sum())}
    trace.append(observe(0.))
    stride=max(1,round(.5/dt))
    steps=round(duration/dt)
    for n in range(1,steps+1):
        gp,gu=g.gradients(psi,u,eta=eta)
        vp-=.5*dt*gp;vu-=.5*dt*gu
        psi+=dt*vp;u+=dt*vu
        gp,gu=g.gradients(psi,u,eta=eta)
        vp-=.5*dt*gp;vu-=.5*dt*gu
        e=g.energy(psi,u,eta=eta)+.5*g.dot(vp,vp)+.5*g.dot(vu,vu)
        max_error=max(max_error,float(abs(e-energy0)/max(1.,abs(energy0))))
        if not np.isfinite(e) or max(abs(psi).max(),abs(u).max())>50:
            completed=False;trace.append(observe(n*dt));break
        if n%stride==0 or n==steps:
            q=observe(n*dt);trace.append(q)
            if q['t']>=5 and q['full_state_return_error']<best[0]:best=(q['full_state_return_error'],q['t'])
    late=[q['excitation_activity_inside_radius2'] for q in trace if q['t']>=.75*duration]
    gates={'completed_window':completed,'energy_control':max_error<.005,
           'late_localization':bool(late) and min(late)>=.8,'sampled_full_state_return':best[0]<=.1}
    return {'parameters':{'amplitude':amplitude,'width':width,'eta':eta,'side':side,'active_sites':int(g.mask.sum()),'dt':dt,'requested_duration':duration,'beta':1.,'shear':1.,'k':1.,'a':1.},
            'initial_energy':float(energy0),'max_scaled_energy_error':max_error,
            'best_sampled_return_error':best[0] if np.isfinite(best[0]) else None,'best_sampled_return_time':best[1],
            'minimum_late_localized_fraction':min(late) if late else None,
            'screening_gates':gates,'candidate_found':all(gates.values()),'trace':trace}


def report():
    configurations=[(.2,1.,2.),(.5,1.,2.),(1.,1.,2.),(1.5,1.,2.),(1.,.7,2.),(1.,1.,0.)]
    runs=[]
    for amplitude,width,eta in configurations:
        runs.append(run(amplitude,width,eta))
    # Select by measured late localization among completed, energy-controlled coupled runs.
    eligible=[r for r in runs if r['parameters']['eta']>0 and r['screening_gates']['completed_window'] and r['screening_gates']['energy_control']]
    chosen=max(eligible,key=lambda r:r['minimum_late_localized_fraction']) if eligible else None
    controls=[]
    if chosen:
        p=chosen['parameters']
        controls=[run(p['amplitude'],p['width'],p['eta'],dt=.01),run(p['amplitude'],p['width'],p['eta'],side=12)]
    return {'reference':'science/native-compression-bridge-20261005 at 8e493c4f1d7d8bfba0eddd9ffc446fd31021b80b',
            'scope':'finite initial-value screen, not an exhaustive periodic-orbit solver or physical clock',
            'observable_definitions':{'activity':'psi^2+v_psi^2, a dimensionless diagnostic, not energy or conserved norm',
               'return':'full psi,v_psi,u,v_u distance to initial state; no recentering, normalization or phase alignment',
               'localization':'fixed-origin radius 2 fraction of excitation activity; displacement activity reported separately'},
            'acceptance':{'duration':40.,'late_fraction_min':.8,'sampled_return_error_max':.1,'max_scaled_energy_error':.005,'first_return_search_time':5.,'sample_interval':.5},
            'runs':runs,'chosen_for_refinement':chosen['parameters'] if chosen else None,'refinement_controls':controls,
            'growth_onset_controls':[run(1.,1.,2.,dt=dt,duration=10.) for dt in (.02,.01,.005)],
            'screened_candidates':sum(r['candidate_found'] for r in runs),
            'limits':['A Gaussian displacement-free seed family does not cover all periodic states or phase/velocity seeds.',
              'Half-unit recurrence sampling can miss short returns; screen failure is not nonexistence proof.',
              'Finite periodic boxes may reassemble dispersing waves; returns alone do not establish confinement.',
              'No translation, timing ratio, perturbation/Floquet stability, four-role necessity or physical calibration claim.',
              'No coefficients were retuned, no norm resets, and no imposed wells or trajectory constraints were used.']}


if __name__=='__main__':
    print(json.dumps(report(),indent=2))
