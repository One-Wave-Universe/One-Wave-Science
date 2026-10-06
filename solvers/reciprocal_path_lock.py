"""Candidate reciprocal path/circulation work law; balance is not a knot lock.
Native FCC baseline preserved by explicit coupling-off control.
"""
import json
import numpy as np
from scipy.linalg import solve
from native_compression_bridge import FCC, seed
from recurrence_domain_check import RefinedOrbit

class PathModel:
    def __init__(self,side=4,kappa=.4,grot=.3,mu=2.,memory_stiffness=.2):
        o=RefinedOrbit(side);self.g=o.g;self.n=o.n;self.L=o.L;self.C=o.C
        self.kappa=kappa;self.grot=grot;self.mu=mu;self.dR=memory_stiffness
        B=np.zeros((5,3,3));B[0]=np.diag([1,-1,0])/np.sqrt(2);B[1]=np.diag([1,1,-2])/np.sqrt(6)
        for j,(a,b) in enumerate([(0,1),(0,2),(1,2)],2):B[j,a,b]=B[j,b,a]=1/np.sqrt(2)
        self.B=B
        Gx,Gy,Gz=o.G;zero=np.zeros_like(Gx)
        self.T=np.block([[zero,-Gz,Gy],[Gz,zero,-Gx],[-Gy,Gx,zero]])
        coords=np.argwhere(self.g.mask);index={tuple(c):i for i,c in enumerate(coords)};edges=[]
        for i,c in enumerate(coords):
            for offset in self.g.offsets:
                j=index[tuple((c+offset)%side)]
                if i<j:edges.append((i,j,np.array(offset)/np.sqrt(2)))
        self.i=np.array([e[0] for e in edges]);self.j=np.array([e[1] for e in edges]);self.normals=np.array([e[2] for e in edges])
        self.nb=np.einsum('ei,kij,ej->ek',self.normals,B,self.normals)
    def unpack(self,x):
        n=self.n;return x[:n],x[n:4*n].reshape(3,n).T,x[4*n:].reshape(5,n).T
    def geometry(self,u,r):
        difference=u[self.i]-u[self.j];d2=np.sum(difference*difference,axis=1)
        w=1+.5*self.kappa*np.sum((r[self.i]+r[self.j])*self.nb,axis=1)
        R=np.einsum('nk,kij->nij',r,self.B)
        q=(self.T@u.T.ravel()).reshape(3,self.n).T
        return difference,d2,w,R,q
    def value_gradient(self,x):
        p,u,r=self.unpack(x);diff,d2,w,R,q=self.geometry(u,r);n=self.n
        c=self.C@u.T.ravel();rho=p*p
        base=.5*p@(self.L@p)+np.sum(.5*(1+rho)*c*c-2*rho*c)
        path=.25*np.sum(w*d2)
        q2=np.sum(q*q,axis=1);Rq=np.einsum('nij,nj->ni',R,q)
        memory=.5*self.mu*np.sum(r*r)+.5*self.dR*np.sum(r*(self.L@r))
        rotation=-self.grot*np.sum(q*Rq)+self.grot**2/(3*self.mu)*np.sum(q2*q2)
        gp=self.L@p+(c*c-4*c)*p
        gu=(self.C.T@((1+rho)*c-2*rho)).reshape(3,n).T
        edgeforce=.5*w[:,None]*diff
        np.add.at(gu,self.i,edgeforce);np.add.at(gu,self.j,-edgeforce)
        gq=-2*self.grot*Rq+4*self.grot**2/(3*self.mu)*q2[:,None]*q
        gu+=(self.T.T@gq.T.ravel()).reshape(3,n).T
        gr=self.mu*r+self.dR*(self.L@r)-self.grot*np.einsum('ni,kij,nj->nk',q,self.B,q)
        strain=.125*self.kappa*d2[:,None]*self.nb
        np.add.at(gr,self.i,strain);np.add.at(gr,self.j,strain)
        return float(self.g.volume*(base+path+memory+rotation)),np.r_[gp,gu.T.ravel(),gr.T.ravel()]
    def balance_r(self,x):
        p,u,r=self.unpack(x);r0=np.zeros_like(r)
        xx=np.r_[p,u.T.ravel(),r0.T.ravel()]
        drive=self.value_gradient(xx)[1][4*self.n:].reshape(5,self.n).T
        balanced=solve(self.mu*np.eye(self.n)+self.dR*self.L,-drive,assume_a='pos')
        return np.r_[p,u.T.ravel(),balanced.T.ravel()]
    def min_accessibility(self,x):
        p,u,r=self.unpack(x);R=np.einsum('nk,kij->nij',r,self.B)
        return float(np.linalg.eigvalsh(np.eye(3)[None,:,:]+self.kappa*R).min())
    def activity(self,x,v):
        p,_,_=self.unpack(x);vp,_,_=self.unpack(v);a=p*p+vp*vp
        co=np.indices(self.g.mask.shape);radius=np.sqrt((np.minimum(co,self.g.side-co)**2).sum(axis=0)/2)[self.g.mask]
        return float(a[radius<=1].sum()/max(1e-30,a.sum()))

