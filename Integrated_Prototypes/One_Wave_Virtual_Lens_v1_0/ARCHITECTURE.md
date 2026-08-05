# Virtual Lens Architecture

## Locked boundary

Vision is a separate sensory loop with separate local memory. It is not fused
with audio before either loop works independently.

## Reference loop

Every visual tick flips `reference_phase` between -1 and +1. The phase is a
low-cost loop-continuity heartbeat, not a conscious statement. A tick returns a
`VisualStatePacket` containing current events, confidence, prediction, movement,
and loop status.

## Persistent inner world

Only the first local lens view establishes the initial reference. After that,
local brightness-change events update the persistent visual field. Static
regions remain represented while confidence slowly ages.

## Occlusion

When visible motion events stop, the visual loop continues the last inferred
velocity through its prediction field. Reappearance tests whether the internal
continuation was useful.

## Local Hopfield memory

The finished musical Hopfield source remains untouched. The visual brain uses a
local adapter implementing the same core method over visual patterns:

- symmetric Hebbian matrix;
- zero diagonal;
- asynchronous unit updates;
- nonincreasing energy audit;
- raw settled state;
- committed closest stored attractor.

The local visual vector has four equal blocks: persistent occupancy, event
polarity, predicted position, and distributed motion/context. This is not the
higher five-way multimodal memory allocation and does not redefine HOLD.

## Future boundaries

1. Add controlled gaze movement.
2. Add more shapes, shadows, and two-object ambiguity.
3. Build the independent audio loop with its own persistent field and memory.
4. Let M4 route compact visual/audio packets while maintaining State, Scale,
   Caution, Drive, and the duplex oversight chain.
5. Let Boltzmann compress cross-modal candidate relationships without rewriting
   the local Hopfield banks.
