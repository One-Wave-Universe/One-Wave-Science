"""Candidate reciprocal displacement/density closure on a periodic FCC lattice.

No physical calibration, particle targets, norm resets or forced boundary crossing.
Compression is constrained to -div(u); constitutive coupling is a hypothesis.
"""
import itertools
import json
import platform
import numpy as np
from scipy.sparse.linalg import LinearOperator, cg


class FCC:
    def __init__(self, side=8, spacing=1.0):
        if side < 4 or side % 2 or spacing <= 0:
            raise ValueError("side must be even >=4; spacing must be positive")
        self.side, self.spacing = side, spacing
        self.mask = np.indices((side,) * 3).sum(axis=0) % 2 == 0
        self.volume = spacing ** 3 / np.sqrt(2)
        self.offsets = []
        for zero in range(3):
            for signs in itertools.product((-1, 1), repeat=2):
                o = [0, 0, 0]
                for j, sign in zip([j for j in range(3) if j != zero], signs):
                    o[j] = sign
                self.offsets.append(tuple(o))

    def shift(self, x, o):
        return np.roll(x, tuple(-v for v in o), axis=(0, 1, 2))

    def lap(self, x):
        return (12 * x - sum(self.shift(x, o) for o in self.offsets)) / (2 * self.spacing ** 2)

    def grad(self, x):
        return sum(self.shift(x, o)[..., None] * np.array(o) / np.sqrt(2)
                   for o in self.offsets) / (4 * self.spacing)

    def div(self, u):
        return sum(np.sum(self.shift(u, o) * np.array(o) / np.sqrt(2), axis=-1)
                   for o in self.offsets) / (4 * self.spacing)

    def chi(self, u):
        return -self.div(u)

    def gauge(self, u):
        v = u.copy()
        v[self.mask] -= v[self.mask].mean(axis=0)
        v[~self.mask] = 0
        return v

    def dot(self, x, y):
        return self.volume * np.sum(x * y)

    def energy(self, psi, u, beta=1., shear=1., k=1., a=1., eta=2.):
        c, rho = self.chi(u), psi ** 2
        return .5 * beta * self.dot(psi, self.lap(psi)) + .5 * shear * self.dot(u, self.lap(u)) + self.volume * np.sum(.5 * (k + a * rho) * c ** 2 - eta * rho * c)

    def gradients(self, psi, u, beta=1., shear=1., k=1., a=1., eta=2.):
        c, rho = self.chi(u), psi ** 2
        gp = beta * self.lap(psi) + (a * c ** 2 - 2 * eta * c) * psi
        gu = shear * self.lap(u) + self.grad((k + a * rho) * c - eta * rho)
        return gp, gu

    def relax(self, rho, shear=1., k=1., a=1., eta=2.):
        if min(shear, k) <= 0 or a < 0 or np.any(rho < 0):
            raise ValueError("positive shear/k, nonnegative a/rho required")
        n = self.mask.sum() * 3
        def unpack(v):
            u = np.zeros(self.mask.shape + (3,))
            u[self.mask] = v.reshape(-1, 3)
            return u
        def apply(v):
            u = unpack(v)
            return (shear * self.lap(u) + self.grad((k + a * rho) * self.chi(u)))[self.mask].ravel()
        rhs = (eta * self.grad(rho))[self.mask].ravel()
        v, info = cg(LinearOperator((n, n), matvec=apply, dtype=float), rhs, rtol=1e-11, atol=1e-13, maxiter=3000)
        if info:
            raise RuntimeError(f"compression solve failed: {info}")
        u = self.gauge(unpack(v))
        residual = np.linalg.norm(apply(u[self.mask].ravel()) - rhs) / max(1., np.linalg.norm(rhs))
        c = self.chi(u)
        e = .5 * shear * self.dot(u, self.lap(u)) + self.volume * np.sum(.5 * (k + a * rho) * c ** 2 - eta * rho * c)
        # Envelope theorem: derivative wrt rho after constrained minimization.
        f = .5 * a * c ** 2 - eta * c
        return u, c, e, f, residual


def seed(grid):
    coordinates = np.indices(grid.mask.shape)
    d = np.minimum(coordinates, grid.side - coordinates) * grid.spacing / np.sqrt(2)
    return np.exp(-np.sum(d * d, axis=0) / 2) * grid.mask


def evolve(grid, psi, u, dt, time=4., eta=2.):
    psi, u = psi.copy(), u.copy()
    vp, vu = np.zeros_like(psi), np.zeros_like(u)
    initial = grid.energy(psi, u, eta=eta)
    max_error = 0.
    steps = round(time / dt)
    for _ in range(steps):
        gp, gu = grid.gradients(psi, u, eta=eta)
        vp -= .5 * dt * gp
        vu -= .5 * dt * gu
        psi += dt * vp
        u += dt * vu
        gp, gu = grid.gradients(psi, u, eta=eta)
        vp -= .5 * dt * gp
        vu -= .5 * dt * gu
        total = grid.energy(psi, u, eta=eta) + .5 * grid.dot(vp, vp) + .5 * grid.dot(vu, vu)
        max_error = max(max_error, abs(total - initial) / max(1., abs(initial)))
        if not np.isfinite(total):
            raise RuntimeError("nonfinite evolution")
    return {"dt": dt, "time": steps * dt, "max_scaled_energy_error": max_error,
            "peak_amplitude": float(np.max(np.abs(psi))), "compression_sum": float(np.sum(grid.chi(u))),
            "final_density_sum": float(grid.volume * np.sum(psi ** 2))}