def evolve(m,x,dt=.01,time=20,perturbation=0):
    x=x.copy();v=np.zeros_like(x);n=m.n
    if perturbation:
        # Reproducible positional perturbation; no subsequent reset.
        x[1]+=(perturbation*np.linalg.norm(x[:n]))
    ref=x.copy();e0=m.value_gradient(x)[0];error=0.;minK=m.min_accessibility(x);trace=[]
    peakcurl=0.;minlate=1.;returned=[];complete=True
    for step in range(round(time/dt)+1):
        if step:
            grad=m.value_gradient(x)[1];v-=.5*dt*grad;x+=dt*v;v-=.5*dt*m.value_gradient(x)[1]
        potential,grad=m.value_gradient(x);e=potential+.5*m.g.volume*(v@v)
        error=max(error,abs(e-e0)/max(1,abs(e0)));minK=min(minK,m.min_accessibility(x))
        p,u,r=m.unpack(x);q=(m.T@u.T.ravel()).reshape(3,n).T
        curlnorm=float(np.linalg.norm(q));peakcurl=max(peakcurl,curlnorm)
        activity=m.activity(x,v)
        if step*dt>=.75*time:minlate=min(minlate,activity)
        distance=float(np.sqrt(np.sum((x-ref)**2)+v@v)/max(1e-30,np.linalg.norm(ref)))
        if step%round(.2/dt)==0:trace.append({'t':float(step*dt),'localized_activity_radius1':activity,'full_state_return_error':distance,'curl_displacement_norm':curlnorm,'mean_reorganization_norm':float(np.linalg.norm(r)/np.sqrt(n))})
        if not np.isfinite(e) or np.max(abs(x))>50 or minK<=0:
            complete=False;break
    for a,b,c in zip(trace,trace[1:],trace[2:]):
        if b['t']>=5 and b['full_state_return_error']<=.1 and b['full_state_return_error']<a['full_state_return_error'] and b['full_state_return_error']<=c['full_state_return_error'] and (not returned or b['t']-returned[-1]>=1):returned.append(b['t'])
    lock=complete and error<.005 and minlate>=.8 and len(returned)>=2
    return {'completed':complete,'end_time':float(step*dt),'dt':dt,'max_scaled_energy_error':float(error),'min_accessibility_eigenvalue':minK,'max_displacement_curl_norm':peakcurl,'min_final_quarter_localized_activity':minlate,'qualifying_returns':returned,'passes_preliminary_lock_screen':bool(lock),'trace':trace}

