"""Explicit external-drive experiment for the existing bulk constitutive model.

No physical mass fit. All quantities are dimensionless. The original solver is
unchanged; the external potential and source work are declared additions.
"""
from copy import copy
import numpy as np


def force_vector(value):
    if (not isinstance(value, (list, tuple, np.ndarray)) or np.shape(value) != (3,) or
            any(not isinstance(x, (int, float, np.integer, np.floating)) or isinstance(x, (bool, np.bool_)) for x in value)):
        raise ValueError('Numeric force vector required')
    f = np.asarray(value, dtype=float)
    if f.shape != (3,) or not np.isfinite(f).all() or np.max(abs(f)) > .02:
        raise ValueError('Three finite force coefficients in [-0.02, 0.02] required')
    return f


def potential(engine, force):
    f = force_vector(force)
    wave = 2*np.pi/(engine.side*engine.spacing/np.sqrt(2))
    return -np.sin(wave*engine.xyz) @ f/wave


def driven_step(engine, field, dt, force):
    phase = np.exp(-.5j*dt*potential(engine, force))[:, None]
    return phase*engine.step(phase*field, dt)


def external_energy(engine, field, force):
    n = np.sum(abs(field)**2, axis=1)
    return float(engine.volume*np.dot(potential(engine, force), n))


def applied_force(engine, field, force):
    wave = 2*np.pi/(engine.side*engine.spacing/np.sqrt(2))
    n = np.sum(abs(field)**2, axis=1)
    return engine.volume*(n @ np.cos(wave*engine.xyz))*force_vector(force)


def centroid_chart(engine, field, previous=None):
    """Ordinary weighted centroid in a circularly selected, unwrapped chart.

    The circular mean is not used as the dynamical centroid. Concentration and
    seam criteria are declared conservative reporting policies, not laws.
    """
    n = np.sum(abs(field)**2, axis=1)
    total = np.sum(n)
    if not np.isfinite(n).all() or total <= 0:
        raise ValueError('Finite nonzero field norm required')
    box = engine.side*engine.spacing/np.sqrt(2)
    moment = n @ np.exp(2j*np.pi*engine.xyz/box)/total
    concentration = abs(moment)
    anchor = np.angle(moment)*box/(2*np.pi)
    if previous is not None:
        anchor += box*np.round((np.asarray(previous)-anchor)/box)
    relative = (engine.xyz-anchor+box/2) % box-box/2
    chart = anchor+relative
    center = (n @ chart)/total
    seam = float(np.sum(n[np.any(abs(relative) > box/2-engine.spacing/np.sqrt(2), axis=1)])/total)
    reasons = []
    if np.min(concentration) < .5:
        reasons.append('circular concentration below 0.5')
    if seam > .01:
        reasons.append('more than 1% norm near the chart seam')
    if previous is not None and np.max(abs(center-previous)) >= box/4:
        reasons.append('internal-step motion exceeds a quarter box')
    return {'valid': not reasons, 'reason': '; '.join(reasons),
            'position': center.tolist() if not reasons else None,
            'concentration': concentration.tolist(), 'seam_fraction': seam,
            'branch_uncertainty': box*seam}


def prepare_linear_packet(engine, norm=1., width=3.):
    """Project a Gaussian onto the lowest band without deleting FCC aliases."""
    if engine.c.focusing or engine.c.saturation:
        raise ValueError('Lowest-band control requires the linear model')
    if not np.isfinite(norm) or norm <= 0 or not np.isfinite(width) or width <= 0:
        raise ValueError('Positive finite norm and width required')
    envelope = np.exp(-np.sum(engine.xyz**2, axis=1)/(2*width**2))
    seed = envelope[:, None]*np.ones((1, 4))/2
    transformed = np.fft.fftn(engine.full(seed), axes=(0, 1, 2))
    vector = engine.basis[..., :, 0]
    projected = vector*np.sum(vector.conj()*transformed, axis=-1)[..., None]
    full = np.fft.ifftn(projected, axes=(0, 1, 2))
    leakage = float(np.linalg.norm(full[~engine.mask])/max(np.linalg.norm(full), 1e-30))
    if leakage > 1e-10:
        raise ValueError('Projection failed FCC parity/alias invariance')
    field = full[engine.mask]
    return field*np.sqrt(norm/engine.norm(field)), leakage


