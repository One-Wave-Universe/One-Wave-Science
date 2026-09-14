# Next 25 steps

50 mA knob until step 18. Fill the receipt line before you skip ahead.

1. Tape three rails on an 830 board: RED +12, BLUE 0, BLACK −12. Supply OFF.
2. Land ±12 and 0 on column 1. 100 nF RED–BLUE and BLACK–BLUE at the posts.
3. Two 10 kΩ 1% : RED–BLUE and BLACK–BLUE.
4. Put I_0 in BLUE (DMM mA or 1 Ω shunt) at the home end.
5. Knob 50 mA. ON. Write V+, V−, VG, I_0. I_0 must be ~0.
6. Pull the RED 10 k. Write I_0. G must sit. Plug back. Repeat BLACK 10 k.
7. Tie three 1 kΩ to a STAR on BLUE far. Other ends = PA PB PC. Star vs BLUE ~0.
8. Fit station A only: P-MOS high + 2N7000 low, 220 Ω gates, 10 k pulldowns to OFF.
9. STAY. Repeat step 5. PA not slammed. I_0 still quiet.
10. A = +1 (P-MOS ON, N OFF). Write V_PA, I_0. G sits. Back to STAY.
11. A = −1. Write the opposite I_0. Never both FETs ON.
12. Copy station B. STAY/STAY. I_0 quiet.
13. Speaker (32 Ω or 8 Ω+47 Ω) between PA and PB. Not to BLUE.
14. STAY/STAY: ~0 V across coil, silence. A+1 B−1: click. Swap: click.
15. Run `python brain_2state.py` and `python nerve_cell.py`. Confirm asserts.
16. Map Thought: engage 0 → STAY/STAY; lean+ → push; lean− → pull. One click from the script/jumpers.
17. Glue 10 k NTC (47 k to 5 V, NTC to BLUE). Log ADC → R → β-temp. Bias ≤ 100 µA.
18. SS49E at the star (5 V vs BLUE). Log quiet / during click / after STAY.
19. Piezo on the board or can. Log quiet vs click. That is sensor cell gate 1.
20. Void rule on paper: hot NTC or fat I_0 or scream piezo → no next click.
21. Fit station C with 1 k to star (third winding). Walk A then B then C +1, others STAY. Write I_0 each.
22. Second copy of rails-on-a-mini-ring (two 10 k + one station is enough). Tap its G to the same spine.
23. Cell 0 +1, cell 1 STAY. I_0 moves. Cell 1 Hall/NTC quiet. Swap. Height-2 cube.
24. Electret mic vs BLUE. Clap → onset → one allowed click. That is drummer lock, not human-level hearing.
25. Write the full receipt (rails, I_0 table, click, NTC, Hall, two-cell test, override silence). Stop. Motor smaller than the knob only after this page exists.
