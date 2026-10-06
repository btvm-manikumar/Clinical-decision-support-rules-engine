import random
from datetime import datetime

from app.cds.models import PatientContext


def generate_synthetic_patient(patient_id: str | None = None) -> PatientContext:
    genders = ["male", "female", "non-binary"]
    conditions_pool = [
        "hypertension",
        "type 2 diabetes",
        "obesity",
        "asthma",
        "hyperlipidemia",
        "depression",
        "arthritis",
        "COPD",
    ]
    medications_pool = [
        "amlodipine",
        "lisinopril",
        "metformin",
        "atorvastatin",
        "albuterol",
        "ibuprofen",
        "levothyroxine",
    ]

    patient_id = patient_id or f"PAT-{random.randint(1000, 9999)}"
    gender = random.choice(genders)
    age = random.randint(18, 85)
    current_year = datetime.now().year
    birth_year = current_year - age

    conditions = random.sample(conditions_pool, k=random.randint(0, min(3, len(conditions_pool))))
    medications = random.sample(medications_pool, k=random.randint(0, min(3, len(medications_pool))))
    allergies = []
    if random.random() < 0.2:
        allergies = ["penicillin"]

    systolic_bp = random.randint(100, 175)
    diastolic_bp = random.randint(60, 110)
    last_screening_year = random.choice([None, 2013, 2015, 2018, 2020, 2022, 2024])
    observations = {
        "systolic_bp": systolic_bp,
        "diastolic_bp": diastolic_bp,
    }
    if last_screening_year is not None:
        observations["last_colorectal_screening_year"] = last_screening_year

    return PatientContext(
        patientId=patient_id,
        age=age,
        gender=gender,
        dateOfBirth=f"{birth_year}-01-01",
        conditions=conditions,
        medications=medications,
        allergies=allergies,
        observations=observations,
        laboratoryResults={},
        immunizations=[],
        encounter={"type": random.choice(["outpatient", "inpatient", "telehealth"])},
    )
