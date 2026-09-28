# Where the two machines and the loop are

`software-zer0/coupled_loop.py`

```text
        u  +  bus
             |
             v
     +---------------+        +---------------+
     |  TC–AC body   |        |  BC–DC brain  |
     |  - / 0 / +    | -----> |  N or Y       |
     |  ground walks | <----- |  no Y on HOLD |
     +---------------+        +---------------+
             |
             v
         action
             |
             v
      bus = 0.7 bus + 0.3 action
```

One call: `CoupledLoop.flip(u)`.

The old one-walker `engine.py` is gone.
QC–RC is not in this file yet.
