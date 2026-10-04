"""Joint four-interaction linear-response candidate on the native FCC12 shell.

No particle target inputs or physical energy conversion. This is a reflecting
cavity response control, not a self-localized knot or a quark mass prediction.
W and all constitutive coefficients are declared candidate inputs.
"""
from dataclasses import dataclass
from itertools import product
import warnings
import numpy as np
from scipy.linalg import LinAlgWarning, eigh, solve

ROLES = ("knot", "electrical_shell", "mirror", "weave")
OFFSETS = tuple(p for p in product((-1, 0, 1), repeat=3)
                if sum(x*x for x in p) == 2)


@dataclass(frozen=True)
class Coefficients:
    spatial: tuple = (1.0, 0.8, 1.2, 0.6)
    cross: float = 0.12
    phase_lock: float = 0.04
    work_unit: float = 1.0
    port_coupling: float = 0.25


def cycle_laplacian():
    incidence = np.zeros((4, 4))
    for i in range(4):
        incidence[i, i] = 1; incidence[i, (i+1) % 4] = -1
    return incidence.T @ incidence


class JointResponse:
    def __init__(self, radius=1.01, coefficients=Coefficients(), spacing=1.0):
        if not np.isfinite(radius) or not np.isfinite(spacing) or spacing <= 0 or not 1 <= radius/spacing <= 3.1:
            raise ValueError("Use a finite radius spanning 1..3.1 positive lattice spacings")
        c = coefficients
        values = np.array([*c.spatial, c.cross, c.phase_lock, c.work_unit, c.port_coupling])
        if len(c.spatial) != 4 or not np.isfinite(values).all() or min(c.spatial) <= 0 or c.cross < 0 or c.phase_lock < 0 or c.work_unit <= 0 or c.port_coupling <= 0:
            raise ValueError("Positive spatial/work/port and nonnegative cross/phase coefficients required")
        self.coefficients = c
        self.spacing = spacing
        self.radius = radius
        # Four sites in an FCC cubic cell of side sqrt(2)*spacing.
        self.cell_volume = spacing**3/np.sqrt(2)
        extent = int(np.ceil(radius/spacing*np.sqrt(2)))
        self.sites = tuple(p for p in product(range(-extent, extent+1), repeat=3)
                           if sum(p) % 2 == 0 and sum(x*x for x in p) <= 2*(radius/spacing)**2+1e-12)
        self.xyz = spacing*np.array(self.sites, float)/np.sqrt(2)
        index = {p: i for i, p in enumerate(self.sites)}
        self.edges = []
        self.neighbors = [[] for _ in self.sites]
        lap = np.zeros((len(self.sites), len(self.sites)))
        for i, p in enumerate(self.sites):
            for offset in OFFSETS:
                neighbor = tuple(p[k]+offset[k] for k in range(3))
                j = index.get(neighbor)
                if j is not None and i < j:
                    self.edges.append((i, j))
                    self.neighbors[i].append(j); self.neighbors[j].append(i)
                    lap[i, i] += 1; lap[j, j] += 1
                    lap[i, j] -= 1; lap[j, i] -= 1
        self.laplacian = lap
        phase = cycle_laplacian()
        self.interaction_block = np.diag(c.spatial) + c.cross*phase
        # Missing exterior bonds are absent: no geometric penetration links.
        # Local relative-phase lock is a declared candidate, not a scalar gap.
        unit = c.work_unit*self.cell_volume
        self.H = unit*(np.kron(lap/(12*spacing**2), self.interaction_block) + np.kron(np.eye(len(self.sites)), c.phase_lock*phase))
        self.W = unit*np.eye(len(self.H))
        self.boundary_sites = [i for i, n in enumerate(self.neighbors) if len(n) < 12]
        self.port_site = max(self.boundary_sites, key=lambda i: tuple(self.xyz[i]))
        self.boundary = np.arange(4*self.port_site, 4*self.port_site+4)
        self.interior = np.array([i for i in range(len(self.H)) if i not in self.boundary])
        self.B = np.eye(len(self.H))[:, self.boundary]*c.port_coupling*np.sqrt(unit)
        self.eigenvalues, self.modes = eigh(self.H, self.W)
        self.eigenvalues[np.abs(self.eigenvalues) < 1e-12] = 0

    def stable_dt(self, fraction=0.5):
        if not 0 < fraction < 1:
            raise ValueError("Use a timestep strictly inside the stability interval")
        return fraction*2/np.sqrt(self.eigenvalues.max())

    def step_metric(self, dt):
        if not np.isfinite(dt) or dt <= 0 or dt*dt*self.eigenvalues.max() >= 4:
            raise ValueError("Timestep violates positive-energy stability condition")
        return self.W-dt*dt*self.H/4

    def advance(self, previous, current, dt):
        self.step_metric(dt)
        return 2*current-previous-dt*dt*(self.H @ current)/self.W[0, 0]

    def energy(self, previous, current, dt):
        velocity = (current-previous)/dt
        midpoint = (current+previous)/2
        return float((velocity @ self.step_metric(dt) @ velocity + midpoint @ self.H @ midpoint)/2)

    def mechanical_schur(self, z):
        d = self.H-z*self.W
        b, i = self.boundary, self.interior
        ii, ib = d[np.ix_(i, i)], d[np.ix_(i, b)]
        return d[np.ix_(b, b)]-d[np.ix_(b, i)] @ solve(ii, ib, assume_a="sym")

    def boundary_inertia(self):
        b, i = self.boundary, self.interior
        ii = self.H[np.ix_(i, i)]
        minimum = float(eigh(ii, eigvals_only=True)[0])
        if minimum <= 1e-12:
            raise ValueError("Boundary does not anchor every free internal direction")
        t = np.zeros((len(self.H), 4)); t[b] = np.eye(4)
        t[i] = -solve(ii, self.H[np.ix_(i, b)], assume_a="pos")
        return {"stiffness": t.T @ self.H @ t, "inertia": t.T @ self.W @ t,
                "embedding": t, "internal_min_eigenvalue": minimum}

    def scatter(self, omega, incident=None, internal_damping=0.0):
        if not np.isfinite(omega) or omega <= 0 or not np.isfinite(internal_damping) or internal_damping < 0:
            raise ValueError("Positive frequency and nonnegative finite damping required")
        damping = internal_damping*self.W
        d = self.H-omega*omega*self.W-1j*omega*(self.B @ self.B.T+damping)
        # A dark mode can make the full lossless resolvent singular although
        # its observable-port limit exists. Do not silently add damping.
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error", LinAlgWarning)
                response = solve(d, self.B, assume_a="gen")
        except (LinAlgWarning, np.linalg.LinAlgError) as exc:
            raise ValueError("Unresolved singular lossless frequency; detune or derive the observable-subspace limit") from exc
        residual = np.linalg.norm(d @ response-self.B)/(np.linalg.norm(d)*np.linalg.norm(response)+np.linalg.norm(self.B))
        if not np.isfinite(response).all() or residual > 1e-10:
            raise ValueError("Frequency solve did not meet its residual tolerance")
        s = np.eye(4)+2j*omega*self.B.T @ response
        a = np.array([1, 0, 0, 0], complex) if incident is None else np.asarray(incident, complex)
        if a.shape != (4,) or not np.isfinite(a).all():
            raise ValueError("Four finite flux-normalized incident amplitudes required")
        q = response @ a; out = s @ a
        pin = float(np.vdot(a, a).real); pout = float(np.vdot(out, out).real)
        loss = float(4*omega*omega*np.vdot(q, damping @ q).real)
        return {"S": s, "output": out, "power_in": pin, "power_out": pout,
                "internal_loss": loss, "ledger_residual": pin-pout-loss,
                "solve_residual": float(residual)}

    def mode_gradients(self, mode_index):
        if not 0 <= mode_index < len(self.eigenvalues):
            raise ValueError("Invalid mode index")
        profile = self.modes[:, mode_index].reshape((-1, 4))
        derivatives = np.zeros((len(self.sites), 4, 3))
        ranks = []
        for i, neighbors in enumerate(self.neighbors):
            geometry = self.xyz[neighbors]-self.xyz[i]
            gradient, _, rank, _ = np.linalg.lstsq(geometry, profile[neighbors]-profile[i], rcond=None)
            derivatives[i] = gradient.T; ranks.append(rank)
        if min(ranks) != 3:
            raise ValueError("Native 3D derivative geometry is rank deficient")
        return derivatives.reshape((-1, 3))

    def carried_tensor(self, mode_index, dt):
        # Unit-normalized cavity eigenmode, not a self-selected particle profile.
        metric = self.step_metric(dt)
        eigenvalue = self.eigenvalues[mode_index]
        midpoint_factor = np.sqrt(1-dt*dt*eigenvalue/4)
        gradients = midpoint_factor*self.mode_gradients(mode_index)
        return gradients.T @ metric @ gradients/2  # cycle average cos² = 1/2

    def cycle_energy(self, mode_index, dt, velocity, phases=64):
        self.step_metric(dt)
        mode = self.modes[:, mode_index]
        frequency = 2*np.arcsin(dt*np.sqrt(self.eigenvalues[mode_index])/2)/dt
        gradients = self.mode_gradients(mode_index)
        energies = []
        for phase in np.linspace(0, 2*np.pi, phases, endpoint=False):
            midpoint = np.cos(phase)*np.cos(frequency*dt/2)*mode
            base = -2*np.sin(phase)*np.sin(frequency*dt/2)*mode/dt
            carried = np.cos(phase)*np.cos(frequency*dt/2)*(gradients @ np.asarray(velocity))
            flow = base-carried
            energies.append(self.energy(midpoint-dt*flow/2, midpoint+dt*flow/2, dt))
        return float(np.mean(energies))
