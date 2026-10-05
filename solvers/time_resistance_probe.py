"""A-114 exact-root and moving-packet timing control, not a bound clock."""
import json
import platform
import numpy as np


def branch(k, beta=.5, gamma=0.):
    b = 2 - gamma + beta * (np.cos(k) - 1)
    disc = b * b - 4 * (1 - gamma)
    # Lower-imaginary branch carries positive-k packets to increasing x.
    z = .5 * (b - np.sqrt(disc.astype(complex)))
    return z


def dispersion(k, beta, gamma):
    z = branch(np.array(k), beta, gamma)
    if abs(z.imag) < 1e-12:
        raise ValueError("no oscillatory branch at this k")
    omega = -np.angle(z)
    h = 1e-6
    vg = (-np.angle(branch(np.array(k+h), beta, gamma)) + np.angle(branch(np.array(k-h), beta, gamma))) / (2*h)
    return float(omega), float(vg), float(-np.log(abs(z)))


def run(k0, gamma, width=24., beta=.5, sites=1024, steps=240):
    x = np.arange(sites)
    ks = 2*np.pi*np.fft.fftfreq(sites)
    omega, vg, decay = dispersion(k0, beta, gamma)
    initial = np.exp(-.5*((x-sites/4)/width)**2 + 1j*k0*x)
    spectrum = np.fft.fft(initial)
    roots = branch(ks, beta, gamma)
    prev = np.fft.ifft(spectrum/roots)
    psi = initial.copy()
    centers, signals, amplitudes = [], [], []
    coefficient = 2-gamma+beta*(np.cos(ks)-1)
    residual = float(abs(branch(np.array(k0),beta,gamma)**2 - (2-gamma+beta*(np.cos(k0)-1))*branch(np.array(k0),beta,gamma) + 1-gamma))
    for n in range(steps+1):
        density = abs(psi)**2
        center = np.angle(np.sum(density*np.exp(2j*np.pi*x/sites)))*sites/(2*np.pi)
        if center < 0:
            center += sites
        centers.append(center)
        # Spectral interpolation at actual packet centroid, without recentering dynamics.
        signals.append(np.sum(np.fft.fft(psi)*np.exp(1j*ks*center))/sites)
        amplitudes.append(float(np.linalg.norm(psi)))
        if n < steps:
            # Execute nearest-neighbor recurrence in real space, independently of roots.
            nxt=(2-gamma)*psi-(1-gamma)*prev+beta*(.5*(np.roll(psi,1)+np.roll(psi,-1))-psi)
            prev,psi=psi,nxt
    times=np.arange(steps+1)
    measured_v=float(np.polyfit(times,centers,1)[0])
    measured_phase_rate=float(-np.polyfit(times,np.unwrap(np.angle(signals)),1)[0])
    measured_decay=float(-np.polyfit(times,np.log(amplitudes),1)[0])
    # Independently execute single carrier recurrence and read temporal phase.
    z=branch(np.array(k0),beta,gamma)
    q,old=1+0j,1/z
    trace=[]
    for n in times:
        trace.append(q)
        q,old=(2-gamma+beta*(np.cos(k0)-1))*q-(1-gamma)*old,q
    carrier_omega=float(-np.polyfit(times,np.unwrap(np.angle(trace)),1)[0])
    c_longwave=np.sqrt(beta/2)
    phase_ratio=(omega-k0*vg)/omega
    # Comparator is not inserted into the evolving dynamics.
    target=float(np.sqrt(max(0.,1-(vg/c_longwave)**2))) if abs(vg)<=c_longwave else None
    return {"k":k0,"gamma":gamma,"beta":beta,"sites":sites,"steps":steps,"width":width,
            "omega_exact":omega,"omega_measured":carrier_omega,"group_speed_exact":vg,
            "group_speed_measured":measured_v,"amplitude_decay_exact":decay,"amplitude_decay_measured":measured_decay,
            "moving_phase_rate_exact":omega-k0*vg,"moving_phase_rate_measured":measured_phase_rate,
            "carrier_moving_phase_ratio":phase_ratio,"longwave_speed":float(c_longwave),
            "lorentz_comparator_at_longwave_speed":target,"root_residual":residual,
            "packet_speed_error":abs(measured_v-vg),"moving_phase_rate_error":abs(measured_phase_rate-(omega-k0*vg)),
            "carrier_frequency_error":abs(carrier_omega-omega),"decay_error":abs(measured_decay-decay)}


def report():
    runs=[run(k,gamma) for k in (.5,1.,1.5) for gamma in (0.,.05,.1)]
    checks={"root_equation":all(r['root_residual']<1e-12 for r in runs),
            "carrier_frequency":all(r['carrier_frequency_error']<1e-10 for r in runs),
            "packet_group_speed":all(r['packet_speed_error']<.003 for r in runs),
            "moving_phase":all(r['moving_phase_rate_error']<.003 for r in runs),
            "amplitude_decay":all(r['decay_error']<1e-6 for r in runs)}
    return {"scope":"one-dimensional linear A-114 propagation control; no bound clock or native 3D model",
            "reference_main":"a7a1b0bea412600edaed60b374a38d85c2343f4e",
            "environment":{"python":platform.python_version(),"numpy":np.__version__},
            "checks":checks,"all_pass":all(checks.values()),"runs":runs,
            "interpretation":["Resistance/change interpretation is a hypothesis owned by E-533.",
             "gamma is memory damping in this run, not an established measure of all transport difficulty Xi.",
             "Moving carrier phase is omega-k*v_g, a transport observable; it is not proper time of a self-held clock.",
             "No Lorentz factor or remaining-capacity law was inserted in the recurrence.",
             "The longwave speed sqrt(beta/2) and structural front ceiling 1 are distinct dimensionless controls.",
             "Changing damping changes decay and dispersion, but does not derive a universal timing law.",
             "Energy removed by damping has no retained receiving field here; this is not a closed superfluid energy model.",
             "Next: evolve a self-held periodic excitation and compare internal recurrence, motion and reversible work under one native coupled law."]}


if __name__=='__main__':
    r=report()
    print(json.dumps(r,indent=2))
    raise SystemExit(0 if r['all_pass'] else 1)
