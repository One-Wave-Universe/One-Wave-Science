"""Fixed-law FCC initial-state search with phase/velocity and retained u."""
import json
import numpy as np
from native_compression_bridge import FCC


def initial(g,kind,amplitude,relaxed=False):
    coords=np.indices(g.mask.shape).astype(float)
    coords=np.where(coords>g.side/2,coords-g.side,coords)/np.sqrt(2)
    radius=np.sqrt(np.sum(coords**2,axis=0))
    envelope=amplitude*np.exp(-.5*radius**2)*g.mask
    phase=np.zeros_like(envelope)
    if kind=='travel':phase=coords[0]
    if kind=='angular':
        phase=np.arctan2(coords[1],coords[0])
        envelope*=np.sqrt(coords[0]**2+coords[1]**2)
    psi=envelope*np.cos(phase)
    vp=envelope*np.sin(phase)
    if kind=='kick':vp=.5*envelope
    if kind=='quadrature':psi=np.zeros_like(envelope);vp=envelope
    u=g.relax(psi**2)[0] if relaxed else np.zeros(g.mask.shape+(3,))
    return psi,vp,u,np.zeros_like(u),radius


def run(kind,amplitude=.2,relaxed=False,eta=2.,side=8,dt=.02,duration=40.):
    g=FCC(side);psi,vp,u,vu,radius=initial(g,kind,amplitude,relaxed)
    e0=g.energy(psi,u,eta=eta)+.5*g.dot(vp,vp)+.5*g.dot(vu,vu)
    max_error=0.;trace=[];reference=None;best=float('inf');returns=[];complete=True
    sample_every=max(1,round(.5/dt))
    previous_error=None;previous_previous_error=None;previous_time=None
    for n in range(round(duration/dt)+1):
        t=n*dt
        if n%sample_every==0:
            if reference is None and t>=5:
                reference=tuple(v.copy() for v in (psi,vp,u,vu))
                reference_size=sum(g.dot(v,v) for v in reference)
            error=None
            if reference is not None:
                error=float(np.sqrt(sum(g.dot(v-r,v-r) for v,r in zip((psi,vp,u,vu),reference))/max(reference_size,1e-300)))
                if t>=10:
                    best=min(best,error)
                    if previous_previous_error is not None and previous_error<previous_previous_error and previous_error<=error and previous_error<=.1:
                        if not returns or previous_time-returns[-1]>=1:returns.append(previous_time)
                    previous_previous_error,previous_error,previous_time=previous_error,error,t
            activity=psi**2+vp**2;total=float(activity.sum())
            trace.append({'t':t,'localized_fraction':float(activity[radius<=2].sum()/max(total,1e-300)),
                          'return_to_time5_error':error,'peak_amplitude':float(abs(psi).max()),
                          'compression_sum':float(g.chi(u).sum()),'activity':g.volume*total})
        if n==round(duration/dt):break
        gp,gu=g.gradients(psi,u,eta=eta)
        vp-=.5*dt*gp;vu-=.5*dt*gu;psi+=dt*vp;u+=dt*vu
        gp,gu=g.gradients(psi,u,eta=eta);vp-=.5*dt*gp;vu-=.5*dt*gu
        energy=g.energy(psi,u,eta=eta)+.5*g.dot(vp,vp)+.5*g.dot(vu,vu)
        max_error=max(max_error,float(abs(energy-e0)/max(1.,abs(e0))))
        if not np.isfinite(energy) or max(abs(psi).max(),abs(u).max())>50:
            complete=False;t=(n+1)*dt;break
    late=[q['localized_fraction'] for q in trace if q['t']>=.75*duration]
    gates={'completed':complete,'energy':max_error<.005,'late_localization':bool(late) and min(late)>=.8,'two_sampled_returns':len(returns)>=2}
    return {'parameters':{'kind':kind,'amplitude':amplitude,'relaxed_u':relaxed,'eta':eta,'side':side,'sites':int(g.mask.sum()),'dt':dt,'duration':duration,'phase_or_velocity_scale':1.,'kick_scale':.5},
            'actual_end_time':t,'initial_energy':float(e0),'max_scaled_energy_error':max_error,
            'min_late_localized_fraction':min(late) if late else None,'best_reference_return_error':best if np.isfinite(best) else None,
            'sampled_return_times':returns,'gates':gates,'candidate':all(gates.values()),'trace':trace}


