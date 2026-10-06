from app.cds.base_rule import BaseRule
from app.cds.models import CDSCard, PatientContext
from app.config.settings import settings


class BloodPressureRule(BaseRule):
    rule_id = "blood-pressure"
    name = "Blood Pressure Monitoring"
    description = "Generates blood pressure alerts based on configured thresholds"
    priority = 20
    enabled = settings.cds_blood_pressure_enabled
    service_ids = ["clinical-risk"]

    def evaluate(self, context: PatientContext) -> list[CDSCard]:
        systolic = context.systolic_bp
        diastolic = context.diastolic_bp

        if systolic is None or diastolic is None:
            return []

        high_systolic = systolic >= settings.cds_high_systolic_bp
        high_diastolic = diastolic >= settings.cds_high_diastolic_bp

        if not (high_systolic or high_diastolic):
            return []

        if systolic >= 180 or diastolic >= 110:
            indicator = "critical"
            summary = "Severe blood pressure elevation detected"
            detail = "The patient's blood pressure is markedly above the configured threshold. This is synthetic decision support only."
        else:
            indicator = "warning"
            summary = "Elevated blood pressure detected"
            detail = "The patient's blood pressure is above the configured threshold. This is synthetic decision support only."

        return [
            CDSCard(
                summary=summary,
                detail=detail,
                indicator=indicator,
                source={"label": "Clinical Decision Support"},
                suggestions=[{"label": "Repeat measurement", "action": "Confirm blood pressure reading"}],
                links=[],
            )
        ]
