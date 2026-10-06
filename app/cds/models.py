from __future__ import annotations

from datetime import date
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PatientContext(BaseModel):
    model_config = ConfigDict(extra="ignore")

    patientId: str = Field(..., min_length=1)
    age: int = Field(..., ge=0, le=130)
    gender: str = Field(..., min_length=1)
    dateOfBirth: date | None = None
    conditions: list[str] = Field(default_factory=list)
    medications: list[str] = Field(default_factory=list)
    allergies: list[str] = Field(default_factory=list)
    observations: dict[str, Any] = Field(default_factory=dict)
    laboratoryResults: dict[str, Any] = Field(default_factory=dict)
    immunizations: list[str] = Field(default_factory=list)
    encounter: dict[str, Any] = Field(default_factory=dict)

    @field_validator("gender")
    @classmethod
    def normalize_gender(cls, value: str) -> str:
        return value.strip().lower()

    @property
    def last_colorectal_screening_year(self) -> int | None:
        value = self.observations.get("last_colorectal_screening_year")
        if value is None:
            return None
        return int(value)

    @property
    def systolic_bp(self) -> int | None:
        value = self.observations.get("systolic_bp")
        if value is None:
            return None
        return int(value)

    @property
    def diastolic_bp(self) -> int | None:
        value = self.observations.get("diastolic_bp")
        if value is None:
            return None
        return int(value)


class CardSource(BaseModel):
    label: str = "Clinical Decision Support"


class CDSCard(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid4()))
    summary: str
    detail: str
    indicator: Literal["info", "warning", "critical"]
    source: CardSource = Field(default_factory=CardSource)
    suggestions: list[dict[str, Any]] = Field(default_factory=list)
    links: list[dict[str, Any]] = Field(default_factory=list)


class CardListResponse(BaseModel):
    cards: list[CDSCard] = Field(default_factory=list)
