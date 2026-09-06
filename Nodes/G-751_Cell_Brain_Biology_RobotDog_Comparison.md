---
id: G-751
title: Primitive Cell and Brain-Cell Skins versus Biology and Layered Robot Dogs
status: yellow-comparison
claim_boundary: mapping table only; does not change Updated 43/44 kernel; does not claim Spot/Unitree identity
---

# G-751 — Compare the builds, do not merge them

Three skins share the same six-route address space. None of them is proof of the others.

## 1. Primitive cell (hardware proposition, G-741)

Still unbuilt on the bench. Intended loop:

- Field choice then Void choice (DC)
- ternary AC around virtual ground `-(0)+`
- quadratic second phase / left-right steer
- SiC bidirectional gates as endurance claim, not as kernel law
- five verbs: Idle, Primed, Executing, Vectoring, Resolving
- void pickup of the six-route loop after Resolving (G-744 wrapper)

This is a **nerve segment**. It must not speak.

## 2. Brain cell (existing `One_Wave_Bench/brain`)

Already executable as command/memory only:

- BC-DC then TC-AC then QC-RC up and down
- Dream Engine proposes (GPU / Field)
- Administrator commits (CPU / Void)
- M4 is fast associative recall, not authority
- Hopfield attraction + bounded Boltzmann ambiguity
- `STOP` is Administrator even with no motors

`nested_rotation.py` already stores Point/Path/Field phases per carrier. G-749/G-750 now supply the rigid-frame transport law those phases must obey if they are ever treated as rates: `omega = omega_c + R_c^T omega_p`.

Brain package still does **not** drive legs. Comparison to dogs is architectural, not a port.

## 3. Biology (comparison only)

| One-Wave skin | Biological analog | What is actually similar | What is not |
|---|---|---|---|
| Primitive cell + 5-unit dead band | axon initial segment / synaptic threshold | coincidence + hysteresis before fire | not a MOSFET |
| ternary DOWN/HOLD/UP | stretch reflex: shorten / hold / lengthen | three local moves | not YES/NO |
| CaMKII-style latch (earlier note) | LTP late phase | history-gated hold | not magnetic memory yet |
| six-gate oscillator | CPG half-center pair | rhythm without a sentence | CPG is not six kernel routes |
| M4 / Hopfield | brainstem + cerebellum fast correction | fast, local, not verbal | cerebellum is not GPU |
| Administrator | cortex / basal-ganglia go-nogo | permission after proposal | not a moral faculty |
| body-rate transport | neck-on-trunk angular add | adjoint composition | not a neuron equation |

Biology has comparators: opponent interneurons, reciprocal inhibition, Purkinje pause. They are **not** op-amp symbols. Map timing and threshold, not parts lists.

## 4. Tech that already layers the same way

Quadruped stacks in the literature keep a fast unconscious loop under a slow chooser. Typical split:

- **Spinal / CPG / low-level policy** — rhythm, compliance, stance. Runs whether or not vision has an opinion. Analog of primitive cell + six-gate oscillator + G-722 motor memory.
- **Cerebellar / mid skill layer** — reusable corrections, balance, gesture primitives. Analog of M4 / Hopfield.
- **Descending / cortex-like policy** — vision, task, sit/stand/go. Analog of Dream Engine proposal + Administrator commit.

Published shapes: CPG modulated by a descending network; freeze low-level skills then train a slower commander; high-level API sit/stand versus low-level RL gestures; cerebellum-like stance on HyQ. Boston Dynamics Spot, MIT Cheetah, ANYmal, Unitree A1-class dogs all *use* some version of this split even when the paper is RL-only.

Fit to One-Wave:

```text
low / fast / nonverbal / cannot commit STOP
   primitive cell, CPG, reflex, G-722
mid / associative / M4
   Hopfield recall, skill reuse, body-rate transport on joints
up / slow / language optional
   Dream proposal, Administrator permission, G-740 views up / actions down
```

Language stays an adapter (G-742). A dog does not need words to walk. Neither does the cell.

## 5. What to update in builds (and what not to)

Update:

- point brain `nested_rotation` at G-750 when phases are interpreted as rates
- keep primitive cell and brain cell as **two skins, one address space**
- use robot-dog hierarchy as the Gray control architecture for any future leg adapter

Do not update:

- YES/NO or DOWN/HOLD/UP
- six-route count
- Mass Effect from damping
- 125 GeV into a0

## 6. Next measured work

G-741 P0: rail voltages and Hold margins on one cell. Brain package: a nonverbal cycle receipt that can run with command strings stripped. Dog adapter: only after those two exist.
