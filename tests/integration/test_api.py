import pytest

def test_health_endpoint(test_client):
    """Verify that the health check endpoint returns 200 OK and healthy status."""
    response = test_client.get("/api/v1/monitoring/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_version" in data

def test_predict_endpoint_valid(test_client):
    """Verify that the prediction endpoint yields a successful transition prediction."""
    payload = {
        "timestamp": "2026-07-26T12:03:00Z",
        "pulp_flow_m3h": 420.0,
        "consistency_pct": 3.10,
        "steam_pressure_bar": 3.80,
        "machine_speed_mpm": 820.0
    }
    response = test_client.post("/api/v1/prediction/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "is_transitioning" in data
    assert "confidence_score" in data
    assert isinstance(data["is_transitioning"], bool)

def test_predict_endpoint_invalid_schema(test_client):
    """Verify that sending a malformed request returns a 422 Unprocessable Entity error."""
    payload = {
        "timestamp": "2026-07-26T12:03:00Z",
        "pulp_flow_m3h": "not-a-float", # Invalid data type
        "consistency_pct": 3.10
    }
    response = test_client.post("/api/v1/prediction/predict", json=payload)
    assert response.status_code == 422
