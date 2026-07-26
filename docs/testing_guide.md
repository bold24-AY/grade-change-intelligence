# Testing & Verification Guide - Grade Change Intelligence

This document guides developers on how to write, execute, and verify automated test suites.

---

## 📂 Testing Directory Layout

All tests are placed under the `tests/` root folder:

```text
tests/
├── conftest.py               # Shared pytest fixtures (mock API clients, test variables)
├── integration/
│   └── test_api.py           # REST API routes testing (health, status endpoints)
└── unit/
    ├── test_config.py        # Config loader settings checks
    ├── test_dashboard.py     # Streamlit assets and PDF generation logic tests
    ├── test_ml.py            # Model wrappers, registries, and metrics calculators tests
    ├── test_pipeline.py      # DataLoader, Cleaners, and FeatureEngineer calculations tests
    └── test_preprocessors.py # Telemetry boundary checks tests
```

---

## 🧪 Running Test Suites

Before running tests, activate your Python virtual environment.

### 1. Execute All Tests
Run `pytest` to execute all unit and integration test blocks:
```cmd
venv\Scripts\python -m pytest
```

### 2. View Test Coverage
To generate a test coverage report (assessing which code statements are executed by tests):
```cmd
venv\Scripts\python -m pytest --cov=backend
```

---

## ✍ Writing New Test Cases

When extending modules, follow these testing best practices:

### 1. Mocking Data Streams
Use the `sample_raw_dataframe` fixture defined in `tests/unit/test_pipeline.py` to test your new cleaners or features. Avoid loading real files to keep tests fast and deterministic.

### 2. Mocking ML Models
If your feature requires predicting or attributions, use `RandomForestWrapper` to fit on small mock datasets (as shown in `tests/unit/test_ml.py`).

### 3. API Integrations
Use the `test_client` fixture to submit requests to routers. Example test:
```python
def test_custom_endpoint(test_client):
    response = test_client.get("/api/v1/custom-route")
    assert response.status_code == 200
```
