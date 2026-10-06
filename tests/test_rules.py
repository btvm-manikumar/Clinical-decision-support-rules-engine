from app.cds.rules.preventive_care import PreventiveCareRule
from app.cds.rules.blood_pressure import BloodPressureRule
from app.cds.models import PatientContext


def test_preventive_care_rule_matches_due_screening():
    context = PatientContext(
        patientId="PAT-1001",
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
    cards = PreventiveCareRule().evaluate(context)
    assert len(cards) >= 1
    assert cards[0].summary.startswith("Colorectal")


def test_preventive_care_rule_no_match_when_recent_screening():
    context = PatientContext(
        patientId="PAT-2002",
        age=45,
        gender="female",
        conditions=[],
        medications=[],
        allergies=[],
        observations={"systolic_bp": 120, "diastolic_bp": 80, "last_colorectal_screening_year": 2025},
        laboratoryResults={},
        immunizations=[],
        encounter={"type": "outpatient"},
    )
    cards = PreventiveCareRule().evaluate(context)
    assert cards == []


def test_blood_pressure_rule_matches_threshold():
    context = PatientContext(
        patientId="PAT-3003",
        age=65,
        gender="male",
        conditions=["hypertension"],
        medications=["lisinopril"],
        allergies=[],
        observations={"systolic_bp": 150, "diastolic_bp": 95},
        laboratoryResults={},
        immunizations=[],
        encounter={"type": "outpatient"},
    )
    cards = BloodPressureRule().evaluate(context)
    assert len(cards) >= 1
    assert cards[0].indicator == "warning"


def test_blood_pressure_rule_no_match():
    context = PatientContext(
        patientId="PAT-4004",
        age=30,
        gender="female",
        conditions=[],
        medications=[],
        allergies=[],
        observations={"systolic_bp": 120, "diastolic_bp": 80},
        laboratoryResults={},
        immunizations=[],
        encounter={"type": "outpatient"},
    )
    cards = BloodPressureRule().evaluate(context)
    assert cards == []
