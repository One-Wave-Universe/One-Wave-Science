---
id: G-752
title: Triad Brain from Three Loops
status: yellow-architecture
claim_boundary: CPU-native brain definition; Jetson is optional skin; kernel six-route count unchanged
---

# G-752 — Build the brain from the 3-loop triad

Jetson is no longer required. GPU/NPU split was a placement convenience (G-724). The brain is three nested loops on one address space.

## The triad

1. **DC loop** — Field choice then Void choice. Polarity. Administrator lives here. STOP is a DC commit.
2. **AC loop** — ternary `DOWN / HOLD / UP` around virtual ground `(0)`. Rhythm. CPG-like. Primitive cell lives here.
3. **Quadratic loop** — four views up, four actions down (G-740). Phase / steer / leftover that DC+AC cannot name.

One system flip is three nerve cycles of this triad, not a Jetson boot.

```text
AC  = low  = cell / CPG / cannot commit STOP
QC  = mid  = M4 steer / Hopfield / associative
DC  = up   = Administrator polarity / only commit
```

Language is optional (G-742). Dream Engine may propose on any device, including CPU. It still cannot authorize.

## What "remove the Jetson" means

- Native runtime: CPU reference, `triad_brain.py`
- `jetson_runtime.py` and `install_jetson.sh` become **optional adapters**
- Device labels in receipts may read `CPU_REFERENCE` for all three seats
- No test may fail because `/dev/nvhost-gpu` is missing

Do not delete the Jetson files. They are a skin for later, like a robot-dog low-level board.

## Nest attachment

Hex/pyramid Points (G-748) sit on the AC ring. Body-rate transport (G-750) is how a child cell reports into the parent DC frame. Quadratic leftover is Path-level steer, not a seventh route.

## Not claimed

Three loops are not three MOSFETs. Not three neurons. Not proof of biology. SiC endurance stays G-741 Yellow.
