from pydantic import BaseModel, Field
from typing import List, Dict

class FeatureInfluence(BaseModel):
    """Represents a single feature's driver impact on prediction."""
    variable_name: str = Field(..., description="Process variable name")
    value: float = Field(..., description="Current raw value of feature")
    shap_value: float = Field(..., description="SHAP attribution value")
    percentage_impact: float = Field(..., description="Percentage contribution to deviation risk")
    direction: str = Field(..., description="'INCREASE' if pushing risk up, 'DECREASE' if reducing it")

class SimilarCaseReference(BaseModel):
    """Historical case context reference for operator reassurance."""
    timestamp: str = Field(..., description="Timestamp of matched historical event")
    description: str = Field(..., description="What was adjusted and what happened")
    similarity: float = Field(..., description="State similarity score (0 to 1)")

class XAIExplanationResponse(BaseModel):
    """Explainable AI response card targeted for control room plant operators."""
    risk_percentage: float = Field(..., description="Model predicted probability of off-spec deviation scaled to percent")
    why_nlp: str = Field(..., description="Operator friendly plain English summary of why the model triggered this state")
    influential_variables: List[FeatureInfluence] = Field(..., description="Top drivers behind prediction sorted by magnitude")
    historical_references: List[SimilarCaseReference] = Field(..., description="References to similar historical states resolved successfully")
    confidence_score: float = Field(..., description="Classifier prediction confidence score")
