# Grade Change Intelligence in Paper Making Process

An enterprise-ready, modular decision-support system designed to monitor, predict, and optimize paper grade change transitions. Grade transitions are continuous process phases where a paper machine switches from manufacturing one grade specification (e.g., standard 80gsm paper) to another (e.g., heavyweight 120gsm cardstock).

This system provides real-time sensor analytics, anomaly boundaries check, and machine learning models to detect transition status, forecast target values alignment, and minimize paper waste ("broke").

---

## 📂 Project Architecture & Folder Rationales

Every folder in this repository has a clear, isolated purpose supporting maintainability and team scaling:

- **`backend/`**: Contains the FastAPI REST microservice. It handles telemetry parsing, validation checks, and hosts ML model inference.
- **`frontend/`**: Contains the React + Vite single-page application. Features interactive dashboard sliders to simulate DCS telemetry, real-time charts, and alarm indicators.
- **`data/`**: Structured data directories:
  - `raw/`: Unmodified sensor telemetry CSV captures.
  - `processed/`: Processed datasets with rolling features and transition targets.
  - `external/`: External specs (JSON catalog) defining tolerances for basis weight and moisture targets.
- **`docs/`**: Production documentation for developers, field engineers, and system operators.
- **`research/`**: Workspace for data science experimentation. Includes notebooks for exploratory data analysis (EDA) and transition literature notes.
- **`ppt_assets/`**: Slide structures, diagrams, and pitching assets for presentation demos.
- **`scripts/`**: Automation scripts to bootstrap dev environments and run engineering data pipelines.
- **`tests/`**: Automated verification framework containing isolated unit and integration test sweeps.

---

## 🛠 SOLID Principles Compliance

We structure the backend and data services around the five core SOLID software engineering principles:

1. **Single Responsibility Principle (SRP)**: Modules are split by logical concern. Telemetry checks exist in [validation_service.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/services/validation_service.py), machine learning scoring in [prediction_service.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/services/prediction_service.py), and config loading in [config.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/core/config.py).
2. **Open/Closed Principle (OCP)**: The model runner is built around [base.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/models/base.py)'s `BaseMLModel` abstract class. New models (XGBoost, LSTMs, Neural Nets) can be plugged in without refactoring the prediction service or endpoint layers.
3. **Liskov Substitution Principle (LSP)**: All classifiers implementing the `BaseMLModel` contract can be injected interchangeably into the prediction orchestration logic.
4. **Interface Segregation Principle (ISP)**: API endpoints are modularized by concern ([prediction.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/api/v1/endpoints/prediction.py) vs [monitoring.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/api/v1/endpoints/monitoring.py)). Clients only load the interfaces they require.
5. **Dependency Inversion Principle (DIP)**: Top-level API router handlers depend on abstract service definitions. Real concrete instances are resolved dynamically during runtime via dependency injection.

---

## 🚀 Running the System

### Docker Compose (Recommended)
Boot up both backend and frontend inside isolated Docker containers:
```bash
docker-compose up --build
```
- **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)

### Local Dev Setup

#### 1. Backend (Python/FastAPI)
Initialize virtual environment and install requirements:
```cmd
# Navigate to scripts directory and run setup
.\scripts\setup_env.bat

# Activate environment and start development server
venv\Scripts\activate
uvicorn backend.app.main:app --reload --port 8000
```

#### 2. Frontend (React/Vite)
Install NPM modules and run Vite:
```bash
cd frontend
npm install
npm run dev
```

---

## 🧪 Testing and Verification

Verify that endpoints, configurations, and preprocessing computations execute successfully:

```bash
# Ensure virtualenv is active
pytest
```
Tests will execute unit checks on configs and sensors bounds, and run integration calls on health/prediction routes.
