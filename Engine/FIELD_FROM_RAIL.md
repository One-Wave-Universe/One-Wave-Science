# Field rotation from hop + fifths

AZ0 Y/Z used as *slots*, not a rebase.

- Y1 AXIS = parent
- Y2 CLOCKWISE = +7 on 12-rail. +7 ≡ -5 (mod 12). No semitone language.
- Y3 ROTATE / STABILIZE / REVERSE still open for path vs point.
- Z6 RATIO = 7/12, PHASE via L(Δφ)=[1+cos Δφ]/2, LOCK not T6.

$$
\omega_{\mathrm{field}} = \frac{2\pi\cdot 7}{12\cdot \mathrm{TOP}}
$$

For packet `6|12|13`, TOP=12 ⇒ ω = 0.30543.

Typed 0.07 from rotations3.py is **not** this. `imposed_0_07_is_this = false`.

12 ≡ next 0. 13 ≡ next +1. Fifths walk of 12 steps returns to 0.

T6 RESOLVE→REBASE is still denied. r,g,q_max stay working calibration, unused here.
