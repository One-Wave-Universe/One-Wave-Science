# One-Wave Science — Rational Repo Split

This folder defines the target documentation structure for consolidating the repository without creating either giant documents or hundreds of tiny Markdown files.

## Target: 12 main documents

1. [01_CANON_AND_CORE_MODEL.md](01_CANON_AND_CORE_MODEL.md)
2. [02_PHYSICS_AND_COSMOLOGY.md](02_PHYSICS_AND_COSMOLOGY.md)
3. [03_MATH_GEOMETRY_AND_ENCODING.md](03_MATH_GEOMETRY_AND_ENCODING.md)
4. [04_HARDWARE_AND_CIRCUITS.md](04_HARDWARE_AND_CIRCUITS.md)
5. [05_VIRTUAL_BREADBOARD_AND_SIMULATION.md](05_VIRTUAL_BREADBOARD_AND_SIMULATION.md)
6. [06_BIOLOGY_BRAIN_AND_ANDROID_ARCHITECTURE.md](06_BIOLOGY_BRAIN_AND_ANDROID_ARCHITECTURE.md)
7. [07_LATTICE_MEMORY_AND_MINIVERSE.md](07_LATTICE_MEMORY_AND_MINIVERSE.md)
8. [08_AI_AGENTS_JETSON_AND_TERMINAL.md](08_AI_AGENTS_JETSON_AND_TERMINAL.md)
9. [09_APPS_ANIMATOR_AND_USER_TOOLS.md](09_APPS_ANIMATOR_AND_USER_TOOLS.md)
10. [10_LEARNING_SYSTEM_AND_MATH_RULES.md](10_LEARNING_SYSTEM_AND_MATH_RULES.md)
11. [11_TESTS_EXPERIMENTS_AND_VALIDATION.md](11_TESTS_EXPERIMENTS_AND_VALIDATION.md)
12. [12_ROADMAP_STATUS_AND_COLLABORATION.md](12_ROADMAP_STATUS_AND_COLLABORATION.md)

## Split rule

Put a fact in the document whose subject owns it. Link across documents rather than duplicating long explanations. Keep active implementation instructions next to their system, and keep project-wide status in document 12.

## Size rule

Aim for roughly 5–20k words per main document. If one document grows past that because it contains a truly distinct subsystem, split that subsystem only then. Do not create a new Markdown file just because a note is small.

## Migration rule

This folder is initially a clean destination map. Existing repository documents should be consolidated carefully, preserving source information and avoiding accidental deletion of canonical material.