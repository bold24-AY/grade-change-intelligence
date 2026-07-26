from fastapi import APIRouter
from backend.app.api.v1.endpoints import prediction, monitoring

api_router = APIRouter()

# Include routers with appropriate tags
api_router.include_router(
    prediction.router, 
    prefix="/prediction", 
    tags=["Prediction Operations"]
)
api_router.include_router(
    monitoring.router, 
    prefix="/monitoring", 
    tags=["System Monitoring"]
)
