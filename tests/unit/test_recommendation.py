import pytest
from fastapi.testclient import TestClient
from backend.app.recommendation.schema import ProcessTelemetryInput, PredictionInput
from backend.app.recommendation.engine import RecommendationEngine

@pytest.fixture
def sample_inputs():
    """Provides valid telemetry and prediction inputs for recommendation tests."""
    telemetry = ProcessTelemetryInput(
        pulp_flow_m3h=450.0,
        consistency_pct=3.4,
        steam_pressure_bar=4.2,
        machine_speed_mpm=850.0,
        basis_weight_gsm=82.0, # Target is 80.0, so +2.0 deviation
        active_grade_id="GRADE_A"
    )
    
    prediction = PredictionInput(
        is_basis_weight_off_spec=True,
        confidence_score=0.88,
        basis_weight_dev=2.0 # off-spec high
    )
    return telemetry, prediction

def test_recommendation_rules_calculation(sample_inputs):
    """Verify that PhysicsControlRules calculates correct directional adjustments."""
    telemetry, prediction = sample_inputs
    engine = RecommendationEngine()
    
    output = engine.generate_recommendation(telemetry, prediction)
    
    # Positive deviation (basis weight too high) should trigger REDUCED stock flow delta
    assert output.adjustments.stock_flow_m3h_delta < 0.0
    assert output.adjustments.filler_flow_lmin_delta < 0.0
    
    # Why explanation should detail the negative stock flow shift
    assert "reduce stock flow" in output.explanation.why.lower()
    assert 0.0 <= output.explanation.confidence <= 1.0

def test_historical_runs_matcher(sample_inputs):
    """Verify that HistoricalMatcher outputs valid matches and similarity scores."""
    telemetry, _ = sample_inputs
    engine = RecommendationEngine()
    
    output = engine.generate_recommendation(telemetry, sample_inputs[1])
    
    assert len(output.explanation.historical_evidence) > 0
    # Match similarity should be a percentage bounded [0, 1]
    for evidence in output.explanation.historical_evidence:
        assert 0.0 <= evidence.similarity_score <= 1.0
        assert evidence.timestamp is not None

def test_api_recommendation_endpoint(test_client):
    """Verify the /recommend REST API endpoint returns a successful payload."""
    payload = {
        "telemetry": {
            "pulp_flow_m3h": 450.0,
            "consistency_pct": 3.4,
            "steam_pressure_bar": 4.2,
            "machine_speed_mpm": 850.0,
            "basis_weight_gsm": 82.0,
            "active_grade_id": "GRADE_A"
        },
        "prediction": {
            "is_basis_weight_off_spec": True,
            "confidence_score": 0.88,
            "basis_weight_dev": 2.0
        }
    }
    
    response = test_client.post("/api/v1/prediction/recommend", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "adjustments" in data
    assert "explanation" in data
    assert data["active_grade_id"] == "GRADE_A"
    assert data["adjustments"]["stock_flow_m3h_delta"] < 0.0
