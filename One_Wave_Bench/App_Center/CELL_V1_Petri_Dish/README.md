# CELL_V1 Petri Dish

A visible single-cell software sandbox.

## What you can watch
- six side connections: A+/B+/C+ and A-/B-/C-
- Field and Void accumulation
- ternary state: UP / STAY / DOWN
- lean
- hysteresis hold/release
- retained memory
- reinjection
- state history

## Important implementation rule
The browser animation loop is only the visual refresh. The cell state is not clock-sequenced. Each state transition is driven by the current differential inputs and the hysteretic thresholds.

## Run
Serve this folder with any local static server, for example:

```bash
python3 -m http.server 8790
```

Then open `http://127.0.0.1:8790/`.

## Boundary
This is a software model for exercising the CELL_V1 architecture. It does not establish that the physical hardware implementation has been proven.
