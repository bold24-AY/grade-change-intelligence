from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TelemetryInput(BaseModel):
    """
    Schema representing incoming telemetry frame from sensors.
    """
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Timestamp of the sensor reading"
    )
    pulp_flow_m3h: float = Field(
        ..., 
        ge=0.0, 
        le=2000.0, 
        description="Pulp thick stock flow in cubic meters per hour"
    )
    consistency_pct: float = Field(
        ..., 
        ge=0.0, 
        le=10.0, 
        description="Pulp fiber consistency in percentage"
    )
    steam_pressure_bar: float = Field(
        ..., 
        ge=0.0, 
        le=15.0, 
        description="Dryer steam pressure in bars"
    )
    machine_speed_mpm: float = Field(
        ..., 
        ge=0.0, 
        le=2000.0, 
        description="Machine reel speed in meters per minute"
    )

class PredictionResponse(BaseModel):
    """
    Schema representing model inference outcome.
    """
    timestamp: datetime = Field(..., description="Timestamp of inference execution")
    is_transitioning: bool = Field(..., description="Flag indicating if a grade change is currently in progress")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Model classification confidence score")
    predicted_target_grade: Optional[str] = Field(None, description="The target grade the machine is transitioning towards")
    anomaly_detected: bool = Field(default=False, description="Flag indicating if current sensor readings are anomalous")
