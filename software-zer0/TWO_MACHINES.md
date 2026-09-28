# Where the two machines and the loop are

Programmed version (software only):

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
      bus = 0.7 bus + 0.3 action     ← reinjection loop
             |
             +--> next flip (same tick grammar)
```

One call is `CoupledLoop.flip(u)`.
Both machines update in that call. Ground only moves if brain says Y.

`engine.py` is the four-branch grammar walker. It is **not** the two-machine loop.
`bench_assist.py` scores bench voltages. It is **not** the loop.

QC–RC (opposed rotating fields) is not in this file yet.
