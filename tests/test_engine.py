import time

from app.cds.engine import RulesEngine
from app.cds.registry import RuleRegistry
from app.cds.rules.preventive_care import PreventiveCareRule
from app.cds.rules.blood_pressure import BloodPressureRule
from app.cds.models import PatientContext


def test_multiple_rules_are_evaluated():
    registry = RuleRegistry()
    registry.register(PreventiveCareRule())
    registry.register(BloodPressureRule())

    engine = RulesEngine(registry)
    context = PatientContext(
        patientId="PAT-5005",
        age=52,
        gender="male",
        conditions=["hypertension"],
        medications=["amlodipine"],
        allergies=[],
        observations={"systolic_bp": 150, "diastolic_bp": 95, "last_colorectal_screening_year": 2014},
        laboratoryResults={},
        immunizations=[],
        encounter={"type": "outpatient"},
    )
    cards = engine.evaluate(context)
    assert len(cards) >= 2


def test_no_matching_rules_returns_empty_list():
    registry = RuleRegistry()
    registry.register(PreventiveCareRule())
    registry.register(BloodPressureRule())
    engine = RulesEngine(registry)
    context = PatientContext(
        patientId="PAT-6006",
        age=30,
        gender="female",
        conditions=[],
        medications=[],
        allergies=[],
        observations={"systolic_bp": 120, "diastolic_bp": 80, "last_colorectal_screening_year": 2024},
        laboratoryResults={},
        immunizations=[],
        encounter={"type": "outpatient"},
    )
    cards = engine.evaluate(context)
    assert cards == []


def test_rule_failure_isolation():
    class FailRule:
        rule_id = "fail-rule"
        name = "Fail Rule"
        description = "Should fail"
        priority = 10

        def evaluate(self, context):
            raise RuntimeError("simulated failure")

    registry = RuleRegistry()
    registry.register(PreventiveCareRule())
    registry.register(FailRule())
    registry.register(BloodPressureRule())
    engine = RulesEngine(registry)
    context = PatientContext(
        patientId="PAT-7007",
        age=52,
        gender="male",
        conditions=["hypertension"],
        medications=["amlodipine"],
        allergies=[],
        observations={"systolic_bp": 150, "diastolic_bp": 95, "last_colorectal_screening_year": 2014},
        laboratoryResults={},
        immunizations=[],
        encounter={"type": "outpatient"},
    )
    cards = engine.evaluate(context)
    assert len(cards) >= 2


def test_performance_target():
    registry = RuleRegistry()
    registry.register(PreventiveCareRule())
    registry.register(BloodPressureRule())
    engine = RulesEngine(registry)
    context = PatientContext(
        patientId="PAT-8008",
        age=52,
        gender="male",
        conditions=["hypertension"],
        medications=["amlodipine"],
        allergies=[],
        observations={"systolic_bp": 150, "diastolic_bp": 95, "last_colorectal_screening_year": 2014},
        laboratoryResults={},
        immunizations=[],
        encounter={"type": "outpatient"},
    )
    timings = []
    for _ in range(25):
        start = time.perf_counter()
        engine.evaluate(context)
        timings.append((time.perf_counter() - start) * 1000)
    avg = sum(timings) / len(timings)
    assert avg < 200
