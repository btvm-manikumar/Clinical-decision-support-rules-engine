from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, HttpUrl

from app.cds.models import CDSCard, PatientContext


class CDSHookRequest(BaseModel):
    hook: str = Field(..., min_length=1)
    hookInstance: str = Field(..., min_length=1)
    fhirServer: HttpUrl | str = Field(...)
    context: PatientContext


class ServiceSpec(BaseModel):
    id: str
    hook: str
    title: str
    description: str
    prefetch: dict[str, Any] = Field(default_factory=dict)


class ServiceDiscoveryResponse(BaseModel):
    services: list[ServiceSpec] = Field(default_factory=list)


class CDSCardsResponse(BaseModel):
    cards: list[CDSCard] = Field(default_factory=list)


class SyntheticPatientResponse(BaseModel):
    synthetic: bool = True
    patient: PatientContext
    notes: str
