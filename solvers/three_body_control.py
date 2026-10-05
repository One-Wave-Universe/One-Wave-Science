#!/usr/bin/env python3
"""Finite-time Newtonian control required by A-115; not a derived One-Wave law.

Dimensionless G=1, three positions/velocities in native R^3. Planar fixtures
explicitly have z=vz=0. No softening, damping, wake, lattice or fitted coupling.
Phi_i=-G sum(j!=i) m_j/r_ij; a_i=-grad(Phi_i). Masses are supplied inputs.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.integrate import solve_ivp

FIGURE_EIGHT_PERIOD = 6.32591398  # approximate reference, not fitted by this code
SOURCE = 'https://people.ucsc.edu/~rmont/Nbdy.html'


def unpack(state):
    state = np.asarray(state, dtype=float)
    if state.shape != (18,) or not np.all(np.isfinite(state)):
        raise ValueError('state must contain 18 finite coordinates')
    s = state.reshape(3, 6)
    return s[:, :3], s[:, 3:]


def pack(r, v):
    return np.concatenate((r, v), axis=1).ravel()


class NewtonianControl:
    def __init__(self, masses=(1., 1., 1.), G=1.):
        self.masses = np.asarray(masses, dtype=float)
        self.G = float(G)
        if (self.masses.shape != (3,) or not np.all(np.isfinite(self.masses))
                or np.any(self.masses <= 0) or not np.isfinite(G) or G <= 0):
            raise ValueError('three positive finite masses and positive finite G required')

    def acceleration(self, r):
        r = np.asarray(r, dtype=float)
        if r.shape != (3, 3) or not np.all(np.isfinite(r)):
            raise ValueError('positions must be finite 3 by 3 array')
        a = np.zeros((3, 3))
        for i in range(3):
            for j in range(i + 1, 3):
                d = r[j] - r[i]
                distance = np.linalg.norm(d)
                if distance <= 1e-10:
                    raise ValueError('collision/near-collision: unregularized control stops')
                pair = self.G * d / distance**3
                a[i] += self.masses[j] * pair
                a[j] -= self.masses[i] * pair
        return a

    def rhs(self, t, state):
        r, v = unpack(state)
        return pack(v, self.acceleration(r))

    def invariants(self, state):
        r, v = unpack(state)
        self.acceleration(r)  # same finite/separation guard
        kinetic = .5 * np.sum(self.masses[:, None] * v*v)
        potential = -self.G * sum(self.masses[i]*self.masses[j] /
            np.linalg.norm(r[j]-r[i]) for i in range(3) for j in range(i+1, 3))
        momentum = np.sum(self.masses[:, None]*v, axis=0)
        angular = np.sum(self.masses[:, None]*np.cross(r, v), axis=0)
        center = np.average(r, weights=self.masses, axis=0)
        return float(kinetic+potential), momentum, angular, center

    def integrate(self, state, times, rtol=1e-11, atol=1e-13):
        unpack(state)
        times = np.asarray(times, dtype=float)
        if (times.ndim != 1 or len(times)<2 or not np.all(np.isfinite(times))
                or np.any(np.diff(times)<=0)):
            raise ValueError('times must be finite and strictly increasing')
        result = solve_ivp(self.rhs, (times[0], times[-1]), state, t_eval=times,
                           method='DOP853', rtol=rtol, atol=atol)
        if not result.success or result.y.shape[1] != len(times) or not np.all(np.isfinite(result.y)):
            raise RuntimeError(result.message)
        return result.y.T


def figure_eight():
    # Simo ICs as published on Montgomery's page (SOURCE), including velocity sign.
    r = np.array([[-.97000436, .24308753, 0], [.97000436, -.24308753, 0], [0,0,0.]])
    v = np.array([[-.466203685, -.432365730, 0], [-.466203685, -.432365730, 0], [.93240737, .86473146, 0]])
    return pack(r, v)


def euler_collinear():
    # Equal masses at -1,0,1: outer acceleration 1+1/4, omega^2=5/4.
    r = np.array([[-1.,0,0], [0.,0,0], [1.,0,0]])
    omega = np.sqrt(1.25)
    v = np.cross(np.array([0.,0,omega]), r)
    return pack(r,v), omega


def verlet(model, initial, duration, steps):
    """Independent fixed-step integrator, same declared force law."""
    r, v = (x.copy() for x in unpack(initial))
    h = duration/steps
    a = model.acceleration(r)
    for _ in range(steps):
        r += h*v + .5*h*h*a
        next_a = model.acceleration(r)
        v += .5*h*(a + next_a)
        a = next_a
    return pack(r,v)


def conservation(model, trajectory, times):
    values = [model.invariants(s) for s in trajectory]
    energies = np.array([x[0] for x in values])
    p = np.array([x[1] for x in values])
    angular = np.array([x[2] for x in values])
    centers = np.array([x[3] for x in values])
    expected = centers[0] + (np.asarray(times)-times[0])[:,None]*p[0]/sum(model.masses)
    return dict(relative_energy_drift=float(np.max(abs(energies-energies[0])) / max(abs(energies[0]), 1e-15)),
        momentum_drift=float(np.max(np.linalg.norm(p-p[0], axis=1))),
        angular_momentum_drift=float(np.max(np.linalg.norm(angular-angular[0], axis=1))),
        center_of_mass_error=float(np.max(np.linalg.norm(centers-expected, axis=1))))


def validate():
    model = NewtonianControl()
    initial = figure_eight()
    times = np.linspace(0, FIGURE_EIGHT_PERIOD, 1001)
    traj = model.integrate(initial, times)
    metrics = conservation(model, traj, times)
    metrics['figure_eight_return_error'] = float(np.linalg.norm(traj[-1]-initial))
    tight = model.integrate(initial, times, rtol=1e-12, atol=1e-14)
    metrics['tolerance_refinement_difference'] = float(np.max(np.linalg.norm(traj-tight,axis=1)))
    errors = [float(np.linalg.norm(verlet(model, initial, FIGURE_EIGHT_PERIOD, n)-tight[-1])) for n in (2000,4000,8000)]
    metrics['verlet_errors'] = errors
    metrics['verlet_refinement_ratio_min'] = min(errors[0]/errors[1],errors[1]/errors[2])
    euler, omega = euler_collinear()
    t = np.linspace(0,1.,101)  # unstable orbit: bound this control to t<=1
    measured = model.integrate(euler,t)
    r0,v0 = unpack(euler)
    exact = []
    for ti in t:
        c,s=np.cos(omega*ti),np.sin(omega*ti)
        rot=np.array([[c,-s,0],[s,c,0],[0,0,1]])
        exact.append(pack(r0@rot.T,v0@rot.T))
    metrics['euler_analytic_error'] = float(np.max(np.linalg.norm(measured-np.array(exact),axis=1)))
    spatial = initial.reshape(3,6).copy()
    spatial[:,2] = [.2,-.1,.3]
    spatial[:,5] = [.05,.1,-.05]
    unequal = NewtonianControl((1.,2.,3.))
    ts = np.linspace(0,.2,101)
    metrics['unequal_mass_3d'] = conservation(unequal,unequal.integrate(spatial.ravel(),ts),ts)
    # Reproduce old force sign; it must be rejected by the attractive-orbit gate.
    try:
        from .three_body_solver import ThreeBodyPressureField
    except ImportError:
        from three_body_solver import ThreeBodyPressureField
    r,v = unpack(euler)
    old_accel = ThreeBodyPressureField().equations_of_motion(euler,0).reshape(3,6)[:,3:]
    metrics['legacy_outer_radial_acceleration'] = float(np.dot(old_accel[0],r[0]))
    limits = {'relative_energy_drift':1e-8,'momentum_drift':1e-10,
        'angular_momentum_drift':1e-9,'center_of_mass_error':1e-10,
        'figure_eight_return_error':2e-6,'tolerance_refinement_difference':1e-7,
        'euler_analytic_error':1e-8}
    checks = {k:bool(np.isfinite(metrics[k]) and metrics[k]<v) for k,v in limits.items()}
    checks['verlet_second_order'] = bool(metrics['verlet_refinement_ratio_min'] > 3.5 and errors[-1]<1e-4)
    checks['unequal_mass_3d_conservation'] = all(metrics['unequal_mass_3d'][k]<limits[k] for k in metrics['unequal_mass_3d'])
    checks['legacy_repulsion_detected'] = metrics['legacy_outer_radial_acceleration']>0
    return dict(status='PASS' if all(checks.values()) else 'FAIL',
        scope='Finite-time Newtonian control only; One-Wave source derivation and general analytic solution remain open.',
        units='dimensionless G=1; input masses; R^3; planar Euler/figure-eight fixtures explicitly restricted to z=vz=0',
        parameters=dict(masses=[1,1,1],G=1,softening=0,rtol=1e-11,atol=1e-13,
                        figure_eight_period=FIGURE_EIGHT_PERIOD,figure_eight_initial=initial.tolist()),
        source=SOURCE,limits=limits,metrics=metrics,checks=checks,
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
        source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in
            [Path(__file__),Path(__file__).with_name('three_body_solver.py'),Path(__file__).with_name('test_three_body_control.py')]})


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    result=validate()
    payload=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.write_text(payload)
    print(payload,end='')
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
