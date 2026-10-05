"""Domain lift and harmonic refinement of a nonzero native FCC recurrence.
No new potential or coefficients. Even-time Fourier sector remains restricted.
"""
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.optimize import least_squares
from native_compression_bridge import FCC
from periodic_orbit_solve import Orbit, integrate

class RefinedOrbit:
    def __init__(self,side=4,psi_h=(1,3,5),u_h=(0,2,4,6)):
        self.g=FCC(side);self.n=int(self.g.mask.sum());n=self.n
        self.psi_h=list(psi_h);self.u_h=list(u_h);self.np=len(psi_h)
        self.h=np.array(list(psi_h)+list(u_h)*3);self.nh=len(self.h)
        self.component=np.array([0]*self.np+sum(([k+1]*len(u_h) for k in range(3)),[]))
        self.samples=64;self.angles=2*np.pi*np.arange(self.samples)/self.samples
        self.B=np.zeros((self.samples,4,self.nh))
        for j,(h,f) in enumerate(zip(self.h,self.component)):self.B[:,f,j]=np.cos(h*self.angles)
        self.P=self.B/self.samples
        self.P*=np.where(self.h==0,1,2)[None,None,:]
        self.L=np.zeros((n,n));self.G=np.zeros((3,n,n))
        for i in range(n):
            q=np.zeros(self.g.mask.shape);q[self.g.mask]=np.eye(n)[i]
            self.L[:,i]=self.g.lap(q)[self.g.mask]
            self.G[:,:,i]=self.g.grad(q)[self.g.mask].T
        self.C=np.concatenate([self.G[k].T for k in range(3)],axis=1)
        self.dc=[self.np+k*len(u_h) for k in range(3)]
    def state(self,x):
        a=x[:-1].reshape(self.nh,self.n)
        return a,np.einsum('tfj,jn->tfn',self.B,a),x[-1]
    def force(self,q):
        p=q[:,0];u=q[:,1:].reshape(self.samples,3*self.n);c=u@self.C.T
        fp=p@self.L.T+(c*c-4*c)*p
        fu=(q[:,1:]@self.L.T).reshape(self.samples,3*self.n)+((1+p*p)*c-2*p*p)@self.C
        return np.concatenate([fp[:,None,:],fu.reshape(self.samples,3,self.n)],axis=1),c
    def residual(self,x,amp):
        a,q,w=self.state(x);f,c=self.force(q)
        r=np.einsum('tfj,tfn->jn',self.P,f)-w*w*self.h[:,None]**2*a
        return np.r_[r.ravel(),a[:self.np,0].sum()-amp,a[self.dc].mean(axis=1)]
    def jac(self,x,amp):
        a,q,w=self.state(x);_,c=self.force(q);p=q[:,0];n=self.n
        J=np.zeros((self.nh*n+4,self.nh*n+1))
        Cparts=[self.C[:,k*n:(k+1)*n] for k in range(3)]
        for i,fi in enumerate(self.component):
            for j,fj in enumerate(self.component):
                weight=self.P[:,fi,i]*self.B[:,fj,j];mean=weight.sum()
                if fi==0 and fj==0:
                    block=mean*self.L+np.diag(weight@(c*c-4*c))
                elif fi==0:
                    block=(weight@((2*c-4)*p))[:,None]*Cparts[fj-1]
                elif fj==0:
                    block=Cparts[fi-1].T*(weight@((2*c-4)*p))[None,:]
                else:
                    block=Cparts[fi-1].T@((weight@(1+p*p))[:,None]*Cparts[fj-1])
                    if fi==fj:block+=mean*self.L
                if i==j:block-=w*w*self.h[i]**2*np.eye(n)
                J[i*n:(i+1)*n,j*n:(j+1)*n]=block
        J[:self.nh*n,-1]=(-2*w*self.h[:,None]**2*a).ravel()
        for j in range(self.np):J[self.nh*n,j*n]=1
        for k,j in enumerate(self.dc):J[self.nh*n+1+k,j*n:(j+1)*n]=1/n
        return J
    def diagnostics(self,x,amp):
        a,q,w=self.state(x);f,c=self.force(q)
        acc=-w*w*np.einsum('tfj,jn->tfn',self.B,a*self.h[:,None]**2)
        activity=.5*np.sum(a[:self.np]**2*(1+(w*self.h[:self.np,None])**2),axis=0)
        coordinates=np.indices(self.g.mask.shape);d=np.minimum(coordinates,self.g.side-coordinates)/np.sqrt(2)
        r=np.sqrt((d*d).sum(axis=0))[self.g.mask];total=activity.sum()
        eig,vec=np.linalg.eigh(self.L);p1=a[0];spectral=(vec.T@p1)**2
        return {'omega':float(w),'period':float(2*np.pi/w),
                'projected_residual_norm':float(np.linalg.norm(self.residual(x,amp))),
                'full_equation_relative_defect':float(np.linalg.norm(acc+f)/max(1,np.linalg.norm(f))),
                'amplitude_anchor_error':float(abs(a[:self.np,0].sum()-amp)),
                'mean_activity_inside_radius1':float(activity[r<=1].sum()/max(1e-30,total)),
                'mean_activity_inside_radius2':float(activity[r<=2].sum()/max(1e-30,total)),
                'effective_active_sites':float(total*total/max(1e-30,activity@activity)),
                'rms_activity_radius':float(np.sqrt(activity@(r*r)/max(1e-30,total))),
                'mean_displacement_dc':a[self.dc].mean(axis=1).tolist(),
                'peak_compression':float(np.max(abs(c))),
                'fundamental_fraction_in_top_L_eigenspace':float(spectral[eig>8-1e-8].sum()/max(1e-30,spectral.sum())),
                'top_L_eigenspace_dimension':int(np.sum(eig>8-1e-8)),
                'next_L_below_top':float(eig[eig<8-1e-8].max())}

