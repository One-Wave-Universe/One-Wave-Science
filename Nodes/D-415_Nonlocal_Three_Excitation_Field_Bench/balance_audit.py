"""Energy and charge audit of the unchanged D-415 candidate, not a new law."""
import hashlib
import json
from dataclasses import replace
from pathlib import Path
import platform
import numpy as np
from nonlocal_field_bench import Config, advance, global_reference, make_global_kernel, seed_three_excitations, triangular_laplacian


def force(u, cfg, kh):
    return (cfg.wave_speed**2*triangular_laplacian(u,cfg.dx)
            -cfg.linear_response*u-cfg.nonlinear_response*abs(u)**2*u
            -cfg.nonlocal_response*(u-global_reference(u,kh)))


def energy(u,v,cfg,kh):
    """Real two-component convention; area per triangular-lattice site included."""
    area=np.sqrt(3)*cfg.dx**2/2
    return area*dict_sum(dict(kinetic=.5*np.vdot(v,v).real,
        gradient=-.5*cfg.wave_speed**2*np.vdot(u,triangular_laplacian(u,cfg.dx)).real,
        linear=.5*cfg.linear_response*np.sum(abs(u)**2),
        nonlinear=.25*cfg.nonlinear_response*np.sum(abs(u)**4),
        nonlocal_term=.5*cfg.nonlocal_response*np.vdot(u,u-global_reference(u,kh)).real))


def dict_sum(values):
    return float(sum(values.values()))


def charge(u,v,cfg):
    return float(np.sqrt(3)*cfg.dx**2/2*np.vdot(u,v).imag)


def trajectory(cfg,duration=4.8):
    _,kh=make_global_kernel(cfg)
    prev,u,_=seed_three_excitations(cfg)
    v=(u-prev)/cfg.dt
    # Same physical initial u,v across dt; second-order Taylor start for the audit.
    # The production seed's first-order prior state remains unchanged.
    prev=u-cfg.dt*v+.5*cfg.dt**2*(force(u,cfg,kh)-cfg.damping*v)
    e=[]; power=[]; q=[]
    steps=round(duration/cfg.dt)
    for _ in range(steps+1):
        nxt=advance(prev,u,cfg,kh)
        centered_v=(nxt-prev)/(2*cfg.dt)
        e.append(energy(u,centered_v,cfg,kh))
        power.append(cfg.damping*np.sqrt(3)*cfg.dx**2/2*np.vdot(centered_v,centered_v).real)
        # Staggered charge obeys Q_next=(1-gamma*dt) Q_now exactly in this recurrence.
        q.append(charge(prev,(u-prev)/cfg.dt,cfg))
        prev,u=u,nxt
    heat=cfg.dt*np.sum((np.array(power[:-1])+power[1:])/2)
    expected=np.array(q[0])*(1-cfg.damping*cfg.dt)**np.arange(steps+1)
    return dict(dt=cfg.dt,duration=steps*cfg.dt,initial_energy=e[0],final_energy=e[-1],
        dissipated_energy=float(heat),relative_ledger_residual=float(abs(e[-1]-e[0]+heat)/e[0]),
        max_charge_recurrence_error=float(np.max(abs(np.array(q)-expected))))


def audit():
    cfg=Config(n=24)
    kernel,kh=make_global_kernel(cfg)
    rng=np.random.default_rng(415)
    u=.3*(rng.normal(size=(24,24))+1j*rng.normal(size=(24,24)))
    h=rng.normal(size=u.shape)+1j*rng.normal(size=u.shape)
    area=np.sqrt(3)*cfg.dx**2/2
    eps=1e-6
    observed=(energy(u+eps*h,np.zeros_like(u),cfg,kh)-energy(u-eps*h,np.zeros_like(u),cfg,kh))/(2*eps)
    expected=-area*np.vdot(h,force(u,cfg,kh)).real
    derivative_error=abs(observed-expected)/max(1,abs(expected))
    idx=(-np.arange(cfg.n))%cfg.n
    symmetry_error=float(np.max(abs(kernel-kernel[np.ix_(idx,idx)])))
    nonlocal_min=float(np.min(1-kh.real))
    rows=[trajectory(replace(cfg,dt=dt)) for dt in (.08,.04,.02,.01)]
    ratios=[rows[i]['relative_ledger_residual']/rows[i+1]['relative_ledger_residual'] for i in range(3)]
    conservative=trajectory(replace(cfg,damping=0,dt=.01))
    checks=dict(force_is_negative_energy_gradient=derivative_error<1e-7,
        kernel_is_even=symmetry_error<1e-14,nonlocal_quadratic_is_psd=nonlocal_min>-1e-12,
        damped_ledger_refines=min(ratios)>1.5,
        refined_ledger_small=rows[-1]['relative_ledger_residual']<1e-3,
        charge_recurrence=max(x['max_charge_recurrence_error'] for x in rows)<1e-9,
        undamped_charge=conservative['max_charge_recurrence_error']<1e-9,
        undamped_energy_error=conservative['relative_ledger_residual']<1e-4)
    checks={k:bool(v) for k,v in checks.items()}
    return dict(status='PASS' if all(checks.values()) else 'FAIL',checks=checks,
        scope='Exact energy functional and continuum-time dissipation identity for the existing periodic 2D candidate; no persistent-mode or physical-law validation.',
        derivative_error=float(derivative_error),kernel_symmetry_error=symmetry_error,
        minimum_nonlocal_quadratic_eigenvalue=nonlocal_min,refinement=rows,
        ledger_error_reduction=ratios,undamped=conservative,
        parameters=dict(n=cfg.n,dx=cfg.dx,wave_speed=cfg.wave_speed,alpha=cfg.linear_response,
        beta=cfg.nonlinear_response,kappa=cfg.nonlocal_response,gamma=cfg.damping,kernel_length=cfg.kernel_length),
        environment=dict(python=platform.python_version(),numpy=np.__version__),
        sha256={p:hashlib.sha256(Path(__file__).with_name(p).read_bytes()).hexdigest() for p in ['balance_audit.py','nonlocal_field_bench.py']})


if __name__=='__main__':
    result=audit()
    Path(__file__).with_name('balance_receipt.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2,allow_nan=False))
    raise SystemExit(0 if result['status']=='PASS' else 1)
