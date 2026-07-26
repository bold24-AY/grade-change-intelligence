# Grade Change Intelligence (GCI) 🏭

[![SIH Theme](https://img.shields.io/badge/SIH%20Theme-Smart%20Automation-blueviolet?style=for-the-badge)](https://www.sih.gov.in/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An enterprise-ready, modular decision-support system designed to monitor, predict, and optimize paper machine grade change transitions. Grade transitions are transient phases where a paper machine switches from manufacturing one grade specification (e.g., standard 80gsm copy paper) to another (e.g., heavyweight 120gsm cardstock). 

GCI minimizes paper waste ("broke") and off-spec downtime by providing real-time telemetry analytics, machine learning model selection, explainable AI (SHAP attributions), and an interactive control room setpoint optimizer.

---

## 📺 Control Room Dashboard Layout

To run and capture screenshots/demo GIFs of the live operator command center:
1.  **Overview Page**: Displays active telemetry cards (Pulp Flow, Consistency, Speed) alongside color-coded spec alarm indicator panels (`🚨 ALARM: OFF SPEC` vs `🟢 ON SPECIFICATION`).
2.  **Prediction / Risk Page**: Features a Plotly gauge showing real-time off-spec probability and horizontal bar charts mapping SHAP driver attributions.
3.  **Analytics Page**: Displays trend graphs showing continuous sensor logs split dynamically with red dashed lines representing **Projected Deviation Trajectories** if deviations persist.
4.  **Recommendations Page**: Highlights suggested stock flow, speed, and steam pressure adjustments. Every delta card lists its **Inference Source** (e.g., physics loops, nearest-neighbors match), and features interactive **Accept** / **Reject** controls that log actions in a CSV database.

---

## 📂 Project Structure

```text
grade-change-intelligence/
├── backend/
│   └── app/
│       ├── api/v1/          # FastAPI REST Routers (/predict, /recommend, /explain)
│       ├── core/            # Configuration and structured logging handlers
│       ├── ml/              # Modular RandomForest, XGBoost, LightGBM, CatBoost wrappers
│       ├── pipeline/        # Ingestion loader, cleaners, feature engineer, and validator
│       ├── recommendation/  # Control rules and historical similarity matchers
│       ├── services/        # Orchestration services (PredictionService, ValidationService)
│       └── xai/             # SHAP values calculations and operator NLP compilers
├── data/
│   ├── raw/                 # Incoming CSV telemetry logs
│   └── processed/           # Standardized features and versioning manifests
├── docs/                    # Extensive technical documentation guides
├── frontend/
│   └── app.py               # Streamlit Command Center UI
├── ppt_assets/              # Vector SVG wireframes and SIH pitch structures
├── scripts/                 # Automation batch and training runners
└── tests/                   # Automated pytest suite (Unit and Integration checks)
```

---

## 🛠 SOLID Principles Design Compliance

The codebase is built on strict Object-Oriented SOLID design patterns:
*   **Single Responsibility (SRP)**: Each class (e.g., `DataCleaner`, `PhysicsControlRules`, `ModelRegistry`) has a single logical duty.
*   **Open/Closed (OCP)**: The model predictor depends on the abstract interface class `BaseMLClassifier`. Incorporating deep learning models or LSTMs requires writing a new subclass without altering the REST endpoint logic.
*   **Liskov Substitution (LSP)**: All wrapper subclasses inherit from `BaseMLClassifier` and can be substituted interchangeably.
*   **Interface Segregation (ISP)**: Endpoints are modularized; clients query only what they need (`/predict`, `/recommend`, or `/explain`).
*   **Dependency Inversion (DIP)**: Core services depend on abstract model interface definitions, not concrete implementations.

---

## 🚀 Quick Start Guide

### Local Workstation Setup (Windows)

#### 1. Bootstrap Workspace
Run the automated environment setup batch script:
```cmd
.\scripts\setup_env.bat
```

#### 2. Run Data Pipeline & Train ML Models
Process telemetry logs and retrain the comparative models:
```cmd
# Run ingestion cleaning & feature extraction
venv\Scripts\python scripts/run_pipeline.py

# Train ML classifiers & register champion model
venv\Scripts\python scripts/train_pipeline.py
```

#### 3. Launch App Services
Run the Streamlit frontend client and FastAPI server:
```cmd
# Start Streamlit command center dashboard
venv\Scripts\streamlit run frontend/app.py

# Start FastAPI web server (separate shell)
venv\Scripts\python -m uvicorn backend.app.main:app --reload --port 8000
```
- **Operator UI**: [http://localhost:8501](http://localhost:8501)
- **API Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Verification Status

We run full test coverages using pytest:
```cmd
venv\Scripts\python -m pytest
```
**Outcome**: All **25 automated tests pass cleanly**, verifying data preprocessing calculations, classifier inference outputs, nearest-neighbor lookups, and API responses.