def report():
    g = FCC()
    rng = np.random.default_rng(107)
    psi = seed(g)
    rho = psi ** 2
    u, c, energy, f, residual = g.relax(rho)
    direction = rng.normal(size=rho.shape) * rho
    eps = 1e-5
    ep = g.relax(rho + eps * direction)[2]
    em = g.relax(rho - eps * direction)[2]
    measured, predicted = (ep - em) / (2 * eps), g.dot(f, direction)
    gu = g.gauge(rng.normal(size=u.shape))
    q = rng.normal(size=rho.shape) * g.mask
    adjoint_error = abs(g.dot(g.chi(gu), q) - g.dot(gu, g.grad(q)))
    gp, gd = g.gradients(psi, u)
    dp = rng.normal(size=psi.shape) * g.mask
    du = g.gauge(rng.normal(size=u.shape))
    full_fd = (g.energy(psi + eps * dp, u + eps * du) - g.energy(psi - eps * dp, u - eps * du)) / (2 * eps)
    full_expected = g.dot(gp, dp) + g.dot(gd, du)
    ablated = g.relax(rho, eta=0.)
    uniform = g.relax(g.mask.astype(float))
    local_c = 2 * rho / (1 + rho)
    dynamics = [evolve(g, .2 * psi, np.zeros_like(u), dt) for dt in (.04, .02, .01)]
    # Native linear recurrence is recovered exactly when compression coupling is off.
    prev = .9 * psi
    beta, dt = .7, .03
    expected = 2 * psi - prev - dt ** 2 * beta * g.lap(psi)
    gp0 = g.gradients(psi, np.zeros_like(u), beta=beta, eta=0.)[0]
    actual = 2 * psi - prev - dt ** 2 * gp0
    # Conditional stationary scaling identity, not a computed lattice equilibrium.
    # V(t,s)=P t^2+U s^2+A s^2 t^2-B s t^2.
    # Stationarity implies P=2U+A, B=2(U+A).
    witness_u, witness_a = 1., .5
    scaling_hessian = np.array([[0., -4 * witness_u],
                                [-4 * witness_u, 2 * (witness_u + witness_a)]])
    scaling_det = float(np.linalg.det(scaling_hessian))
    checks = {"adjoint": adjoint_error < 1e-10, "compression_stationarity": residual < 1e-9,
              "zero_total_compression": abs(c.sum()) < 1e-10,
              "reduced_force_gradient": abs(measured-predicted) < 1e-7,
              "reciprocal_full_gradient": abs(full_fd-full_expected) < 1e-7,
              "coupling_off": np.max(np.abs(ablated[0])) == 0.,
              "uniform_density": np.max(np.abs(uniform[0])) < 1e-10,
              "canonical_linear_limit": np.max(np.abs(actual-expected)) < 1e-14,
              "timestep_convergence": dynamics[0]['max_scaled_energy_error'] > 3.5 * dynamics[1]['max_scaled_energy_error'] and dynamics[1]['max_scaled_energy_error'] > 3.5 * dynamics[2]['max_scaled_energy_error'],
              "stationary_scaling_saddle_identity": abs(scaling_det + 16 * witness_u ** 2) < 1e-12 and np.linalg.eigvalsh(scaling_hessian)[0] < 0}
    checks = {name: bool(passed) for name, passed in checks.items()}
    return {"scope": "dimensionless constitutive hypothesis; constrained compression elimination and reciprocal second-order update",
            "environment": {"python": platform.python_version(), "numpy": np.__version__},
            "parameters": {"side": 8, "sites": int(g.mask.sum()), "spacing": 1., "volume_per_site": g.volume, "beta": 1., "shear": 1., "k": 1., "a": 1., "eta": 2., "seed": 107},
            "checks": checks, "all_pass": all(checks.values()), "adjoint_error": adjoint_error,
            "stationarity_relative_residual": residual, "total_compression": float(c.sum()),
            "compression_min": float(c.min()), "compression_max": float(c.max()),
            "reduced_energy": float(energy), "reduced_force_gradient_error": abs(measured-predicted),
            "full_force_gradient_error": abs(full_fd-full_expected),
            "invalid_local_compression_sum": float(local_c.sum()), "dynamics": dynamics,
            "stationary_scaling_result": {"scope": "conditional analytic theorem for this real unconstrained law; witness is not a solved lattice state", "hessian_determinant": "-16 U^2", "witness_U": witness_u, "witness_A": witness_a, "witness_hessian": scaling_hessian.tolist(), "witness_eigenvalues": np.linalg.eigvalsh(scaling_hessian).tolist(), "consequence": "Every stationary state with nonzero gauge-fixed displacement is an energy saddle; stable static localization is excluded. Time-periodic excitations are not ruled out."},
            "limits": ["Coupling eta and density-dependent stiffness a are assumptions, not derived constants.", "No localization, vortex, four-interaction necessity, mass or physical calibration claim.", "Periodic finite FCC; no HCP, 2D comparison, detector, spatial/domain convergence or dynamic compression elimination validation.", "Central divergence has high-frequency blind modes; positive bond shear regularizes displacement solve.", "Density psi^2 is not conserved by this real second-order update.", "Static elimination is a zero-frequency approximation; full displacement dynamics are retained in evolution."]}


if __name__ == '__main__':
    result = report()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['all_pass'] else 1)
