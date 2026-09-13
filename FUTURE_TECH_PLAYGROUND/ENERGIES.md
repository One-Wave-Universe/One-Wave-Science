# Playground energies

Parent numbers: `../MATH.md`. Cell lean on 1 kΩ at 12 V is **144 mW**, **12 mA**. Law pair idle **28.8 mW**. That is the floor we actually know.

## Dust intake

Grain mass \(m\), relative speed \(v\):

\[
K=\tfrac12 m v^2
\]

Example: \(m=10^{-12}\,\mathrm{kg}\) (big dust), \(v=20\,\mathrm{km/s}\) (LEO-ish):

\[
K=0.2\,\mathrm{J}
\]

At 12 V that is \(0.2/12\approx17\,\mathrm{mC}\) if every joule became charge on the rail — it will not. Tap efficiency \(\eta\ll1\). Power from a flux of grains \(N\) per second: \(P=\eta N K\). To beat the cell's 29 mW idle you need many grains or higher \(v\), or \(\eta\) that is not a joke.

Interstellar \(v\sim30\,\mathrm{km/s}\) same order unless the grain is huge. Relativistic dust is a different octave — playground, not F0.

## Slip vs plow

Plow energy along a path of length \(L\):

\[
E_\text{plow}\sim \kappa L
\]

Slip: you pay a **window** plus a **quantum of phase**, not \(\kappa L\).

\[
E_\text{slip}\sim \int_{\tau}P_\text{lean}(t)\,dt + E_\phi
\]

On the bench \(E_\text{lean}\) for a 10 ms +1 on 1 kΩ:

\[
E=0.144\times0.010=1.44\,\mathrm{mJ}
\]

If leftover B is real, the next hop is cheaper than 1.44 mJ. If leftover is zero, you pay 1.44 mJ every time — no engine, just clicks. That measurement is step 37 of `../Virtual_Breadboard/BUILD_26_50.md`.

## Sheath (off-hull) vs skin (on-hull)

On-hull hold: STAY floor (law + pucks).  
Off-hull: extra AC walk to keep a phase sheet off the plate. Energy is the **correction pulses**, not a DC hover. If \(P_\text{sheath}\) stays near the lean budget (144 mW class per cell) you are renting. Rip emergency = short high \(P\) then STAY.

## 125.11 GeV vs the rail

\[
E_H=2.00\times10^{-8}\,\mathrm{J}
\qquad
\frac{E_H}{e\cdot12\,\mathrm{V}}=1.04\times10^9
\]

A billion 12 V electrons per Higgs quantum. You do not stack that on BLUE. Octave marker only (`../GRAV/FIELD_TAP_SLIP_125.md`).

## Packet tau (medium defense)

Energy in a dissipating packet \(E_p\), life \(\tau\):

\[
P_\text{diss}\sim E_p/\tau
\]

Finite \(\tau\) is the law: no eternal \(E_p\). Pick \(\tau\) from RC of the launcher plus a designed decay, not from hope.

## SiC vs 2N7000

Switching energy \(\sim \tfrac12 C_\text{oss}V^2\) plus \(Q_g V_\text{drive}\). SiC wins when \(V\) and \(T_j\) are high. At 12 V / 50 mA the difference is noise. F2 hull, not F0 board (`KITTY_HAWK.md`).
