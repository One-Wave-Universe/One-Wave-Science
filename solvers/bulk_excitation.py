"""Hypothetical nonlinear closure, separate from the canonical memory update.
Native FCC12 bulk with periodic images, no enclosing reflecting cavity.
All quantities dimensionless; norm is a conserved model input, not particle count.
"""
from dataclasses import dataclass
from itertools import product
import numpy as np
from scipy.optimize import minimize
from joint_boundary_response import cycle_laplacian, OFFSETS

@dataclass(frozen=True)
class BulkCoefficients:
    spatial: tuple = (1., .8, 1.2, .6)
    cross: float = .12
    phase_lock: float = .04
    alpha: tuple = (1., .9, 1.1, .8)
    focusing: float = 2.
    saturation: float = 1.

class BulkExcitation:
    def __init__(self, side=12, spacing=1., coefficients=BulkCoefficients()):
        if not isinstance(side,int) or side < 4 or side%2 or not np.isfinite(spacing) or spacing<=0:
            raise ValueError('Even periodic side >=4 and finite positive spacing required')
        c=coefficients
        values=np.array([*c.spatial,*c.alpha,c.cross,c.phase_lock,c.focusing,c.saturation])
        if len(c.spatial)!=4 or len(c.alpha)!=4 or not np.isfinite(values).all() or min(c.spatial)<=0 or min(c.alpha)<=0 or min(c.cross,c.phase_lock,c.focusing,c.saturation)<0:
            raise ValueError('Invalid constitutive inputs')
        if c.focusing>0 and c.saturation<=0: raise ValueError('Focusing candidate requires amplitude saturation')
        self.side,self.spacing,self.c=side,spacing,c
        self.volume=spacing**3/np.sqrt(2)
        grid=np.indices((side,)*3).transpose(1,2,3,0)
        self.mask=(grid.sum(axis=-1)%2==0)
        self.xyz=(grid[self.mask]-side//2)*spacing/np.sqrt(2)
        self.R=cycle_laplacian(); self.C=np.diag(c.spatial)+c.cross*self.R
        self.alpha=np.array(c.alpha)
        k=2*np.pi*np.fft.fftfreq(side)
        kk=np.stack(np.meshgrid(k,k,k,indexing='ij'),axis=-1)
        symbol=sum(1-np.cos(np.einsum('...j,j->...',kk,o)) for o in OFFSETS)
        block=symbol[...,None,None]*self.C/(12*spacing**2)+c.phase_lock*self.R
        self.band,self.basis=np.linalg.eigh(block)
        self._propagators={}

    def full(self, field):
        x=np.zeros((self.side,)*3+(4,),dtype=np.asarray(field).dtype); x[self.mask]=field; return x

    def linear(self, field):
        x=self.full(field)
        lap=12*x-sum(np.roll(x,o,axis=(0,1,2)) for o in OFFSETS)
        return (lap@self.C/(12*self.spacing**2)+self.c.phase_lock*(x@self.R))[self.mask]

    def density(self, field): return (abs(field)**2)@self.alpha
    def norm(self, field): return float(self.volume*np.sum(abs(field)**2))
    def gradient(self, field):
        rho=self.density(field)
        return self.linear(field)+((-self.c.focusing*rho+self.c.saturation*rho*rho)[:,None]*self.alpha)*field

    def energies(self, field):
        x=self.full(field); diagonal=np.diag(self.c.spatial)
        diag=cross=0.
        for o in OFFSETS:
            d=x-np.roll(x,o,axis=(0,1,2)); d=d[self.mask]
            diag+=float(np.vdot(d,d@diagonal).real)
            cross+=float(np.vdot(d,d@(self.c.cross*self.R)).real)
        rho=self.density(field)
        return {'spatial_diagonal':self.volume*diag/(24*self.spacing**2),
                'spatial_cross':self.volume*cross/(24*self.spacing**2),
                'phase_lock':self.volume*self.c.phase_lock*float(np.vdot(field,field@self.R).real),
                'focusing':-self.volume*self.c.focusing*np.sum(rho*rho)/2,
                'saturation':self.volume*self.c.saturation*np.sum(rho**3)/3}
    def energy(self, field): return float(sum(self.energies(field).values()))

    def seed(self,norm=20.,width=1.5,shift=(0,0,0)):
        r=self.xyz-np.asarray(shift)
        f=np.exp(-np.sum(r*r,axis=1)/(2*width**2))[:,None]*np.array([1.,.8,1.1,.7])[None,:]
        return f*np.sqrt(norm/self.norm(f))

    def stationary(self,norm=20.,width=1.5,shift=(0,0,0),maxiter=1500):
        """Real-amplitude stationary branch; not a global complex minimum."""
        if not np.isfinite(norm) or norm<=0: raise ValueError('Positive norm required')
        initial=self.seed(norm,width,shift)
        # Minimize on the fixed-norm sphere using a normalized parameterization.
        def objective(y):
            raw=y.reshape((-1,4)); scale=np.sqrt(norm/self.norm(raw)); f=raw*scale
            grad=self.gradient(f); mu=float(np.vdot(f,grad).real/np.vdot(f,f).real)
            return self.energy(f),(2*self.volume*scale*(grad-mu*f)).ravel()
        result=minimize(objective,initial.ravel(),jac=True,method='L-BFGS-B',options={'maxiter':maxiter,'ftol':1e-14,'gtol':1e-9,'maxls':40})
        f=result.x.reshape((-1,4)); f*=np.sqrt(norm/self.norm(f))
        grad=self.gradient(f); mu=float(np.vdot(f,grad).real/np.vdot(f,f).real)
        residual=float(np.linalg.norm(grad-mu*f)/np.linalg.norm(f))
        return f,{'optimizer_success':bool(result.success),'message':str(result.message),'iterations':int(result.nit),'mu':mu,'stationary_residual':residual}

    def step(self,field,dt):
        if not np.isfinite(dt) or dt==0: raise ValueError('Finite nonzero step required')
        def local(f,h):
            rho=self.density(f)
            return f*np.exp(-1j*h*(-self.c.focusing*rho+self.c.saturation*rho*rho)[:,None]*self.alpha)
        f=local(field,dt/2)
        if dt not in self._propagators:
            self._propagators[dt]=np.einsum('...ik,...k,...jk->...ij',self.basis,np.exp(-1j*dt*self.band),self.basis)
        transformed=np.fft.fftn(self.full(f),axes=(0,1,2))
        transformed=np.einsum('...ij,...j->...i',self._propagators[dt],transformed)
        f=np.fft.ifftn(transformed,axes=(0,1,2))[self.mask]
        return local(f,dt/2)  # no evolution renormalization

    def measurements(self,field):
        weight=np.sum(abs(field)**2,axis=1); n=np.sum(weight)
        # Minimal-image position relative to the density maximum.
        center=self.xyz[np.argmax(weight)]; box=self.side*self.spacing/np.sqrt(2)
        r=(self.xyz-center+box/2)%box-box/2
        width=float(np.sqrt(np.sum(weight*np.sum(r*r,axis=1))/n))
        return {'norm':self.norm(field),'energy':self.energy(field),'rms_radius':width,
                'effective_volume':float(self.volume*n*n/np.sum(weight*weight)),
                'core_fraction_r2':float(np.sum(weight[np.linalg.norm(r,axis=1)<=2])/n),
                'outer_image_fraction':float(np.sum(weight[np.max(abs(r),axis=1)>box*.4])/n),
                'role_norms':(self.volume*np.sum(abs(field)**2,axis=0)).tolist()}

    def detector(self,field,radius=1.):
        weights=(np.linalg.norm(self.xyz,axis=1)<=radius).astype(float)
        return {'amplitude_real':(self.volume*(weights@field)).real.tolist(),
                'amplitude_imag':(self.volume*(weights@field)).imag.tolist(),
                'intensity':float(self.volume*np.sum(weights[:,None]*abs(field)**2))}

    def evolve(self,field,duration=20.,dt=.02,stride=50):
        if not np.isfinite(duration) or duration<=0 or not np.isfinite(dt) or dt<=0 or not isinstance(stride,int) or stride<=0:
            raise ValueError('Positive finite duration/dt and positive integer stride required')
        count=int(round(duration/dt))
        if count<=0 or not np.isclose(count*dt,duration): raise ValueError('Duration must be a positive integer number of steps')
        initial=field.astype(complex).copy(); f=initial.copy(); e0=self.energy(f); n0=self.norm(f)
        trace=[]; norm_error=energy_error=0.
        for step in range(count+1):
            e=self.energy(f); n=self.norm(f)
            norm_error=max(norm_error,abs(n/n0-1)); energy_error=max(energy_error,abs(e-e0)/max(abs(e0),1.))
            if step%stride==0 or step==count:
                overlap=np.vdot(initial,f); aligned=f*np.exp(-1j*np.angle(overlap))
                trace.append({'time':step*dt,**self.measurements(f),'phase_aligned_error':float(np.linalg.norm(aligned-initial)/np.linalg.norm(initial)),'detector_r1':self.detector(f,1.),'detector_r2':self.detector(f,2.)})
            if step<count: f=self.step(f,dt)
        return f,{'max_norm_relative_error':norm_error,'max_energy_relative_error':energy_error,'trace':trace}
