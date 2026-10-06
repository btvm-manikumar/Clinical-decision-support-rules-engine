# Clinical Decision Support Rules Engine

## 1. Project overview
This project is a synthetic, CDS Hooks-style clinical decision support rules engine built with FastAPI. It demonstrates a pluggable architecture for evaluating patient context in real time and returning actionable CDS cards without using real patient data.

The engine is intentionally lightweight and designed for speed. It does not call external APIs during rule evaluation and does not require a database for normal runtime operation.

## 2. Architecture
The application is organized into modular layers:

- API layer: handles HTTP requests and validation
- Service registry: exposes service discovery metadata
- Rules engine: evaluates enabled rules
- Rule registry: registers rule implementations
- Individual rule modules: implement clinical logic and produce cards
- Pydantic model layer: validates patient and CDS card payloads

The flow is:

CDS API -> CDS Service Registry -> Rules Engine -> Rule Registry -> Individual Rules -> CDS Cards

## 3. CDS Hooks concept
CDS Hooks is a standard way to integrate external clinical decision support into an EHR workflow. In this synthetic implementation, the API exposes patient-view hooks and returns cards that describe preventive reminders and risk alerts.

This project does not claim to be production clinical software. It is a demonstration engine for architecture, validation, and synthetic evaluation logic.

## 4. Folder structure

cds-hooks-rules-engine/
- app/
  - __init__.py
  - main.py
  - api/
    - __init__.py
    - cds_hooks.py
  - cds/
    - __init__.py
    - engine.py
    - registry.py
    - base_rule.py
    - models.py
    - rules/
      - __init__.py
      - preventive_care.py
      - blood_pressure.py
  - schemas/
    - __init__.py
    - cds.py
  - config/
    - __init__.py
    - settings.py
  - utils/
    - __init__.py
    - synthetic_data.py
- tests/
  - __init__.py
  - test_cds_hooks.py
  - test_rules.py
  - test_engine.py
- .env.example
- .gitignore
- requirements.txt
- README.md
- run.py

## 5. Installation

Windows:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Linux/macOS:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 6. Environment setup
Copy the example environment file and edit the values as needed:

cp .env.example .env

Available configuration values include:

- CDS_COLORECTAL_SCREENING_AGE
- CDS_COLORECTAL_SCREENING_INTERVAL_YEARS
- CDS_HIGH_SYSTOLIC_BP
- CDS_HIGH_DIASTOLIC_BP
- CDS_PREVENTIVE_CARE_ENABLED
- CDS_BLOOD_PRESSURE_ENABLED
- LOG_LEVEL

## 7. Running the application

Windows:

venv\Scripts\activate
uvicorn app.main:app --reload

Linux/macOS:

source venv/bin/activate
uvicorn app.main:app --reload

You can also use:

python run.py

## 8. Swagger testing
Open the Swagger UI at:

- http://127.0.0.1:8001/docs

The ReDoc interface is available at:

- http://127.0.0.1:8001/redoc

## 9. CDS discovery
The CDS service discovery endpoint is:

GET /cds-services

Example response:

{
  "services": [
    {
      "id": "preventive-care",
      "hook": "patient-view",
      "title": "Preventive Care Decision Support",
      "description": "Evaluates patient context and generates preventive care recommendations",
      "prefetch": {}
    },
    {
      "id": "clinical-risk",
      "hook": "patient-view",
      "title": "Clinical Risk Decision Support",
      "description": "Evaluates dynamic clinical measurements and generates risk alerts",
      "prefetch": {}
    }
  ]
}

## 10. CDS request
The main CDS endpoint is:

POST /cds-services/{service_id}

Example payload:

{
  "hook": "patient-view",
  "hookInstance": "dynamic-uuid",
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
      "last_colorectal_screening_year": 2014
    },
    "laboratoryResults": {},
    "immunizations": [],
    "encounter": {
      "type": "outpatient"
    }
  }
}

The response returns a list of CDS cards:

{
  "cards": [
    {
      "uuid": "...",
      "summary": "Colorectal cancer screening may be due",
      "detail": "...",
      "indicator": "info",
      "source": {"label": "Clinical Decision Support"}
    }
  ]
}

## 11. Rules engine
The rules engine evaluates all enabled rules in priority order. It catches exceptions from individual rules so that one failing rule does not block the rest of the request.

Rules are defined in modules under app/cds/rules.

## 12. Plugin architecture
Each rule extends the abstract BaseRule class and implements evaluate(context). The registry registers rules dynamically and the engine loads only enabled rules.

This makes it straightforward to add new rules without changing the API endpoint logic.

## 13. Adding a new rule
1. Create a new file under app/cds/rules.
2. Define a subclass of BaseRule.
3. Set rule_id, name, description, priority, and enabled state.
4. Register it in the RuleRegistry in app/api/cds_hooks.py or a factory file.
5. Return a list of CDSCard objects.

Example pattern:

class NewRule(BaseRule):
    rule_id = "new-rule"
    priority = 30

    def evaluate(self, context):
        if condition:
            return [CDSCard(...)]
        return []

## 14. Dynamic patient data
The patient context is read from the incoming request body using Pydantic validation. No patient is hardcoded in the production logic.

This means the same rule logic works for any valid synthetic patient context. The app accepts dynamic ids, ages, conditions, medications, vitals, and screening history.

## 15. Synthetic data
The app includes a synthetic patient generator at app/utils/synthetic_data.py. It creates random patient ids, age, gender, conditions, medications, blood pressure, and screening history.

A test endpoint is included:

POST /synthetic/patient

This endpoint intentionally marks the payload as synthetic only.

## 16. Postman testing
The following example requests are suitable for Postman:

1. Health
GET /health

2. CDS discovery
GET /cds-services

3. Preventive care
POST /cds-services/preventive-care

4. Clinical risk
POST /cds-services/clinical-risk

5. Dynamic patient testing
POST /synthetic/patient

Examples for patient scenarios:

- Patient A: Age 52, BP 150/95, screening 2014 -> preventive reminder + BP warning
- Patient B: Age 30, BP 120/80, screening 2024 -> no reminder, no warning
- Patient C: Age 65, BP 145/92, screening 2015 -> multiple cards
- Patient D: Age 45, BP 120/80, screening 2025 -> no unnecessary reminder
- Patient E: Age 70, BP 135/85, no screening history -> preventive reminder

These are examples only and should not be used as production clinical logic.

## 17. Unit testing
Run tests with:

pytest -v

This project includes tests for:

- health endpoint
- CDS discovery
- valid request
- invalid request
- unknown service
- preventive-care rule
- blood-pressure rule
- multiple rules
- no match
- rule failure isolation
- dynamic patient data
- configuration
- performance

## 18. Performance testing
The performance target is under 200 ms for normal synthetic requests. The engine measures execution time in milliseconds and logs the elapsed time for each request.

The app is intentionally simple and does not perform external API calls during rule evaluation.

## 19. Limitations
- This is a synthetic demo for software architecture and CDS Hook patterns.
- It does not integrate with a real EHR or FHIR server.
- It does not provide production-grade clinical safety or decision support.
- It should not be used as a clinical decision system without expert review.
