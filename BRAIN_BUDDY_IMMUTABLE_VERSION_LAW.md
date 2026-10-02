# Brain Buddy Immutable Version Law

**Status:** Mandatory development and recovery law.

## Prime rule

**NOTHING REPLACES A WORKING BRAIN BUDDY VERSION.**

A working version is a preserved historical implementation. Once identified as working, its exact commit remains a permanent recovery point. A newer version, even when fully tested and better, does not replace, rewrite, move, or erase the older working version.

## Evolution rule

Every change follows this exact pattern:

```text
WORKING VERSION / EXACT COMMIT
        |
        +--> NEW CHILD BRANCH
                |
                +--> COPY/EXPAND THE WORKING IMPLEMENTATION
                +--> MAKE THE NEW CHANGE
                +--> TEST THE NEW VERSION
                |
                +--> FAIL -> preserve/abandon that experimental branch; parent stays untouched
                |
                +--> PASS -> record this child as ANOTHER proven working version
                              parent still stays untouched
                              next evolution starts from an explicitly chosen proven version
                              on ANOTHER new child branch
```

## Forbidden

Never:

- edit a preserved known-good branch to add the next feature;
- move a known-good branch ref forward to newer code;
- force-push or rewrite a known-good version;
- call a newer implementation a replacement for an older working implementation;
- merge experimental reconstruction into the preserved recovery version;
- delete an older working implementation because a newer one passes;
- treat `latest`, `main`, or the newest recovery branch as more authoritative than an explicitly identified working version;
- stack a second substantial evolution onto the same experimental branch after the first evolution has been proven. Preserve the proven child and branch again.

## Proven-version lineage

Brain Buddy development is a tree of preserved versions, not a single branch that continually mutates.

Each proven version must retain:

- exact repository;
- branch;
- commit SHA;
- behavior that was proven;
- test/receipt evidence when available;
- parent working version;
- transport/auth assumptions relevant to that version.

A later proven child is **another known-good version**, not a replacement.

## Current preserved baseline

The recovered September 29 back-and-forth Brain Buddy baseline is:

- repository: `One-Wave-Universe/One-Wave-Science`
- preserved branch: `recovery/brain-buddy-known-good-20260929`
- original working commit: `64537d18115c786699b6c0a87c32df4f1931d859`
- behavior: cumulative Brain Buddy discussion/back-and-forth lineage with Gemini + DeepSeek Council modes.

The original commit above is the immutable recovery point. Documentation commits on the preserved branch do not redefine the runtime baseline.

## Final law

**REFERENCE A PROVEN VERSION -> CREATE A NEW CHILD BRANCH -> COPY/EXPAND -> TEST -> PRESERVE RESULT.**

Pass or fail, never destroy or overwrite the parent.
