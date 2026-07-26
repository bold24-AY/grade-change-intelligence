from typing import Dict, Tuple, List
from backend.app.services.base import BaseService

class TelemetryValidationService(BaseService):
    """
    Service for validating raw telemetry input bounds.
    Detects sensor failures, signal noise, and out-of-spec operational envelopes.
    """
    
    # Standard boundaries for paper machine operations
    BOUNDS = {
        "pulp_flow_m3h": {"min": 0.0, "max": 1500.0},
        "consistency_pct": {"min": 0.0, "max": 8.0},
        "steam_pressure_bar": {"min": 0.0, "max": 10.0},
        "machine_speed_mpm": {"min": 0.0, "max": 2000.0}
    }
    
    def get_service_status(self) -> dict:
        return {
            "validation_bounds_count": len(self.BOUNDS)
        }
        
    def validate_telemetry_bounds(self, telemetry_dict: Dict[str, float]) -> Tuple[bool, List[str]]:
        """
        Validate incoming variables against boundary constraints.
        Returns a tuple of (is_valid, list_of_errors).
        """
        errors = []
        for variable, values in self.BOUNDS.items():
            if variable in telemetry_dict:
                val = telemetry_dict[variable]
                if val < values["min"] or val > values["max"]:
                    errors.append(
                        f"Variable '{variable}' value {val} is outside valid envelope "
                        f"[{values['min']}, {values['max']}]."
                    )
        
        is_valid = len(errors) == 0
        return is_valid, errors
