# Code ledger c04

## /home/user/Builds/Virtual_Breadboard/js/board.js
- Purpose / node IDs cited: Geometry and bare-board netlist for the Virtual Breadboard simulator. Builds three physical board kinds: solderless breadboard (rails + a-e/f-j strips, lines 34-62, 145-170), perfboard (isolated 0.1" pads, 64-75, 175-199), and the CELL_V1 hex-cell PCB (three mirrors A/B/C, CENTER island, V_BUS pour, J_PWR VP/RET, two isolated-pad proto blocks, 201-316). Also: cellId assignment (108-120), component-free netlist (129-141), multi-board layout (325-367), hit testing (369-383), solder runs (397-418), perfboard pot/DIP-8 footprints (430-453), canvas drawing (469-684). The only references are to hardware docs (cad/pcb_hex.svg, cell-v1/HEX_SEATS.md, cell-v1/PHYSICAL_NET.md, lines 203-204). No C-/G-/E-/A- node IDs are cited.
- Point rotation: not present. "side 0..5 clockwise" (222, 277-278) is hexagon edge numbering, not spin. No omega, L, inertia, or attitude.
- Path rotation: not present.
- Field: not present. There is no curl, wake, chi, or grad chi.
- Magnetism: not present. "Mirrors" A+/A-, B+/B-, C+/C- (221-223) are copper pad pairs, not B, R, K_L, or kappa_R. The board does not build or couple any gravity term.
- Parent/child: not present. The only composition is the board-layout xOffset/yOffset translation (339-358), which is 2D pixel placement with no rate transport.
- Hard-coded targets / refits: none of the physics kind. The constants are only physical board dimensions: 63/30 columns (35-36), perf 63x24 / 30x18 pads (71-72), 2.54 mm pitch (75), hex net hole counts (225-234), and HEX_R = 22*HOLE (238). Line 238 notes that the drawing is larger than the real 40 mm board.
- Pass criterion: none in this file. It holds no tests or pass bit. netlist() (129-141) is described as the ground truth for strip/rail/channel connectivity. That is a topology check, not physics.
- Violations: none. The file is electrical-board geometry and is out of scope for the Point/Path/Field, magnetism, and gravity rules.

## Slice summary
- Canonical point rotation: none. The one file in the slice (board.js) has no rotation, field, magnetism, or gravity code.
- Violations: none.
- Live vs dead: board.js is a live module of the Virtual Breadboard app. It exports to module.exports and window.Board (694-695), and its comments say the click UI and the headless simulate.js share it (420-421). It is not a physics solver.
- (a) Bearing node IDs/chapters: none cited.
- (b) Conflicts: none.
- (c) Cross-references outside the slice: cad/pcb_hex.svg, cell-v1/HEX_SEATS.md, cell-v1/PHYSICAL_NET.md, and js simulate.js. These are hardware/netlist files and do not bear on point rotation or magnetism. Lines 208 and 231 describe the CENTER island as the "lean reference", which is a circuit virtual-ground term and not a physics node.
