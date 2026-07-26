# Installation Guide - Grade Change Intelligence

This guide walks you through setting up the local development environment for the Grade Change Intelligence system on a Windows workspace.

---

## Prerequisites

Before starting, ensure you have the following installed on your machine:
- **Python 3.10** or higher
- **Git**
- **C++ Compiler Tools** (optional, but recommended for model frameworks)

---

## 🛠 Local Setup Instructions

### 1. Clone the Repository
Clone the project code to your local machine:
```bash
git clone <repository-url>
cd grade-change-intelligence
```

### 2. Run Environment Initializer
Execute the workspace setup batch script:
```cmd
.\scripts\setup_env.bat
```
This script will:
- Initialize a local virtual environment named `venv/`.
- Upgrade `pip` to the latest version.
- Install all core dependencies (FastAPI, Uvicorn, Pandas, Scikit-Learn, XGBoost, LightGBM, CatBoost, Streamlit, Plotly, FPDF2, PyTest, etc.).

### 3. Verify Local Dependencies
Activate the virtual environment and inspect the installed packages:
```cmd
venv\Scripts\activate
pip list
```

---

## ⚙ Ingestion & Modeling Pipeline Setup

Once dependencies are installed, bootstrap the mock database and train the initial champion model.

### 1. Generate Raw Data
Simulate machinery telemetry streams:
```cmd
venv\Scripts\python scripts/generate_synthetic_data.py
```
This writes CSV and Excel data logs to the `data/raw/` folder.

### 2. Execute Preprocessing
Load, clean, and engineer rolling window variables:
```cmd
venv\Scripts\python scripts/run_pipeline.py
```
This writes clean datasets to `data/processed/` and logs version manifests.

### 3. Train ML Classifier Models
Train candidate estimators and register the champion:
```cmd
venv\Scripts\python scripts/train_pipeline.py
```
This writes the model binary checkpoint to `backend/app/models/checkpoints/` and registers the model details.

---

## 🚀 Running Dashboard and Servers

### 1. Streamlit Dashboard
```cmd
venv\Scripts\streamlit run frontend/app.py
```
Acccessible via: [http://localhost:8501](http://localhost:8501)

### 2. FastAPI Backend REST Server
```cmd
venv\Scripts\python -m uvicorn backend.app.main:app --reload --port 8000
```
Acccessible via: [http://localhost:8000/docs](http://localhost:8000/docs)
