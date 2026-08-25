# Branch-Step 04 — Build Versions and Primitive Spine

## MAIN GOAL

Make the real build clear without changing its structure.

## CORRECTION

The state-machine lifecycle is not the whole build. The repository must distinguish:

1. the programmable version that models and validates the build; and
2. the actual primitive version built as:

`Scalar -> Differential -> Vector -> Tensor -> Harmonic`

The state machine controls and observes movement through that primitive spine. It does not replace the primitives.

## ONE CHANGE

Lock the two build versions and the exact five-primitive order.

## RESULT

The build-version relationship and primitive spine are now machine-readable in `BUILD_VERSIONS.yaml` and protected by `BUILD_STRUCTURE_LOCK.yaml`.

## HARD STOP

Do not invent primitive interfaces in this step. The next branch-step defines the Scalar contract from authoritative sources and records every assumption.
