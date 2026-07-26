import pytest
from backend.app.services.validation_service import TelemetryValidationService

def test_telemetry_validation_valid():
    """Verify that valid telemetry values pass validation."""
    validator = TelemetryValidationService()
    
    # Valid payload
    payload = {
        "pulp_flow_m3h": 450.0,
        "consistency_pct": 3.4,
        "steam_pressure_bar": 4.2,
        "machine_speed_mpm": 850.0
    }
    
    is_valid, errors = validator.validate_telemetry_bounds(payload)
    assert is_valid is True
    assert len(errors) == 0

def test_telemetry_validation_out_of_bounds():
    """Verify that out-of-bounds telemetry values fail validation with errors."""
    validator = TelemetryValidationService()
    
    # Invalid speed and consistency
    payload = {
        "pulp_flow_m3h": 450.0,
        "consistency_pct": -0.5, # negative consistency impossible
        "steam_pressure_bar": 4.2,
        "machine_speed_mpm": 5000.0 # way too fast for standard paper machine
    }
    
    is_valid, errors = validator.validate_telemetry_bounds(payload)
    assert is_valid is False
    assert any("consistency_pct" in err for err in errors)
    assert any("machine_speed_mpm" in err for err in errors)

