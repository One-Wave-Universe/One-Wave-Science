"""Bounded Fourier/Galerkin solve of the unchanged FCC compression candidate.
Even-time sector: psi harmonics 1,3; retained u harmonics 0,2,4.
No normalization during dynamics, no new potential, no physical calibration.
"""
import json
import numpy as np
from scipy.optimize import least_squares
from native_compression_bridge import FCC, seed

class Orbit:
    def __init__(self, side=4):
        self.g=FCC(side);self.n=int(self.g.mask.sum());n=self.n
        self.angles=2*np.pi*np.arange(32)/32
        self.B=np.zeros((32,4,11));self.h=np.array([1,3]+[0,2,4]*3)
        for j,h in enumerate([1,3]):self.B[:,0,j]=np.cos(h*self.angles)
        for k in range(3):
            for j,h in enumerate([0,2,4]):self.B[:,k+1,2+3*k+j]=np.cos(h*self.angles)
        self.P=self.B.copy()/32
        for j,h in enumerate(self.h):self.P[:,:,j]*=1 if h==0 else 2
        self.L=np.zeros((n,n));self.G=np.zeros((3,n,n))
        for i in range(n):
            q=np.zeros(self.g.mask.shape);q[self.g.mask]=np.eye(n)[i]
            self.L[:,i]=self.g.lap(q)[self.g.mask]
            self.G[:,:,i]=self.g.grad(q)[self.g.mask].T
        # Compression C=-div is the adjoint of grad, component-major.
        self.C=np.concatenate([self.G[k].T for k in range(3)],axis=1)
    def state(self,x):
        coeff=x[:-1].reshape(11,self.n)
        q=np.einsum('tfj,jn->tfn',self.B,coeff)
        return coeff,q,x[-1]
    def force(self,q):
        p=q[:,0];u=q[:,1:].reshape(32,3*self.n);c=u@self.C.T
        fp=p@self.L.T+(c*c-4*c)*p
        fu=(q[:,1:]@self.L.T).reshape(32,3*self.n)+((1+p*p)*c-2*p*p)@self.C
        return np.concatenate([fp[:,None,:],fu.reshape(32,3,self.n)],axis=1),c
    def residual(self,x,amp):
        a,q,w=self.state(x);f,c=self.force(q)
        r=np.einsum('tfj,tfn->jn',self.P,f)-w*w*self.h[:,None]**2*a
        # Anchor initial central excitation to prohibit trivial Ground.
        return np.r_[r.ravel(),(a[0,0]+a[1,0]-amp),a[[2,5,8]].mean(axis=1)]
    def jac(self,x,amp):
        a,q,w=self.state(x);_,c=self.force(q);n=self.n
        J=np.zeros((11*n,11*n));eye=np.eye(n)
        for t in range(32):
            p=q[t,0];cc=c[t]
            pp=self.L+np.diag(cc*cc-4*cc)
            pu=np.diag((2*cc-4)*p)@self.C
            uu=np.kron(np.eye(3),self.L)+self.C.T@np.diag(1+p*p)@self.C
            F=np.block([[pp,pu],[pu.T,uu]])
            bt=np.kron(self.B[t],eye);pt=np.kron(self.P[t].T,eye)
            J+=pt@F@bt
        J-=np.diag(np.repeat(w*w*self.h*self.h,n))
        dw=(-2*w*self.h[:,None]**2*a).ravel()
        full=np.zeros((11*n+4,11*n+1));full[:11*n,:-1]=J;full[:11*n,-1]=dw
        full[11*n,0]=1;full[11*n,n]=1
        for row,j in enumerate([2,5,8]):full[11*n+1+row,j*n:(j+1)*n]=1/n
        return full
    def diagnostics(self,x,amp):
        a,q,w=self.state(x);f,c=self.force(q)
        acc=-w*w*np.einsum('tfj,jn->tfn',self.B,a*self.h[:,None]**2)
        defect=float(np.linalg.norm(acc+f)/max(1,np.linalg.norm(f)))
        # Mean activity includes analytic excitation velocity over the period.
        activity=.5*np.sum(a[:2]**2*(1+(w*self.h[:2,None])**2),axis=0)
        coords=np.indices(self.g.mask.shape);d=np.minimum(coords,self.g.side-coords)/np.sqrt(2)
        r=np.sqrt((d*d).sum(axis=0))[self.g.mask]
        return {'omega':float(w),'period':float(2*np.pi/w),'projected_residual_norm':float(np.linalg.norm(self.residual(x,amp))),
                'full_equation_relative_defect':defect,'amplitude_anchor_error':float(abs(a[0,0]+a[1,0]-amp)),
                'mean_activity_inside_radius1':float(activity[r<=1].sum()/max(1e-30,activity.sum())),
                'effective_active_sites':float(activity.sum()**2/max(1e-30,(activity**2).sum())),
                'mean_displacement_dc':a[[2,5,8]].mean(axis=1).tolist(), 'peak_compression':float(np.max(np.abs(c))), 'peak_displacement':float(np.max(np.abs(q[:,1:])))}

