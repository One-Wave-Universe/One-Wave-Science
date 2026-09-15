# Evidence Bench

The Evidence Bench is where source-specific representations and One Wave hypothesis-derived transforms are tested against declared controls. Its purpose is not to produce attractive outputs; it is to generate reproducible comparison records.

## First two benchmarks

### LIGO: event versus control

- Lock a named on-source window and at least one off-source/control window in a source manifest.
- Normalize both using the same adapter and encode both with identical parameters.
- Measure predeclared quantities such as spectral power, coherence, or reconstruction residual.
- Keep development and hold-out windows separate.

### CERN: representation benchmark

- Lock an openly accessible event sample and selection recipe.
- Encode each event under a fixed transform revision.
- Compare the representation against a conventional baseline on one narrow task.
- Report data split, score definition, uncertainty, and transform configuration.

## Non-negotiable rule

A representation is not a physical conclusion. `VALIDATED` means only that a predeclared result met its test criterion; it does not certify the proposed mechanism without a comparison that directly tests that mechanism.
