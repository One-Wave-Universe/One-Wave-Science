# One-Wave Shared Bridge Contract v1.1

The Hopfield Dream Engine, Boltzmann Administrator, and future M4 operator use
the same signed pathway coordinates.

## Input to Administrator

- `new_up[5]`: current/new oversight rising through the chain
- `old_down[5]`: previous resolved reference descending simultaneously
- each value: continuous decimal in `[-5.5, +5.5]`
- `flip_phase`: `0` or `1`
- `mode`: `waking`, `daydream`, or `dream_sleep`

## Output from Administrator

- committed action
- candidate confidence
- hidden compression vector
- reconstructed NEW and OLD pathway estimates
- `next_old_reference[5]`
- Gate-6 broadcast packet
- external-release recommendation for M4

## Required chain

`4 tells 5 → 5 tells 6 → 6 tells everybody`

The Gate-6 result becomes the next OLD oversight moving downward while the next
NEW oversight rises. Both directions advance during the same system tick.

## Multimodal memory boundary

The companion Hopfield memory reserves 20% each for dialogue, sound, image,
body pressure, and movement/gaze. These five memory media are not automatically
the five bridge pathways. M4 will later perform the live mixture and routing.
