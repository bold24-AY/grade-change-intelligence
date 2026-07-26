# Grade Change Intelligence in Paper Making Process

An enterprise-ready, modular decision-support system designed to monitor, predict, and optimize paper grade change transitions. Grade transitions are continuous process phases where a paper machine switches from manufacturing one grade specification (e.g., standard 80gsm paper) to another (e.g., heavyweight 120gsm cardstock).

This system provides real-time sensor analytics, anomaly boundaries checks, machine learning model comparisons (Random Forest, XGBoost, LightGBM, CatBoost), explainable AI (SHAP attributions), and an operator advice controller dashboard to minimize paper waste ("broke").

---

## 📂 Project Architecture & Folder Rationales

Every folder in this repository has a clear, isolated purpose supporting maintainability and team scaling:

- **`backend/`**: Contains the FastAPI REST microservice and model inference services.
  - `app/pipeline/`: Decoupled ingestion loader, cleaner, rolling feature engineer, scaler, validator, and data versioner.
  - `app/ml/`: Modular ML wrappers (RandomForest, XGBoost, LightGBM, CatBoost), trainer comparative engine, and checkpoint registry.
  - `app/recommendation/`: Control rules engine and historical nearest-neighbor similarity matcher.
  - `app/xai/`: SHAP attribution values engine and NLP operator report generator.
- **`frontend/`**: Contains the React/Vite SPA and the Streamlit dashboard command center client (`app.py`).
- **`data/`**: Structured data directories (`raw/`, `processed/`, `external/`).
- **`docs/`**: Production documentation for developers, field engineers, and system operators.
- **`research/`**: Workspace for data science experimentation, literature review, and references.
- **`ppt_assets/`**: Presentation slides structures andPitch assets.
- **`scripts/`**: Automation scripts to run data pipelines and ML training cycles.
- **`tests/`**: Automated verification framework containing unit and integration tests.

---

## 🛠 SOLID Principles Compliance

We structure the backend and data services around the five core SOLID software engineering principles:

1.  **Single Responsibility Principle (SRP)**: Modules are split by logical concern. Telemetry checks exist in [validation_service.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/services/validation_service.py), machine learning scoring in [prediction_service.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/services/prediction_service.py), and config loading in [config.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/core/config.py).
2.  **Open/Closed Principle (OCP)**: The model runner is built around [base_model.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/ml/base_model.py)'s `BaseMLClassifier` abstract class. New models (LSTMs, PyTorch neural networks) can be plugged in without refactoring the prediction service or endpoint layers.
3.  **Liskov Substitution Principle (LSP)**: All classifiers implementing the `BaseMLClassifier` contract can be injected interchangeably into the prediction orchestration logic.
4.  **Interface Segregation Principle (ISP)**: API endpoints are modularized by concern ([prediction.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/api/v1/endpoints/prediction.py)). Clients only load the interfaces they require.
5.  **Dependency Inversion Principle (DIP)**: Top-level API router handlers depend on abstract service definitions. Real concrete instances are resolved dynamically during runtime via dependency injection.

---

## 🚀 Running the System

### Local Dev Setup (Windows)

#### 1. Setup Environment
Initialize virtual environment and install dependencies:
```cmd
# Execute environment setup batch script
.\scripts\setup_env.bat
```

#### 2. Run Data Pipeline & Train ML Models
Generate synthetic telemetry logs, engineer rolling features, train all candidate models, and select the champion:
```cmd
# Run data loader, cleaner and versioner
venv\Scripts\python scripts/run_pipeline.py

# Train Random Forest, XGBoost, LightGBM, CatBoost and select champion
venv\Scripts\python scripts/train_pipeline.py
```

#### 3. Launch Streamlit Dashboard Client
Start the industrial-grade dark mode dashboard:
```cmd
venv\Scripts\streamlit run frontend/app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

#### 4. Launch FastAPI REST Server
Start the backend web server:
```cmd
venv\Scripts\python -m uvicorn backend.app.main:app --reload --port 8000
```
API Documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 🧪 Testing and Verification

Verify that endpoints, configurations, preprocessing, ML models, recommendations, and XAI calculations execute successfully:

```cmd
venv\Scripts\python -m pytest
```
Tests will execute unit checks on configs, sensors bounds, and run integration calls on health, prediction, recommendation, and explanation routes.
