# 3-body relay (non-local envelope)

Brick: YELLOW.

Classical 3-body under point 1/r^2 is chaotic and has no general closed form. This file does not claim that prize.

## Claim under test

Gravity is not a puncture at a point. Kernel

$$
W(r;\sigma)=e^{-r/\sigma}/\sqrt{r^2+0.04\sigma^2}
$$

is finite at r=0 (W(0,6)=5/6). Bodies share

$$
\chi = W_{\mathrm{parent}}+\sum_k W_k
$$

Each feels g=-alpha nabla chi of the *common* field (relay). That is non-local as shared envelope, not a signal faster than the field.

Newton pairwise 1/r^2 is Gray comparison only.

## Receipt (this run)

| Measure | Value |
|---|---|
| W at r=0 | 0.833 finite |
| spread tail, relay + parent | 2.999 |
| spread tail, relay, parent off | 2.125 |
| spread tail, Newton pairwise | 1.460 |
| parent_tightens | FALSE |
| pass (finite AND parent tightens) | FALSE |

So: no point-puncture, yes. Parent envelope as a binder for this triad, no. Pairwise Newton still held tighter on this calibration. Sweeping parent amp 1..4 and sigma 4..12 made spread *worse*, not better.

Next cut: change the relay (magnetic axis couple from MAGNETIC_AXIS.md, or a narrower leftover, or a dead-band so parent only orients). Do not declare 3-body solved.
