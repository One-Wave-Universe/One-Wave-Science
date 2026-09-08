#!/usr/bin/env python3
"""Generate one illustrative SVG figure per Book5_Macro chapter."""
import numpy as np
import matplotlib.pyplot as plt
import os, textwrap

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

INK = "#0d1b2a"
CYAN = "#1a8fa3"
GOLD = "#c9821c"
PURPLE = "#7c3fbf"
GRID = "#d8dee3"
BG = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.facecolor": BG, "figure.facecolor": BG, "savefig.facecolor": BG,
})


def new_fig(figsize=(6.4, 3.8)):
    fig, ax = plt.subplots(figsize=figsize, dpi=140)
    ax.set_facecolor(BG)
    return fig, ax


def finish(fig, ax, name, title, xlabel="", ylabel="", legend=False, grid=True):
    if grid:
        ax.grid(True, color=GRID, linewidth=0.7, alpha=0.9)
    wrapped = "\n".join(textwrap.wrap(title, width=46))
    ax.set_title(wrapped, fontsize=11.5, color=INK, weight="bold", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    if legend:
        ax.legend(frameon=False, fontsize=8.7, loc="best")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.svg", format="svg")
    plt.close(fig)
    print("wrote", name)


# Ch1 - Galaxy rotation curve: Keplerian falloff vs flat observed, gap = R_ring
def ch1():
    fig, ax = new_fig()
    r = np.linspace(0.5, 12, 300)
    v_kepler = 220/np.sqrt(r/2)
    v_obs = np.full_like(r, 190) * (1 - np.exp(-(r/1.5)))
    ax.plot(r, v_kepler, color=GOLD, lw=2, ls="--", label=r"expected from visible mass  $v\propto r^{-1/2}$")
    ax.plot(r, v_obs, color=CYAN, lw=2.2, label="observed flat rotation curve")
    ax.fill_between(r, v_kepler, v_obs, where=(v_obs > v_kepler), color=PURPLE, alpha=0.15,
                     label=r"gap attributed to $R_{ring}$, not dark matter")
    ax.set_ylim(0, 260)
    finish(fig, ax, "ch1_rotation_curve",
           "Galaxy Rotation: the flat-curve gap as a compression-ring contribution",
           "orbital radius  r  (kpc)", "orbital velocity  v  (km/s)", legend=True)


# Ch2 - Stellar hydrostatic balance: compression pressure vs restoring response
def ch2():
    fig, ax = new_fig()
    r = np.linspace(0, 1, 300)
    Pc = 1.0*(1-r)**2 + 0.05
    Row = 0.05 + 0.95*r**1.6
    ax.plot(r, Pc, color=GOLD, lw=2.2, label="interior compression pressure")
    ax.plot(r, Row, color=CYAN, lw=2.2, label=r"restoring response  $R_{OW}=-A(\nabla\psi)$")
    idx = np.argmin(np.abs(Pc-Row))
    ax.axvline(r[idx], color=PURPLE, ls="--", lw=1.3)
    ax.annotate("stable balance\n(hydrostatic equivalent)", xy=(r[idx], Pc[idx]),
                xytext=(r[idx]+0.08, Pc[idx]+0.25), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    finish(fig, ax, "ch2_stellar_balance",
           "Stars: compression and restoring response held in balance",
           "fractional radius  r/R_star", "pressure (arb. units)", legend=True)


# Ch3 - Supernova break condition: |M_i| crosses R_i over stellar decline
def ch3():
    fig, ax = new_fig()
    t = np.linspace(0, 10, 300)
    M = 0.3 + 0.09*t**1.7
    R = 3.2*np.exp(-0.28*t) + 0.4
    ax.plot(t, M, color=GOLD, lw=2.2, label=r"carried mismatch  $|M_i|$")
    ax.plot(t, R, color=CYAN, lw=2.2, label=r"restoring capacity  $R_i$")
    idx = np.argmin(np.abs(M-R))
    ax.axvline(t[idx], color=PURPLE, ls="--", lw=1.4)
    ax.annotate("Break Condition\n" + r"$|M_i| > R_i$" + "\n(supernova)", xy=(t[idx], M[idx]),
                xytext=(t[idx]+0.6, M[idx]+1.1), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    finish(fig, ax, "ch3_break_condition",
           "Supernovae: restoring capacity exceeded by the carried mismatch",
           "stellar decline time (arb. units)", "amplitude (arb. units)", legend=True)


# Ch4 - Black hole boundary: v_max collapses as lattice step definition fails
def ch4():
    fig, ax = new_fig()
    x = np.linspace(0.02, 1, 300)
    v_max = np.sqrt(0.3) * x  # ordinary compressed object: small but defined v_max
    ax.plot(x, v_max, color=CYAN, lw=2.2, label=r"ordinary compressed mode: $v_{max}$ small but defined")
    xc = 0.12
    ax.axvline(xc, color=GOLD, ls="--", lw=1.6)
    ax.fill_betweenx([0, 0.6], 0, xc, color=GOLD, alpha=0.10)
    ax.annotate("structural failure:\n" + r"$\Delta x$ undefined $\Rightarrow v_{max}$ undefined" + "\n(candidate black-hole boundary)",
                xy=(xc, 0.05), xytext=(xc+0.15, 0.35), fontsize=9,
                arrowprops=dict(arrowstyle="->", color=INK, lw=1))
    ax.set_xlim(0, 1); ax.set_ylim(0, 0.6)
    ax.invert_xaxis()
    finish(fig, ax, "ch4_black_hole_boundary",
           r"Black Holes: where the lattice-step $\Delta x$ stops being defined",
           r"lattice step size  $\Delta x$  (decreasing $\rightarrow$)", r"propagation ceiling  $v_{max}$", legend=True)


# Ch5 - Stellar nucleosynthesis: sequential threshold crossings, staircase
def ch5():
    fig, ax = new_fig((6.8, 4.0))
    stages = ["H", "He", "C", "O", "Si", "Fe"]
    t_stage = [0, 2, 3.6, 4.8, 5.7, 6.3, 7.0]
    levels = [0.15, 0.32, 0.5, 0.66, 0.82, 0.97]
    for i in range(len(stages)):
        ax.plot([t_stage[i], t_stage[i+1]], [levels[i], levels[i]], color=CYAN, lw=2.4)
        if i < len(stages)-1:
            ax.plot([t_stage[i+1], t_stage[i+1]], [levels[i], levels[i+1]], color=GOLD, lw=1.6, ls="--")
        ax.text((t_stage[i]+t_stage[i+1])/2, levels[i]+0.035, stages[i], ha="center", fontsize=10, color=INK, weight="bold")
    ax.set_xlim(0, 7); ax.set_ylim(0, 1.08)
    ax.set_yticks([])
    ax.axhspan(0, 1.08, color=BG)
    finish(fig, ax, "ch5_nucleosynthesis_staircase",
           r"Nucleosynthesis: $P_{core}(t)$ climbing through each fusion threshold $T_n$",
           "stellar core time", r"core compression  $P_{core}$")


for fn in [ch1, ch2, ch3, ch4, ch5]:
    fn()
print("done")
