from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.prediction import TelemetryInput, PredictionResponse
from backend.app.services.prediction_service import PredictionService
from backend.app.models.grade_transition_model import GradeTransitionModel

router = APIRouter()

# Simple Dependency Injection Provider
def get_prediction_service() -> PredictionService:
    from backend.app.ml.registry import ModelRegistry
    import os
    import pandas as pd
    
    registry_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "models", "checkpoints")
    registry = ModelRegistry(registry_dir=registry_dir)
    try:
        model = registry.load_model("basis_weight_deviation_champion")
    except Exception:
        # Fallback Mock Model
        from backend.app.ml.random_forest import RandomForestWrapper
        model = RandomForestWrapper()
        model.fit(pd.DataFrame({
            "pulp_flow_m3h": [0.0, 1.0], 
            "consistency_pct": [0.0, 1.0], 
            "steam_pressure_bar": [0.0, 1.0], 
            "machine_speed_mpm": [0.0, 1.0]
        }), [0, 1])
        
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

from backend.app.recommendation.schema import ProcessTelemetryInput, PredictionInput, RecommendationOutput
from backend.app.recommendation.engine import RecommendationEngine

def get_recommendation_engine() -> RecommendationEngine:
    return RecommendationEngine()

@router.post("/recommend", response_model=RecommendationOutput)
def generate_recommendation(
    telemetry: ProcessTelemetryInput,
    prediction: PredictionInput,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
) -> RecommendationOutput:
    """
    Generate real-time controller setpoint adjustments and physical explanations.
    """
    try:
        response = engine.generate_recommendation(telemetry, prediction)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate setpoint recommendations: {str(e)}"
        )

from backend.app.xai.schema import XAIExplanationResponse
from backend.app.xai.shap_explainer import ShapExplanationService
from backend.app.xai.nlp_explainer import NlpExplanationService
from typing import Dict

def get_xai_explainer() -> tuple:
    from backend.app.ml.registry import ModelRegistry
    import os
    import pandas as pd
    
    registry_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "models", "checkpoints")
    registry = ModelRegistry(registry_dir=registry_dir)
    try:
        model = registry.load_model("basis_weight_deviation_champion")
    except Exception:
        # Fallback Mock Model
        from backend.app.ml.random_forest import RandomForestWrapper
        model = RandomForestWrapper()
        model.fit(pd.DataFrame({"f1": [0.0, 1.0], "f2": [0.0, 1.0]}), [0, 1])
        
    # Read background features for baseline comparisons
    processed_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "processed", "engineered_features_sample.csv")
    background_df = None
    if os.path.exists(processed_path):
        try:
            background_df = pd.read_csv(processed_path)
        except Exception:
            pass
            
    shap_service = ShapExplanationService(model, background_df)
    nlp_service = NlpExplanationService()
    return shap_service, nlp_service

@router.post("/explain", response_model=XAIExplanationResponse)
def explain_prediction(
    features_payload: Dict[str, float]
) -> XAIExplanationResponse:
    """
    Generate SHAP attribution values and plain English causal explanation cards for a process state.
    """
    try:
        import pandas as pd
        shap_service, nlp_service = get_xai_explainer()
        
        # Transform payload dict into a 1-row DataFrame
        df_inst = pd.DataFrame([features_payload])
        
        # Calculate attributions
        attributions, expected_val = shap_service.compute_shap_attributions(df_inst)
        
        # Call model prediction probability
        prob = 0.5
        try:
            raw_prob = shap_service.model.predict_proba(df_inst)
            prob = float(raw_prob[0, 1]) if raw_prob.ndim > 1 and raw_prob.shape[1] > 1 else float(raw_prob[0])
        except Exception:
            pass
            
        response = nlp_service.compile_operator_explanation(
            attributions=list(attributions),
            feature_names=list(df_inst.columns),
            raw_values=list(df_inst.values.ravel()),
            prediction_prob=prob
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Explainable AI summary card: {str(e)}"
        )


