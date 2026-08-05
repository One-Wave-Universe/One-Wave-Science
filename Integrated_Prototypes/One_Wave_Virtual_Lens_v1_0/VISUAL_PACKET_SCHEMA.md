# Compact Visual State Packet

The visual brain exports one packet per local loop tick. This is an input
candidate for the future M4 switchboard, not a declaration that these fields
are the five canonical M4 pathways.

```text
tick
loop_exists
reference_phase                 -1 or +1
gaze_x, gaze_y
event_count
positive_events, negative_events
observed_x, observed_y
predicted_x, predicted_y
velocity_x, velocity_y
mean_confidence
active_confidence
prediction_confidence
local_change_pressure
occluded
memory_attractor
memory_overlap
```

Raw 256×256 arrays remain local to the visual loop. M4 should receive the
compact packet unless it explicitly requests a visual-memory reconstruction.