def report():
    m=PathModel();n=m.n;rng=np.random.default_rng(319)
    x=rng.normal(0,.03,9*n);d=rng.normal(size=x.size);eps=1e-6
    value,gradient=m.value_gradient(x)
    derivative=(m.value_gradient(x+eps*d)[0]-m.value_gradient(x-eps*d)[0])/(2*eps)
    ge=abs(derivative-m.g.volume*(gradient@d))/max(1,abs(derivative))
    # Reciprocity is an independent cross-direction finite difference of the force.
    e=rng.normal(size=x.size)
    Hd=(m.value_gradient(x+eps*d)[1]-m.value_gradient(x-eps*d)[1])/(2*eps)
    He=(m.value_gradient(x+eps*e)[1]-m.value_gradient(x-eps*e)[1])/(2*eps)
    reciprocity=abs(e@Hd-d@He)/max(1,abs(e@Hd),abs(d@He))
    ab=PathModel(kappa=0,grot=0);p,u,_=ab.unpack(x);xx=x.copy();xx[4*n:]=0
    pp=np.zeros(ab.g.mask.shape);uu=np.zeros(ab.g.mask.shape+(3,));pp[ab.g.mask]=p;uu[ab.g.mask]=u
    native=ab.g.gradients(pp,uu);aenergy,ag=ab.value_gradient(xx)
    recovery=max(np.max(abs(ag[:n]-native[0][ab.g.mask])),np.max(abs(ag[n:4*n].reshape(3,n).T-native[1][ab.g.mask])))
    energy_recovery=abs(aenergy-ab.g.energy(pp,uu))
    # Exact conditional R force balance for fixed excitation/displacement.
    balanced=m.balance_r(x);balance_error=float(np.linalg.norm(m.value_gradient(balanced)[1][4*n:]))
    zero=m.value_gradient(np.zeros(9*n));zero_error=float(np.linalg.norm(zero[1]))
    # Conservative frequency/energy check, with one fixed law for all runs.
    co=np.indices(m.g.mask.shape);signed=np.where(co>m.g.side//2,co-m.g.side,co)/np.sqrt(2)
    envelope=seed(m.g)[m.g.mask];p=.2*envelope*(1+.2*signed[0][m.g.mask])
    u=np.zeros((n,3));r=np.zeros((n,5));base=np.r_[p,u.T.ravel(),r.T.ravel()]
    compression=evolve(m,base);compression_refined=evolve(m,base,dt=.005)
    # Seed circulation explicitly; no claim of a spontaneously formed Vortex Phase.
    u[:,0]=-.03*signed[1][m.g.mask]*envelope;u[:,1]=.03*signed[0][m.g.mask]*envelope
    u-=u.mean(axis=0);swirl=m.balance_r(np.r_[p,u.T.ravel(),r.T.ravel()])
    swirl_balance=float(np.linalg.norm(m.value_gradient(swirl)[1][4*n:]))
    rotation=evolve(m,swirl);refined=evolve(m,swirl,dt=.005);perturbed=evolve(m,swirl,perturbation=.01)
    off=evolve(ab,base)
    checks={'energy_gradient':bool(ge<1e-7),'reciprocity':bool(reciprocity<1e-7),'native_force_recovery':bool(recovery<1e-12),'native_energy_recovery':bool(energy_recovery<1e-12),'conditional_reorganization_balance':bool(balance_error<1e-10),'zero_input':bool(zero_error==0)}
    return {'scope':'New constitutive candidate reciprocal path/rotation core, not derived physical coefficients or complete boundary weave.',
      'parameters':{'side':4,'sites':n,'kappa':m.kappa,'grot':m.grot,'mu':m.mu,'memory_stiffness':m.dR,'beta':1,'shear':1,'k':1,'a':1,'eta':2,'seed':319},
      'checks':checks,'measurements':{'energy_gradient_error':ge,'reciprocity_error':reciprocity,'native_force_error':float(recovery),'native_energy_error':energy_recovery,'conditional_R_balance_error':balance_error,'swirl_initial_R_balance_error':swirl_balance},
      'runs':{'compression_only':compression,'compression_only_half_dt':compression_refined,'seeded_circulation_balanced_R':rotation,'seeded_circulation_half_dt':refined,'seeded_circulation_1percent_perturbation':perturbed,'coupling_off_compression':off},
      'limits':['Reciprocal energy core is a new hypothesis; C-319 first-order relaxation is not derived by unit-kinetic R dynamics.','R is symmetric traceless; SPD domain is monitored and leaving it stops the run.','Strain-driven R term is new, not the original magnetic-only relaxation source.','Periodic 32-site graph, no evolving closed boundary, shell or Mirror phase coordinate.','Conditional R balance is not simultaneous force equilibrium or a physical lock.','No imposed normalization, localization potential or force through a boundary.']}
if __name__=='__main__':
    r=report();print(json.dumps(r,indent=2));raise SystemExit(0 if all(r['checks'].values()) else 1)
