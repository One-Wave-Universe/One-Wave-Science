"""One-Wave Hopfield Melody Cell v1.

Status: UNVERIFIED EXPERIMENTAL MODULE.

Associative-memory module storing melodic/sign patterns in a Hopfield weight
matrix. Its presence in the repository is for direct testing; it is not
evidence that Hopfield dynamics implement CELL_V1 or biological memory.
"""

from __future__ import annotations


class HopfieldMelodyCell:
    def __init__(self, size: int = 5):
        if size <= 0:
            raise ValueError("size must be positive")
        self.size = size
        self.weights = [[0.0 for _ in range(size)] for _ in range(size)]

    def _validate(self, pattern):
        if len(pattern) != self.size:
            raise ValueError("pattern length must equal cell size")

    def store_pattern(self, pattern):
        """Store one bipolar pattern using the requested Hebbian rule."""
        self._validate(pattern)
        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    self.weights[i][j] += pattern[i] * pattern[j]

    def recall(self, input_pattern):
        """Run one synchronous recall pass."""
        self._validate(input_pattern)
        output = []
        for i in range(self.size):
            val = sum(
                self.weights[i][j] * input_pattern[j]
                for j in range(self.size)
                if i != j
            )
            output.append(1 if val >= 0 else -1)
        return output


def verification_cases():
    """Small explicit cases for future qualification tests."""
    return {
        "exact_recall": "stored pattern should recall itself",
        "noisy_recall": "single-bit corruption should be tested for recovery",
        "collision": "conflicting patterns should be tested for spurious attractors",
        "restart": "serialized weights should reproduce recall after restart",
    }