def lift(source,target,x):
    """Embed one centered periodic cell into a larger Ground region, then resolve.
    This is a discrete-domain lift, not a continuous branch identity proof.
    """
    a,_,w=source.state(x);b=np.zeros((target.nh,target.n))
    source_coords=np.argwhere(source.g.mask)
    target_index={tuple(c):j for j,c in enumerate(np.argwhere(target.g.mask))}
    for i,c in enumerate(source_coords):
        signed=np.where(c>source.g.side//2,c-source.g.side,c)
        j=target_index[tuple(signed%target.g.side)]
        for h,f,value in zip(source.h,source.component if hasattr(source,'component') else [0,0]+[1]*3+[2]*3+[3]*3,a[:,i]):
            matches=np.flatnonzero((target.h==h)&(target.component==f));b[matches[0],j]=value
    b[target.dc]-=b[target.dc].mean(axis=1,keepdims=True)
    return np.r_[b.ravel(),w]

def controls(o):
    rng=np.random.default_rng(1936);x=rng.normal(0,.015,o.nh*o.n+1);x[-1]=2.9
    v=rng.normal(size=x.size);eps=1e-6
    jv=o.jac(x,.2)@v
    err=np.linalg.norm((o.residual(x+eps*v,.2)-o.residual(x-eps*v,.2))/(2*eps)-jv)/max(1,np.linalg.norm(jv))
    control=np.zeros_like(x);control[:o.n]=.2*(-1.)**np.indices(o.g.mask.shape)[0][o.g.mask];control[-1]=np.sqrt(8)
    defect=o.diagnostics(control,.2)['full_equation_relative_defect']
    return {'jacobian_directional_error':float(err),'exact_extended_control_defect':defect,'pass':bool(err<1e-7 and defect<1e-12)}

def solve(o,x,label,max_nfev=30):
    initial=o.diagnostics(x,.2)
    lo=np.full(x.size,-np.inf);hi=-lo;lo[-1]=.2;hi[-1]=5
    fit=least_squares(o.residual,x,jac=o.jac,args=(.2,),bounds=(lo,hi),max_nfev=max_nfev,ftol=1e-10,xtol=1e-10,gtol=1e-10)
    d=o.diagnostics(fit.x,.2);d.update(label=label,side=o.g.side,sites=o.n,psi_harmonics=o.psi_h,u_harmonics=o.u_h,
        initial=initial,nfev=int(fit.nfev),solver_success=bool(fit.success),message=fit.message)
    d['passes_equation_and_localization_screen']=bool(d['full_equation_relative_defect']<1e-6 and d['amplitude_anchor_error']<1e-6 and d['mean_activity_inside_radius1']>=.8)
    d['direct_evolution']=integrate(o,fit.x,400)
    d['coefficients']=fit.x[:-1].reshape(o.nh,o.n).tolist()
    print(label,{k:d[k] for k in ['omega','full_equation_relative_defect','mean_activity_inside_radius1','effective_active_sites','nfev']},flush=True,file=__import__('sys').stderr)
    return fit.x,d

def top_band_audit(runs):
    rows=[]
    for side in [4,6,8,10,12]:
        coords=np.indices((side,)*3);mask=coords.sum(axis=0)%2==0
        cos=np.cos(2*np.pi*np.arange(side)/side)
        cx,cy,cz=np.meshgrid(cos,cos,cos,indexing='ij')
        ell=6-2*(cx*cy+cx*cz+cy*cz)
        top=np.isclose(ell,8,atol=1e-12,rtol=0)
        delta=np.zeros((side,)*3);delta[0,0,0]=1
        kernel=np.fft.ifftn(np.fft.fftn(delta)*top).real
        v=kernel[mask];activity=v*v
        rad=np.sqrt((np.minimum(coords,side-coords)**2).sum(axis=0)/2)
        points=np.argwhere(mask&(rad<=1));offset=(points[:,None,:]-points[None,:,:])%side
        restriction=kernel[tuple(offset.transpose(2,0,1))]
        bound=float(np.linalg.eigvalsh(restriction)[-1])
        row={'side':side,'sites':int(mask.sum()),'top_eigenspace_dimension':int(top.sum()//2),
             'derived_top_eigenspace_dimension':3*side-3,
             'maximum_single_site_fraction_in_top_space':float((3*side-3)/mask.sum()),
             'maximum_radius1_fraction_in_top_space':bound,
             'projected_delta_radius1_fraction':float(activity[rad[mask]<=1].sum()/activity.sum()),
             'projected_delta_effective_sites':float(activity.sum()**2/(activity@activity)),
             'eigenvector_error':float(np.linalg.norm(np.fft.ifftn(np.fft.fftn(kernel)*(ell-8)).real)),
             'inactive_sublattice_error':float(np.max(abs(kernel[~mask])))}
        if side in [4,6]:
            d=runs[[4,6].index(side)];o=RefinedOrbit(side);a=np.array(d['coefficients'])
            eig,V=np.linalg.eigh(o.L);projector=V[:,eig>8-1e-8]@V[:,eig>8-1e-8].T
            weighted=a[:o.np]*np.sqrt(.5*(1+(d['omega']*o.h[:o.np,None])**2))
            outside=float(np.linalg.norm(weighted-weighted@projector)**2/np.linalg.norm(weighted)**2)
            row['activity_fraction_outside_top_space']=outside
            row['near_top_space_radius1_upper_bound']=float(min(1,(np.sqrt(bound)*np.sqrt(1-outside)+np.sqrt(outside))**2))
            fundamental=a[0];row['solved_fundamental_overlap_with_projected_delta']=float(abs(fundamental@v)/np.linalg.norm(fundamental)/np.linalg.norm(v))
            f=projector@fundamental;f/=f[0]
            M=np.kron(np.eye(3),o.L)+o.C.T@o.C
            mu,U=np.linalg.eigh(M);D=o.C.T@(f*f);z=U.T@D;nz=mu>1e-10
            shift=float(-4*np.sum(z[nz]**2*(1/mu[nz]+.5/(mu[nz]-32)))/(f@f))
            row['leading_omega_squared_shift_per_amplitude_squared']=shift
            row['small_amplitude_predicted_omega']=float(np.sqrt(8+.2**2*shift))
            row['observed_omega']=d['omega'];row['compression_operator_max_eigenvalue']=float(mu.max())
        rows.append(row)
    return rows

def rotation_closure_audit(runs):
    rows=[]
    for d in runs:
        o=RefinedOrbit(d['side']);a=np.array(d['coefficients'])
        u=a[o.np:].reshape(3,len(o.u_h),o.n)
        curl_coeff=np.stack([u[2]@o.G[1].T-u[1]@o.G[2].T,
                            u[0]@o.G[2].T-u[2]@o.G[0].T,
                            u[1]@o.G[0].T-u[0]@o.G[1].T])
        def curl(v):
            return np.stack([v[:,2]@o.G[1].T-v[:,1]@o.G[2].T,
                             v[:,0]@o.G[2].T-v[:,2]@o.G[0].T,
                             v[:,1]@o.G[0].T-v[:,0]@o.G[1].T],axis=1)
        rng=np.random.default_rng(320);q=rng.normal(size=(o.samples,4,o.n));force,_=o.force(q)
        identity_error=float(np.max(abs(curl(force[:,1:])-curl(q[:,1:])@o.L.T)))
        K=np.kron(np.diag([1.2,.9,.9]),np.eye(o.n))
        weighted=K@(o.C.T@o.C)
        asymmetry=float(np.linalg.norm(weighted-weighted.T)/max(1,np.linalg.norm(weighted)))
        rows.append({'side':d['side'],'max_solved_displacement_curl_coefficient':float(np.max(abs(curl_coeff))),
                     'curl_force_equals_L_curl_u_error':identity_error,
                     'naive_path_weighting_K_diagonal':[1.2,.9,.9],
                     'naive_unit_kinetic_weighted_compression_jacobian_asymmetry':asymmetry,
                     'interpretation':'Baseline compression cannot generate curl from zero curl. Simply multiplying its force by K fails reciprocity in the existing unit kinetic coordinates.'})
    return rows

def report():
    previous=json.loads(Path(__file__).with_name('periodic_orbit_results.json').read_text())['runs'][0]
    old=Orbit();x=np.r_[np.array(previous['coefficients']).ravel(),previous['omega']]
    small=RefinedOrbit();cs=controls(small)
    assert cs['pass']
    refined,ds=solve(small,lift(old,small,x),'side4_harmonic_refinement')
    larger=RefinedOrbit(6);cl=controls(larger);assert cl['pass']
    large,dl=solve(larger,lift(small,larger,refined),'side6_Ground_domain_lift')
    dl['half_timestep_evolution']=integrate(larger,large,800)
    return {'scope':'Bounded harmonic refinement and discrete-domain lift; unchanged native constitutive law.',
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
        'parameters':{'amplitude_anchor':.2,'beta':1,'shear':1,'k':1,'a':1,'eta':2,'temporal_samples':64,'max_nfev':30},
        'controls':{'side4':cs,'side6':cl},'runs':[ds,dl],
        'top_band_audit':top_band_audit([ds,dl]),
        'rotation_closure_audit':rotation_closure_audit([ds,dl]),
        'limits':['Even-time finite-harmonic sector is not exhaustive.','Discrete-domain lift may select a different branch; no continuous branch-identity claim.','Periodic larger domain is not an outgoing or unbounded boundary condition.','Radius1 screen deliberately held fixed across domains; activity is not conserved energy.','No Persistent Mode, Mass Effect, clock or complete four-interaction closure is established.']}
if __name__=='__main__':
    r=report();print(json.dumps(r,indent=2));raise SystemExit(0 if all(c['pass'] for c in r['controls'].values()) else 1)
