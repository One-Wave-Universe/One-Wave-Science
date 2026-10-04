"""Reproduce target-free joint response controls; write JSON to stdout."""
import json, platform
import numpy as np
from joint_boundary_response import JointResponse, Coefficients


def run():
    m=JointResponse(); dt=m.stable_dt(.25)
    groups=[]
    for value in np.unique(np.round(m.eigenvalues,10)):
        ids=np.where(np.abs(m.eigenvalues-value)<1e-9)[0]
        tensor=sum((m.carried_tensor(int(i),dt) for i in ids),np.zeros((3,3)))/len(ids)
        groups.append({'frequency':float(np.sqrt(max(value,0))), 'multiplicity':len(ids), 'mean_carried_tensor':tensor.tolist()})
    curves=[]; rejected=[]; unity=0.; ledger=0.; residual=0.
    for w in np.linspace(.01,2,401):
        try: r=m.scatter(float(w))
        except ValueError as e: rejected.append({'frequency':float(w),'reason':str(e)}); continue
        unity=max(unity,float(np.linalg.norm(r['S'].conj().T@r['S']-np.eye(4))))
        residual=max(residual,r['solve_residual'])
        ledger=max(ledger,abs(r['ledger_residual']))
        curves.append({'frequency':float(w),'port_power':(abs(r['output'])**2).tolist(),'determinant_phase':float(np.angle(np.linalg.det(r['S'])))})
    damp=max(abs(m.scatter(float(w),internal_damping=.07)['ledger_residual']) for w in np.linspace(.02,2,40))
    inertia=m.boundary_inertia()['inertia']; z=1e-6
    derivative=-(m.mechanical_schur(z)-m.mechanical_schur(-z))/(2*z)
    rng=np.random.default_rng(24); p=rng.normal(size=len(m.H)); q=p+dt*rng.normal(size=len(m.H)); e0=m.energy(p,q,dt); drift=0.
    for _ in range(500):
        p,q=q,m.advance(p,q,dt); drift=max(drift,abs(m.energy(p,q,dt)-e0)/e0)
    refinement=[]
    for spacing in (1.,.5,1/3):
        x=JointResponse(spacing=spacing)
        spatial=[i for i in range(len(x.eigenvalues)) if np.linalg.norm(x.mode_gradients(i))>1e-8]
        refinement.append({'spacing':spacing,'sites':len(x.sites),'first_spatial_frequency':float(np.sqrt(x.eigenvalues[spatial[0]]))})
    off=JointResponse(coefficients=Coefficients(cross=0,phase_lock=0)).scatter(.51)['S']
    scaled=JointResponse(coefficients=Coefficients(work_unit=4))
    return {'reference_head':'0f005afb9afc8ac15a1ea061c2900cf3f6b0187c','scope':'Dimensionless reflecting FCC12 cavity; candidate inputs; no self-localized particle or GeV prediction',
      'python':platform.python_version(),'coefficients':vars(m.coefficients),'sites':len(m.sites),'dt':dt,
      'spectral_groups':groups,'boundary_inertia':inertia.tolist(),
      'checks':{'unitarity_error':unity,'lossless_ledger_error':ledger,'damped_ledger_error':damp,'solve_residual':residual,'energy_relative_drift_500_steps':drift,'schur_inertia_relative_error':float(np.linalg.norm(derivative-inertia)/np.linalg.norm(inertia)), 'disconnected_offdiagonal_norm':float(np.linalg.norm(off-np.diag(np.diag(off)))),'work_scale_inertia_error':float(np.linalg.norm(scaled.boundary_inertia()['inertia']-4*inertia))},
      'mesh_refinement':refinement,'frequency_window':[.01,2.],'samples':curves,'unresolved_samples':rejected}

if __name__=='__main__': print(json.dumps(run(),indent=2))
