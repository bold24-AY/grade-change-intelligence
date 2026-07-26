import numpy as np
import pandas as pd
from datetime import datetime
from backend.app.services.base import BaseService
from backend.app.models.base import BaseMLModel
from backend.app.schemas.prediction import TelemetryInput, PredictionResponse

class PredictionService(BaseService):
    """
    Service to orchestrate and run ML predictions on sensor telemetry streams.
    Adheres to Dependency Inversion: depends on BaseMLModel interface, not a concrete model class.
    """
    
    def __init__(self, ml_model: BaseMLModel):
        self.ml_model = ml_model
        
    def get_service_status(self) -> dict:
        """Returns model load status."""
        return {
            "model_loaded": self.ml_model is not None,
            "model_type": type(self.ml_model).__name__
        }
        
    def predict_grade_transition(self, telemetry: TelemetryInput) -> PredictionResponse:
        """
        Ingests a single telemetry frame, converts it to features, and runs model classification.
        """
        # Convert Pydantic model to dataframe for the ML model (mock feature vectors)
        features_dict = {
            "pulp_flow_m3h": [telemetry.pulp_flow_m3h],
            "consistency_pct": [telemetry.consistency_pct],
            "steam_pressure_bar": [telemetry.steam_pressure_bar],
            "machine_speed_mpm": [telemetry.machine_speed_mpm]
        }
        features_df = pd.DataFrame(features_dict)
        
        # Invoke model methods
        prediction = self.ml_model.predict(features_df)
        probabilities = self.ml_model.predict_proba(features_df)
        
        is_transitioning = bool(prediction[0] == 1)
        confidence_score = float(probabilities[0][1] if is_transitioning else probabilities[0][0])
        
        # Basic heuristic to predict target grade during transitions
        target_grade = None
        if is_transitioning:
            # Let's say if speed decreases, we transition to a thicker, heavier GRADE_B
            if telemetry.machine_speed_mpm < 800.0:
                target_grade = "GRADE_B"
            else:
                target_grade = "GRADE_A"
                
        return PredictionResponse(
            timestamp=telemetry.timestamp,
            is_transitioning=is_transitioning,
            confidence_score=round(confidence_score, 4),
            predicted_target_grade=target_grade,
            anomaly_detected=False
        )
