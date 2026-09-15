"""Shared evidence contract for source-to-wave experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping, Sequence


VALID_STATUSES = {"RAW", "NORMALIZED", "ENCODED", "HYPOTHESIS_DERIVED", "VALIDATED", "QUARANTINED"}


@dataclass(frozen=True)
class EvidencePlan:
    experiment_id: str
    observation: str
    proposed_mechanism: str
    transform_name: str
    transform_version: str
    parameters_fixed_before_holdout: Mapping[str, Any]
    assumptions: Sequence[str]
    baseline: str
    prediction: str
    development_split: str
    holdout_split: str
    decision_rule: str
    status: str = "ENCODED"
    notes: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid status: {self.status}")
        required = {
            "experiment_id": self.experiment_id,
            "observation": self.observation,
            "transform_name": self.transform_name,
            "transform_version": self.transform_version,
            "baseline": self.baseline,
            "prediction": self.prediction,
            "development_split": self.development_split,
            "holdout_split": self.holdout_split,
            "decision_rule": self.decision_rule,
        }
        missing = [name for name, value in required.items() if not str(value).strip()]
        if missing:
            raise ValueError(f"missing evidence-plan fields: {', '.join(missing)}")
        return asdict(self)


def require_predeclared_controls(plan: Mapping[str, Any], results: Mapping[str, Any]) -> None:
    """Refuse validated status if required baseline/holdout evidence is absent."""
    if plan.get("status") == "VALIDATED":
        required = ("baseline_result", "holdout_result", "uncertainty")
        absent = [key for key in required if key not in results]
        if absent:
            raise ValueError(f"VALIDATED requires: {', '.join(absent)}")
