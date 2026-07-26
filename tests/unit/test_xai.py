import pytest
import pandas as pd
import numpy as np
from fastapi.testclient import TestClient
from backend.app.ml.random_forest import RandomForestWrapper
from backend.app.xai.shap_explainer import ShapExplanationService
from backend.app.xai.nlp_explainer import NlpExplanationService

@pytest.fixture
def mock_setup():
    """Sets up simple model wrapper and background dataframe."""
    np.random.seed(42)
    # Background feature set
    background = pd.DataFrame({
        "pulp_flow_m3h": np.random.normal(450, 10, 10),
        "machine_speed_mpm": np.random.normal(850, 20, 10)
    })
    
    # Active instance
    instance = pd.DataFrame([{
        "pulp_flow_m3h": 480.0, # significantly above average 450
        "machine_speed_mpm": 850.0
    }])
    
    # Pre-fit mock classifier
    model = RandomForestWrapper()
    model.fit(background, [0] * 5 + [1] * 5)
    
    return model, background, instance

def test_shap_service_computes_values(mock_setup):
    """Verify ShapExplanationService yields attribution vectors."""
    model, background, instance = mock_setup
    service = ShapExplanationService(model, background)
    
    attributions, expected_val = service.compute_shap_attributions(instance)
    
    assert len(attributions) == 2
    # Pulp flow was 480 (high compared to 450), attribution should be non-zero
    assert attributions[0] != 0.0

def test_nlp_translation_text_assembly(mock_setup):
    """Verify NlpExplanationService compiles operator summary cards."""
    _, _, instance = mock_setup
    nlp = NlpExplanationService()
    
    attributions = [2.5, -0.2]
    feature_names = ["pulp_flow_m3h", "machine_speed_mpm"]
    raw_vals = [480.0, 850.0]
    
    response = nlp.compile_operator_explanation(
        attributions=attributions,
        feature_names=feature_names,
        raw_values=raw_vals,
        prediction_prob=0.85
    )
    
    assert response.risk_percentage == 85.0
    assert "Thick Stock Pulp Flow" in response.why_nlp
    assert len(response.influential_variables) == 2
    assert response.influential_variables[0].variable_name == "Thick Stock Pulp Flow"
    assert response.influential_variables[0].direction == "INCREASE"
    assert len(response.historical_references) == 2

def test_api_explain_endpoint(test_client):
    """Verify POST /explain returns correct schema validation."""
    payload = {
        "pulp_flow_m3h": 480.0,
        "machine_speed_mpm": 850.0
    }
    
    response = test_client.post("/api/v1/prediction/explain", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "risk_percentage" in data
    assert "why_nlp" in data
    assert "influential_variables" in data
    assert "historical_references" in data
    assert len(data["influential_variables"]) > 0
