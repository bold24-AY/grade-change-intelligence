import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.logging_config import setup_logging
from backend.app.api.v1.router import api_router

# Initialize structured logging
logger = setup_logging()

# Instantiate FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="REST API interface for paper machine Grade Change transition prediction and optimization.",
    version=settings.MODEL_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS Middleware for frontend web app integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Router namespace
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def on_startup():
    logger.info(f"Grade Change API platform launching in [{settings.ENV}] mode...")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Grade Change API platform shutting down.")

if __name__ == "__main__":
    # If executed directly, run using Uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG
    )
