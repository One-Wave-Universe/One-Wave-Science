"""Epistemic status vocabulary.

The engine must never silently collapse an accepted scientific observation,
a One-Wave hypothesis, and a mythological interpretation into a single
merged claim -- even when they concern the same concept. `EpistemicStatus`
is the tag that keeps those apart everywhere a claim is stored (definitions
and relations alike).
"""

from __future__ import annotations

from enum import Enum


class EpistemicStatus(str, Enum):
    DEFINITION = "definition"
    OBSERVED = "observed"
    DERIVED = "derived"
    CANDIDATE = "candidate"
    METAPHOR = "metaphor"
    MYTHOLOGY = "mythology"
    REJECTED = "rejected"
    # Not in the original required list, but required by section 25:
    # inferred relations/claims must never be auto-promoted into DEFINITION,
    # OBSERVED, or DERIVED without an explicit validation step. INFERRED is
    # the holding pen for that case.
    INFERRED = "inferred"
