# Code ledger instructions

Repos: /home/user/One-Wave-Science and /home/user/Builds. Read EVERY file in your slice IN FULL (page through long files). Do not edit the repo. Do not run anything that writes into the repo.

Canonical rules to audit against are in Full_Scope_Ledger_2026-10-08/LEDGER_INSTRUCTIONS.md (read that file first, the "Canonical rules" list).

Write one section per file to your output path:

```
## <path>
- Purpose / node IDs cited: ...
- Point rotation: how spin / omega / L / attitude is represented, how it is STARTED, what CHANGES it (line numbers). Does gravity or a compression gradient change it? Is there an open/closed magnetic switch (dL/dt = 0 vs -gamma L)? Is there a parent "organization" target rate? "not present" if none.
- Path rotation: orbit / turning / ride; does it carry L? (lines)
- Field: curl / wake / chi / grad chi (lines)
- Magnetism: how B, R, K_L, kappa_R are built. Is R built from B (W_B = B⊗B - |B|²I/3) or from something else? K_L tensor or scalar? kappa_R value hard-coded? Does B produce gravity when grad chi = 0? (lines)
- Parent/child: rates transported (omega_c + R_c^T omega_p) or added raw? (lines)
- Hard-coded targets / refits: observed values used as inputs and then reported as predictions (e.g. Mercury 3:2 period, Moon 1:1, 125 GeV, measured masses) (lines)
- Pass criterion: what makes it "pass"? Is the pass bit point rotation, spread, or something else?
- Violations: list with file:line against the canonical rules. "none" if none.
```

End with `## Slice summary`: which files implement point rotation canonically, which violate it and how, and which are the live solvers vs dead/legacy.

Final reply: output path, files read count (must equal slice count), violation list. Under 300 words.
