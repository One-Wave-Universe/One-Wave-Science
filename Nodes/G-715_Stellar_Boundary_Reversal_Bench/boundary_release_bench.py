"""Two-layer boundary-release toy bench for Node G-715 (Stellar Boundary Reversal).

This is a YELLOW numerical toy, not a validated solar model. It uses
dimensionless model units, not measured solar parameters (photosphere
~5800 K, corona ~1-3 MK are the real numbers; this bench does not try to
reproduce them quantitatively).

Question this bench asks, per G-715 section 13 ("Test / Simulation
direction"):

    Can a dense boundary layer remain cooler while a thin outer layer
    becomes hotter, when wave/magnetic release is deposited above the
    boundary rather than delivered as ordinary conduction?

Two compartments:

    Layer A ("surface"): dense, high radiative-loss boundary hold.
    Layer B ("corona"):  thin, low radiative-loss release layer.

Two modes:

    "control"    - only ordinary conduction links the layers
                   (Q ~ k_cond * (T_s - T_cor)). Conduction can only move
                   heat from hot to cold, so this mode cannot produce
                   T_cor > T_s except as a transient -- it is the naive
                   "core hot -> surface cooler -> outer atmosphere
                   cooler" expectation from G-715 section 2.
    "hypothesis" - a fraction of the interior input bypasses layer A as
                   a release channel (wave/magnetic tension) and is
                   deposited directly into layer B, per G-715's
                   Hold -> Fold -> Release -> Heat -> Flow chain.

The bench does not derive the release fraction, k_rad_s, k_rad_cor, or
k_wind from any first-principles MHD/Alfven-wave calculation. They are
chosen to give layer A a high radiative coupling (dense boundary) and
layer B a low radiative coupling (thin plasma), which is the qualitative
structure G-715 section 10 already argues for. This bench only checks
that the resulting two-compartment system is thermodynamically
self-consistent (energy is conserved, a steady state exists) and that
the control case cannot fake the reversal.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    # Heat capacities per unit area (arbitrary model units).
    c_s: float = 40.0     # dense boundary layer: large heat capacity
    c_cor: float = 0.5    # thin release layer: small heat capacity

    # Steady interior input reaching the boundary.
    q_interior: float = 6.0

    # Radiative loss coefficients: loss = k_rad * T^4.
    k_rad_s: float = 4.0e-6     # dense layer: strong radiative coupling
    k_rad_cor: float = 2.0e-9   # thin layer: weak radiative coupling

    # Corona-only extra loss (represents solar-wind / expansion loss),
    # linear in T so it remains bounded and does not require T^4 to win.
    k_wind: float = 0.02

    # Ordinary conduction coefficient linking the two layers.
    k_cond: float = 0.8

    # Fraction of q_interior diverted into the release channel in
    # "hypothesis" mode. 0.0 must reduce hypothesis mode to the same
    # shape as control mode (see test_release_zero_matches_control).
    release_fraction: float = 0.6

    # Initial temperatures (arbitrary model units, not kelvin).
    t_s0: float = 1.0
    t_cor0: float = 1.0

    dt: float = 0.01
    steps: int = 200_000


@dataclass(frozen=True)
class Result:
    t_s: float
    t_cor: float
    t_s_series: list
    t_cor_series: list
    energy_in: float
    energy_out: float
    energy_stored: float


def _derivatives(t_s: float, t_cor: float, cfg: Config, mode: str):
    """Return (dT_s/dt, dT_cor/dt, loss_s, loss_cor, release_or_cond)."""
    loss_s = cfg.k_rad_s * t_s**4
    loss_cor = cfg.k_rad_cor * t_cor**4 + cfg.k_wind * t_cor

    if mode == "control":
        transfer = cfg.k_cond * (t_s - t_cor)  # surface -> corona only
        d_s = (cfg.q_interior - transfer - loss_s) / cfg.c_s
        d_cor = (transfer - loss_cor) / cfg.c_cor
    elif mode == "hypothesis":
        release = cfg.release_fraction * cfg.q_interior
        surface_input = cfg.q_interior - release
        d_s = (surface_input - loss_s) / cfg.c_s
        d_cor = (release - loss_cor) / cfg.c_cor
        transfer = release
    else:
        raise ValueError(f"unknown mode: {mode!r}")

    return d_s, d_cor, loss_s, loss_cor, transfer


def simulate(cfg: Config, mode: str, record_every: int = 1000) -> Result:
    """Advance the two-layer system with forward Euler and return a Result.

    Also accumulates an explicit energy ledger (input, radiated/wind
    losses, and stored heat) so conservation can be checked directly
    rather than assumed.
    """
    t_s, t_cor = cfg.t_s0, cfg.t_cor0
    t_s_series = [t_s]
    t_cor_series = [t_cor]

    energy_in = 0.0
    energy_out = 0.0

    for step in range(cfg.steps):
        d_s, d_cor, loss_s, loss_cor, _transfer = _derivatives(t_s, t_cor, cfg, mode)

        energy_in += cfg.q_interior * cfg.dt
        energy_out += (loss_s + loss_cor) * cfg.dt

        t_s = t_s + d_s * cfg.dt
        t_cor = t_cor + d_cor * cfg.dt

        if (step + 1) % record_every == 0:
            t_s_series.append(t_s)
            t_cor_series.append(t_cor)

    energy_stored = cfg.c_s * (t_s - cfg.t_s0) + cfg.c_cor * (t_cor - cfg.t_cor0)

    return Result(
        t_s=t_s,
        t_cor=t_cor,
        t_s_series=t_s_series,
        t_cor_series=t_cor_series,
        energy_in=energy_in,
        energy_out=energy_out,
        energy_stored=energy_stored,
    )


def is_steady(cfg: Config, t_s: float, t_cor: float, mode: str, tol: float = 1e-6) -> bool:
    d_s, d_cor, *_ = _derivatives(t_s, t_cor, cfg, mode)
    return abs(d_s) < tol and abs(d_cor) < tol


if __name__ == "__main__":
    cfg = Config()
    for mode in ("control", "hypothesis"):
        result = simulate(cfg, mode)
        steady = is_steady(cfg, result.t_s, result.t_cor, mode)
        balance = result.energy_in - result.energy_out - result.energy_stored
        print(
            f"[{mode:10s}] T_s={result.t_s:10.4f}  T_cor={result.t_cor:10.4f}  "
            f"T_cor>T_s={result.t_cor > result.t_s}  steady={steady}  "
            f"energy_balance_residual={balance:.6g}"
        )
