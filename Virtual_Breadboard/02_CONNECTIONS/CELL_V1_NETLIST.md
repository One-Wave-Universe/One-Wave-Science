# CELL_V1 netlist (logical)

```
NET_P     + rail
NET_G     0 rail / virtual ground / return to controller
NET_N     − rail

GPLUS     station between NET_P and NET_G (and mirrored NET_N–NET_G leg)
GZERO     center hold/crossing station on NET_G
GMINUS    station between NET_N and NET_G (and mirrored NET_P–NET_G leg)

CTRL      controller / rail-origin at the home end of NET_G
VGBUF     mid buffer output == NET_G at controller end
```

Do not daisy-chain NET_G station-to-station around the rim.
Each station mid tap stars to NET_G spine.
Loads that run NET_P to NET_N do not count against VGBUF current.
Only imbalance current enters NET_G.