class DrivenBulk:
    def __init__(self, engine, field):
        self.engine = engine
        self.force = np.zeros(3)
        self.switch_work = self.intervention_work = 0.
        self.initial_energy = engine.energy(field)
        self.initial_norm = engine.norm(field)
        self.chart = centroid_chart(engine, field)
        self.initial_center = self.chart['position']
        self.initial_branch_uncertainty = self.chart['branch_uncertainty']
        self.tracking_valid = self.chart['valid']
        self.time = 0.
        self.max_balance_error = 0.
        self.max_norm_error = 0.
        self.events = []

    def fork(self):
        result = copy(self)
        result.force = self.force.copy()
        result.chart = dict(self.chart)
        result.events = list(self.events)
        return result

    def total_energy(self, field):
        return self.engine.energy(field)+external_energy(self.engine, field, self.force)

    def set_force(self, field, force):
        force = force_vector(force)
        if len(self.events) >= 64:
            raise ValueError('64 intervention events reached; export and reset')
        old = self.force.copy()
        energy_before = self.total_energy(field)
        delta = external_energy(self.engine, field, force)-external_energy(self.engine, field, self.force)
        self.switch_work += delta
        self.force = force.copy()
        self.events.append({'kind': 'force_switch', 'time': self.time, 'old_force': old.tolist(),
                            'new_force': force.tolist(), 'density': np.sum(abs(field)**2, axis=1).tolist(),
                            'work': delta, 'energy_before': energy_before, 'energy_after': self.total_energy(field)})
        self.observe(field)
        return delta

    def observe(self, field):
        balance = self.total_energy(field)-self.initial_energy-self.switch_work-self.intervention_work
        self.max_balance_error = max(self.max_balance_error, abs(balance))
        self.max_norm_error = max(self.max_norm_error, abs(self.engine.norm(field)/self.initial_norm-1))

    def update_chart(self, field):
        previous = self.chart['position'] if self.tracking_valid else None
        chart = centroid_chart(self.engine, field, previous)
        self.tracking_valid = self.tracking_valid and chart['valid']
        if not self.tracking_valid:
            chart['valid'] = False
            chart['position'] = None
            chart['reason'] = chart['reason'] or 'tracking lost earlier; reset to establish a new chart'
        self.chart = chart

    def advance(self, field, dt):
        updated = driven_step(self.engine, field, dt, self.force)
        self.update_chart(updated)  # every internal step, never only rendered frames
        self.time += dt
        self.observe(updated)
        return updated

    def intervention(self, before, after, shift):
        if len(self.events) >= 64:
            raise ValueError('64 intervention events reached; export and reset')
        delta = self.total_energy(after)-self.total_energy(before)
        self.intervention_work += delta
        self.events.append({'kind': 'imposed_translation', 'time': self.time, 'work': delta,
                            'shift_in_lattice_indices': list(shift),
                            'force': self.force.tolist(),
                            'before_density': np.sum(abs(before)**2, axis=1).tolist(),
                            'after_density': np.sum(abs(after)**2, axis=1).tolist(),
                            'internal_energy_change': self.engine.energy(after)-self.engine.energy(before),
                            'energy_before': self.total_energy(before), 'energy_after': self.total_energy(after)})
        self.update_chart(after)
        self.observe(after)

    def measurements(self, field):
        centroid = dict(self.chart)
        displacement = None
        if self.tracking_valid and self.initial_center is not None:
            displacement = (np.asarray(centroid['position'])-self.initial_center).tolist()
        centroid['displacement'] = displacement
        centroid['displacement_branch_uncertainty'] = centroid['branch_uncertainty']+self.initial_branch_uncertainty
        centroid['geometrically_resolved'] = bool(displacement is not None and np.linalg.norm(displacement) > 10*centroid['displacement_branch_uncertainty'])
        centroid['temporal_refinement'] = 'not established by one interactive run'
        total = self.total_energy(field)
        return {'initial_energy': self.initial_energy, 'initial_norm': self.initial_norm,
                'initial_center': self.initial_center, 'initial_branch_uncertainty': self.initial_branch_uncertainty,
                'protocol_events': list(self.events), 'force_coefficients': self.force.tolist(), 'applied_force': applied_force(self.engine, field, self.force).tolist(),
                'external_energy': external_energy(self.engine, field, self.force), 'total_energy': total,
                'switch_work': self.switch_work, 'intervention_work': self.intervention_work,
                'energy_balance_residual': total-self.initial_energy-self.switch_work-self.intervention_work,
                'max_balance_error': self.max_balance_error, 'max_norm_relative_error': self.max_norm_error,
                'centroid': centroid,
                'scope': 'External periodic drive of a chosen field model; no fitted inertia or physical mass'}
