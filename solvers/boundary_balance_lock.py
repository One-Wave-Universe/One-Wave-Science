"""Reduced 3D pressure/tension radius lock, not a native FCC knot derivation.
A freely moving radius couples reciprocally to one cavity recurrence coordinate.
The assumed cavity frequency is Omega(R)=frequency_radius/R.
"""
import json
import numpy as np

SIGMA=.01
FREQUENCY_RADIUS=1.
BOUNDARY_KINETIC_WEIGHT=100.
J=8*np.pi*SIGMA/FREQUENCY_RADIUS

def energy(q,p,R,P,sigma=SIGMA):
    return .5*p*p+.5*(FREQUENCY_RADIUS*q/R)**2+P*P/(2*BOUNDARY_KINETIC_WEIGHT)+4*np.pi*sigma*R*R

def gradient(q,R,sigma):
    return FREQUENCY_RADIUS**2*q/R**2,8*np.pi*sigma*R-FREQUENCY_RADIUS**2*q*q/R**3

def run(sigma=SIGMA,action=J,radius_perturbation=0,dt=.01,time=200):
    R=1+radius_perturbation;P=0.;omega=FREQUENCY_RADIUS/R
    q=np.sqrt(2*action/omega);p=0.;initial=energy(q,p,R,P,sigma)
    lo=R;hi=R;err=0.;trace=[];complete=True;averages=[]
    for step in range(round(time/dt)+1):
        if step:
            gq,gR=gradient(q,R,sigma);p-=.5*dt*gq;P-=.5*dt*gR
            q+=dt*p;R+=dt*P/BOUNDARY_KINETIC_WEIGHT
            if R<=.05 or R>5:complete=False;break
            gq,gR=gradient(q,R,sigma);p-=.5*dt*gq;P-=.5*dt*gR
        lo=min(lo,R);hi=max(hi,R);e=energy(q,p,R,P,sigma);err=max(err,abs(e-initial)/max(1,abs(initial)))
        wave=.5*p*p+.5*(FREQUENCY_RADIUS*q/R)**2
        wave_pressure=FREQUENCY_RADIUS**2*q*q/(4*np.pi*R**5)
        tension_pressure=2*sigma/R
        if step*dt>=.5*time:averages.append([R,wave_pressure,tension_pressure])
        if step%round(2/dt)==0:trace.append({'t':float(step*dt),'radius':float(R),'wave_coordinate':float(q),'wave_energy':float(wave),'wave_action':float(wave/(FREQUENCY_RADIUS/R)),'wave_pressure':float(wave_pressure),'tension_pressure':float(tension_pressure)})
    mean=np.mean(averages,axis=0).tolist() if averages else None
    return {'completed':complete,'dt':dt,'end_time':float(step*dt),'radius_min':float(lo),'radius_max':float(hi),'max_scaled_energy_error':float(err),'late_mean_radius_pressure_tension':mean,
            'passes_radius_lock_screen':bool(complete and lo>.8 and hi<1.2 and err<1e-4),'trace':trace}

def report():
    Rstar=(J*FREQUENCY_RADIUS/(8*np.pi*SIGMA))**(1/3)
    curvature=24*np.pi*SIGMA
    # Instantaneous reciprocal force validation, not averaged equations in evolution.
    q,R=.6,1.1;eps=1e-6;gq,gR=gradient(q,R,SIGMA)
    fq=(energy(q+eps,.2,R,.1)-energy(q-eps,.2,R,.1))/(2*eps)
    fR=(energy(q,.2,R+eps,.1)-energy(q,.2,R-eps,.1))/(2*eps)
    runs={'balanced_radius':run(),'half_timestep':run(dt=.005),'radius_plus_10percent':run(radius_perturbation=.1),'radius_minus_10percent':run(radius_perturbation=-.1),'no_tension':run(sigma=0),'no_recurrence':run(action=0)}
    checks={'instantaneous_energy_gradient':bool(max(abs(fq-gq),abs(fR-gR))<1e-8),'positive_averaged_curvature':bool(curvature>0),'balanced_radius_numerical_lock':runs['balanced_radius']['passes_radius_lock_screen'],'both_radius_perturbations_lock':bool(runs['radius_plus_10percent']['passes_radius_lock_screen'] and runs['radius_minus_10percent']['passes_radius_lock_screen']),'both_ablations_lose_lock':bool(not runs['no_tension']['passes_radius_lock_screen'] and not runs['no_recurrence']['passes_radius_lock_screen'])}
    return {'scope':'Reduced moving-surface pressure/recurrence balance; assumed one-carrier cavity reduction, not spatial confinement proof.',
      'parameters':{'sigma':SIGMA,'frequency_radius':FREQUENCY_RADIUS,'boundary_kinetic_weight':BOUNDARY_KINETIC_WEIGHT,'initial_wave_action':J,'duration':200},
      'balance':{'radius':Rstar,'wave_pressure':J*FREQUENCY_RADIUS/(4*np.pi*Rstar**4),'tension_pressure':2*SIGMA/Rstar,'averaged_energy_curvature':curvature,'small_radial_frequency':float(np.sqrt(curvature/BOUNDARY_KINETIC_WEIGHT))},
      'checks':checks,'energy_gradient_error':float(max(abs(fq-gq),abs(fR-gR))),'runs':runs,
      'limits':['Action J is used for the averaged prediction and initial condition only; it is not reset or constrained during dynamics.','Frequency inverse radius is a declared mode-reduction assumption; carrier confinement is not derived.','Surface coefficient and boundary kinetic weight are illustrative, not measured Mass Effect.','No spatial FCC field, phase-locking three-vortex knot, shell or Mirror response in this reduced calculation.','Radius lock does not imply full-state or phase lock.','No penetration force; radius is a moving boundary coordinate with reciprocal pressure-work.']}
if __name__=='__main__':
    r=report();print(json.dumps(r,indent=2));raise SystemExit(0 if all(r['checks'].values()) else 1)
