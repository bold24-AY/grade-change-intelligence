import time
import json
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException
from backend.app.schemas.monitoring import HealthCheckResponse
from backend.app.core.config import settings

router = APIRouter()
START_TIME = time.time()

@router.get("/health", response_model=HealthCheckResponse)
def health_check() -> HealthCheckResponse:
    """
    Check application status, uptime, and model version alignment.
    """
    uptime = int(time.time() - START_TIME)
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        model_version=settings.MODEL_VERSION,
        uptime_seconds=uptime
    )

@router.get("/specs")
def get_grade_specifications():
    """
    Retrieve grade specification tolerances (basis weight, moisture, machine speed ranges).
    """
    spec_path = settings.GRADE_SPEC_PATH
    # Defer standard checks for testing directories
    if not os.path.exists(spec_path):
        # Fallback to local default relative check
        spec_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), "data", "external", "grade_specifications.json")

    if not os.path.exists(spec_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Grade specifications database file not found at: {settings.GRADE_SPEC_PATH}"
        )
        
    try:
        with open(spec_path, "r") as f:
            specs = json.load(f)
        return specs
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read grade specifications metadata: {str(e)}"
        )
