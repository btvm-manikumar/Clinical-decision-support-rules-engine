import logging
import time
from typing import Any

from app.cds.models import CDSCard, PatientContext
from app.cds.registry import RuleRegistry

logger = logging.getLogger("cds_hooks.engine")


class RulesEngine:
    def __init__(self, registry: RuleRegistry) -> None:
        self.registry = registry

    def evaluate(self, context: PatientContext) -> list[CDSCard]:
        start = time.perf_counter()
        cards: list[CDSCard] = []
        rules = self.registry.list_rules()
        logger.info(
            "Evaluating rules",
            extra={
                "patient_id": context.patientId,
                "rules_evaluated": [rule.rule_id for rule in rules],
            },
        )

        for rule in rules:
            try:
                if not getattr(rule, "enabled", True):
                    logger.info("Rule disabled, skipping", extra={"rule_id": rule.rule_id})
                    continue
                results = rule.evaluate(context)
                if results:
                    cards.extend(results)
                    logger.info("Rule triggered", extra={"rule_id": rule.rule_id, "trigger_count": len(results)})
            except Exception as exc:  # pragma: no cover - defensive safety for rule failures
                logger.exception("Rule failed during evaluation", extra={"rule_id": getattr(rule, "rule_id", "unknown")})

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "Rules evaluation completed in %.2f ms",
            elapsed_ms,
            extra={
                "patient_id": context.patientId,
                "elapsed_ms": round(elapsed_ms, 2),
                "rules_triggered": [card.summary for card in cards],
            },
        )
        return cards
