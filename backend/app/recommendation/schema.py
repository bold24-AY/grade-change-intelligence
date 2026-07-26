from pydantic import BaseModel, Field
from typing import List, Optional

class ProcessTelemetryInput(BaseModel):
    """Current sensor readings on the paper machine."""
    pulp_flow_m3h: float = Field(..., description="Current thick stock pulp flow rate")
    consistency_pct: float = Field(..., description="Slurry fiber consistency")
    steam_pressure_bar: float = Field(..., description="Dryer steam pressure")
    machine_speed_mpm: float = Field(..., description="Active machine reel speed")
    basis_weight_gsm: float = Field(..., description="Measured basis weight from scanner")
    active_grade_id: str = Field(..., description="Active grade label (e.g. GRADE_A)")

class PredictionInput(BaseModel):
    """Inference inputs from classifier models."""
    is_basis_weight_off_spec: bool = Field(..., description="Predicts if basis weight will violate tolerance band")
    confidence_score: float = Field(..., description="Model classification confidence probability")
    basis_weight_dev: float = Field(..., description="Measured basis weight offset deviation from target setpoint")

class AdjustmentRecommendation(BaseModel):
    """Recommended changes for main machine actuators."""
    stock_flow_m3h_delta: float = Field(..., description="Delta change to apply to pulp stock flow valve")
    filler_flow_lmin_delta: float = Field(..., description="Delta change to apply to ash filler dosing pump")
    steam_pressure_bar_delta: float = Field(..., description="Delta change to apply to dryer steam pressure")
    machine_speed_mpm_delta: float = Field(..., description="Delta change to apply to reel speed drive")

class EvidenceEntry(BaseModel):
    """Historical telemetry run match details."""
    timestamp: str = Field(..., description="Time of historical log match")
    pulp_flow_m3h: float = Field(..., description="Pulp flow at that timestamp")
    machine_speed_mpm: float = Field(..., description="Machine speed at that timestamp")
    similarity_score: float = Field(..., description="State vector matching similarity (0 to 1)")

class ExplanationDetails(BaseModel):
    """Explanations supporting recommended actions."""
    why: str = Field(..., description="Causal physical explanation for suggested adjustments")
    confidence: float = Field(..., description="Engine confidence score in proposed corrections")
    historical_evidence: List[EvidenceEntry] = Field(..., description="Success templates from historical runs")
    operator_notes: str = Field(..., description="Relevant operating guide reminders")

class RecommendationOutput(BaseModel):
    """Overall recommendation payload returned to operators."""
    active_grade_id: str = Field(..., description="Target active paper grade")
    adjustments: AdjustmentRecommendation = Field(..., description="Setpoint delta recommendations")
    explanation: ExplanationDetails = Field(..., description="Supporting explanations and notes")
