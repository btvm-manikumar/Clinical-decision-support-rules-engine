import logging
import time
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.cds.engine import RulesEngine
from app.cds.models import PatientContext
from app.cds.registry import RuleRegistry, ServiceRegistry
from app.cds.rules.blood_pressure import BloodPressureRule
from app.cds.rules.preventive_care import PreventiveCareRule
from app.schemas.cds import CDSHookRequest, CDSCardsResponse, ServiceDiscoveryResponse, SyntheticPatientResponse
from app.utils.synthetic_data import generate_synthetic_patient

logger = logging.getLogger("cds_hooks.api")
router = APIRouter()

service_registry = ServiceRegistry()
service_registry.register(
    "preventive-care",
    "patient-view",
    "Preventive Care Decision Support",
    "Evaluates patient context and generates preventive care recommendations",
)
service_registry.register(
    "clinical-risk",
    "patient-view",
    "Clinical Risk Decision Support",
    "Evaluates dynamic clinical measurements and generates risk alerts",
)

rule_registry = RuleRegistry()
rule_registry.register(PreventiveCareRule())
rule_registry.register(BloodPressureRule())
engine = RulesEngine(rule_registry)


@router.get("/cds-services", response_model=ServiceDiscoveryResponse)
def list_services() -> ServiceDiscoveryResponse:
    logger.info("CDS services discovered")
    return ServiceDiscoveryResponse(services=service_registry.list_services())


@router.post("/cds-services/{service_id}", response_model=CDSCardsResponse)
def evaluate_service(service_id: str, request: CDSHookRequest):
    start_ts = time.perf_counter()
    logger.info(
        "CDS request started",
        extra={"service_id": service_id, "hook": request.hook, "patient_id": request.context.patientId},
    )

    service = service_registry.get(service_id)
    if service is None:
        logger.warning("Unknown CDS service requested", extra={"service_id": service_id})
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown CDS service: {service_id}")

    if service.hook != request.hook:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service '{service_id}' does not support hook '{request.hook}'.",
        )

    try:
        cards = engine.evaluate(request.context)
    except Exception:
        logger.exception("Rules engine failed", extra={"service_id": service_id, "patient_id": request.context.patientId})
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Rules evaluation failed")

    elapsed_ms = (time.perf_counter() - start_ts) * 1000
    logger.info(
        "CDS request completed in %.2f ms",
        elapsed_ms,
        extra={
            "service_id": service_id,
            "patient_id": request.context.patientId,
            "rules_evaluated": engine.registry.list_rule_ids(),
            "rules_triggered": [card.summary for card in cards],
            "execution_time_ms": round(elapsed_ms, 2),
        },
    )
    return CDSCardsResponse(cards=cards)


@router.post("/synthetic/patient", response_model=SyntheticPatientResponse)
def synthetic_patient() -> SyntheticPatientResponse:
    patient = generate_synthetic_patient()
    logger.info("Synthetic patient generated", extra={"patient_id": patient.patientId})
    return SyntheticPatientResponse(
        synthetic=True,
        patient=patient,
        notes="Synthetic data only. This endpoint is for testing and demonstration purposes.",
    )
