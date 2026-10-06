from __future__ import annotations

from abc import ABC, abstractmethod

from app.cds.models import CDSCard, PatientContext


class BaseRule(ABC):
    rule_id: str = "base-rule"
    name: str = "Base Rule"
    description: str = "Abstract rule implementation"
    priority: int = 100
    enabled: bool = True
    service_ids: list[str] = []

    @abstractmethod
    def evaluate(self, context: PatientContext) -> list[CDSCard]:
        raise NotImplementedError
