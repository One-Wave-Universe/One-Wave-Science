# Algorithms — fleshed, and what they still need

Brick: YELLOW. Structure LOCKED. Calibration OPEN. T6 not authorized.

Parents: Algorythm-Zer0 X/Y/Z/T + Universal Rules workbooks; G-721; D-414; `rabbit_hop_music.py`; `rabbit_hop_scale_rail.py`.

Local executable: `OneWaveEngine/busts/az0_algorithms.py`

---

## What they have now (was missing as code)

### 1. Recursive state

```text
L(Δφ) = [1 + cos(Δφ)] / 2
q(n+1) = clip( r q(n) + g b m d L , -q_max, +q_max )
```

Demo: aligned L=1, opposed L=0, first step q=0.12 at r=0.92 g=0.24 m=0.5.
`r,g,q_max` remain WORKING CALIBRATION. Not constants of nature.

### 2. Thresholds with gaps

Named bands only: 0–10, 15–25, 30–40, 45–55, 60–70, 75–85, 90–100.
Score 12 returns TRANSITION. Gaps are not filled.

### 3. Commitment hysteresis

```text
-3 full disagree · -2 partial disagree · 0 reference · +2 partial agree · +3 full agree
±1 unused on purpose
partial enter 0.40 > exit 0.28
full enter 0.82 > exit 0.68
```

### 4. Circle of Fifths as Y rotation

AXIS = declared tonic. CLOCKWISE +7. COUNTERCLOCKWISE -7.
`C G D A E B F# C# G# D# A# F`

### 5. Octave as hop rail

```text
octave k  →  speed 2^k on the 48-pt envelope
N = clip(6+k, 1, 12)
packet ORIGINAL  N | 2N | 2N+s
```

### 6. T6 lock

`Whole.rebase(allow=False)` → `T6_REBASE_NOT_AUTHORIZED`.
Xn·Yn·Zn·Tn is not committed from this file.

### 7. Wave drives

CERN/CODATA → Z_K envelope. LIGO → Z_M envelope. Keepin → Z_T. EEG → Z_E.
Source experiments stay themselves.

---

## What they still need

1. Domain calibration of `r,g,q_max,epsilon,center_width,hold_width,dwell,phase_lock,strength,recovery,termination`.
2. T5 rate edges sloth/slow/normal/fast/accelerated **measured**, not guessed.
3. Hex lattice that **holds** three blobs. Current hex run: 0 locked / 5 failed, rim-running.
4. `ω_s² = 3τ/2` from the **field**, not an overlay spring.
5. Official D-413 well replaced by source χ.
6. Hop receipt enforced inside D-413 / D-414 HTML, not only Python busts.
7. Live `waves_bundle.json` instead of sliced envelopes.
8. Z5 WITHIN vs BEYOND fired on a real series with a stated rule.
9. Mass Effect = second derivative of cycle-averaged E4. Hook only. No 938.
10. Real E(x,r) before any Gray → Red.

---

## Must not

Fill threshold gaps. Use ±1 as a state. Treat r=0.92 as physics. Rebase T6 from a notebook. Rewrite Gray. Call Yellow Gold.

AZ0 evidence sheet already said this. The algorithms now **do** the locked half and **refuse** the open half.
