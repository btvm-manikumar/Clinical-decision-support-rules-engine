from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Clinical Decision Support Rules Engine"
    app_version: str = "1.0.0"
    app_description: str = (
        "CDS Hooks compatible clinical decision support rules engine using dynamic synthetic patient context."
    )
    cds_colorectal_screening_age: int = 45
    cds_colorectal_screening_interval_years: int = 10
    cds_high_systolic_bp: int = 140
    cds_high_diastolic_bp: int = 90
    cds_preventive_care_enabled: bool = True
    cds_blood_pressure_enabled: bool = True
    log_level: str = "INFO"


settings = Settings()
