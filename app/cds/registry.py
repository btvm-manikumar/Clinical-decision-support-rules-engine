from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CDSService:
    id: str
    hook: str
    title: str
    description: str
    prefetch: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "hook": self.hook,
            "title": self.title,
            "description": self.description,
            "prefetch": self.prefetch,
        }


class ServiceRegistry:
    def __init__(self) -> None:
        self._services: dict[str, CDSService] = {}

    def register(self, service_id: str, hook: str, title: str, description: str, prefetch: dict[str, Any] | None = None) -> CDSService:
        service = CDSService(service_id, hook, title, description, prefetch or {})
        self._services[service_id] = service
        return service

    def list_services(self) -> list[dict[str, Any]]:
        return [service.to_dict() for service in sorted(self._services.values(), key=lambda item: item.id)]

    def get(self, service_id: str) -> CDSService | None:
        return self._services.get(service_id)


class RuleRegistry:
    def __init__(self) -> None:
        self._rules: dict[str, object] = {}

    def register(self, rule: object) -> object:
        self._rules[rule.rule_id] = rule
        return rule

    def list_rules(self) -> list[object]:
        return sorted(self._rules.values(), key=lambda rule: rule.priority)

    def list_rule_ids(self) -> list[str]:
        return [rule.rule_id for rule in self.list_rules()]

    def get(self, rule_id: str) -> object | None:
        return self._rules.get(rule_id)
