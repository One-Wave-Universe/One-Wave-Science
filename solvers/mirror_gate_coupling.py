"""Conservative boundary coupling witness, not a microscopic One-Wave derivation.

All ports are exterior/tangential response modes. No penetration port exists.
Amplitudes are flux normalized; generator and interaction time are dimensionless.
"""
import numpy as np

CHANNELS = ("reflection", "deflection", "roll_off", "scattering")


def operator(generator, interaction_time=1.0):
    h = np.asarray(generator, dtype=complex)
    if h.shape != (4, 4) or not np.isfinite(h).all():
        raise ValueError("Expected a finite four-channel generator")
    if not np.isfinite(interaction_time) or not np.allclose(h, h.conj().T, atol=1e-12, rtol=0):
        raise ValueError("Conservative witness requires a Hermitian generator and finite time")
    eigenvalues, eigenvectors = np.linalg.eigh(h)
    return (eigenvectors * np.exp(-1j * eigenvalues * interaction_time)) @ eigenvectors.conj().T


def respond(generator, incident, interaction_time=1.0):
    a = np.asarray(incident, dtype=complex)
    if a.shape != (4,) or not np.isfinite(a).all():
        raise ValueError("Expected four finite flux-normalized incident amplitudes")
    b = operator(generator, interaction_time) @ a
    power_in = float(np.vdot(a, a).real)
    power_out = float(np.vdot(b, b).real)
    return {"channels": dict(zip(CHANNELS, np.abs(b) ** 2)),
            "amplitudes": b, "power_in": power_in, "power_out": power_out,
            "ledger_residual": power_in - power_out,
            "scope": "dimensionless closed conservative witness; no physical calibration"}
