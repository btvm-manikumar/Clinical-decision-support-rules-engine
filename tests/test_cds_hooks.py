from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cds_services_discovery():
    response = client.get("/cds-services")
    assert response.status_code == 200
    data = response.json()
    assert "services" in data
    assert len(data["services"]) >= 2


def test_valid_cds_request():
    payload = {
        "hook": "patient-view",
        "hookInstance": "test-instance-1",
        "fhirServer": "https://example.org/fhir",
        "context": {
            "patientId": "PAT-1001",
            "age": 52,
            "gender": "male",
            "conditions": ["hypertension"],
            "medications": ["amlodipine"],
            "allergies": [],
            "observations": {
                "systolic_bp": 150,
                "diastolic_bp": 95,
                "last_colorectal_screening_year": 2014,
            },
            "laboratoryResults": {},
            "immunizations": [],
            "encounter": {"type": "outpatient"},
        },
    }
    response = client.post("/cds-services/preventive-care", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "cards" in data


def test_invalid_cds_request():
    bad_payload = {
        "hook": "patient-view",
        "hookInstance": "test-instance-2",
        "fhirServer": "https://example.org/fhir",
        "context": {"patientId": ""},
    }
    response = client.post("/cds-services/preventive-care", json=bad_payload)
    assert response.status_code == 422


def test_unknown_service():
    payload = {
        "hook": "patient-view",
        "hookInstance": "test-instance-3",
        "fhirServer": "https://example.org/fhir",
        "context": {
            "patientId": "PAT-2002",
            "age": 45,
            "gender": "female",
            "conditions": [],
            "medications": [],
            "allergies": [],
            "observations": {"systolic_bp": 120, "diastolic_bp": 80},
            "laboratoryResults": {},
            "immunizations": [],
            "encounter": {"type": "outpatient"},
        },
    }
    response = client.post("/cds-services/unknown-service", json=payload)
    assert response.status_code == 404


def test_synthetic_patient_endpoint():
    response = client.post("/synthetic/patient")
    assert response.status_code == 200
    body = response.json()
    assert body["synthetic"] is True
    assert "patient" in body
    assert body["patient"]["patientId"]
