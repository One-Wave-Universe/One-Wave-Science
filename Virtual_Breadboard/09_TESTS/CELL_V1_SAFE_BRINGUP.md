# CELL_V1 safe bring-up

Current-limited. Low voltage. One station at a time.

1. Three rails only. Label. Measure order `+ | 0 | −`.
2. Mid buffer on. Test points at controller end and far end of NET_G.
3. G0 station + one RC branch only.
4. Log: V+−V0, V−−V0, V+−V−, I_G, RC delay, temperature.
5. Add G+ and G−.
6. Small AC on controlled DC offsets. Does G stay, oscillate, or collapse.
7. Magnetic *sense* only.
8. Write `10_RECEIPTS/` JSON. Pass/fail is the mid staying in belt under the named stimulus.
