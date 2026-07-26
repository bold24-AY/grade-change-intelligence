import pytest
import os
import yaml
from fastapi.testclient import TestClient

@pytest.fixture
def mock_config():
    """Fixture providing a mock configuration dict."""
    return {
        "app": {
            "name": "Test Grade Change Intel",
            "env": "testing",
            "debug": True
        },
        "server": {
            "host": "127.0.0.1",
            "port": 8000
        },
        "data": {
            "raw_sensor_path": "data/raw/sensor_readings_sample.csv",
            "processed_features_path": "data/processed/engineered_features_sample.csv",
            "grade_spec_path": "data/external/grade_specifications.json"
        }
    }

@pytest.fixture
def test_client():
    """Fixture providing an HTTP test client for the FastAPI app."""
    # We defer import until test execution to avoid early loading exceptions
    from backend.app.main import app
    with TestClient(app) as client:
        yield client
