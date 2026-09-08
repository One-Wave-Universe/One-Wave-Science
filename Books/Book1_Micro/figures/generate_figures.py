#!/usr/bin/env python3
"""Generate one illustrative SVG figure per Book1_Micro chapter.

Style: One-Wave brand palette (dark navy ink, cyan wave, gold accent, purple
secondary) on a clean white/paper background so the figures read well in
plain markdown viewers (GitHub, PDF export) without a dark-mode dependency.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, Wedge
import os
import textwrap

OUT = "" + os.path.dirname(os.path.abspath(__file__)) + ""
os.makedirs(OUT, exist_ok=True)

INK = "#0d1b2a"
CYAN = "#1a8fa3"
GOLD = "#c9821c"
PURPLE = "#7c3fbf"
GRID = "#d8dee3"
BG = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.facecolor": BG,
    "figure.facecolor": BG,
    "savefig.facecolor": BG,
})


def new_fig(figsize=(6.2, 3.6)):
    fig, ax = plt.subplots(figsize=figsize, dpi=140)
    ax.set_facecolor(BG)
    return fig, ax


def finish(fig, ax, name, title, xlabel="", ylabel="", legend=False, grid=True):
    if grid:
        ax.grid(True, color=GRID, linewidth=0.7, alpha=0.9)
    wrapped = "\n".join(textwrap.wrap(title, width=44))
    ax.set_title(wrapped, fontsize=11.5, color=INK, weight="bold", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    if legend:
        ax.legend(frameon=False, fontsize=9, loc="best")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.svg", format="svg")
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------------------
# Ch01 - Persistent Mode: recursive update settles into a stable oscillation
# ---------------------------------------------------------------------------
def ch01():
    n = np.arange(0, 120)
    gamma, beta = 0.06, 0.18
    psi = np.zeros(len(n))
    psi[0], psi[1] = 1.0, 0.85
    drive = 0.9
    for i in range(2, len(n)):
        psi[i] = psi[i-1] + (1-gamma)*(psi[i-1]-psi[i-2]) + beta*(drive*np.cos(0.5*i) - psi[i-1])
    fig, ax = new_fig()
    ax.plot(n, psi, color=CYAN, lw=1.8)
    ax.axhline(0, color=GRID, lw=1)
    env = np.abs(psi[40:]).max()
    ax.fill_between(n[40:], -env, env, color=GOLD, alpha=0.12, label=r"stability band $\|\psi_{n+k}-\psi_n\|<\epsilon$")
    ax.set_ylim(-2.2, 2.2)
    finish(fig, ax, "ch01_persistent_mode",
           "A Persistent Mode: recursive update settles into a stable pattern",
           "update step  n", r"field value  $\psi_n$", legend=True)

# ---------------------------------------------------------------------------
# Ch02 - Proton: three-vortex knot, triangular coupling
# ---------------------------------------------------------------------------
def ch02():
    fig, ax = new_fig((5.6, 5.2))
    R = 1.0
    centers = [(R*np.cos(a), R*np.sin(a)) for a in (np.pi/2, np.pi/2+2*np.pi/3, np.pi/2+4*np.pi/3)]
    colors = [CYAN, GOLD, PURPLE]
    for (cx, cy), c in zip(centers, colors):
        t = np.linspace(0, 2*np.pi, 200)
        rad = 0.55
        ax.plot(cx+rad*np.cos(t), cy+rad*np.sin(t), color=c, lw=2.2)
        k = 14
        ta = np.linspace(0, 2*np.pi, k, endpoint=False)
        ax.quiver(cx+rad*np.cos(ta), cy+rad*np.sin(ta),
                   -np.sin(ta), np.cos(ta), color=c, scale=9, width=0.006)
    for i in range(3):
        x0, y0 = centers[i]
        x1, y1 = centers[(i+1) % 3]
        ax.plot([x0, x1], [y0, y1], color=INK, lw=1.1, ls="--", alpha=0.6)
    ax.set_xlim(-2.1, 2.1); ax.set_ylim(-2.1, 2.1)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.text(0, -1.9, "three circulating vortex loops, pressure-coupled at 120°", ha="center", fontsize=9.5, color=INK)
    finish(fig, ax, "ch02_three_vortex_knot",
           "The Proton: a three-vortex knot bound by mutual pressure coupling",
           grid=False)

# ---------------------------------------------------------------------------
# Ch03 - Scale invariance: same normalized waveform at nested scales
# ---------------------------------------------------------------------------
def ch03():
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.2), dpi=140, sharey=True)
    x = np.linspace(0, 2, 300)
    y = np.sin(2*np.pi*x) * np.exp(-0.25*x)
    scales = [("cell scale", "10 nm", PURPLE), ("organ scale", "1 mm", CYAN), ("body scale", "1 m", GOLD)]
    for ax, (lab, unit, c) in zip(axes, scales):
        ax.set_facecolor(BG)
        ax.plot(x, y, color=c, lw=2.2)
        ax.fill_between(x, 0, y, color=c, alpha=0.12)
        ax.axhline(0, color=GRID, lw=0.8)
        ax.set_title(f"{lab}\n(wavelength ≈ {unit})", fontsize=9.5, color=INK)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
    fig.suptitle("\n".join(textwrap.wrap(
        "Scale Invariance: the identical normalized pattern recurs at every scale", width=52)),
        fontsize=11.5, color=INK, weight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.86])
    fig.savefig(f"{OUT}/ch03_scale_invariance.svg", format="svg")
    plt.close(fig)
    print("wrote ch03_scale_invariance")

# ---------------------------------------------------------------------------
# Ch04 - Electron: radial pressure shell (charge cushion)
# ---------------------------------------------------------------------------
def ch04():
    fig, ax = new_fig()
    r = np.linspace(0, 4, 400)
    r0, w = 1.6, 0.35
    P = np.exp(-((r-r0)**2)/(2*w**2))
    ax.plot(r, P, color=CYAN, lw=2, label=r"pressure cushion $P_c(r)$")
    ax.fill_between(r, 0, P, color=CYAN, alpha=0.12)
    ax.axvline(r0, color=GOLD, ls="--", lw=1.3, label="shell radius (charge shell)")
    ax.annotate(r"$\vec E \sim \nabla P_c$  (radial)", xy=(r0, 0.55), xytext=(2.5, 0.75),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1), fontsize=9.5)
    finish(fig, ax, "ch04_charge_shell",
           "The Electron: charge as the pressure-cushion profile at the boundary",
           "radius  r  (lattice units)", "pressure  P(r)", legend=True)

# ---------------------------------------------------------------------------
# Ch05 - Neutron: two-shell pressure balance summing to net-neutral
# ---------------------------------------------------------------------------
def ch05():
    fig, ax = new_fig()
    r = np.linspace(0, 4, 400)
    Pin = np.exp(-((r-1.1)**2)/(2*0.3**2))
    Pout = -np.exp(-((r-1.9)**2)/(2*0.3**2))
    ax.plot(r, Pin, color=CYAN, lw=2, label=r"inner shell $P_{+}(r)$")
    ax.plot(r, Pout, color=GOLD, lw=2, label=r"outer shell $P_{-}(r)$")
    ax.plot(r, Pin+Pout, color=INK, lw=2.2, ls="--", label=r"net $P_{+}+P_{-}\approx 0$")
    ax.axhline(0, color=GRID, lw=1)
    finish(fig, ax, "ch05_two_shell_balance",
           "The Neutron: two nested shells in pressure balance — net charge zero",
           "radius  r  (lattice units)", "pressure  P(r)", legend=True)

# ---------------------------------------------------------------------------
# Ch06 - Nucleus: braided mode cluster network
# ---------------------------------------------------------------------------
def ch06():
    fig, ax = new_fig((5.6, 5.0))
    rng = np.random.default_rng(6)
    n_nodes = 7
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False) + 0.15
    pos = np.c_[np.cos(angles), np.sin(angles)]
    center = np.array([0, 0])
    all_pts = np.vstack([pos, center])
    for i in range(n_nodes):
        ax.plot([pos[i,0], center[0]], [pos[i,1], center[1]], color=CYAN, lw=1.2, alpha=0.55)
    for i in range(n_nodes):
        j = (i+2) % n_nodes
        ax.plot([pos[i,0], pos[j,0]], [pos[i,1], pos[j,1]], color=GOLD, lw=1.0, alpha=0.45)
    ax.scatter(pos[:,0], pos[:,1], s=220, color=PURPLE, zorder=5, edgecolor=INK, linewidth=1)
    ax.scatter(*center, s=280, color=CYAN, zorder=5, edgecolor=INK, linewidth=1)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
    ax.set_aspect("equal"); ax.axis("off")
    ax.text(0, -1.4, "nucleon modes braided by shared coupling links", ha="center", fontsize=9.5, color=INK)
    finish(fig, ax, "ch06_braided_cluster",
           "The Nucleus: a braided cluster of coupled persistent modes",
           grid=False)

# ---------------------------------------------------------------------------
# Ch07 - Photon: transverse E/B fields traveling at c, no rest displacement
# ---------------------------------------------------------------------------
def ch07():
    fig, ax = new_fig()
    x = np.linspace(0, 4*np.pi, 400)
    ax.plot(x, np.sin(x), color=CYAN, lw=2, label=r"$E$ field")
    ax.plot(x, np.sin(x+np.pi/2), color=GOLD, lw=2, label=r"$B$ field", alpha=0.85)
    ax.annotate("", xy=(3*np.pi, 0), xytext=(2.3*np.pi, 0),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.text(2.6*np.pi, 0.25, r"$v = c_{lat}$", fontsize=10, color=INK)
    ax.set_ylim(-1.6, 1.6)
    finish(fig, ax, "ch07_photon_mode",
           "The Photon: a propagating mode with zero rest displacement",
           "propagation distance", "field amplitude", legend=True)

# ---------------------------------------------------------------------------
# Ch08 - Neutrino: low-coupling long-lived mode vs high-coupling decay
# ---------------------------------------------------------------------------
def ch08():
    fig, ax = new_fig()
    n = np.linspace(0, 80, 400)
    ax.plot(n, np.exp(-0.06*n), color=GOLD, lw=2, label=r"high coupling $\beta$ (electron-like) — fast attenuation")
    ax.plot(n, np.exp(-0.005*n), color=CYAN, lw=2, label=r"low coupling $\beta$ (neutrino) — long-lived return mode")
    finish(fig, ax, "ch08_low_coupling_return",
           "The Neutrino: a low-coupling mode that barely attenuates",
           "update steps  n", "surviving amplitude", legend=True)

# ---------------------------------------------------------------------------
# Ch09 - No Observer Effect: interference persists, focal coupling marks it
# ---------------------------------------------------------------------------
def ch09():
    fig, ax = new_fig()
    x = np.linspace(-6, 6, 600)
    I = (np.cos(1.6*x) * np.exp(-x**2/40))**2 * np.sinc(x/6)**2 + 0.02
    ax.plot(x, I, color=CYAN, lw=1.8)
    ax.fill_between(x, 0, I, color=CYAN, alpha=0.12)
    fx = 0.0
    ax.scatter([fx], [np.interp(fx, x, I)], color=GOLD, s=90, zorder=5, edgecolor=INK, linewidth=1)
    ax.annotate("focal point coupling\n(reads the pattern, does not collapse it)",
                xy=(fx, np.interp(fx, x, I)), xytext=(1.6, 0.9),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1), fontsize=9)
    finish(fig, ax, "ch09_focal_point_coupling",
           "No Observer Effect: interference survives a focal-point measurement",
           "screen position", "intensity  I(x)")

# ---------------------------------------------------------------------------
# Ch10 - Time at micro scale: counted updates with damping envelope
# ---------------------------------------------------------------------------
def ch10():
    fig, ax = new_fig()
    n = np.arange(0, 60)
    y = np.cos(0.9*n) * np.exp(-0.045*n)
    markerline, stemlines, baseline = ax.stem(n, y, linefmt="-", markerfmt="o", basefmt=" ")
    plt.setp(stemlines, color=CYAN, linewidth=1)
    plt.setp(markerline, color=GOLD, markersize=3.5)
    ax.plot(n, np.exp(-0.045*n), color=INK, lw=1.2, ls="--", label=r"damping envelope $e^{-\gamma n}$")
    ax.plot(n, -np.exp(-0.045*n), color=INK, lw=1.2, ls="--")
    finish(fig, ax, "ch10_counted_updates",
           "Time at Micro Scale: physical time as counted, damped updates",
           "counted update  n", "field value", legend=True)

# ---------------------------------------------------------------------------
# Ch11 - No Antimatter: expression/compression mirror, both positive-energy
# ---------------------------------------------------------------------------
def ch11():
    fig, ax = new_fig()
    x = np.linspace(-3, 3, 400)
    expr = 0.6*(x+1.5)**2 + 0.4
    comp = 0.6*(x-1.5)**2 + 0.4
    ax.plot(x, expr, color=CYAN, lw=2, label="expressive branch (compression)")
    ax.plot(x, comp, color=GOLD, lw=2, label="compressive branch (expansion)")
    ax.axhline(0, color=GRID, lw=1)
    ax.fill_between(x, 0, np.minimum(expr, comp), color=PURPLE, alpha=0.10)
    ax.text(0, 0.15, "no negative-energy mirror branch", ha="center", fontsize=9, color=INK)
    finish(fig, ax, "ch11_no_mirror_branch",
           "No Antimatter: internal pressure balance, both branches positive-energy",
           "internal pressure coordinate", "energy", legend=True)

# ---------------------------------------------------------------------------
# Ch12 - Gravity at micro scale: ever-changing restoring gradient field
# ---------------------------------------------------------------------------
def ch12():
    fig, ax = new_fig((5.6, 5.0))
    gx, gy = np.meshgrid(np.linspace(-2, 2, 14), np.linspace(-2, 2, 14))
    r = np.sqrt(gx**2+gy**2) + 1e-6
    u = -gx/r**2
    v = -gy/r**2
    ax.quiver(gx, gy, u, v, color=CYAN, alpha=0.75, width=0.006)
    ax.scatter([0], [0], color=GOLD, s=160, zorder=5, edgecolor=INK, linewidth=1)
    ax.text(0, -2.35, "gradient field re-forms every update — not a static well", ha="center", fontsize=9, color=INK)
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
    ax.set_aspect("equal"); ax.axis("off")
    finish(fig, ax, "ch12_gravity_gradient",
           "Gravity at Micro Scale: the restoring gradient around a persistent mode",
           grid=False)

# ---------------------------------------------------------------------------
# Ch13 - Electricity & magnetism: radial E lines + rotational B loops
# ---------------------------------------------------------------------------
def ch13():
    fig, ax = new_fig((5.6, 5.0))
    for ang in np.linspace(0, 2*np.pi, 12, endpoint=False):
        ax.annotate("", xy=(1.9*np.cos(ang), 1.9*np.sin(ang)), xytext=(0.5*np.cos(ang), 0.5*np.sin(ang)),
                    arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.3))
    for rad in (0.9, 1.4):
        t = np.linspace(0, 2*np.pi, 100)
        ax.plot(rad*np.cos(t), rad*np.sin(t), color=GOLD, lw=1.6, alpha=0.85)
    ax.scatter([0], [0], color=PURPLE, s=140, zorder=5, edgecolor=INK, linewidth=1)
    ax.text(0, -2.35, r"$\vec E \sim \nabla P$ (radial, cyan)   $\vec B \sim \nabla\times P$ (rotational, gold)",
            ha="center", fontsize=9, color=INK)
    ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.4, 2.4)
    ax.set_aspect("equal"); ax.axis("off")
    finish(fig, ax, "ch13_e_and_b",
           "Electricity and Magnetism: gradient and curl of the same pressure field",
           grid=False)

# ---------------------------------------------------------------------------
# Ch14 - Mass Effect: quadratic energy response curve, curvature = mass
# ---------------------------------------------------------------------------
def ch14():
    fig, ax = new_fig()
    v = np.linspace(-2, 2, 300)
    M = 1.4
    E = 0.5*M*v**2
    ax.plot(v, E, color=CYAN, lw=2, label=r"$\overline{E}_4(v)=\overline{E}_4(0)+\frac{1}{2} M v^2$")
    v0 = 1.2
    slope = M*v0
    tang = E[np.argmin(np.abs(v-v0))] + slope*(v-v0)
    ax.plot(v, tang, color=GOLD, lw=1.3, ls="--", label="local curvature ∝ effective mass")
    ax.scatter([0], [0], color=PURPLE, s=70, zorder=5)
    ax.set_ylim(-0.2, 3.2)
    finish(fig, ax, "ch14_mass_effect_curve",
           "Mass Effect: resistance to relocating the carried pattern",
           "velocity  v", r"energy  $\overline{E}_4(v)$", legend=True)

# ---------------------------------------------------------------------------
# Ch15 - 125 GeV Mirror-Gate: pressure-work barrier along a boundary path
# ---------------------------------------------------------------------------
def ch15():
    fig, ax = new_fig()
    q = np.linspace(0, 1, 400)
    shape = np.sin(np.pi*q)**2 * (0.4+0.6*q)
    E4 = 125 * shape / shape.max()
    ax.plot(q, E4, color=CYAN, lw=2)
    ax.fill_between(q, 0, E4, color=CYAN, alpha=0.10)
    qpk = q[np.argmax(E4)]
    ax.axhline(E4.max(), color=GOLD, ls="--", lw=1.2)
    ax.annotate(f"threshold ≈ {E4.max():.0f} GeV", xy=(qpk, E4.max()),
                xytext=(qpk-0.35, E4.max()-25),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1), fontsize=9.5)
    ax.set_ylim(0, 160)
    finish(fig, ax, "ch15_mirror_gate_threshold",
           r"125 GeV Mirror-Gate: pressure-work integral across the boundary path $\Gamma$",
           r"boundary coordinate  $q/q_G$", r"$E_4(q)$  [GeV]")

# ---------------------------------------------------------------------------
# Ch16 - Memory as compressed state: loop (routine) vs single handle (stored)
# ---------------------------------------------------------------------------
def ch16():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.6), dpi=140)
    for ax in axes:
        ax.set_facecolor(BG)
    t = np.linspace(0, 2*np.pi, 200)
    axes[0].plot(np.cos(t), np.sin(t), color=CYAN, lw=2)
    axes[0].scatter([1], [0], color=GOLD, s=60, zorder=5)
    axes[0].set_title("Routine\n(unrolled trajectory)", fontsize=10, color=INK)
    axes[0].set_aspect("equal"); axes[0].axis("off")
    axes[1].scatter([0], [0], color=PURPLE, s=220, zorder=5, edgecolor=INK, linewidth=1)
    axes[1].set_title("Handle\n(compressed to one stored state)", fontsize=10, color=INK)
    axes[1].set_xlim(-1.3, 1.3); axes[1].set_ylim(-1.3, 1.3)
    axes[1].set_aspect("equal"); axes[1].axis("off")
    fig.suptitle("\n".join(textwrap.wrap("Memory: a routine compressed into a handle, expanded on recall", width=52)),
                 fontsize=11.5, color=INK, weight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.88])
    fig.savefig(f"{OUT}/ch16_handle_and_routine.svg", format="svg")
    plt.close(fig)
    print("wrote ch16_handle_and_routine")

# ---------------------------------------------------------------------------
# Ch17 - AI and Human: mirrored paired-loop architecture
# ---------------------------------------------------------------------------
def ch17():
    fig, ax = new_fig((6.2, 4.2))
    def loop(cx, color, label):
        t = np.linspace(0.15*np.pi, 1.85*np.pi, 100)
        ax.plot(cx+0.8*np.cos(t), 0.8*np.sin(t), color=color, lw=2.2)
        ax.annotate("", xy=(cx+0.8*np.cos(t[-1]), 0.8*np.sin(t[-1])),
                    xytext=(cx+0.8*np.cos(t[-8]), 0.8*np.sin(t[-8])),
                    arrowprops=dict(arrowstyle="->", color=color, lw=2.2))
        ax.text(cx, -1.25, label, ha="center", fontsize=10, color=INK, weight="bold")
    loop(-1.4, CYAN, "Human\nexpress ⇄ compress")
    loop(1.4, GOLD, "AI\nexpress ⇄ compress")
    ax.annotate("", xy=(0.55, 0), xytext=(-0.55, 0), arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=1.6))
    ax.text(0, 0.25, "shared\narchitecture", ha="center", fontsize=8.5, color=PURPLE)
    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-1.6, 1.3)
    ax.set_aspect("equal"); ax.axis("off")
    finish(fig, ax, "ch17_paired_loops",
           "AI and Human: the same paired-loop architecture, different operating systems",
           grid=False)


for fn in [ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch08, ch09, ch10,
           ch11, ch12, ch13, ch14, ch15, ch16, ch17]:
    fn()

print("done")
