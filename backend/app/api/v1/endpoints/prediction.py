from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.prediction import TelemetryInput, PredictionResponse
from backend.app.services.prediction_service import PredictionService
from backend.app.models.grade_transition_model import GradeTransitionModel

router = APIRouter()

# Simple Dependency Injection Provider
def get_prediction_service() -> PredictionService:
    # In a real system, we load the model from settings path or a model registry
    model = GradeTransitionModel()
    model.fit(None, None)  # Pre-fit mock model
    return PredictionService(ml_model=model)

@router.post("/predict", response_model=PredictionResponse)
def predict_grade_change(
    telemetry: TelemetryInput,
    service: PredictionService = Depends(get_prediction_service)
) -> PredictionResponse:
    """
    Submit real-time sensor measurements from the paper machine to evaluate transition probability.
    """
    try:
        response = service.predict_grade_transition(telemetry)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Inference error during grade change prediction: {str(e)}"
        )
