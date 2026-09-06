"""Finite-difference Hessian of G-757 E4. 14 coordinates: 7 amplitudes + 7 phases."""

from __future__ import annotations

import math
from typing import List

from e4_seven_cell import Coeff, State, e4


def pack(state: State) -> List[float]:
    return list(state.a) + list(state.phi)


def unpack(x: List[float]) -> State:
    return State(a=list(x[:7]), phi=list(x[7:]))


def hessian(state: State, coeff: Coeff = Coeff(), h: float = 1e-5) -> List[List[float]]:
    x0 = pack(state)
    n = 14
    H = [[0.0] * n for _ in range(n)]

    def f(x: List[float]) -> float:
        return e4(unpack(x), coeff)["total"]

    for i in range(n):
        for j in range(i, n):
            if i == j:
                xp = x0[:]; xm = x0[:]
                xp[i] += h; xm[i] -= h
                val = (f(xp) - 2.0 * f(x0) + f(xm)) / (h * h)
            else:
                xpp = x0[:]; xpm = x0[:]; xmp = x0[:]; xmm = x0[:]
                xpp[i] += h; xpp[j] += h
                xpm[i] += h; xpm[j] -= h
                xmp[i] -= h; xmp[j] += h
                xmm[i] -= h; xmm[j] -= h
                val = (f(xpp) - f(xpm) - f(xmp) + f(xmm)) / (4.0 * h * h)
            H[i][j] = H[j][i] = val
    return H


def eigenvalues(H: List[List[float]]) -> List[float]:
    n = len(H)
    a = [row[:] for row in H]
    for _ in range(80 * n * n):
        best = 0.0
        p = q = 0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > best:
                    best = abs(a[i][j])
                    p, q = i, j
        if best < 1e-12:
            break
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        tau = (aqq - app) / (2.0 * apq)
        t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau * tau))
        c = 1.0 / math.sqrt(1.0 + t * t)
        s = t * c
        for k in range(n):
            if k != p and k != q:
                akp, akq = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c * akp - s * akq
                a[k][q] = a[q][k] = s * akp + c * akq
        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0
    return sorted(a[i][i] for i in range(n))


def spectrum_receipt(state: State, coeff: Coeff = Coeff()) -> dict:
    ev = eigenvalues(hessian(state, coeff))
    return {
        "eigenvalues": ev,
        "n_negative": sum(1 for l in ev if l < -1e-6),
        "n_soft": sum(1 for l in ev if abs(l) <= 1e-6),
        "min": ev[0],
        "max": ev[-1],
        "energy": e4(state, coeff)["total"],
    }
