# Sensor cells

Not a puck species. A cell that *senses* instead of (or as well as) torque.
Same mid. Same three gates. Same flip.

```
heat cell       lean = hotter / colder than local G-ref
vibe cell       lean = more / less hash than hold belt
balance cell    lean = this side vs opposite side
```

Or **one** sensor cell with three gates:

```
gate 0   heat     NTC vs mid divider
gate 1   vibe     piezo vs belt
gate 2   balance  Hall or I vs the opposite cell
STAR G            same blue
```

That is the motor head, spoken as a hexagon. Motor windings can share that star (one body cell + one sense cell on the same G) or the sense cell *is* the motor cell with extra UP nodes.

Output of a sensor cell is a Thought fragment: lean + live + “ask engage”. It never stamps. Void reads it.

First build: the puck *is* the sensor cell in hardware. Later: three analog windows on one tiny board, same pulldowns, same G tap as the winding it watches.
