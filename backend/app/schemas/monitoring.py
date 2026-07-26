from pydantic import BaseModel, Field
from datetime import datetime

class HealthCheckResponse(BaseModel):
    """
    Schema for API health status metrics.
    """
    status: str = Field(..., description="API operational status (e.g. healthy, degraded)")
    timestamp: datetime = Field(..., description="Server current timestamp")
    model_version: str = Field(..., description="Active ML model version")
    uptime_seconds: int = Field(..., description="System server uptime in seconds")

class GradeSpecDetails(BaseModel):
    """
    Detailed constraints and setpoints for a single paper grade.
    """
    name: str = Field(..., description="Human-readable name of the paper grade")
    target_basis_weight_gsm: float = Field(..., description="Target basis weight in grams per square meter")
    tolerance_basis_weight_gsm: float = Field(..., description="Acceptable basis weight tolerance band (+/-)")
    target_moisture_pct: float = Field(..., description="Target percentage moisture content")
    tolerance_moisture_pct: float = Field(..., description="Acceptable moisture tolerance band (+/-)")
    nominal_machine_speed_mpm: float = Field(..., description="Nominal machine operating speed")

class GradeSpecResponse(BaseModel):
    """
    Schema representing the key-value specifications map of grades.
    """
    # Simply wraps dynamic grade keys mapped to spec details
    pass
