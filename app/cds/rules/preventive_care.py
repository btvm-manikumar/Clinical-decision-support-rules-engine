from datetime import datetime

from app.cds.base_rule import BaseRule
from app.cds.models import CDSCard, PatientContext
from app.config.settings import settings


class PreventiveCareRule(BaseRule):
    rule_id = "preventive-care"
    name = "Preventive Care"
    description = "Generates preventive care reminders based on age and screening history"
    priority = 10
    enabled = settings.cds_preventive_care_enabled
    service_ids = ["preventive-care"]

    def evaluate(self, context: PatientContext) -> list[CDSCard]:
        if context.age < settings.cds_colorectal_screening_age:
            return []

        screening_year = context.last_colorectal_screening_year
        current_year = datetime.now().year

        if screening_year is None:
            due = True
        else:
            due = current_year - screening_year >= settings.cds_colorectal_screening_interval_years

        if not due:
            return []

        return [
            CDSCard(
                summary="Colorectal cancer screening may be due",
                detail=(
                    "The patient may be due for colorectal cancer screening based on age and screening history. "
                    "This is synthetic decision support only and should not replace clinical judgment."
                ),
                indicator="info",
                source={"label": "Clinical Decision Support"},
                suggestions=[{"label": "Review screening history", "action": "Confirm screening status"}],
                links=[],
            )
        ]
