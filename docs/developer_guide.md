# Developer Guide - Grade Change Intelligence

This guide is for software and machine learning engineers looking to extend, refactor, or maintain the Grade Change Intelligence codebase.

---

## 📂 Codebase Layout

```text
grade-change-intelligence/
├── backend/app/
│   ├── api/v1/endpoints/  # API router endpoints (health, predict, recommend, explain)
│   ├── core/              # Global config manager and settings (config.py)
│   ├── ml/                # ML wrappers, training selector, registry
│   ├── pipeline/          # Ingestion loader, cleaners, feature engineer, validator
│   ├── recommendation/    # Causal rules, similarity matcher, engine
│   └── xai/               # SHAP attributions, NLP compilers
├── frontend/
│   └── app.py             # Streamlit dashboard client
├── scripts/               # run_pipeline.py, train_pipeline.py, generate_synthetic_data.py
├── tests/                 # Unit and integration test suites
└── config.yaml            # System configurations
```

---

## 🔌 Extension Points

### 1. Adding a New Sensor Feature
To engineer a new time-series feature (e.g. exponential moving averages):
1.  Open [features.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/pipeline/features.py).
2.  Add a method in `FeatureEngineer` (e.g. `add_exponential_averages`).
3.  Add the new columns to the `exclude_cols` list in [run_pipeline.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/scripts/run_pipeline.py) if they represent targets, otherwise they will automatically be standardized as features.

### 2. Adding a New ML Model
To integrate a new classifier (e.g. PyTorch MLP or Keras LSTM):
1.  Inherit from `BaseMLClassifier` in [base_model.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/ml/base_model.py).
2.  Create your model wrapper class (e.g. `backend/app/ml/pytorch_model.py`), implementing all abstract methods.
3.  Register the model class inside `candidates` dict in [trainer.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/ml/trainer.py) and `WRAPPERS` in [registry.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/ml/registry.py).

### 3. Modifying Control Rules
To alter recommended adjustments:
1.  Update recommendation gains and limits in [config.yaml](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/config.yaml).
2.  Open [rules.py](file:///C:/Users/itsay/.gemini/antigravity/scratch/grade-change-intelligence/backend/app/recommendation/rules.py) and modify `calculate_recommendations` calculations.

---

## 🎨 Coding Standards
- **Formatting**: Adhere to PEP 8 standards. Code must pass linting with `flake8` and autoformatting with `black`.
- **Typing**: Use static Python typing annotations wherever possible.
- **Single Responsibility Principle**: Keep classes focused on one task (e.g., separate model loading from inference evaluation).
- **Error Handling**: Use `loguru` log captures instead of raw `print` statements.
