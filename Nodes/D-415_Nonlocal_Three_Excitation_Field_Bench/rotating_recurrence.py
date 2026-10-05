"""Conservative rotating-orbit diagnostic for unchanged D-415; not a law proof."""
from dataclasses import replace, asdict
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.optimize import root
from scipy.linalg import eig
from nonlocal_field_bench import Config, make_global_kernel, global_reference, triangular_laplacian, advance, periodic_axial_distance2
from balance_audit import energy


def operator(u, cfg, kh):
    return (-cfg.wave_speed**2*triangular_laplacian(u,cfg.dx)
            +cfg.linear_response*u+cfg.nonlocal_response*(u-global_reference(u,kh)))


def orbit(cfg, omega=1.5):
    if cfg.damping != 0 or cfg.nonlinear_response <= 0:
        raise ValueError('This ansatz requires zero damping and positive quartic response')
    if cfg.n < 12:
        raise ValueError('Three separated centers require n >= 12')
    _, kh = make_global_kernel(cfg)
    impulse=np.zeros((cfg.n,cfg.n)); impulse[0,0]=1
    band=np.fft.fft2(operator(impulse,cfg,kh)).real
    if omega**2 <= band.max():
        raise ValueError('Choose frequency above the linear band')
    c=cfg.n//2-2
    centers=[(c,c),(c+4,c),(c,c+4)]
    phi=np.zeros((cfg.n,cfg.n))
    for p in centers:
        phi[p]=np.sqrt((omega**2-cfg.linear_response)/cfg.nonlinear_response)
    residuals=[]
    for coupling in np.linspace(0,1,21):
        def fun(x):
            u=x.reshape(phi.shape)
            au=cfg.linear_response*u+coupling*(operator(u,cfg,kh).real-cfg.linear_response*u)
            return (au+cfg.nonlinear_response*u**3-omega**2*u).ravel()
        result=root(fun,phi.ravel(),method='krylov',options={'fatol':1e-11,'maxiter':100})
        error=float(np.max(abs(fun(result.x))))
        if not result.success or error>1e-8:
            raise RuntimeError(f'Continuation failed at {coupling}: {error}')
        phi=result.x.reshape(phi.shape)
        residuals.append(error)
    mask=np.zeros_like(phi,dtype=bool)
    d2=periodic_axial_distance2(cfg.n)
    for p in centers:
        mask |= np.roll(d2,p,axis=(0,1))<=1
    return phi,kh,dict(omega=omega,centers=centers,band_max_frequency=float(np.sqrt(band.max())),
        stationary_relative_residual=float(np.linalg.norm(fun(phi.ravel()))/(omega**2*np.linalg.norm(phi))),
        continuation_max_absolute_residual=max(residuals),core_intensity_fraction=float(np.sum(phi[mask]**2)/np.sum(phi**2)),
        peak_amplitudes=[float(phi[p]) for p in centers])


def stability(phi,cfg,kh,omega):
    """Full real rotating-frame Jacobian, including both position and velocity."""
    size=phi.size
    eye=np.eye(size)
    a=np.column_stack([operator(eye[:,j].reshape(phi.shape),cfg,kh).real.ravel() for j in range(size)])
    lp=a-omega**2*eye+np.diag(3*cfg.nonlinear_response*phi.ravel()**2)
    lm=a-omega**2*eye+np.diag(cfg.nonlinear_response*phi.ravel()**2)
    zero=np.zeros_like(a)
    matrix=np.block([[zero,zero,eye,zero],[zero,zero,zero,eye],[-lp,zero,zero,2*omega*eye],[zero,-lm,-2*omega*eye,zero]])
    values,vectors=eig(matrix)
    k=np.argmax(values.real); val=values[k]; vec=vectors[:,k]
    return dict(max_real_growth_rate=float(val.real),imaginary_part=float(val.imag),
        eigen_relative_residual=float(np.linalg.norm(matrix@vec-val*vec)/(np.linalg.norm(matrix)*np.linalg.norm(vec))),
        status='linearly_unstable' if val.real>1e-6 else 'no_growth_resolved_on_this_grid')


def trajectory(phi,cfg,kh,omega,periods=12,perturbation=0.):
    # Initial samples from the continuous orbit, no per-step forcing or normalization.
    # Fixed deterministic real amplitude perturbation, shared between refinements.
    rng=np.random.default_rng(415)
    perturb=rng.normal(size=phi.shape)
    perturb*=perturbation*np.linalg.norm(phi)/np.linalg.norm(perturb)
    current=(phi+perturb).astype(complex)
    previous=(phi+perturb)*np.exp(-1j*omega*cfg.dt)
    initial_energy=None; max_energy_error=0.; max_error=0.
    steps=round(periods*2*np.pi/(omega*cfg.dt))
    for step in range(steps+1):
        following=advance(previous,current,cfg,kh)
        v=(following-previous)/(2*cfg.dt)
        e=energy(current,v,cfg,kh)
        if initial_energy is None: initial_energy=e
        max_energy_error=max(max_energy_error,abs(e-initial_energy)/abs(initial_energy))
        error=float(np.linalg.norm(current-phi*np.exp(1j*omega*step*cfg.dt))/np.linalg.norm(phi))
        max_error=max(max_error,error)
        previous,current=current,following
    return dict(dt=cfg.dt,duration=steps*cfg.dt,perturbation=perturbation,
        max_relative_orbit_error=max_error,final_relative_orbit_error=error,max_relative_energy_error=float(max_energy_error))


def run():
    cfg=Config(n=12,damping=0)
    omega=1.5
    phi,kh,profile=orbit(cfg,omega)
    spectrum=stability(phi,cfg,kh,omega)
    trajectories=[trajectory(phi,replace(cfg,dt=dt),kh,omega) for dt in (.04,.02,.01)]
    perturbed=[trajectory(phi,replace(cfg,dt=dt),kh,omega,perturbation=1e-4) for dt in (.02,.01)]
    domains=[]
    for n in (18,24):
        _,_,p=orbit(replace(cfg,n=n),omega)
        domains.append(dict(n=n,**p))
    checks=dict(stationary_residual=profile['stationary_relative_residual']<1e-10,
        eigenpair_residual=spectrum['eigen_relative_residual']<1e-10,
        three_localized_peaks=profile['core_intensity_fraction']>.95,
        domain_stationary_residual=all(p['stationary_relative_residual']<1e-10 for p in domains),
        energy_refines=all(trajectories[i+1]['max_relative_energy_error']<trajectories[i]['max_relative_energy_error'] for i in (0,1)))
    files=['rotating_recurrence.py','nonlocal_field_bench.py','balance_audit.py']
    return dict(status='PASS' if all(checks.values()) else 'FAIL',checks=checks,
        scope='Existence and finite-grid stability diagnostic of a supplied-frequency stationary three-peak rotating field. Not orbiting bodies, an attractor, arbitrary initial data, or a physical law.',
        config=asdict(cfg),profile=profile,stability=spectrum,unperturbed=trajectories,perturbed=perturbed,domain_profiles=domains,
        sha256={f:hashlib.sha256(Path(__file__).with_name(f).read_bytes()).hexdigest() for f in files},
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))

if __name__=='__main__':
    receipt=run()
    Path(__file__).with_name('recurrence_receipt.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    print(json.dumps(receipt,indent=2,allow_nan=False))
    raise SystemExit(0 if receipt['status']=='PASS' else 1)
