# ONE-WAVE FRAMEWORK
## Book 2 — Small
## Chapter 4: Signals, Thresholds, and Cellular Memory

**Status:** GRAY reference / YELLOW One-Wave comparison  
**Dependencies:** A-109 Inertial Memory, A-110 Oscillation, A-111 Recursion, A-112 Persistent Mode  

---

## Gray

Cells respond to chemical, electrical, mechanical, thermal, and optical signals. A response may be graded, thresholded, oscillatory, adaptive, or history dependent. The word "memory" at cellular scale therefore needs precision: it can mean a molecular state, altered gene expression, receptor abundance, chromatin state, protein modification, network hysteresis, or another measurable persistence of past input.

A simple saturating receptor response is often approximated by

$$
R(L)=R_{max}\frac{L}{K_d+L},
$$

where $L$ is ligand concentration and $K_d$ sets the half-response scale in this idealized form.

A cooperative response can be represented by a Hill function:

$$
R(L)=R_{max}\frac{L^n}{K^n+L^n}.
$$

Large $n$ makes the curve steeper, but a steep curve is still not automatically a binary switch.

## 2D — input/state/output map

Draw signal processing as three separate quantities:

$$
\text{input }u(t)\rightarrow \text{internal state }x(t)\rightarrow \text{output }y(t).
$$

A first-order memory state can be modeled as

$$
\tau\dot x=-x+u(t),
$$

with output

$$
y=g(x).
$$

The time constant $\tau$ gives the system a finite memory of recent input. If $\tau\to0$, that memory disappears.

## 3D — networks and propagation

Cells participate in signaling networks rather than isolated chains. Let $x_i$ be a state on node $i$ and $W_{ij}$ a measured or proposed coupling. One generic network equation is

$$
\dot x_i=F_i(x_i,u_i)+\sum_jW_{ij}H(x_j-x_i).
$$

The equation is deliberately general. It allows the book to distinguish topology, local dynamics, and coupling rather than smearing them into one metaphor.

## Mathematics — thresholds and hysteresis

A hard threshold is

$$
y=
\begin{cases}
1,&x\ge \theta,\\
0,&x<\theta.
\end{cases}
$$

Many biological systems are better described by smooth nonlinearities. A logistic response is

$$
y(x)=\frac{1}{1+e^{-k(x-\theta)}}.
$$

True hysteresis requires different transition conditions depending on direction/history. A minimal two-threshold rule is

$$
0\to1\quad\text{when }x\ge\theta_{on},
$$

$$
1\to0\quad\text{when }x\le\theta_{off},
\qquad \theta_{off}<\theta_{on}.
$$

The width

$$
\Delta\theta=\theta_{on}-\theta_{off}
$$

is measurable. This is much stronger than calling any delayed response "memory."

For oscillatory signals,

$$
x(t)=A(t)\cos\phi(t),
$$

with instantaneous angular frequency

$$
\omega(t)=\frac{d\phi}{dt}.
$$

Amplitude, phase, frequency, and damping should be measured separately.

## One-Wave comparison

- A-109 Inertial Memory is a candidate language for persistence caused by prior state.
- A-110 Oscillation applies only when a measured variable actually cycles.
- A-111 Recursion applies when an update explicitly depends on previous state.
- A-112 Persistent Mode is a candidate description for a maintained pattern, not a license to call every molecule a mode.

A testable recursive update is

$$
x_{n+1}=F(x_n,x_{n-1},u_n;\boldsymbol\theta).
$$

The key question is whether the $x_{n-1}$ term improves out-of-sample prediction over a simpler $F(x_n,u_n)$ control.

## Graph requirement

Each signaling chapter result should include at least one appropriate figure:

- dose-response curve;
- hysteresis loop with direction arrows;
- time series showing input and output on the same time axis;
- phase plot for an oscillator;
- prediction residuals for memoryless vs recursive models.

## Predictions / tests

1. Fit smooth and hard-threshold models to the same response data.
2. Test hysteresis with both upward and downward sweeps; one-direction data cannot establish it.
3. Estimate memory duration from perturb-and-release experiments.
4. Compare recursive and memoryless predictions on held-out time windows.
5. For oscillations, verify spectral peaks and phase continuity rather than eyeballing repeated bumps.

## Yellow Audit

- Cellular memory is real but mechanistically diverse; no single One-Wave memory mechanism has been established across all cases.
- Threshold, oscillation, recursion, and persistence are distinct mathematical properties.
- A ternary or two-state abstraction may be useful for control, but it must not erase graded biological state.

## Future Work

Build a benchmark notebook that generates synthetic graded, thresholded, hysteretic, and oscillatory signals and verifies that the analysis pipeline distinguishes them correctly before touching biological data.

## Closing Thoughts

The useful pattern is not "cells behave like switches." Cells can remember, integrate, oscillate, switch, adapt, and ignore. The job of Book 2 is to say which behavior is present, write it mathematically, and then test whether the One-Wave vocabulary compresses the description without losing what the data actually do.