def integrate(o,x,steps_per_period=400,periods=10):
    a,q,w=o.state(x);g=o.g
    psi=q[0,0].copy();u=q[0,1:].reshape(3*o.n).copy()
    vp=np.zeros_like(psi);vu=np.zeros_like(u)
    p0=psi.copy();u0=u.copy();norm=max(1e-30,np.dot(p0,p0)+np.dot(u0,u0))
    def force(p,v):
        c=o.C@v
        return o.L@p+(c*c-4*c)*p, (v.reshape(3,o.n)@o.L.T).ravel()+o.C.T@((1+p*p)*c-2*p*p)
    def energy(p,v,pv,uv):
        c=o.C@v
        return g.volume*(.5*p@(o.L@p)+.5*np.sum(v.reshape(3,o.n)*(v.reshape(3,o.n)@o.L.T))+np.sum(.5*(1+p*p)*c*c-2*p*p*c)+.5*(pv@pv+uv@uv))
    # Matrix operations are assembled from the native operators, not a new law.
    pp=np.zeros(g.mask.shape);uu=np.zeros(g.mask.shape+(3,));pp[g.mask]=psi;uu[g.mask]=u.reshape(3,o.n).T
    gp,gu=g.gradients(pp,uu);fp,fu=force(psi,u)
    assert np.max(abs(fp-gp[g.mask]))<1e-10 and np.max(abs(fu.reshape(3,o.n).T-gu[g.mask]))<1e-10
    assert abs(energy(psi,u,vp,vu)-g.energy(pp,uu))<1e-10
    e0=energy(psi,u,vp,vu);err=0.;returns=[];dt=2*np.pi/w/steps_per_period
    for step in range(1,steps_per_period*periods+1):
        gp,gu=force(psi,u);vp-=.5*dt*gp;vu-=.5*dt*gu
        psi+=dt*vp;u+=dt*vu
        gp,gu=force(psi,u);vp-=.5*dt*gp;vu-=.5*dt*gu
        en=energy(psi,u,vp,vu)
        err=max(err,abs(en-e0)/max(1,abs(e0)))
        if not np.isfinite(en) or max(np.max(abs(psi)),np.max(abs(u)))>50:
            return {'completed':False,'dt':float(dt),'end_time':float(step*dt),'max_scaled_energy_error':float(err),'period_returns':returns}
        if step%steps_per_period==0:
            distance=np.sqrt((np.sum((psi-p0)**2)+np.sum((u-u0)**2)+vp@vp+vu@vu)/norm)
            returns.append(float(distance))
    return {'completed':True,'dt':float(dt),'periods':periods,'max_scaled_energy_error':float(err),'period_returns':returns}

def report():
    o=Orbit();n=o.n
    parity=(-1.)**np.indices(o.g.mask.shape)[0][o.g.mask]
    x=np.zeros(11*n+1);x[:n]=.2*parity;x[-1]=np.sqrt(8)
    control=o.diagnostics(x,.2)
    rng=np.random.default_rng(193);z=x+rng.normal(0,.01,x.shape);z[-1]=2.9;v=rng.normal(size=x.size);e=1e-6
    jacerr=np.linalg.norm((o.residual(z+e*v,.2)-o.residual(z-e*v,.2))/(2*e)-o.jac(z,.2)@v)/max(1,np.linalg.norm(o.jac(z,.2)@v))
    runs=[]
    for amp in [.2,.5,1.]:
        x=np.zeros(11*n+1);x[:n]=amp*seed(o.g)[o.g.mask];x[-1]=2.9
        lo=np.full(x.size,-np.inf);hi=-lo;lo[-1]=.2;hi[-1]=5
        fit=least_squares(o.residual,x,jac=o.jac,args=(amp,),bounds=(lo,hi),max_nfev=80,ftol=1e-10,xtol=1e-10,gtol=1e-10)
        d=o.diagnostics(fit.x,amp);d.update(amplitude=amp,side=4,sites=n,nfev=fit.nfev,solver_success=bool(fit.success),message=fit.message)
        d['passes_equation_and_localization_screen']=bool(d['full_equation_relative_defect']<1e-6 and d['amplitude_anchor_error']<1e-6 and d['mean_activity_inside_radius1']>=.8)
        d['direct_evolution']=integrate(o,fit.x)
        if amp==.2:d['half_timestep_evolution']=integrate(o,fit.x,800)
        d['coefficients']=fit.x[:-1].reshape(11,n).tolist();runs.append(d)
        print('finished amplitude',amp,'defect',d['full_equation_relative_defect'],flush=True,file=__import__('sys').stderr)
    checks={'exact_extended_recurrence_control':bool(control['full_equation_relative_defect']<1e-12),'analytic_jacobian':bool(jacerr<1e-7)}
    return {'scope':'Even-time finite-harmonic candidate solve; unchanged dimensionless native law. Not an exhaustive periodic-orbit search.',
            'parameters':{'side':4,'sites':n,'temporal_samples':32,'psi_harmonics':[1,3],'u_harmonics':[0,2,4],'beta':1,'shear':1,'k':1,'a':1,'eta':2},
            'checks':checks,'jacobian_directional_error':float(jacerr),'extended_control':control,'runs':runs,
            'limits':['Finite harmonics and restricted time symmetry may miss solutions.','Side 4 is a minimal periodic graph, not a large-domain localization proof.','Center anchor is a solve constraint, not a physical force or a reset in evolution.','Candidate needs direct integration, stability, larger-domain and radiation checks before Persistent Mode classification.']}
if __name__=='__main__':
    r=report();print(json.dumps(r,indent=2));raise SystemExit(0 if all(r['checks'].values()) else 1)