def vacuum_bands():
    # Fourier symbols of the unchanged FCC bond and central-divergence operators.
    resolution=64
    K=2*np.pi*np.indices((resolution,)*3)/resolution
    c=np.cos(K);s=np.sin(K)
    ell=6-2*(c[0]*c[1]+c[0]*c[2]+c[1]*c[2])
    q2=sum((s[i]*(c[(i+1)%3]+c[(i+2)%3])/np.sqrt(2))**2 for i in range(3))
    return {'grid_resolution_each_axis':resolution,'scalar_squared_frequency_max_exact':8.,
            'scalar_frequency_band':[0.,float(np.sqrt(8.))],
            'transverse_frequency_band':[0.,float(np.sqrt(ell.max()))],
            'longitudinal_max_sampled':float(np.sqrt((ell+q2).max())),
            'longitudinal_max_rigorous_upper_bound':float(np.sqrt(14.)),
            'reason_upper_bound':'L<=8 and each q component has square <=2, so |q|^2<=6',
            'radiation_condition':'Far-field harmonics in a vacuum band have propagating channels; localization then requires an actual cancellation or nonradiating mechanism. Frequency above a band alone does not prove a nonlinear localized orbit.',
            'compression_forcing':'psi^2 can drive displacement at DC and twice a single carrier frequency; compare those harmonics with longitudinal response.'}


def report():
    configs=[('standing',.2,False,2.),('kick',.2,False,2.),('quadrature',.2,False,2.),
             ('travel',.2,False,2.),('travel',.5,True,2.),('angular',.2,True,2.),('travel',.2,False,0.)]
    runs=[run(*p) for p in configs]
    eligible=[r for r in runs if r['parameters']['eta']>0 and r['gates']['completed'] and r['gates']['energy']]
    selected=max(eligible,key=lambda r:r['min_late_localized_fraction']) if eligible else None
    controls=[]
    if selected:
        p=selected['parameters']
        controls=[run(p['kind'],p['amplitude'],p['relaxed_u'],p['eta'],dt=.01),
                  run(p['kind'],p['amplitude'],p['relaxed_u'],p['eta'],side=12)]
    return {'reference':'PR193 at 7c1bd2f33f9b5ee0451b35913fd7a3607e90ba9d',
            'scope':'real scalar excitation and vector displacement under unchanged candidate law; phase labels denote initial quadratures, not topological vortices',
            'law_parameters':{'beta':1.,'shear':1.,'k':1.,'a':1.},
            'run_environment':'isolated scientific workspace; not a device-side simulation receipt',
            'runs':runs,'refinement_controls':controls,'selected':selected['parameters'] if selected else None,
            'candidate_count':sum(r['candidate'] for r in runs),
            'vacuum_band_analysis':vacuum_bands(),
            'limits':['Initial sin/cos quadratures are prescribed seeds, not a derived frequency or conserved phase charge.',
                'Angular seed is not proof of vector vorticity or vortex topology.',
                'Reference is full state at time 5; no normalization, phase alignment or recentering.',
                'Return minima are sampled every .5 and separated by at least 1; no exhaustive orbit/Floquet proof.',
                'Activity psi^2+v_psi^2 is a dimensionless diagnostic, not energy or norm conservation.',
                'No perturbation stability, translation clock ratio, particle classification or SI calibration established.']}


if __name__=='__main__':print(json.dumps(report(),indent=2))
