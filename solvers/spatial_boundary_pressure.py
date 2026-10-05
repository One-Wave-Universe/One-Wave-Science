"""Computed native FCC cavity pressure and moving-metric work control.
Reflecting graph is declared, not emergent confinement; no exterior is present.
"""
import json
import itertools
import numpy as np
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
from native_compression_bridge import FCC

SIGMA=.01
J=8*np.pi*SIGMA
WR=100.
UNIT=1/np.sqrt(2)

def operators():
    sites=[p for p in itertools.product(range(-2,3),repeat=3) if sum(p)%2==0 and sum(v*v for v in p)<=2*1.01**2]
    index={p:i for i,p in enumerate(sites)};L=np.zeros((len(sites),len(sites)))
    for i,p in enumerate(sites):
        for d in FCC().offsets:
            j=index.get(tuple(np.array(p)+d))
            if j is not None and i<j:
                L[i,i]+=1;L[j,j]+=1;L[i,j]-=1;L[j,i]-=1
    incidence=np.eye(4)-np.roll(np.eye(4),1,axis=1);phase=incidence.T@incidence
    C=np.diag([1.,.8,1.2,.6])+.12*phase
    A=np.kron(L/12,C);B=np.kron(np.eye(len(sites)),.04*phase)
    return L,C,phase,A,B

L,C,PHASE,A,B=operators()
LAM=float(eigh(L,eigvals_only=True)[1])

def carrier(R,role_branch=0,spatial_eigenvalue=LAM):
    D=spatial_eigenvalue*C/(12*R*R)+.04*PHASE
    lam,V=eigh(D);w=np.sqrt(max(0,lam[role_branch])) if lam[role_branch]>1e-12 else 0.;f=V[:,role_branch]
    if w<1e-12:return 0.,0.
    derivative=-spatial_eigenvalue*(f@C@f)/(12*w*R**3)
    return float(w),float(derivative)

def average_force(R):return -J*carrier(R)[1]-8*np.pi*SIGMA*R

RSTAR=brentq(average_force,.2,3,xtol=1e-13)

def energy(y):
    n=len(A);q=y[:n];p=y[n:2*n];R=y[-2];P=y[-1]
    return .5*(p@p)/(UNIT*R**3)+.5*UNIT*(R*q@A@q+R**3*q@B@q)+P*P/(2*WR)+4*np.pi*SIGMA*R*R

def rhs(t,y):
    n=len(A);q=y[:n];p=y[n:2*n];R=y[-2];P=y[-1]
    pressure_force=1.5*(p@p)/(UNIT*R**4)-.5*UNIT*(q@A@q+3*R*R*q@B@q)
    return np.r_[p/(UNIT*R**3),-UNIT*(R*(A@q)+R**3*(B@q)),P/WR,pressure_force-8*np.pi*SIGMA*R]

def run(perturb=0,rtol=1e-9):
    R=RSTAR*(1+perturb);lam,V=eigh(A/R**2+B)
    idx=np.argmin(abs(lam-carrier(R)[0]**2));mode=V[:,idx]/np.sqrt(UNIT*R**3)
    w=np.sqrt(lam[idx]);q=np.sqrt(2*J/w)*mode;y=np.r_[q,np.zeros_like(q),R,0.]
    e0=energy(y);out=solve_ivp(rhs,(0,200),y,method='DOP853',rtol=rtol,atol=rtol*.01,max_step=.2,dense_output=True)
    errors=[abs(energy(v)-e0)/max(1,abs(e0)) for v in out.y.T]
    r=out.y[-2];lo=float(r.min());hi=float(r.max())
    return {'completed':bool(out.success),'rtol':rtol,'radius_min':lo,'radius_max':hi,'max_accepted_step_energy_error':float(max(errors)),
            'passes_radius_screen':bool(out.success and lo>.8*RSTAR and hi<1.2*RSTAR and max(errors)<1e-6),
            'trace':[{'t':float(t),'radius':float(v[-2]),'energy':float(energy(v))} for t,v in zip(np.arange(0,200.01,2),out.sol(np.arange(0,200.01,2)).T)]}

def report():
    w,dw=carrier(RSTAR);eps=1e-5
    derivative_error=abs((carrier(RSTAR+eps)[0]-carrier(RSTAR-eps)[0])/(2*eps)-dw)
    curvature=-(average_force(RSTAR+eps)-average_force(RSTAR-eps))/(2*eps)
    # Full Hamiltonian derivative with variable W(R), not fixed-mass carrier dynamics.
    rng=np.random.default_rng(317);y=rng.normal(0,.02,2*len(A)+2);y[-2]=.9
    v=rng.normal(size=y.size);e=1e-6;measured=(energy(y+e*v)-energy(y-e*v))/(2*e)
    flow=rhs(0,y);n=len(A);grad=np.r_[-flow[n:2*n],flow[:n],-flow[-1],flow[-2]]
    gradient_error=abs(measured-grad@v)
    balanced=run();precise=run(rtol=1e-11);plus=run(.1);minus=run(-.1)
    uniform=[{'role_branch':k,'omega':carrier(1,k,0)[0],'omega_radius_derivative':carrier(1,k,0)[1]} for k in range(4)]
    checks={'frequency_derivative':bool(derivative_error<1e-7),'full_moving_metric_energy_gradient':bool(gradient_error<1e-7),'positive_balance_curvature':bool(curvature>0),'all_four_radius_runs':bool(all(r['passes_radius_screen'] for r in [balanced,precise,plus,minus])),'uniform_phase_modes_zero_pressure':bool(all(v['omega_radius_derivative']==0 for v in uniform))}
    return {'scope':'Computed 13-site four-role reflecting-cavity carrier coupled to a self-similar radius; not emergent spatial Knot Lock.',
            'parameters':{'sites':len(L),'role_coordinates':4,'sigma':SIGMA,'initial_action':J,'boundary_kinetic_weight':WR,'duration':200,'spatial_coefficients':[1,.8,1.2,.6],'cross':.12,'phase_lock':.04},
            'balance':{'radius':RSTAR,'omega':w,'omega_radius_derivative':dw,'carrier_pressure':-J*dw/(4*np.pi*RSTAR**2),'surface_pressure':2*SIGMA/RSTAR,'averaged_curvature':float(curvature),'old_assumed_radius':1.,'actual_carrier_at_radius1':carrier(1)[0]},
            'checks':checks,'frequency_derivative_error':float(derivative_error),'Hamiltonian_gradient_error':float(gradient_error),'uniform_phase_controls':uniform,
            'runs':{'computed_balance':balanced,'tight_tolerance':precise,'plus10percent':plus,'minus10percent':minus},
            'limits':['Cavity carrier is computed; reflecting graph and self-similar geometry are still imposed.','Mass metric W(R)=UNIT R^3 I and stiffness H(R)=UNIT(R A+R^3 B) are declared material-coordinate hypotheses.','Full skin shape, exterior scattering, spatial circulation/reorganization and three-phase topology are not coupled here.','All numerical weights and surface coefficients are illustrative, not measured Mass Effect.']}
if __name__=='__main__':
    r=report();print(json.dumps(r,indent=2));raise SystemExit(0 if all(r['checks'].values()) else 1)
