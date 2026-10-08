# Ledger instructions (every slice worker reads this)

Repo: /home/user/One-Wave-Science. You are one of 12 workers. Together we must reference EVERY node and EVERY chapter. No keyword filtering. Do not skip a file because it "looks unrelated". Do not edit the repo.

1. Read EVERY file listed in your slice file, IN FULL (use Read with no limit; page through files longer than 2000 lines). Do not grep-and-skim.
2. Write your ledger to the output path you were given. One section per file, in slice order:

```
## <NODE-ID or chapter> — <canonical name>   (`<path>`)
- Gate / lifecycle: ...
- Upstream: ...   Downstream / cites: ...
- Core claim: <1-3 lines, verbatim where possible, with line numbers>
- Equations: <verbatim, or "none">
- Point / Path / Field role: what this file says about the Point (point rotation, spin, L, attitude, inertia, resistance), the Path (ride, circulation, orbit, route), the Field (curl, wake, compression, gradient). Write "none stated" if none — do not invent.
- Magnetism / gravity / rotation link: what it says, or "none stated".
- Open / parked / not-set items: ...
- Conflicts: anything that contradicts the canonical rules below, with file:line. Else "none".
```

Canonical rules to check against (from C-306, C-307, C-311, C-319, C-320, G-749, G-750, G-769, Internal_Proofs/COMPLETE_NODE_SYSTEM.md, Books/Book1_Micro/NODE_SUPPLY_Ch12_Ch13.md):
- Point / Path / Field are three separate rates. Point rotation (G-749) carries L = I omega. Path rotation (G-769) is the ride, carries no L. Field curl is neither. Missing one of the three leaves a node incomplete.
- A thing keeps the point spin it has; it does not start one on its own. Stable axes are greatest and least inertia; middle fights.
- Magnetism opens the point. Open magnetic gradient: dL/dt = 0. Closed: dL/dt = -gamma L. Gravity does not start or affect point rotation.
- Parent/child: R_child^ground = R_parent R_child; omega_body = omega_c + R_c^T omega_p. Transport first, then add.
- Magnetism does not become gravity. g = -alpha K_L grad chi, K_L = I + kappa_R R. R=0 -> A-115 baseline. grad chi = 0 -> g = 0. kappa_R not set.
- Bound lattice: shared organization pulls bound bodies to one point rate; resistance = mass / organization; Moon 1:1, Mercury 3:2; magnetic channel off must still leave the face; no lunar dipole required.
- No expansion, no scale factor; redshift = E-528 path loss; E-530 reinjection.
- C-306/C-307 own torque and angular momentum; nothing adds an exception to L bookkeeping.

3. Finish with a section `## Slice summary`: (a) every node ID / chapter in your slice that bears on Point, Path, Field, rotation, magnetism, gravity, inertia, mass, resistance, lattice organization or locking, with one line each on how; (b) all conflicts found; (c) cross-references you saw to nodes or files outside your slice that matter for point rotation or magnetism.

4. Your final reply to the orchestrator: only the output path, the count of files read (must equal the slice file count), and the conflict list. Keep it under 300 words.
