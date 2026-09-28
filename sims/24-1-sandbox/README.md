# 24→1 Sandbox

Common wrapper for modular One-Wave scientific simulations and visualizations.

- `GOLD_STANDARD.md` is the canonical contract.
- `sandbox.py` validates the module registry headlessly.
- `module-manifest.template.json` is the manifest starting point.
- `modules/01..24/` are adapters, not independent incompatible engines.

The first milestone is **adapter-first**: wrap existing simulations without changing their physics. Once an adapter reproduces the original receipt, the common 2D/3D visual layer can consume its renderer-neutral geometry.

Run:

```bash
python3 sandbox.py --json
```

A module may be exploratory and still run in the sandbox. GOLD status is separate and requires the full checklist in `GOLD_STANDARD.md`.
